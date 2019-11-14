<template>
  <div class='row container-fluid'>
    <div class='col-md-2'></div>
    <div class='col-md-8'>
      <b-form class='w3-border w3-round w3-padding w3-light-gray'>
        <b-form-group id="exampleInputGroup1"
                      label="Name:"
                      label-for="name" >
          <input class="w3-input w3-padding-16" type="text" placeholder="Enter name" id='name'
           v-model='name' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup1"
                      label="Email:"
                      label-for="email" >
          <input class="w3-input w3-padding-16" type="email" placeholder="Enter email" id='email'
           v-model='email' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup2"
                      label="Username:"
                      label-for="username">
          <input class="w3-input w3-padding-16" type="text" placeholder="Enter username" id='username'
          v-model='username' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup2"
                      label="Password:"
                      label-for="password">
          <input class="w3-input w3-padding-16" type="password" placeholder="Enter password" id='password'
          v-model='password' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="User Type:"
                      label-for="userType">
            <select class="w3-select" id="userType" v-model='userType' required>
               <option value="" disabled selected> Choose user type</option>
               <option value="STUDENT">Student</option>
               <option value="STAFF">Staff Member</option>
               <option value="ADMIN">Admin</option>
           </select>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="Current Year:"
                      label-for="currentYear"
                      v-if="userType == 'STUDENT'">
            <select class="w3-select" id="currentYear" v-model='currentYear' required>
               <option value="" disabled selected> Choose student's current year</option>
               <option value="0">New Student</option>
               <option value="1">Year 1</option>
               <option value="2">Year 2</option>
               <option value="3">Year 3</option>
               <option value="4">Year 4</option>
           </select>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="Section Number:"
                      label-for="section"
                      v-if="userType == 'STUDENT'">
            <input class="w3-input w3-padding-16" type="text" placeholder="Enter Section Number" id='section'
                      v-model='sectionNo' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="Bench Number:"
                      label-for="bn"
                      v-if="userType == 'STUDENT'">
            <input class="w3-input w3-padding-16" type="text" placeholder="Enter Bench Number" id='bn'
                      v-model='bn' required>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="Course Assigned (Current Semester):"
                      label-for="course"
                      v-if="userType == 'STAFF'  && courses.length > 0">
            <select class="w3-select" id="course" v-model='assignedCourse' required>
               <option value="" disabled selected> Choose a course to assign the staff member to</option>
               <option value="None"> None </option>
               <option v-for='course in courses' :value="`${course.code}`"> {{course.name}}</option>
           </select>
        </b-form-group>
        <b-form-group id="exampleInputGroup3"
                      label="Department:"
                      label-for="department"
                      v-if="userType == 'STAFF'">
            <select class="w3-select" id="department" v-model='department' required>
               <option value="" disabled selected> Choose staff member's department</option>
               <option value="CMP">Computer</option>
               <option value="EEC">Electrionics & Communications</option>
               <option value="AER">Aerospace</option>
               <option value="ARCH">Architecture </option>
               <option value="BMES">Biomedical</option>
               <option value="EPM">Power</option>
               <option value="EMP">Maths & Physics</option>
               <option value="MECH">Mechanical</option>
               <option value="CHE">Chemical</option>
               <option value="MPM">Mining, Petroleum & Metallurgical</option>
           </select>
        </b-form-group>
        <div class='w3-center'>
          <b-button class='w3-button w3-black' type="submit" @click='addUser'>Add User</b-button>
          <b-button type="reset" class='w3-button w3-black'>Reset</b-button>
        </div>
      </b-form>
    </div>
    <div class='col-md-2'></div>
  </div>
</template>

<script>
  import axios from 'axios'
  const usersPath = "http://127.0.0.1:5000/users";
  const coursesPath = 'http://127.0.0.1:5000/courses'
  export default {
    data() {
      return {
        username: '',
        password: '',
        email: '',
        name: '',
        userType: '',
        currentYear: '',
        sectionNo: '',
        bn: '',
        department: '',
        assignedCourse: '',
        courses: []
      }
    },
    methods: {
      addUser: function() {
        if(this.username == '' || this.password == '' || this.name == '' || this.email == '') {
          this.$notify({
            group: 'foo',
            title: 'Cannot create user !',
            text: "All fields cannot be empty !",
            type: 'error'
          })
          return;
        }
        if(this.userType=='STUDENT') {
            if(this.currentYear == '' || this.sectionNo == '' || this.bn == '') {
              this.$notify({
                group: 'foo',
                title: 'Cannot create user !',
                text: "All fields cannot be empty !",
                type: 'error'
              })
              return;
            }
            if(isNaN(this.sectionNo) || isNaN(this.bn)) {
              this.$notify({
                group: 'foo',
                title: 'Cannot create user !',
                text: "Section Number and Bench Number must be integers !",
                type: 'error'
              })
              return;
            }
            var user = {
              userType: this.userType,
              username: this.username,
              password: this.password,
              name: this.name,
              email: this.email,
              currentYear: this.currentYear,
              sectionNo: this.sectionNo,
              bn: this.bn
            }
        }
        else if (this.userType=='STAFF'){
            if(this.department == '' || this.assignedCourse == '') {
              this.$notify({
                group: 'foo',
                title: 'Cannot create user !',
                text: "All fields cannot be empty !",
                type: 'error'
              })
              return;
            }
            var user = {
              userType: this.userType,
              username: this.username,
              password: this.password,
              email: this.email,
              name: this.name,
              department: this.department,
              course: this.assignedCourse
            }
        }
        else {
          var user = {
            userType: this.userType,
            username: this.username,
            password: this.password,
            email: this.email
          }
        }
        // Create payload
        var payload = {
          user: user
        }
        // Send request
        axios.post(usersPath, payload)
          .then(this.userAdded)
          .catch(function(error){
            console.log(error);
          })
      },
      userAdded: function(response) {
        if(response.data.is_successful) {
          this.$notify({
            group: 'foo',
            title: 'Operation Successful !',
            text: response.data.message,
            type: 'success'
          })
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Operation Failed !',
            text: response.data.message,
            type: 'error'
          })
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
      }
    },
    beforeMount() {
      this.loadCourses();
    }
  }
</script>

<style scoped>
  .row {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
