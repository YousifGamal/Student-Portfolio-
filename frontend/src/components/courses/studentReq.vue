<template>
  <div class="container-fluid row">
    <div class = 'col-sm-1'></div>
    <div class = 'col-sm-8'>
      <div class="row">

        <div class="col-sm-12" style="padding:0;">
          <div class="w3-container">
            <h1 v-if="reqInfo[0] != undefined">{{reqInfo[0].reqName}}</h1>
            <div class="w3-responsive ">
              <table class="w3-table w3-striped w3-bordered w3">
              <tr>
                <th></th>
                <th></th>
                <th></th>
                <th></th>
              </tr>
              <tr>
                <td>Course Name:</td>
                <td v-if="reqInfo[0] != undefined">{{reqInfo[0].cName}}</td>
                <td>Document</td>
                <td v-if="reqInfo[0] != undefined">{{reqInfo[0].document}}</td>
              </tr>
              <tr>
                <td>Project Name:</td>
                <td v-if="reqInfo[0] != undefined">{{reqInfo[0].projName}}</td>
                <td>Additional material</td>
                <td v-if="reqInfo[0] != undefined">{{reqInfo[0].additionalMaterial}}</td>
              </tr>
              <tr>
                <td>Type:</td>
                <td v-if="reqInfo[0] != undefined && reqInfo[0].type == 0">Team</td>
                <td v-if="reqInfo[0] != undefined && reqInfo[0].type == 1">Idividual</td>
                <td>Deadline</td>
                <td v-if="reqInfo[0] != undefined && reqInfo[0].deadline == null">N/A</td>
                <td v-if="reqInfo[0] != undefined && reqInfo[0].deadline != null">{{reqInfo[0].deadline}}</td>
              </tr>
            </table>
          </div>
        </div>
      </div>


      </div>
  <!--///////////////////////////// Team Section  //////////////////// -->
      <div class="row" v-if="reqInfo[0] != undefined && reqInfo[0].type == 0 && inTeamboool ">

        <div class="col-sm-6"  >
          <div class="w3-container">
            <h2>Team Info</h2>
            <table class="w3-table w3-striped w3-bordered w3">
              <tr>
                <th></th>
                <th></th>
              </tr>
              <tr>
                <td>Name:</td>
                <td v-if="teamInfo.tmName != undefined">{{teamInfo.tmName}}</td>
              </tr>
              <tr>
                <td>#:</td>
                <td v-if="studentlist != null">{{studentlist.length+1}}</td>
                </tr>
            </table>
          </div>
        </div>
        <div class="col-sm-6">
          <h2>Team Members</h2>
          <ul class="w3-ul w3-card-4">
            <li class="w3-bar" v-for ="student in studentlist">
              <div class="w3-bar-item">
                <span class="w3-large" v-if="studentlist != null">{{student.stdName}}</span><br>
                <span v-if="studentlist != null">{{student.email}}</span>
              </div>
            </li>

          </ul>
          </div>
        </div>

  <!--/////////////////////////////////////////////add Team Section ///////////////////////////////////// -->
            <div class="row"  v-if="reqInfo[0] != undefined && reqInfo[0].type == 0 && !inTeamboool">

              <div class="col-sm-10">
                <div class="container">
          <h2>Create Team</h2>

          <form>
            <div class="form-group">
              <label for="teamName">Team Name</label>
              <input type="text" class="w3-input w3-round-medium" id="teamName" placeholder="Enter Team Name" v-model='teamName'  />
              <label for="teamNo">Team Number</label>
              <input type="number" class="w3-input w3-round-medium" id="teamNo" placeholder="Enter Team Number" v-model.number='teamNo'  />
              <div class="form-group" v-for ="(n,index) in (reqInfo[0].upper-1)" v-if="reqInfo != null">
              <label for="sel1" >Team Member {{index + 1}}</label>
              <select class="w3-select w3-round-medium" id="sel1" v-model = "stdIds[`${index}`]">
                <option value="-1" selected >None</option>
                <option  v-for="std in noTeamStudentList" v-bind:value="`${std.stdId}`">{{std.stdName}}</option>
              </select>
              </div>
              <div class="form-group text-center" style="padding-top:2%">
                <button type="submit" @click.prevent="addStudents()" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                  Submit
                </button>
              </div>
            </div>
          </form>
        </div>

              </div>


            </div>


        <div class="row" >
          <div class="col-sm-6">
            <h1 >Feedback</h1>
            <div >
              <textarea class="w3-input w3-round-large" readonly  v-if="deliverable.feedback != undefined && deliverable.feedback !=null" >Eng. {{deliverable.sName}}: {{deliverable.feedback}}</textarea>
              <p v-else  class="w3-input w3-round-large" >There is no feedback yet</p>
              </div>
            </div>
            <div class="col-sm-6" v-if="reqInfo[0] != undefined && reqInfo[0].type == 1 ||(reqInfo[0].type == 0 && inTeamboool) ">
              <div class="form-group">

                  <h1>Deliver</h1>
                <label for="requirement_id" v-if="!deliverableInfo.isDeliveredd" style="width:100%;">
                  <input type="text" placeholder="Enter the link to your requirement"  class="w3-input w3-round-medium" id="requirement_id"  v-model='deliverableLink'/>
                </label >
                <label for="requirement_id2" v-if="deliverableInfo.isDeliveredd == true" style="width:100%;">
                  <textarea type="text" class="w3-input w3-round-medium" id="requirement_id2"  readonly="true" v-if="deliverable != undefined " v-model="deliverable.dmaterials"/>
                </label >
                </div>
                <div class="form-group text-center">
                  <button type="submit" class="btn btn-primary w3-black w3-button" style="border:#e7e7e7;"v-if="deliverableInfo.isDeliveredd == false" @click.prevent="addnewDeliverable()" >
                    Submit
                  </button>
                </div>
              </div>
          </div>

        </div>
        <div class = 'col-sm-2'></div>
      </div>

