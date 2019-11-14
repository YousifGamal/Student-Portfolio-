<template>
  <div id="app">
    <router-view name='navbar'/>
    <router-view name='mainContent'/>
    <notifications group="foo" position="bottom center" width="30%" />
  </div>
</template>

<script>
export default {
  name: 'App',
  data(){
    return{
      recoveryemail:"",
      username:"",
      reqID:"",
      userType:""

    }},
    beforeMount() {
    if (localStorage.username) {
      this.username = localStorage.username;
    }
    if (localStorage.reqID) {
      this.reqID = localStorage.reqID;
    }
    if (localStorage.userType) {
      this.userType = localStorage.userType;
    }


  },
  watch: {
    username(newName) {
      localStorage.username = newName;
    },
    reqID(newreqID) {
      localStorage.reqID = newreqID;
    },
    userType(newType)
    {
      localStorage.userType = newType;
    }

  }
  }
</script>


<style>
body{
  height: 100vh;
  background: rgb(159,159,159);
  background: linear-gradient(90deg,rgba(159,159,159,1)0%,rgba(226,226,226,1)50%,rgba(159,159,159,1)100%);
}
#app{
  height: 100%;
}

</style>
