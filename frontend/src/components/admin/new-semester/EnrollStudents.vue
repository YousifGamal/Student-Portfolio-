<template>
  <div class='contain-fluid' id='background'>
    <div class='row container-fluid' >
      <div class='col-md-2'></div>
      <div class='col-md-8'>
        <div class='row'>
          <div class='col-md-2'></div>
          <div class='col-md-8 card w3-round-xlarge w3-padding-16'>
            <h3 class='w3-center' id='title'> Year {{currentYear}} Students </h3>
            <ul class='list-group card w3-round-xlarge'>
              <li class='list-group-item' v-for='(student,index) in students'>
                <input class="form-check-input" type="checkbox" :id='`check${index}`' :value="`${student.id}`" >
                <label class="form-check-label" :for="`check${index}`">
                  {{student.name}}
                </label>
              </li>
            </ul>
          </div>
          <div class='col-md-2'></div>
        </div>
        <div class='row'>
          <div class='col-md-3'></div>
          <div class='col-md-6 row'>
            <button class='w3-button w3-black' id='selectAllButton' value='select' @click='selectAll($event)'>
               Select All
             </button>
            <button class='w3-button w3-black' id='moveToNextYearButton' @click='advanceStudents'> Graduate </button>
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
  const studentsPath = "http://127.0.0.1:5000/students";
  const enrollPath = 'http://127.0.0.1:5000/enroll';
  export default {
    data() {
      return {
        currentYear: 4,
        students: []
      }
    },
    methods: {
      next: function() {
        if(this.currentYear == 0) {
          this.goToAssignStaff();
        }
        this.currentYear--;
        document.querySelector('#moveToNextYearButton').textContent = `Advance to Year ${this.currentYear + 1}`
        if(this.currentYear == 0) {
          document.querySelector('#title').textContent = 'New Students'
        }
        this.loadStudents();
      },
      loadStudents: function() {
        axios.get(studentsPath, {
          params: {
          year: this.currentYear
          }
        })
          .then(this.fillStudents)
          .catch(function(error) {
            console.log(error)
          });
      },
      fillStudents: function(response) {
        this.students = response.data;
        // Reset the Select All button
        let button = document.querySelector('#selectAllButton');
        if(button) {
          this.checkAll(false);
          button.innerText = 'Select All';
          button.value = 'select';
        }
      },
      goToAssignStaff: function() {
        this.$parent.$router.replace('/admin/new-semester/assign-staff')
      },
      advanceStudents: function() {
        if (this.students.length == 0) {
          this.next();
          return;
        }
        let advancedStudentsIDs = [];
        let allIDs = [];
        var i;
        for(i = 0; i < this.students.length; i++) {
          allIDs.push(this.students[i].id);
          if(document.querySelector('#check'+i).checked) {
            advancedStudentsIDs.push(this.students[i].id);
          }
        }
        var payload = {
          advanced_student_ids: advancedStudentsIDs,
          ids: allIDs
        }
        axios.post(enrollPath, payload)
          .then(this.studentsEnrolled)
          .catch(function(error) {
            console.log(error)
          });
      },
      checkAll: function(isChecked) {
        var i;
        for(i = 0; i < this.students.length; i++) {
          document.querySelector('#check'+i).checked = isChecked;
        }
      },
      studentsEnrolled: function(response) {
        if(response.data.is_successful) {
          this.$notify({
            group: 'foo',
            title: 'Successful !',
            text: response.data.message,
            type: 'success'
          })
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Failed !',
            text: response.data.message,
            type: 'error'
          })
        }
        this.next();
      },
      selectAll: function(e) {
          if(e.target.value == 'select') {
            this.checkAll(true);
            e.target.innerText = 'Clear Selections';
            e.target.value = 'deselect';
          }
          else {
            this.checkAll(false);
            e.target.innerText = 'Select All';
            e.target.value = 'select';
          }
      }
    },
    beforeMount() {
      this.loadStudents();
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
