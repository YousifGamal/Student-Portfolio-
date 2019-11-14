<template>
    <div class='row container-fluid' id='background'>
      <div class="col-md-3">
  		</div>
      <div class="col-md-6">
        <ul class="w3-ul w3-light-gray w3-center w3-border w3-border-black w3-round" role='tablist'>
          <li class="w3-black w3-xlarge w3-padding-32">
            <div class='w3-xxxlarge lobster'> Courses </div>
              <div class="w3-dropdown-hover w3-medium">
               <button class="w3-button w3-border w3-border-white w3-round" >Year {{currentYear}}</button>
               <div class="w3-dropdown-content w3-bar-block w3-border">
                 <a href="#" class="w3-bar-item w3-button" value='1' @click.prevent='loadYearCourses($event)'>Year 1</a>
                 <a href="#" class="w3-bar-item w3-button" value='2' @click.prevent='loadYearCourses($event)'>Year 2</a>
                 <a href="#" class="w3-bar-item w3-button" value='3' @click.prevent='loadYearCourses($event)'>Year 3</a>
                 <a href="#" class="w3-bar-item w3-button" value='4' @click.prevent='loadYearCourses($event)'>Year 4</a>
               </div>
              </div>
          </li>
          <li v-for="(course, index) in courses">
            <b-card no-body class="mb-1 w3-white">
            <b-card-header header-tag="header" class="p-1" role="tab">
              <b-btn block href="#" v-b-toggle="`accordion${index}`" variant="info" class='w3-large headers'>
                 {{course.name}}
               </b-btn>
            </b-card-header>
            <b-collapse :id="`accordion${index}`" role="tabpanel" accordion="my-accordion">
              <b-card-body>
                <p class="card-text">
                  <div class='input-field'>
                    <label :for="`courseName${index}`">
          						Course Name:
          					</label>
          					<input class="w3-input w3-padding-16" type="text" :id="`courseName${index}`"
                    :value="`${course.name}`" placeholder="Course Name" required readonly>
                  </div>
                  <div class='input-field'>
                    <label :for="`courseCode${index}`">
          						Course Code:
          					</label>
          					<input class="w3-input w3-padding-16" type="text" :id="`courseCode${index}`"
                    :value="`${course.code}`" placeholder="Course Code" required readonly>
                  </div>
                  <div class='input-field'>
                    <label :for="`courseYear${index}`">
          						Course Year:
          					</label>
                    <select class="w3-select" :id="`courseYear${index}`" disabled>
                       <option v-for='i in (1,4)' :value='`${i}`' :selected="i == course.year">Year {{i}} </option>
                   </select>
                  </div>
                  <button class="w3-button w3-black" :value="`edit${index}`" id="editAndSubmit"
                    @click='editSubmitButtonClick($event,`${index}`)'> Edit </button>
                  <button class="w3-button w3-black" :value="index" id="delete"
                    @click='deleteCourse(`${index}`)'> Delete </button>
                  <ul class='w3-ul'>
                    <li>
                      <h4> Staff: </h4>
                    </li>
                    <li v-for="staffMember in course.staff" class="w3-display-container w3-border">
                      {{staffMember}}
                    </li>
                  </ul>
                </p>
              </b-card-body>
            </b-collapse>
          </b-card>
          </li>
          <!--New Course -->
          <li class='w3-dark-gray'>
            <b-card no-body class="mb-1 w3-white">
            <b-card-header header-tag="header" class="p-1" role="tab">
              <b-btn block href="#" v-b-toggle.accordionNew variant="info" class='w3-large headers'>
                 New Course
               </b-btn>
            </b-card-header>
            <b-collapse id="accordionNew" role="tabpanel" accordion="my-accordion">
              <b-card-body>
                <p class="card-text">
                  <div class='input-field'>
                    <label for="courseNameNew">
          						Course Name:
          					</label>
          					<input class="w3-input w3-padding-16" type="text" id='courseNameNew' placeholder="Course Name"
                    v-model='newCourseName'>
                  </div>
                  <div class='input-field'>
                    <label for="courseCodeNew">
          						Course Code:
          					</label>
          					<input class="w3-input w3-padding-16" type="text" id='courseCodeNew' placeholder="Course Code"
                    v-model='newCourseCode'>
                  </div>
                  <div class='input-field'>
                    <label for="courseYearNew">
          						Course Year:
          					</label>
                    <select class="w3-select" id="courseYearNew" v-model='newCourseYear'>
                       <option value="1" selected>Year 1</option>
                       <option value="2">Year 2</option>
                       <option value="3">Year 3</option>
                       <option value="4">Year 4</option>
                   </select>
                  </div>
                  <button class="w3-button w3-black" id="newCourseButton" @click.prevent='addCourse'> Add </button>

                </p>
              </b-card-body>
            </b-collapse>
          </b-card>
          </li>

        </ul>
  		</div>
      <div class="col-md-3">
  		</div>
    </div>
