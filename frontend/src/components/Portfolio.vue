<template>
  <div class="container-fluid">
    <div class="w3-row">
    <div class="w3-rest">
    <div class="w3-padding-64 w3-center">
      <h1 class="w3-xxxlarge">My Portfolio</h1>
    </div>
      </div>
    </div>
    <div class="row" >
      <div class="col-sm-2" ></div>
      <div class="col-sm-3" style="margin-top: .5%; margin-left:2%">
        <div class=" list-group" style="margin-top:8%">
        <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Courses</a>
        <div class=" list-group myul">
        <a href=""  class="list-group-item list-group-item-action" v-for="c in stdcourses" @click.prevent="fillRequirements(c)">{{c}}</a>
      </div>
      </div>
      </div>
      <div class="col-sm-1" ></div>
      <div class="col-sm-4" style="">
        <div class="w3-container" >
          <div class=" list-group" style="margin-top:8%">
          <a class="list-group-item " @click.prevent="" disabled style=" background-color:black; color:white; margin-bottom:.1% ">Assignment/Project</a>
          <div class=" list-group myul">
            <a href="#" class="list-group-item list-group-item-action" v-for="(v,index) in stdRequirements" v-if="stdRequirements[index].name!= null" @click.prevent="update(stdRequirements[index].id)">{{stdRequirements[index].name}}</a>
        </div>
        </div>
        </div>
      </div>
    </div>
     <div v-for="(value,index) in items" v-if="items[index].coursename" >
       <div id="1" class="modal">
         <div class="row" >
           <div class="col-sm-3">

           </div>
           <div class="col-sm-5" >
           <div class="container">
             <ul class="w3-ul w3-card-4 ">
               <li class="w3-bar w3-theme-l5" >
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Course Name:</span>
                   <span class="w3-xlarge"> {{value.coursename}}</span>
                 </div>
               </li>
               <li class="w3-bar w3-theme-l4" v-if="items[index].projectname">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Project Name:</span>
                   <span class="w3-xlarge"> {{value.projectname}}</span>
                 </div>
               </li>
               <li class="w3-bar w3-theme-l3">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Requirement Name:</span>
                   <span class="w3-xlarge"> {{value.reqname}}</span>
                 </div>
               </li>
               <li class="w3-bar w3-theme-l2">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Material:</span>
                   <span class="w3-xlarge"> {{value.material}}</span>
                 </div>
               </li>
               <li v-if="items[index].type==1"  class="w3-bar w3-theme-l1">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Type of delivery:</span>
                   <span class="w3-xlarge"> Single</span>
                 </div>
               </li>
               <div v-else>
                 <li class="w3-bar w3-theme-l1">
                   <div class="w3-bar-item">
                     <span class="w3-xlarge">Type of delivery:</span>
                     <span class="w3-xlarge"> Team</span>
                   </div>
                 </li>
                 <li class="w3-bar w3-theme-l1">
                   <div class="w3-bar-item">
                     <span class="w3-xlarge">Team name:</span>
                     <span class="w3-xlarge"> {{value.teamname}}</span>
                   </div>
                 </li>
               </div>
               <li class="w3-bar w3-theme-l5">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Feedback:</span>
                   <span class="w3-xlarge"> {{value.feedback}}</span>
                 </div>
               </li>
               <li class="w3-bar w3-theme-l4">
                 <div class="w3-bar-item">
                   <span class="w3-xlarge">Date:</span>
                   <span class="w3-xlarge"> {{value.sem}} {{value.year}}</span>
                 </div>
               </li>
             </ul>
             <button type="button" onclick="document.getElementById('1').style.display='none'" class="cancelbtn">Cancel</button>
           </div>
           </div>
           </div>


     </div>

     </div>


  </div>
</template>

<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/getdeliverbleCourse";
  const path2 = "http://127.0.0.1:5000/getdeliverblereq";
  export default {
    data() {
      return {
        stdcourses: [],
        stdRequirements: [],
        items:[]
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
        console.log(this.stdcourses)
      },
      fillRequirements: function(c) {
        console.log(c);
        axios.get(path2,{
        params:{
          username: this.$parent.username,
          coursename:c
        }
      })  .then(this.returnedRequirements)
          .catch(function(error) {
            console.log(error)
          });
      },
      returnedRequirements(response) {
        this.stdRequirements = response.data;
        console.log(this.stdRequirements)
      },
      update:function(id){
        console.log("inupdate");
        const path = 'http://127.0.0.1:5000/Portfolio';
        axios.get(path,{
          params:{
            username: this.$parent.username,
            id:id
          }
        })
        .then(this.fill_data)
          .catch((error) => {
          console.log(error);
        });
      },
      fill_data(res)
      {
        console.log("infilldata");
        console.log(res);
        if(res.data) {
          console.log("infilldata in if conditon");
        this.items=res.data
        document.getElementById(1).style.display="block";
        }
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

    input[type=text] {
      width: 100%;
      padding: 12px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
      margin-top: 6px;
      margin-bottom: 16px;
      resize: vertical;
    }


    button {
        background-color: #000;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: 1px solid #fff;
        cursor: pointer;
        width: 100%;
    }

    button:hover {
        opacity: 0.8;
    }
    input[type=button]:hover {
      background-color: #45a049;
    }

    .container {
      border-radius: 5px;
      background-color: #f2f2f2;
      padding: 20px;

    }
    /* Extra styles for the cancel button */
    .cancelbtn {
        width: auto;
        padding: 10px 18px;
        background-color: #f44336;
    }

    .container {
        padding: 16px;
    }

    span.password {
        float: right;
        padding-top: 16px;
    }

    /* The Modal (background) */
    .modal {
        display: none; /* Hidden by default */
        position: fixed; /* Stay in place */
        z-index: 1; /* Sit on top */
        left: 0;
        top: 0;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgb(0,0,0); /* Fallback color */
        background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
        padding-top: 60px;
    }

    /* Modal Content/Box */
    .modal-content {
        background-color: #fefefe;
        margin: 5% auto 15% auto; /* 5% from the top, 15% from the bottom and centered */
        border: 1px solid #888;
        width: 50%; /* Could be more or less, depending on screen size */
    }

    /* The Close Button (x) */
    .close {
        position: absolute;
        right: 25px;
        top: 0;
        color: #000;
        font-size: 35px;
        font-weight: bold;
    }

    .close:hover,
    .close:focus {
        color: red;
        cursor: pointer;
    }

    /* Add Zoom Animation */
    .animate {
        -webkit-animation: animatezoom 0.6s;
        animation: animatezoom 0.6s
    }

    @-webkit-keyframes animatezoom {
        from {-webkit-transform: scale(0)}
        to {-webkit-transform: scale(1)}
    }

    @keyframes animatezoom {
        from {transform: scale(0)}
        to {transform: scale(1)}
    }

    /* Change styles for span and cancel button on extra small screens */
    @media screen and (max-width: 300px) {
        span.password {
           display: block;
           float: none;
        }
        .cancelbtn {
           width: 100%;
        }

}
</style>
