<template>
  <div id ="Account">
          <div class="adjpos">
          <h2>Account Information</h2>
            <label for="username"><b>UserName</b></label>
            <input type="username" v-model='username' placeholder="Enter your username " name="username" autocomplete="username" readonly=True >
            <label for="email"><b>Emailaddress</b></label>
            <input type="email" v-model="email" placeholder="Enter your recovery email address" name="email" autocomplete="email" readonly=True>
            <label for="type"><b>Type</b></label>
            <input type="username" v-model='type' placeholder="Enter Password" name="username" required="required" readonly=True >
            <div class="container" style="background-color:#f1f1f1">
              <span class="psw"> <button onclick="document.getElementById('2').style.display='block'" style="width:auto;">Edit Your Information</button></span>
            </div>
            </div>
            <div id="2" class="modal">
             <form class="modal-content animate" >
              <span onclick="document.getElementById('2').style.display='none'" class="close" title="Close Modal">&times;</span>
              <div class="container" style="background-color:#f1f1f1">
                <label for="password"><b></b></label>
                <input type="password" v-model='cpassword' placeholder="Enter your current password" name="cpassword" required>
                 <button type="button" v-on:click="checkpassword(`1`)" style="width:auto;">Enter Your current password</button>
                <button type="button" onclick="document.getElementById('2').style.display='none'" class="cancelbtn">Cancel</button>
              </div>
            </form>
          </div>

          <div id="1" class="modal">

          <form class="modal-content animate">
              <span onclick="document.getElementById('1').style.display='none'" class="close" title="Close Modal">&times;</span>
              <div class="container">
                <label for="username"><b>UserName</b></label>
                <input type="username" v-model='username' placeholder="Enter your username " name="username" autocomplete="username"  >
                <label for="email"><b>Emailaddress</b></label>
                <input type="email" v-model="email" placeholder="Enter your recovery email address" name="email" autocomplete="email" >
                <label for="password"><b>Password</b></label>
                <input type="password" v-model='password' placeholder="Enter Password" name="password" required="required"  >
                <button type="button" v-on:click="UpdateInformation()" style="width:auto;"  >UpdateInformation </button>
                <button type="button" onclick="document.getElementById('1').style.display='none'" class="cancelbtn">Cancel</button>
              </div>

          </form>
        </div>


  </div>
</template>

<script>
import axios from 'axios'
const path = 'http://127.0.0.1:5000/Account';
const path1='http://127.0.0.1:5000/Account_update';
export default {
  name: 'Account',
  data() {
    return {
      username:"",
      email:"",
      password:"",
      type:"",
      cpassword:""

    }
  },
  methods: {
    update:function(){
      axios.get(path,{
        params:{
          username: this.$parent.username
        }
      })
      .then(this.fill_data)
        .catch((error) => {
        console.log(error);
      });
    },
    fill_data(res)
    {
      if(res.data.username) {
      this.username=res.data.username;
      this.password=res.data.password;
      this.email=res.data.email;
      this.type=res.data.type;
      }
    },
    UpdateInformation()
    {
      if(this.username==""||this.password==""||this.email=="")
      {
        this.$notify({
          group: 'foo',
          title: 'Update Failed',
          text: 'Please Fill All Areas ',
          type:'error'
      })
      }
      else{
      var payload1 = {
        username: this.username,
        password: this.password,
        email:this.email,
        oldusername:this.$parent.username
      };
      axios.patch(path1, payload1)
      .then(this.done)
        .catch((error) => {
        console.log(error);
        });
    }},
    done(res)
    {
      console.log(res.data.check);
      if(res.data.check)
      {
        this.$notify({
          group: 'foo',
          title: 'Update Succes',
          text: 'Information Updated Succesfully ',
          type:'succes'
      })
      this.$parent.username=this.username
      document.getElementById(1).style.display="none";
    }
    else {
      this.$notify({
        group: 'foo',
        title: 'Update Failed',
        text: 'user name already taken choose another one ',
        type:'error'
    })

  }},
  checkpassword(idno)
  {
    console.log(idno);

    if(this.cpassword===this.password)
    {
      document.getElementById(2).style.display="none";
      document.getElementById(1).style.display="block";

    }
    else{
      this.$notify({
        group: 'foo',
        title: 'Wrong password',
        text:'Please Enter the right password',
        type:'error'
    })
    }

  }
},
  beforeMount()
  {
    this.update()

  }

}
</script>


<style scoped="Account" >
  body {font-family: Arial, Helvetica, sans-serif;
         box-sizing: border-box;}



  input[type=username],input[type=email],input[type=Password] {
    width: 100%;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    margin-top: 6px;
    margin-bottom: 16px;
    resize: vertical;
  }

  input[type=button] {
    background-color: #4CAF50;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: auto;
  }

  input[type=button]:hover {
    background-color: #45a049;
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
  .adjpos{
    padding: 16px;
    background-color: #f2f2f2;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
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
