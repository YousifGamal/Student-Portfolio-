<template>
    <div class='row container-fluid' id='background'>
      <div class="col-md-4">
  		</div>
      <div class="col-md-4">
        <button class="w3-btn w3-black w3-padding-large" @click='goToAdminCourses'>
          <i class="fa fa-book w3-large"></i> Courses
        </button>
        <button class="w3-btn w3-black w3-padding-large" @click='goToAddUser'>
          <i class="fa fa-plus-circle w3-large"></i> Add User
        </button>
        <button class="w3-btn w3-black w3-padding-large" @click='goToNewSemester'>
          <i class="fa fa-plus-circle w3-large"></i> New Semester
        </button>
        <button class="w3-btn w3-black w3-padding-large" @click='logOut'>
          <i class="fa fa-sign-out w3-large"></i> Log Out
        </button>
  		</div>
      <div class="col-md-4">
  		</div>
    </div>
</template>

<script>
  export default {
    methods: {
        goToAdminCourses: function() {
          this.$parent.$router.push('/admin/courses')
        },
        goToAddUser: function() {
          this.$parent.$router.push('/admin/add-user')
        },
        goToNewSemester: function() {
          this.$parent.$router.push('/admin/new-semester/choose-semester')
        },
        logOut: function() {
          this.$parent.$router.replace('/')
        }
    }
  }
</script>

<style scoped>
  #background {
    display: flex;
    justify-content: center;
    align-items: center;
    height:100%;
  }
  button {
    display: block;
    width: 80%;
    margin: 10px auto;
  }
</style>
