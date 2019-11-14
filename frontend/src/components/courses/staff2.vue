<template >
  <div class="container-fluid">
    <div class="w3-container">
      <div class="row">
        <div class="col-sm-2">

        </div>

        <div class="col-sm-6">


            <div class="w3-responsive ">
              <table class="w3-table w3-striped w3-bordered w3">
                <h1>Requirement Info</h1>
              <tr>
                <th></th>
                <th></th>
                <th></th>
                <th></th>
              </tr>
              <tr>
                <td>Course Name:</td>
                <td v-if="reqInfo">{{reqInfo.cName}}</td>
                <td>Project Name</td>
                <td v-if="reqInfo">{{reqInfo.projName}}</td>
              </tr>
              <tr>
                <td>Type </td>
                <td v-if="reqInfo && reqInfo.type == 0">Team</td>
                <td v-if="reqInfo && reqInfo.type == 1">Individual</td>
                <td>#</td>
                <td v-if="reqInfo && reqInfo.type == 0">{{reqInfo.lower}} - {{reqInfo.upper}}</td>
                <td v-if="reqInfo && reqInfo.type == 1">N/A</td>
              </tr>
              </table>
      </div>

    </div>
    </div>
    <div class="w3-container">
      <div class="row" style="padding-top:2%">
        <div class="col-sm-2">
</div>
          <div class="col-sm-3">
            <div class="form-group text-center" style="padding-top:2%">
                  <button type="submit" @click.prevent="unassignReq()"  v-if="" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                    Unassigne
                  </button>
                </div>
                </div>
                <div class="col-sm-3">
                  <div class="form-group text-center" style="padding-top:2%">
                        <button type="submit" @click.prevent="goToStats()"  v-if="" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                          Stats
                        </button>
                      </div>




</div>
      </div>

    </div>
    <div class="row">
      <div class="col-sm-2">

      </div>
      <div class="col-sm-6">
        <form class >
              <div class="form-group" style="">

      <label for="Name"  style="padding-top:2%" >Requirement Name</label>
      <input type="text" v-if="reqInfo" v-model="reqInfo.reqName" readonly class="w3-input w3-round-medium " id="Name" />
      <label for="document" style="padding-top:2%" >Document</label>
      <input type="text" v-if="reqInfo" v-model="reqInfo.document" readonly class="w3-input w3-round-medium " id="document"/>
      <label for="additional" style="padding-top:2%" >Additional Matterials</label>
      <input type="text" v-if="reqInfo" v-model="reqInfo.additionalMaterial" readonly class="w3-input w3-round-medium " id="additional"/>
      <label for="deliverableTime" style="padding-top:2%">DeadLine for the Requirement</label>
      <input type="date" v-if="reqInfo" v-model="deadlineDate" readonly id="deliverableTime" class="w3-input w3-round-medium" >
</div>

      <div class="form-group text-center" style="padding-top:2%">
              <button type="submit" @click.prevent="buttonEditPressed()"  v-if="editReq" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                Edit
              </button>
            </div>
            <div class="form-group text-center" style="padding-top:2%">
                    <button type="submit" @click.prevent="updateReqInfo()" v-if="!editReq" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;">
                      Update
                    </button>
                  </div>
            </form>
    </div>
</div>
<div class="w3-container">


<div class="row" style="margin-top:5%">

<div class="col-sm-6">
  <div class=" list-group"  style="margin-top:4.5%">
    <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white;  margin-bottom:.1%">Deliverables</a>
<div class=" list-group myul" >
    <span class="list-group-item list-group-item-action" v-if ="x != null && x[12]" v-for ="x in deliverablesList">
    <a href="" class="list-group-item-action"  @click.prevent="someDelivInfo(x[8],x[0])" >{{x[12]}}: {{x[4]}}</a>
  <span class="w3-right"> <button type="submit" v-if ="x != null && x[12]" @click.prevent="deleteDeliverable(x[0])"  class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;"> Delete</button></span></span>
<span class="list-group-item list-group-item-action" v-if ="x != null && x[13]" v-for ="x in deliverablesList" >
    <a href=""  class="list-group-item-action"  @click.prevent="someDelivInfo(x[8],x[0])" >{{x[13]}}: {{x[4]}}</a><span class="w3-right"><button type="submit" v-if ="x != null && x[13]" @click.prevent="deleteReq(x.reqID)"  class="btn btn-primary btn-block w3-black" style="border:#e7e7e7;"> Delete</button></span></span>
  </div>
