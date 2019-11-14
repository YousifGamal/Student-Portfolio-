<template>
  <div class="container-fluid">
    <div class="row" >
      <div class="col-sm-1" ></div>
      <div class="col-sm-3" style="margin-top: .5%; margin-left:2%">
        <div class=" list-group" style="margin-top:8%">
        <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Courses</a>
        <div class=" list-group myul">
        <a href=""  class="list-group-item list-group-item-action" v-for="c in stdcourses" @click.prevent="fillRequirements(c.code)">{{c.name}}</a>
      </div>
      </div>
      </div>
      <div class="col-sm-1" ></div>
      <div class="col-sm-4" style="">
        <div class="w3-container" >
          <div class=" list-group" style="margin-top:8%">
          <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Assignment/Project</a>
          <div class=" list-group myul">
            <a href="#" class="list-group-item list-group-item-action" v-for="c in stdRequirements" v-if="c.projName != null" @click.prevent="requirementComponent(c.reqID)">{{c.reqName}} / {{c.projName}}</a>
            <a href="#" class="list-group-item list-group-item-action" v-for="c in stdRequirements" v-if="c.projName == null" @click.prevent="requirementComponent(c.reqID)">{{c.reqName}}</a>
        </div>
        </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/StudentCourse";
  const path2 = "http://127.0.0.1:5000/StudentRequirement";
  export default {
    data() {
      return {
        stdcourses: [],
        stdRequirements: [],
        courseid: '',
        reqid:''
      }
    },
    methods: {
      fillCourses: function() {
        axios.get(path,{
        params:{
          username: this.$parent.username
        }
      })
          .then(this.returnedCourses)
          .catch(function(error) {
            console.log(error)
          });
      },
      returnedCourses(response) {
        this.stdcourses = response.data
        console.log("Courses:");
        console.log(this.stdcourses)
      },
      fillRequirements: function(ccode) {
        this.courseid = ccode
        var id = {
          id: this.courseid
        };
        axios.post(path2, id)
          .then(this.returnedRequirements)
          .catch(function(error) {
            console.log(error)
          });
      },
      returnedRequirements(response) {
        this.stdRequirements = response.data;
        console.log(this.stdRequirements)
      },
      requirementComponent: function(reQid){
        this.reqid = reQid
        this.$parent.reqID = this.reqid
        console.log(this.$parent.reqID)
        this.$parent.$router.push('/studentReq')
      }
    },
    beforeMount(){
      this.fillCourses()
    }
  }

</script>

<style scoped>

  .col-md-4
  {
    padding: 2%;
  };

  .myul{
    overflow-y:scroll;
    max-height:180px
  }

</style>