</template>

<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/stdReq";
  const path2 = "http://127.0.0.1:5000/inTeam";
  const path3 = "http://127.0.0.1:5000/TeamInfo";
  const path4 = "http://127.0.0.1:5000/noTeamStdInfo";
  const path5 = "http://127.0.0.1:5000/AddTeam";
  const path6 = "http://127.0.0.1:5000/deliverable";

  export default {
    data() {
      return {
        reqInfo: [],
        inTeamboool: '', //this variable to know if he is in a team or not
        teamInfo:{
          tmName:"",
          tmNumber:"",
          tmId:""
        },
        studentlist:[],
        wholelist:[],
        teamName:"",
        teamNo:"",
        noTeamStudentList:[],
        stdIds:[],
        teamNoBool:"",
        deliverable: '',
        deliverableInfo:{
          isDeliveredd:false,
        },
        deliverableLink:""
      }
    },
    methods: {
        submitEmail: function() {
          console.log(this.email)
        },
        fillReqInfo: function(){
          axios.get(path,{
            params:{
              reqID: this.$parent.reqID
            }
          })
          .then(this.returnedReqInfo)
          .catch(function(error) {
            console.log(error)
          });
        },returnedReqInfo(response){
          this.reqInfo = response.data
          console.log(this.reqInfo)
          for (var i = 0; i < this.reqInfo[0].upper-1; i++) {
            this.stdIds.push(-1)}
        },
        isInTeam: function(){
          axios.get(path2,{
            params:{
              reqID: this.$parent.reqID,
              username: this.$parent.username
            }
          })
          .then(this.returnedisInTeam)
          .catch(function(error) {
            console.log(error)
          });
        },returnedisInTeam(response){
          this.inTeamboool = response.data
          console.log(this.inTeamboool)
        },
        TeamInfo: function(){
          axios.get(path3,{
            params:{
              reqID: this.$parent.reqID,
              username: this.$parent.username
            }
          })
          .then(this.returnedTeamInfo)
          .catch(function(error) {
            console.log(error)
          });
        },returnedTeamInfo(response){
          this.wholelist = response.data
          console.log(this.wholelist)
          this.studentlist = this.wholelist.Students
          this.teamInfo.tmName = this.wholelist.Team.tmName
          this.teamInfo.tmNumber = this.wholelist.Team.tmNumber
          this.teamInfo.tmId = this.wholelist.Team.tmId

          this.deliverableshit();
        },
        noTeamStudents: function(){
          axios.get(path4,{
            params:{
              reqID: this.$parent.reqID,
              username: this.$parent.username
            }
          })
          .then(this.returnednoTeamStudent)
          .catch(function(error) {
            console.log(error)
          });
        },returnednoTeamStudent(response){
          this.noTeamStudentList = response.data
          console.log(this.noTeamStudentList)
        },
        addStudents: function(){
          var count = 0;
          for (var i = 0; i < this.reqInfo[0].upper-1; i++) {
            if (this.stdIds[i] != -1) {
              count++;
            }
          }
          if (count >= (this.reqInfo[0].lower-1)) {
            console.log("You can add suceefully");
          }
          else {
            this.$notify({
                group: 'foo',
                title: 'Cannot create Team !',
                text: "Number of selected students is less than allowed !",
                type: 'error'
              })
              return;
          }

          if (this.teamNo <= 0) {
            this.$notify({
                group: 'foo',
                title: 'Cannot create Team !',
                text: "Team Number Cannot be zero or negative!",
                type: 'error'
              })
              return;
          }
          this.isTeamNoAviLable();


        },
        isTeamNoAviLable: function(){
          axios.get(path5,{
            params:{
              reqID: this.$parent.reqID,
              tmno: this.teamNo
            }
          })
          .then(this.returnedisTeamNoAviLable)
          .catch(function(error) {
            console.log(error)
          });
        },returnedisTeamNoAviLable(response){
          this.teamNoBool = response.data
          console.log(this.teamNoBool)
          if (!this.teamNoBool) {
            this.$notify({
                group: 'foo',
                title: 'Cannot create Team !',
                text: "This Team Number is taken!",
                type: 'error'
              })
              return;
          }

              for(var i = 0; i < this.stdIds.length; i++) {
                if(this.stdIds[i] == -1) {
                  this.stdIds[i] = this.stdIds[this.stdIds.length - 1];
                  this.stdIds.pop();
                  i--;
                }
              }
              var ncount = this.countUnique(this.stdIds)
              if (ncount < (this.reqInfo[0].lower-1)) {
                this.$notify({
                    group: 'foo',
                    title: 'Cannot create Team !',
                    text: "Number of selected students is less than allowed !",
                    type: 'error'
                  })
                  return;
              }
              else {
                this.$notify({
                    group: 'foo',
                    title: 'success !',
                    text: "Team is Created !",
                    type: 'success'
                  })
              }

              var requirement = this.reqInfo[0]
              var payload = {
                username: this.$parent.username,
                courseCode: requirement.cCode,
                requirementID: requirement.reqID,
                teamName: this.teamName,
                teamNumber: this.teamNo,
                studentIDs: this.stdIds
              }
              axios.post(path5, payload)
              .then(this.teamAdded)
              .catch(function(error) {
                console.log(error);
              })
        },
        teamAdded: function(response) {
          console.log(response.data);
          this.loadData();
        },
        deliverableshit: function(){
          console.log('team info: ' + this.teamInfo)
          console.log("team id: " + this.teamInfo.tmId);
          axios.get(path6,{
            params:{
              reqID: this.$parent.reqID,
              username: this.$parent.username,
              teamID: this.teamInfo.tmId
            }
          })
          .then(this.returneddeliverableshit)
          .catch(function(error) {
            console.log(error)
          });
        },returneddeliverableshit(response){
          var x = response.data
          this.deliverableInfo.isDeliveredd = x.is_delivered
          console.log(x);
          if (this.deliverableInfo.isDeliveredd) {
            this.deliverable = x;
            console.log(this.deliverable);
          }

        },
        addnewDeliverable: function(){
          if (!this.deliverableLink) {
            this.$notify({
              group: 'foo',
              title: 'Cannot add deliverable !',
              text: "Nolink was provided !!",
              type: 'error'
            })
            return
          }
          var payload = {
            req_id:this.$parent.reqID,
            cCode:this.reqInfo[0].cCode,
            materials:this.deliverableLink,
            tmID:this.teamInfo.tmId,
            username: this.$parent.username
          }
          axios.post(path6,payload)
          .then(this.returnedaddnewDeliverable)
          .catch(function(error) {
            console.log(error)
          });
        },returnedaddnewDeliverable(response){
          var x = response.data
          if (!x) {
            this.$notify({
              group: 'foo',
              title: 'Cannot add deliverable !',
              text: "Something went wrong !",
              type: 'error'
            })
          }
          else {
            this.$notify({
              group: 'foo',
              title: 'Delivered !',
              text: "Congrats and have a nice day!",
              type: 'success'
            })
            this.loadData();
          }
        },
         countUnique(iterable) {
          return new Set(iterable).size;
        },
        loadData: function() {
          this.fillReqInfo()
          this.isInTeam()
          this.TeamInfo()
          this.noTeamStudents()
        }

    },
    beforeMount(){
      this.loadData();



    }
  }
</script>

<style scoped>
  .container-fluid {
    margin-left: 120px;
  }
  a:hover {
    text-decoration: none;
  }
  .col-md-4
  {
    padding: 2%;
  };

</style>