</template>

<script>
    import axios from 'axios'
    const path = "http://127.0.0.1:5000/courses";
    export default {
      data() {
        return {
          courses: [],
          currentYear: 1,
          newCourseName: '',
          newCourseCode: '',
          newCourseYear: 1
        }
      },
      methods: {
        loadYearCourses: function (e) {
            let button = e.target;
            let year = button.getAttribute('value');
            this.currentYear = year;
            this.loadCourses(year);
        },
        editSubmitButtonClick: function(e, index) {
          let button = e.target;
          let buttonValue = button.getAttribute('value');
          if(buttonValue.includes('edit')) {
            // Enable input fields
            let inputName = document.querySelector('#courseName'+index);
            let inputCode = document.querySelector('#courseCode'+index);
            let inputYear = document.querySelector('#courseYear'+index);
            inputName.removeAttribute('readonly');
            inputCode.removeAttribute('readonly');
            inputYear.removeAttribute('disabled');
            // Change edit button to submit
            e.target.textContent = 'Submit';
            e.target.setAttribute('value', 'submit'+index);
          }
          else {
            // Get input fields
            let inputName = document.querySelector('#courseName'+index);
            let inputCode = document.querySelector('#courseCode'+index);
            let inputYear = document.querySelector('#courseYear'+index);
            // Get new course attributes
            let courseName = inputName.value;
            let courseCode = inputCode.value;
            let courseYear = inputYear.value;
            // Check for empty fields
            if(courseName == '' || courseCode == '') {
              this.$notify({
                group: 'foo',
                title: 'Operation Failed !',
                text: "Course name and course code cannot be empty !",
                type: 'error'
              })
              return;
            }
            // Disable input fields
            inputName.setAttribute('readonly', 'true');
            inputCode.setAttribute('readonly', 'true');
            inputYear.setAttribute('disabled', 'true');
            // Change edit button to submit
            e.target.textContent = 'Edit';
            e.target.setAttribute('value', 'edit'+index);
            // Submit course modifications
            let course = {
              name: courseName,
              code: courseCode,
              year: courseYear
            }
            this.editCourse(index, course);
          }
        },
        loadCourses: function(coursesYear) {
            axios.get(path, {
              params: {
              year: coursesYear
              }
            })
              .then(this.fillCourses)
              .catch(function(error) {
                console.log(error)
              });
        },
        fillCourses: function(response) {
          this.courses = response.data;
        },
        editCourse: function(index, course) {
          let oldCode = this.courses[index].code;
          var payload = {
            code: oldCode,
            newCourse: course
          }
          axios.put(path, payload)
            .then(this.courseModified)
            .catch(function(error) {
              console.log(error)
            });
        },
        courseModified: function(response) {
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
          this.loadCourses(this.currentYear);
        },
        addCourse: function() {
          // Check for empty fields
          if(this.newCourseName == '' || this.newCourseCode == '') {
            this.$notify({
              group: 'foo',
              title: 'Operation Failed !',
              text: "Course name and course code cannot be empty !",
              type: 'error'
            })
            return;
          }
          // Create payload
          var payload = {
            newCourse: {
              name: this.newCourseName,
              code: this.newCourseCode,
              year: this.newCourseYear
            }
          }
          // Send the request
          axios.post(path, payload)
            .then(this.courseAdded)
            .catch(function(error) {
              console.log(error)
            });
        },
        courseAdded: function(response) {
          if(response.data.is_successful) {
            this.$notify({
              group: 'foo',
              title: 'Operation Successful !',
              text: response.data.message,
              type: 'success'
            })
            // Clear fields
            this.newCourseName = '';
            this.newCourseCode = '';
            this.newCourseYear = 1;
          }
          else {
            this.$notify({
              group: 'foo',
              title: 'Operation Failed !',
              text: response.data.message,
              type: 'error'
            })
          }
          this.loadCourses(this.currentYear);
        },
        deleteCourse: function(index) {
          // Get course code
          let courseCode = this.courses[index].code;
          // Send the request
          axios.delete(path, {
              params: {
              deletedCourseCode: courseCode
              }
            })
          .then(this.courseModified)
          .catch(function(error) {
            console.log(error)
          })
        }

      },
      beforeMount() {
        this.loadCourses(1);
      }
    }
</script>

<style scoped>
  a:hover {
    text-decoration: none;
  }
  #background {
    display: flex;
    justify-content: center;
    align-items: center;
    height:100%;
  }
  label, input, select {
    display: inline;
    width: 50%;
  }
  .input-field {
      margin: 10px auto;
  }
  #editAndSubmit, #newCourseButton, #delete{
    width:30%;
  }
  .headers {
    border-color: black;
    color: white;
    background-color: black;
  }
  .btn-info:focus {
    box-shadow: none;
  }

</style>
