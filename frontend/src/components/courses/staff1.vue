<template>
  <div class="container-fluid">
    <div class="w3-container">
      <div class="row" style="margin-top:1%">
        <div class="col-sm-1">

        </div>
        <div class="col-sm-4">




        <div class=" list-group">
          <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Courses</a>
          <div class=" list-group myul">
          <a href=""  @click.prevent="setCurrentCourse(x.cCode)" class="list-group-item list-group-item-action" v-if ="courseList != null" v-for ="x in courseList">{{x.cName}}</a>
        </div>
        </div>
        </div>
        <div class="col-sm-1">

        </div>
        <div class="col-sm-4">
          <div class=" list-group" v-if="hideBool" >
            <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white;  margin-bottom:.1% ">Requirements</a>
            <div class=" list-group myul" v-if="hideBool" >
            <a href="" @click.prevent="goToreq(x.reqID)" class="list-group-item list-group-item-action"v-for = "x in reqList"  v-if="reqList != null && x.projName != null">{{x.reqName}} / {{x.projName}}</a>
            <a href="" @click.prevent="goToreq(x.reqID)" class="list-group-item list-group-item-action"v-for = "x in reqList"  v-if="reqList != null && x.projName == null">{{x.reqName}}</a>
          </div>
          </div>
        </div>
        </div>
      </div>
      <div class="w3-container" v-if="hideBool">
        <div class="row" style="margin-top:2%">
          <div class="col-sm-1">

          </div>
          <div class="col-sm-4">
              <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white;  "><h5>Add New Requirement</h5></a>
              <form class >
              <div class="form-group" style="padding-top:1%">
              <label for="reqName" style="padding-top:2%">Requirement Name</label>
              <input type="text" class="w3-input w3-round-medium" id="reqName" placeholder="Enter New Requirement Name" v-model="newReqData.Name" />
              <label for="sel1"  style="padding-top:2%">Type</label>
              <select class="w3-select w3-round-medium" id="sel1" v-model="selectedOption" >
                <option value="1" >New Project</option>
                <option value="2" v-if="projList.length">Existing Project</option>
                <option value="3" selected >None Project Related</option>
              </select>
              <label for="projectName"  style="padding-top:2%" v-if="selectedOption == 1">Project Name</label>
              <input type="text" class="w3-input w3-round-medium" id="projectName" placeholder="Enter New Project Name"  v-if="selectedOption == 1" v-model="newReqData.ProjectName"/>
              <label for="projdocument"  style="padding-top:2%" v-if="selectedOption == 1">Project Document</label>
              <input type="text" class="w3-input w3-round-medium" id="projdocument" placeholder="Enter Project Document link" v-if="selectedOption == 1" v-model="newReqData.ProjectDocument" />
              <label for="sel2"  style="padding-top:2%" v-if="selectedOption == 2">Select Project Name</label>
              <select class="w3-select w3-round-medium" id="sel2" v-if=" selectedOption == 2" v-model="projOpt">
                <option v-if="projList[0].projName != undefined " v-for="proj in projList"  v-bind:value="proj.projID" >{{proj.projName}}</option>
                </select>
              <label for="deliverableTime" style="padding-top:2%">DeadLine for the Requirement</label>
              <input type="date" id="deliverableTime" class="w3-input w3-round-medium" min="date" v-model="newReqData.DeadLine">
              <label for="document"  style="padding-top:2%" >Document</label>
              <input type="text" class="w3-input w3-round-medium" id="document" placeholder="Enter Document link" v-model="newReqData.document"  />
              <label for="Additiona-Materials"  style="padding-top:2%" >Additiona Materials</label>
              <input type="text" class="w3-input w3-round-medium" id="Additiona-Materials" placeholder="Enter Additiona Materials link" v-model="newReqData.addMaterials" />

              <label for="sel3"  style="padding-top:2%">Choose Individual or Team </label>
              <select class="w3-select w3-round-medium" id="sel3"  v-model="typeOpt">
                <option value="0" >Team</option>
                <option value="1" selected >Individual</option>
              </select>


              <label for="min"  style="padding-top:2%" v-if="typeOpt == 0" >Min Team Members Number</label>
              <input type="number" min="2" class="w3-input w3-round-medium" v-if="typeOpt == 0" id="min" placeholder="Enter Min number for memebers in team" v-model="newReqData.minNumber" />
              <label for="max" v-if="typeOpt == 0" style="padding-top:2%" >Max Team Members Number</label>
              <input type="number" v-if="typeOpt == 0 " min="2" class="w3-input w3-round-medium" id="max" placeholder="Enter Max number for memebers in team" v-model="newReqData.maxNumber" />
              </div>

              <div class="form-group text-center" style="padding-top:2%">
                <button type="submit" @click.prevent="addNewRequirements()" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                  Add
                </button>
              </div>

            </form>
          </div>
          <div class="col-sm-1">

          </div>
          <div class="col-sm-4">
            <div class=" list-group"  >

              <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Assign Requirment</a>
              <div class=" list-group myul"  >
            <span v-for ="x in unAssignedReqList" class="list-group-item list-group-item-action" v-if ="unAssignedReqList != null && !x.projectName" >  <a href="" class="list-group-item-action"  @click.prevent="assignedReq(x.reqID)" v-if ="unAssignedReqList != null && !x.projectName" >{{x.reqName}}</a>
              <span class="w3-right"> <button type="submit" @click.prevent="deleteReq(x.reqID)"  class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;"> Delete</button></span></span>
          <span v-for ="x in unAssignedReqList" class="list-group-item list-group-item-action" v-if ="unAssignedReqList != null && x.projectName">  <a href=""  class="list-group-item-action" @click.prevent="assignedReq(x.reqID)"   >{{x.reqName}} / {{x.projectName}}</a>
               <span class="w3-right"><button type="submit" @click.prevent="deleteReq(x.reqID)"  class="btn btn-primary btn-block w3-black" v-if ="unAssignedReqList != null && x.projectName" style="border:#e7e7e7;"> Delete</button></span></span>
            </div>
            </div>
          </div>
        </div>

      </div>
    </div>