</div>
    </div>




    <div class="col-sm-4">
            <h1 v-if="!devHide">Feedback</h1>

            <textarea  class="w3-input w3-round-large"  id="deliv" readonly v-if="!devHide && !inputShow" v-model="feedback" style="height:65%"/>
            <input type="text" class="w3-input w3-round-large"  id="deliv"  v-if="!devHide && inputShow" v-model="feedback" style="height:65%"/>
            <button type="submit"   v-if="!devHide && !btnHide" @click.prevent="addFeedback()" class="btn btn-primary btn-block w3-black" style="border:#e7e7e7; margin-top:1%">
              Submit
            </button>
</div>

</div>
</div>
<div class="w3-container">
  <div class="row" style="margin-bottom:3%; margin-top:6.5%">
    <div class="col-sm-6">
      <div class=" list-group"  >
        <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Teams</a>
<div class=" list-group myul"  >
        <a href=""  @click.prevent="deleteTeam(x.teamID)" class="list-group-item list-group-item-action" v-if ="teamsList" v-for ="x in teamsList">{{x.teamName}}</a>
      </div>
</div>
    </div>

  </div>

</div>
</div>
  </div>

</template>


<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/stdReq";
  const path1 = "http://127.0.0.1:5000/deliverablesStaff";
  const path2 = "http://127.0.0.1:5000/teamsinDeliverables";
  const path3 = "http://127.0.0.1:5000/unAssignedReqStaff";
  const path4 = "http://127.0.0.1:5000/deleteDeliverable";
  export default {
    data() {
      return {
        date:"",
        reqInfo:[],
        deadlineDate:"",
        editReq:true,
        date:"",
        deliverablesList:[],
        feedback:"N/A",
        devHide:true,
        btnHide:true,
        delivID:"",
        teamsList:"",
        inputShow:"true",
      }
    },
    methods: {
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
          var x = response.data
          this.reqInfo = x[0]
          this.deadlineDate = new Date(this.reqInfo.deadline).toISOString().split("T")[0];
          var currentdate = new Date();
          this.date = currentdate.getFullYear()+"-"+(currentdate.getMonth()+1) +"-"+currentdate.getDate()
          console.log(this.deadlineDate);
          console.log(this.reqInfo);
          this.filldeliverables()
          this.gatTeams()
        },
        buttonEditPressed:function(){
          this.editReq = false
          document.getElementById('Name').readOnly = false;
          document.getElementById('document').readOnly = false;
          document.getElementById('additional').readOnly = false;
          document.getElementById('deliverableTime').readOnly = false;

        },
        updateReqInfo: function(){
          var payload = {
            reqID:this.$parent.reqID,
            name:this.reqInfo.reqName,
            deadline:this.deadlineDate,
            addMaterials:this.reqInfo.additionalMaterial,
            document:this.reqInfo.document
          }
          if (!this.reqInfo.reqName) {
            this.$notify({
              group: 'foo',
              title: 'Cannot update Requiremnet !',
              text: "Name Cannot be Empty ",
              type: 'error'
            })
            return;
          }
          if (!this.reqInfo.additionalMaterial) {
            this.$notify({
              group: 'foo',
              title: 'Cannot update Requiremnet !',
              text: "Additional Material Cannot be Empty (put N/A if there is nothing to entre)",
              type: 'error'
            })
            return;
          }
          if (!this.reqInfo.document) {
            this.$notify({
              group: 'foo',
              title: 'Cannot update Requiremnet !',
              text: "Document Cannot be Empty ",
              type: 'error'
            })
            return;
          }
          if (this.deadlineDate <= this.date) {
            this.$notify({
              group: 'foo',
              title: 'Cannot Add Requiremnet !',
              text: "Non Acceptable Date!",
              type: 'error'
            })
            return;
          }
            axios.put(path,payload)
            .then(this.returnedupdateReqInfo)
            .catch(function(error) {
              console.log(error)
            });
          },returnedupdateReqInfo(response){
            var x = response.data
            if (x) {
              this.$notify({
                    group: 'foo',
                    title: 'success !',
                    text: "Requirement is updated !",
                    type: 'success'
                  })
                  return;
                }
                else {
                  this.$notify({
                    group: 'foo',
                    title: 'Cannot update Requiremnet !',
                    text: "Something Went Wrong ",
                    type: 'error'
                  })
                  return;
                }

          },
          filldeliverables: function(){
              axios.get(path1,{
                params:{
                  reqID: this.$parent.reqID,
                  cCode: this.reqInfo.cCode
                }
              })
              .then(this.returnedfilldeliverables)
              .catch(function(error) {
                console.log(error)
              });
            },returnedfilldeliverables(response){
              this.deliverablesList= response.data
              console.log(this.deliverablesList)
            },
            someDelivInfo:function(x,y){
              console.log("//////////////////////someDeliverableinfo");
              this.delivID = y
              console.log(this.delivID);
              if (x == null) {
                this.feedback = "n/a"

          //      document.getElementById("deliv").readOnly = false


                this.devHide = false
                this.btnHide = false
                console.log(this.feedback);
                this.inputShow = true;
              //  let inputName = document.querySelector('#deliv');
              //  console.log(inputName);
              //  inputName.removeAttribute('readonly');


              }
              else {
                this.feedback = x
                this.devHide = false
                this.btnHide = true
                this.inputShow = false;

            //    document.getElementById("deliv").readOnly = true

              }
            },
            addFeedback: function(){
              if (!this.feedback) {
                this.$notify({
                  group: 'foo',
                  title: 'Cannot add FeedBack !',
                  text: "there is nothing to submit ",
                  type: 'error'
                })
                return;
              }

              var payload = {
              deliverableID:this.delivID,
              deliverableData:this.feedback,
              staffusername:this.$parent.username
            }
                axios.put(path1,payload)
                .then(this.returnedaddFeedback)
                .catch(function(error) {
                  console.log(error)
                });
              },
              returnedaddFeedback(response){
                var x= response.data
                console.log(this.deliverablesList)
                if (x) {
                  this.$notify({
                        group: 'foo',
                        title: 'success !',
                        text: "Feedback is added !",
                        type: 'success'
                      })
                      return;
                    }
                    else {
                      this.$notify({
                        group: 'foo',
                        title: 'Cannot add FeedBack !',
                        text: "Something Went Wrong ",
                        type: 'error'
                      })
                      return;
                    }
              },
              gatTeams: function(){
                  axios.get(path2,{
                    params:{
                      reqID: this.$parent.reqID,
                      cCode:this.reqInfo.cCode
                    }
                  })
                  .then(this.returnedgatTeams)
                  .catch(function(error) {
                    console.log(error)
                  });
                },returnedgatTeams(response){
                  this.teamsList = response.data
                  console.log(this.teamsList);
                },
                deleteTeam: function(teamID){
                  console.log(teamID);

                    axios.delete(path2,{
                      params:{

                        teamID:teamID
                      }
                    })
                    .then(this.returneddeleteTeam)
                    .catch(function(error) {
                      console.log(error)
                    });
                  },returneddeleteTeam(response){
                    console.log("/////////delete");
                    var x= response.data
                    console.log(this.deliverablesList)
                    if (x) {
                      this.$notify({
                            group: 'foo',
                            title: 'success !',
                            text: "Team is Deleted !",
                            type: 'success'
                          })
                          return;
                        }
                        else {
                          this.$notify({
                            group: 'foo',
                            title: 'Cannot delete team !',
                            text: "Team already deliverd the requirement",
                            type: 'error'
                          })
                          return;
                        }
                  },
                  unassignReq: function(){
                    if (this.deliverablesList.length > 0) {
                      this.$notify({
                        group: 'foo',
                        title: 'Cannot  delete requirement !',
                        text: "There are existing deliverables for this requirement",
                        type: 'error'
                      })
                      return;
                    }

                      axios.delete(path1,{
                        params:{
                          reqID: this.$parent.reqID,
                          cCode:this.reqInfo.cCode
                        }
                      })
                      .then(this.returnedunassignReq)
                      .catch(function(error) {
                        console.log(error)
                      });
                    },returnedunassignReq(response){
                      var x= response.data
                      console.log(this.deliverablesList)
                      if (x) {
                        this.$notify({
                              group: 'foo',
                              title: 'success !',
                              text: "REquirement is unassigned for this SEMESTER !",
                              type: 'success'
                            })
                            return;
                          }
                          else {
                            this.$notify({
                              group: 'foo',
                              title: 'Cannot  delete requirement !',
                              text: "There are existing deliverables for this requirement",
                              type: 'error'
                            })
                            return;
                          }
                    },
                    deleteDeliverable: function(x){
                        axios.delete(path4,{
                          params:{
                            deliverableID: x

                          }
                        })
                        .then(this.returneddeleteDeliverable)
                        .catch(function(error) {
                          console.log(error)
                        });
                      },returneddeleteDeliverable(response){
                        var x= response.data
                        console.log(this.deliverablesList)
                        if (x) {
                          this.$notify({
                                group: 'foo',
                                title: 'success !',
                                text: "Deliverable is Deleted !",
                                type: 'success'
                              })
                              return;
                            }
                            else {
                              this.$notify({
                                group: 'foo',
                                title: 'Cannot delete deliverable !',
                                text: "Something Went Wrong ",
                                type: 'error'
                              })
                              return;
                            }
                      },
                      goToStats:function(){
                        console.log('print a7a msh sh8al');
                        this.$parent.$router.push('/requirement-statistics')
                      }



    },
    beforeMount(){
      this.fillReqInfo()
    }
      }


</script>



<style scoped>
  .container-fluid{
    margin-left:9%
  }
  .myul{
    overflow-y:scroll;
    max-height:180px
  }
  .feed{
    max-width:20%
  }
</style>
