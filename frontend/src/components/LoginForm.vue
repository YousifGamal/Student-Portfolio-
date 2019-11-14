<template>
  <div id="LoginForm" >
    <div class="adjpos">
    <div class="container" style="background-color:#f1f1f1">
      <label for="username"><b>Username</b></label>
      <input type="username" v-model='username' placeholder="Enter your username " name="username" required  autocomplete="username">

      <label for="password"><b>Password</b></label>
      <input type="password" v-model='password' placeholder="Enter Password" name="password" required>


    </div>

    <div class="container" style="background-color:#f1f1f1">
      <span class="psw">
      <button type="button" v-on:click="login()" style="width:auto;" >Login</button>
      <button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Forget Password</button></span>


     </div>
    </div>
    <div id="id01" class="modal">

    <form class="modal-content animate" >

      <span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>

      <div class="container" style="background-color:#f1f1f1">
        <label for="email"><b>Emailaddress</b></label>
        <input type="email" v-model="email" placeholder="Enter your recovery email address" name="email" required>
        <button type="button" v-on:click="Recover()"class="cancelbtn"style="background-color:black" >Recover your account</button>
        <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
      </div>
  </form>

</div>
</div>
</template>

<script>
  import axios from 'axios'
  const path = 'http://127.0.0.1:5000/login';
  const path1 = 'http://127.0.0.1:5000/retrieve_account';
  export default {
    name:'LoginForm',
    data() {
      return {
        username: '',
        password: '',
        email: ''
      }
    },
    methods: {
      login() {
        var payload = {
          username: this.username,
          password: this.password
        };
        //console.log(this.username);
        //console.log(this.password);
        axios.post(path, payload)
        .then(this.isUser)
          .catch((error) => {
          console.log(error);
          });
      },
      isUser(res) {
        if(res.data.username) {
          console.log(res.data);
          console.log(res.data.username);
          this.$parent.username=res.data.username;
          this.$parent.userType= res.data.type;
          if(res.data.type=='ADMIN')
          {
          this.$parent.$router.replace('/admin')
          }
          else{
           this.$parent.$router.replace('/Home')
         }
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Login Failed',
            text: 'Wrong User name or Password try Again !!',
            type:'error'



          });
          console.log("Not a User !");
        }
      },
      Recover() {
        const path1 = 'http://127.0.0.1:5000/retrieve_account';
        var payload1 = {
          email: this.email
        };
        axios.post(path1, payload1)
        .then(this.avi_email)
          .catch((error) => {
          console.log(error);
          });
      },
      avi_email(res) {
        if(res.data.check) {
          console.log("User !");
          this.$parent.recoveryemail=this.email
           this.$parent.$router.replace('/NewPassword')
        }
        else {
          this.$notify({
            group: 'foo',
            title: 'Recovery Failed',
            text: 'Recovery email not found !!',
            position:'top left',
            type:'error'
          });
          console.log("Not a User !");
        }
      }
    }
  }
</script>



<style scoped="LoginForm">
  body {font-family: Arial, Helvetica, sans-serif;
}

  h1{
    color: #f44259;
    position: relative;
  }

  /* Full-width input fields */
  input[type=username], input[type=password],input[type=email] {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      box-sizing: border-box;
  }

  /* Set a style for all buttons */
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
  .adjpos{
    padding: 16px;
    background-color: #f2f2f2;
    position: fixed;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
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
