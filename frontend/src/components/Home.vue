<template lang="html">

    <div class="containerfluid" >
    <div class="container card w3-round-xxlarge" >
      <div class="title">
        <h3>Notifications</h3>
      </div>

        <div v-for="(value, index) in items" v-if="items[index].id">
          <div    class="container0" v-bind:id="`${index}`">
          <div class="alert alert-info">
            <div class="alert-icon">
            <i class="material-icons">info_outline</i>
            </div>
           <p >
            {{ value.notf }}
           </p>
           <button type="button"  v-on:click="Delete(`${index}`)" class="close" data-dismiss="alert" aria-label="Close"><i class="fa fa-trash"></i></button>
           <button type="button" v-on:click="Hide(`${index}`)" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true"><i class="fa fa-close"></i></span>
           </button>
          </div>
        </div>


    </div>
    <div v-else>
      <p >
       No available notifications.
      </p>
    </div>

  </div>
  </div>

</template>

<script>
import axios from 'axios'
export default {
  name:"Home",
  data(){
    return{
        items: []

    }
  },methods:{
    update:function(){
      console.log("inupdate");
      const path = 'http://127.0.0.1:5000/home';
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
      console.log("infilldata");
      console.log(res);
      if(res.data) {
        console.log("infilldata in if conditon");
      this.items=res.data

      }
    },
   Hide:function(e) {
     console.log("in func",this.items[e].id);
    const button=e;

  var x = document.getElementById(button);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
},
  Delete:function(e) {
    const button=e;

  var x = document.getElementById(button);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
    const path1 = 'http://127.0.0.1:5000/delete_notifications';
    axios.delete(path1,{ data:{
      username: this.$parent.username,
      id:this.items[e].id
    }})
    .then(this.deleted)
      .catch((error) => {
      console.log(error);
      });
  },
  deleted(res) {
    if(res.data.check) {
      console.log(res.data.check)
      this.$notify({
        group: 'foo',
        title: 'Delete',
        text: 'Notification deleted',
        type:'succes'
       });
      }
    }
  },
   beforeMount()
{
    this.update()

}

}

</script>

<style lang="css" scoped>

.title h3{
    font-size: 5vw !important;
    font-family: Aleo;
    margin-top: 20px;
    margin-bottom: 25px;
    line-height: 1.4em !important;
    font-weight: 300;
    position: inherit;
    width: auto;
}
p{
  font-size: 2vw;
  font-family:Aleo;
  width: auto;
  display: inline-block;
}
.container0
{
  position: relative;
  width: 100%;



}
.container {
    padding: 16px;
    margin-top: 6px;
    width: 60%;
    background-color:#f2f2f2;
    position: relative;
    top: 50px;

  }

.container2 {
    padding: 16px;
    margin-top: 6px;
    width: 100%;
    position: relative;

}
.adjpos{
  position:sticky;
  left: 25%;
  top: 17%;
  width: auto%;
}

/* alerts */

.alert {
    border: 0;
    border-radius: 0;
    padding: 20px 15px !important;
    line-height: 20px;
    font-weight: 300;
    color: #fff;
}

.alert .alert-icon {
    display: block;
    float: left;
    margin-right: 1.071rem;
}

.close {
    float: right;
    font-size: 1.5rem;
    color: #000;
    text-shadow: 0 1px 0 #fff;
    opacity: .5;
}
.alert .close {
    color: #fff;
    text-shadow: none;
    opacity: .9;
}
.alert .close i {
    font-size: 20px;
}
.alert .close:hover{
    opacity: 1;
    color: #fff;
}

.alert.alert-info {
    background-color: #000;
    color: #fff;
    position: relative;
    width: 100%;


}
.btn {
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 1vw 1vw; /* Some padding */
  font-size: 1vw; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */

}

/* Darker background on mouse-over */
.btn:hover {
  background-color: RoyalBlack;
}
.btn-group{
  position: static;
  float: right;

}



</style>
