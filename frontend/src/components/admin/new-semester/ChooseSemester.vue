<template>
  <div class='contain-fluid' id='background'>
    <div class='row container-fluid' >
      <div class='col-md-3'></div>
      <div class='col-md-6 row card w3-padding w3-round-large'>
        <b-form-group id="exampleInputGroup3"
                      label="Semester:"
                      label-for="semester">
            <select class="w3-select" id="semester" v-model='selectedIndex'>
                <option value="" disabled selected> Choose Semester</option>
                <option v-for="(semester, index) in semesters" :value="`${index}`"> {{semester.semester + ' ' + semester.year}} </option>
            </select>
        </b-form-group>
        <div class='w3-center'>
          <b-button class='w3-button w3-black' type="submit" @click='createSemester'>Create Semester</b-button>
        </div>
      </div>
      <div class='col-md-3'></div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/semesters";
  export default {
    data() {
      return {
          semesters: [],
          possibleSemesters: ['FALL', 'SPRING', 'SUMMER'],
          selectedIndex: ''
      }
    },
    methods : {
      createSemester: function(){
        if(this.selectedIndex == '') {
          this.$notify({
            group: 'foo',
            title: 'Cannot Create Semester !',
            text: "You must choose a semester first !",
            type: 'error'
          })
          return;
        }
        var payload = {
          semester: this.semesters[this.selectedIndex].semester,
          year: this.semesters[this.selectedIndex].year
        }
        axios.post(path, payload)
          .then(this.semesterAdded)
          .catch(function(error) {
            console.log(error)
          });
      },
      semesterAdded: function(response) {
        if(response.data.is_successful) {
          this.$notify({
            group: 'foo',
            title: 'Semester Created !',
            text: response.data.message,
            type: 'success'
          })
          this.$parent.$router.replace('/admin/new-semester/enroll-students/')
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Semester Was Not Created !',
            text: response.data.message,
            type: 'error'
          })
        }
      },
      loadPossibleSemesters: function() {
        axios.get(path)
          .then(this.fillSemesters)
          .catch(function(error) {
            console.log(error)
          });
      },
      fillSemesters: function(response) {
        var year = response.data.year;
        var semester = response.data.semester;
        var i;
        for(i = 0; i < this.possibleSemesters.length; i++) {
          if(this.possibleSemesters[i] == semester)
            break;
        }
        i++;
        if(i == 3) {
          year++;
          i = 0;
        }
        for(i; i < this.possibleSemesters.length; i++) {
          this.semesters.push({'semester': this.possibleSemesters[i], 'year': year});
        }
        year++;
        for(i = 0; i < this.possibleSemesters.length; i++) {
          this.semesters.push({'semester': this.possibleSemesters[i], 'year': year});
        }
      }
    },
    beforeMount() {
      this.loadPossibleSemesters();
    }

}
</script>

<style scoped>
  button {
    margin: 10px auto;
    width: 25%;
  }
  ul {
    max-height: 400px;
    overflow-y: auto;
  }
  li {
    padding: 10px 30px;
  }
  #background {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height:100%;
  }
</style>
