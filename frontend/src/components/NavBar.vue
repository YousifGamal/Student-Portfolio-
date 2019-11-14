<template>
<div id = "nav-bars" class="w3-black">
    <!-- Icon Bar (Sidebar - hidden on small screens) -->
  <nav class="w3-sidebar w3-bar-block w3-small w3-hide-small w3-center">
    <!-- Avatar image in top left corner -->
    <a href="#" class="w3-bar-item w3-button w3-padding-large w3-black" v-on:click.prevent='goToHome'>
      <i class="fa fa-home w3-xxlarge"></i>
      <p>HOME</p>
    </a>
    <a href="#" class="w3-bar-item w3-button w3-padding-large w3-hover-black" v-on:click.prevent='goToAccount'>
      <i class="fa fa-sliders w3-xxlarge"></i>
      <p>ACCOUNT</p>
    </a>
    <a href="#" class="w3-bar-item w3-button w3-padding-large w3-hover-black" v-on:click.prevent='goToPortfolio'
     v-if="$parent.userType == 'STUDENT'">
      <i class="fa fa-user w3-xxlarge"></i>
      <p>PORTOFOLIO</p>
    </a>
    <a href="#" class="w3-bar-item w3-button w3-padding-large w3-hover-black" v-on:click.prevent='goToCourses'>
      <i class="fa fa-book w3-xxlarge"></i>
      <p>COURSES</p>
    </a>
    <a href="#" class="w3-bar-item w3-button w3-padding-large w3-hover-black" v-on:click.prevent='goToLogin'>
      <i class="fa fa-sign-out w3-xxlarge"></i>
      <p>LOGOUT</p>
    </a>

  </nav>

  <!-- Navbar on small screens (Hidden on medium and large screens) -->
  <div class="w3-top w3-hide-large w3-hide-medium" id="myNavbar">
    <div class="w3-bar w3-black w3-opacity w3-hover-opacity-off w3-center w3-small">
      <a href="#" class="w3-bar-item w3-button" style="width:25% !important" v-on:click.prevent='goToHome'> HOME</a>
      <a href="#" class="w3-bar-item w3-button" style="width:25% !important" v-on:click.prevent='goToAccount'>ACCOUNT</a>
      <a href="#" class="w3-bar-item w3-button" style="width:25% !important" v-on:click.prevent='goToPortfolio'
       v-if="$parent.userType == 'STUDENT'" >PORTFOLIO</a>
      <a href="#" class="w3-bar-item w3-button" style="width:25% !important" v-on:click.prevent='goToCourses'>COURSES</a>
      <a href="#" class="w3-bar-item w3-button" style="width:25% !important" v-on:click.prevent='goToLogin'>LOGOUT</a>
    </div>
  </div>
</div>
</template>

<script>
export default {
  methods: {
    goToHome: function() {
      this.$parent.$router.replace('/Home')
    },
    goToAccount: function() {
      this.$parent.$router.replace('/Account')
    },
    goToPortfolio: function() {
      this.$parent.$router.replace('/portfolio')
    },
    goToCourses: function() {
      if(this.$parent.userType == 'STUDENT') {
        this.$parent.$router.replace('/course')
      }
      else {
        this.$parent.$router.replace('/staff1')
      }
    },
    goToLogin: function() {
      this.$parent.$router.replace('/')
      }
  }
}
</script>

<style scoped>
  a:hover {text-decoration: none}
</style>
