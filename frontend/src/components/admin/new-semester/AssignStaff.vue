<template>
  <div class='contain-fluid' id='background'>
    <div class='row container-fluid' >
      <div class='col-md-2'></div>
      <div class='col-md-8'>
        <div class='row'>
          <div class='col-md-2'></div>
          <div class='col-md-8 card w3-round-xlarge w3-padding-16'>
            <h3 class='w3-center' id='title' v-if="courses.length > 0"> Course: {{courses[currentCourseIndex].name}} </h3>
            <ul class='list-group card w3-round-xlarge'>
              <li class='list-group-item' v-for='(staffMember,index) in staff'>
                <input class="form-check-input" type="checkbox" :id='`check${index}`' :value="`${staffMember.id}`" >
                <label class="form-check-label" :for="`check${index}`">
                  {{staffMember.name}}
                </label>
              </li>
            </ul>
          </div>
          <div class='col-md-2'></div>
        </div>
        <div class='row'>
          <div class='col-md-3'></div>
          <div class='col-md-6 row'>
            <button class='w3-button w3-black' id='selectLastSemesterStaffButton' value='select' @click='selectLastSemesterStaff($event)'>
               Select Last Semester's Staff
             </button>
            <button class='w3-button w3-black' id='assignStaff' @click='assignStaff'> Assign </button>
          </div>
          <div class='col-md-3'></div>
        </div>
      </div>
      <div class='col-md-2'></div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  const staffPath = "http://127.0.0.1:5000/staff";
  const teachPath = 'http://127.0.0.1:5000/teach';
  const coursesPath = 'http://127.0.0.1:5000/courses'
  export default {
    data() {
      return {
        currentCourseIndex: 0,
        courses: [],
        staff: []
      }
    },
    methods: {
      nextCourse: function() {
        if(this.currentCourseIndex >= this.courses.length - 1) {
          this.doneCreatingSemester()
        }
        else {
          this.currentCourseIndex++;
        }
      },
      checkLastSemesterStaff: function() {
        let currentCourseCode = this.courses[this.currentCourseIndex].code;
        for(var i = 0; i < this.staff.length; i++){
          document.querySelector('#check'+i).checked = this.staff[i].courses.includes(currentCourseCode);
        }
      },
      selectLastSemesterStaff: function(e) {
        if(e.target.value == 'select') {
          this.checkLastSemesterStaff();
          e.target.innerText = 'Clear Selections';
          e.target.value = 'deselect';
        }
        else {
          this.uncheckAll();
          e.target.innerText = "Select Last Semester's Staff";
          e.target.value = 'select';
        }
      },
      uncheckAll: function() {
        for(var i = 0; i < this.staff.length; i++) {
          document.querySelector('#check'+i).checked = false;
        }
      },
      loadCourses: function() {
        var i = 1;
        // Get the courses of all 4 years
        for(i; i <= 4; i++) {
          axios.get(coursesPath, {
            params: {
            year: i
            }
          })
            .then(this.fillCourses)
            .catch(function(error) {
              console.log(error)
            });
        }
      },
      fillCourses: function(response) {
        // Append the returned list to the list of courses
        this.courses.push.apply(this.courses, response.data);
      },
      loadStaff: function() {
        // Get all the staff members and all the courses they were teaching in the last semester
        axios.get(staffPath)
          .then(this.fillStaff)
          .catch(function(error) {
            console.log(error)
          });
      },
      fillStaff: function(response) {
        this.staff = response.data;
      },
      doneCreatingSemester: function() {
        this.$parent.$router.replace('/admin')
        this.$notify({
          group: 'foo',
          title: 'Semester Created !',
          text: 'The semester was created successfully!',
          type: 'success'
        })
      },
      assignStaff: function() {
        let assignedStaffIDs = [];
        var i;
        for(i = 0; i < this.staff.length; i++) {
          if(document.querySelector('#check'+i).checked) {
            assignedStaffIDs.push(this.staff[i].id);
          }
        }
        if(assignedStaffIDs.length == 0) {
          this.$notify({
            group: 'foo',
            title: 'Error !',
            text: 'You must select at least one staff member !',
            type: 'error'
          })
          return;
        }
        let currentCourseCode = this.courses[this.currentCourseIndex].code;
        var payload = {
          ids: assignedStaffIDs,
          courseCode: currentCourseCode
        }
        axios.post(teachPath, payload)
          .then(this.staffAssigned)
          .catch(function(error) {
            console.log(error)
          });
      },
      staffAssigned: function(response) {
        if(response.data.is_successful) {
          this.$notify({
            group: 'foo',
            title: 'Operation Successful !',
            text: response.data.message,
            type: 'success'
          })
          this.uncheckAll();
          this.nextCourse();
          // Reset "Select last semester's staff" button
          let button = document.querySelector('#selectLastSemesterStaffButton')
          button.innerText = "Select Last Semester's Staff";
          button.value = 'select';
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Operation Failed !',
            text: response.data.message,
            type: 'error'
          })
        }
      }
    },
    beforeMount() {
      this.loadCourses();
      this.loadStaff();
    }

}
</script>

<style scoped>
  button {
    margin: 10px auto;
    max-width: 100%;
  }
  ul {
    max-height: 400px;
    overflow-y: auto;
  }
  li {
    padding: 10px 30px;
  }
  #background {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .container-fluid {
    max-height: 100%;
  }
</style>