</template>


<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/staffcourses";
  const path2 = "http://127.0.0.1:5000/staffReqBycCode";
  const path3 = "http://127.0.0.1:5000/unAssignedReqStaff";
  export default {
    data() {
      return {
        currentCourseCode: '',
        reqList:[],
        courseList:[],
        cCode:"",
        projList:[],
        hideBool:false,
        selectedOption:3,
        projOpt:"",
        typeOpt:1,
        newReqData:{
          cCode:"",
          ProjectID:"",
          ProjectName:"",
          ProjectDocument:"N/A",
          Name:"",
          DeadLine:"",
          addMaterials:"N/A",
          document:"N/A",
          type:"",
          minNumber:1,
          maxNumber:1,
          insertionType:""
        },

        date:"",
        unAssignedReqList:[],
      }
    },
    methods: {
      setCurrentCourse: function(courseCode) {
        this.currentCourseCode = courseCode;
        this.fillRequirementStaff();
      },
      fillCoursesStaff: function() {
      axios.get(path,{
      params:{
        username: this.$parent.username
      }
    })
        .then(this.returnedfillCoursesStaff)
        .catch(function(error) {
          console.log(error)
        });
    },
    returnedfillCoursesStaff(response) {
      this.courseList = response.data
      console.log(this.courseList)
      var currentdate = new Date();
      this.date = currentdate.getFullYear()+"-"+(currentdate.getMonth()+1) +"-"+currentdate.getDate()


    },
    fillRequirementStaff: function() {
      this.cCode = this.currentCourseCode;
      this.hideBool = true;
    axios.get(path2,{
    params:{
      cCode: this.cCode
    }
  })
      .then(this.returnedfillRequirementStaff)
      .catch(function(error) {
        console.log(error)
      });
  },
  returnedfillRequirementStaff(response) {
    this.getUnassignedReq()
    var x = response.data
    this.reqList = x.RDATA
    this.projList = x.PDATA
    console.log(this.reqList)
  },
  addNewRequirements: function() {
    if (!this.newReqData.Name) {
      this.$notify({
              group: 'foo',
              title: 'Cannot Add Requiremnet !',
              text: "Requiremnet Name cannot be empty!",
              type: 'error'
            })
            return;
    }
    if (this.selectedOption == 1) {
      if (!this.newReqData.ProjectName) {
        this.$notify({
                group: 'foo',
                title: 'Cannot Add Requiremnet !',
                text: "Project Name cannot be empty!",
                type: 'error'
              })
              return;
      }
      this.newReqData.insertionType = 1
      this.newReqData.type = this.typeOpt
    }
    if (this.selectedOption == 2) {
      if (!this.projOpt) {
        this.$notify({
                group: 'foo',
                title: 'Cannot Add Requiremnet !',
                text: "CHOOSE Project NAME!",
                type: 'error'
              })
              return;
      }
      this.newReqData.insertionType = 2
      this.newReqData.ProjectID = this.projOpt
    }
    if (this.selectedOption == 3) {
      this.newReqData.insertionType = 3
    }
    if (this.newReqData.DeadLine <= this.date) {
      this.$notify({
              group: 'foo',
              title: 'Cannot Add Requiremnet !',
              text: "Non Acceptable Date!",
              type: 'error'
            })
            return;
    }
    if (this.typeOpt == 0) {
      if (this.newReqData.minNumber > this.newReqData.maxNumber || !this.newReqData.maxNumber || !this.newReqData.minNumber) {
        this.$notify({
                group: 'foo',
                title: 'Cannot Add Requiremnet !',
                text: "Non Acceptable (Min,MaX)!",
                type: 'error'
              })
              return;
      }
    }
    this.newReqData.type = this.typeOpt
    this.newReqData.cCode = this.cCode
  axios.post(path2,this.newReqData)
    .then(this.returnedaddNewRequirements)
    .catch(function(error) {
      console.log(error)
    });
},
returnedaddNewRequirements(response) {
  var x = response.data
  console.log(this.courseList)
  if (x) {
    this.$notify({
              group: 'foo',
              title: 'success !',
              text: "Requirement is Added !",
              type: 'success'
            })
            this.fillRequirementStaff();
            return;
  }
  else {
    this.$notify({
            group: 'foo',
            title: 'Cannot Add Requiremnet !',
            text: "Something Went Wrong ",
            type: 'error'
          })
          return;
  }

},
    getUnassignedReq: function() {
      axios.get(path3,{
        params:{
          cCode: this.cCode
        }
      })
      .then(this.returnedgetUnassignedReq)
      .catch(function(error) {
        console.log(error)
      });
    },
    returnedgetUnassignedReq(response) {
      this.unAssignedReqList = response.data
      console.log(this.unAssignedReqList)
    },
    assignedReq: function(reqId) {
      var payload = {
        reqID:reqId,
        cCode:this.cCode
      }
      axios.post(path3,payload)
      .then(this.returnedassignedReq)
      .catch(function(error) {
        console.log(error)
      });
    },
    returnedassignedReq(response) {
      var x = response.data
      console.log(this.unAssignedReqList)
      if (x) {
        this.$notify({
                  group: 'foo',
                  title: 'success !',
                  text: "Requirement is assigned !",
                  type: 'success'
                })
                this.fillRequirementStaff();
                return;
      }
      else {
        this.$notify({
                group: 'foo',
                title: 'Cannot Assign Requiremnet !',
                text: "Something Went Wrong ",
                type: 'error'
              })
              return;
      }
    },
    goToreq:function(id){
      this.$parent.reqID=id
      this.$parent.$router.push('/staff2')
    },

    deleteReq: function(x){
        axios.delete(path3,{
          params:{
            reqID: x,
          }
        })
        .then(this.returneddeleteReq)
        .catch(function(error) {
          console.log(error)
        });
      },
      returneddeleteReq(response){
        var x= response.data
        console.log(this.deliverablesList)
        if (x) {
          this.$notify({
                group: 'foo',
                title: 'success !',
                text: "Requirement is Deleted !",
                type: 'success'
              })
              this.fillRequirementStaff();
              return;
            }
            else {
              this.$notify({
                group: 'foo',
                title: 'Cannot cannot delete requiremetn !',
                text: "Something Went Wrong ",
                type: 'error'
              })
              return;
            }
      }

    },
    beforeMount(){
      this.fillCoursesStaff()
    }
    }

</script>

<style scoped>
  .container-fluid{
    margin-left:8%
  }
  .myul{
    overflow-y:scroll;
    max-height:180px
  }

</style>
