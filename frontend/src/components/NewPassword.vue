<template>
  <div id="NewPassword" >
    <div class="container">
      <label for="Password"><b>New Password</b></label>
      <input type="text" v-model='password' placeholder="New Password " name="Password" required="required">
      <label for="password"><b>Confirm your Password</b></label>
      <input type="password" v-model='passwordc' placeholder="Confirm your Password" name="password" required="required">
      <button type="button" v-on:click="confirm()"style="width:auto;">Change Password</button>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
const path = 'http://127.0.0.1:5000/retrieve_account';
export default {
  name: 'NewPassword',
  data() {
    return {
      password: '',
      passwordc:'',
      email: this.$parent.recoveryemail
    }
  },
  methods: {
    confirm() {
      if(this.password=="")
      {
        this.$notify({
          group: 'foo',
          title: 'Recovery Failed',
          text: 'Password cannot be empty',
          type:'error'

      })
    }
      else if(this.password==this.passwordc)
      {
        console.log(this.email)
        const path = 'http://127.0.0.1:5000/change_password';
        var payload = {
          password:this.password,
          email: this.email
        };
        axios.patch(path, payload)
        .then(this.if_change)
          .catch((error) => {
          console.log(error);
        });
      }
      else {
        this.$notify({
          group: 'foo',
          title: 'Recovery Failed',
          text: 'Passwords do not match',
          type:'error'
        });
      }
    },
    if_change(res) {

      if(res.data.check) {
        this.$notify({
          group: 'foo',
          title: 'Recovery Succes',
          text: 'Login with your new Password',
          type:'succes'
        });
        console.log("changed Succesfully !");
         this.$parent.$router.replace('/')
      }

      }
    }
  }

</script>





</script>
<style scoped="NewPassword">
  body {font-family: Arial, Helvetica, sans-serif;}

  /* Full-width input fields */
  input[type=text], input[type=password] {
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
      border: none;
      cursor: pointer;
      width: 100%;
  }

  button:hover {
      opacity: 0.8;
  }

  /* Extra styles for the cancel button */
  .cancelbtn {
      width: auto;
      padding: 10px 18px;
      background-color: #f44336;
  }

  /* Center the image and position the close button */
  .imgcontainer {
      text-align: center;
      margin: 24px 0 12px 0;
      position: relative;
  }


  .container {
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
      width: 80%; /* Could be more or less, depending on screen size */
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
