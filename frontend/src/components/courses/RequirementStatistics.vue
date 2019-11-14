<template>
  <div class='container row' id='background'>
    <div class='col-sm-1' style='padding: 0px'></div>
    <div class='col=sm-7' style='padding: 0px'>
      <div class = 'col-sm-12 row'>
        <span class='w3-xxlarge lobster' style='margin: 0 auto 2% auto;'> {{requirementName}} </span>
      </div>
      <div class = 'col-sm-12 row'>
        <table class='w3-table w3-striped w3-bordered w3 w3-center'>
          <tr >
            <th class='w3-center'> Total Number of {{requirementType}} </th>
            <th class='w3-center'> Delivered Before The Deadline </th>
            <th class='w3-center'> Delivered After The Deadline </th>
            <th class='w3-center'> Did Not Deliver </th>
            <th class='w3-center'> Received Feedback </th>
            <th class='w3-center'> Did Not Receive Feedback </th>
          </tr>
          <tr>
            <td class='w3-center'> {{nTotal}} </td>
            <td class='w3-center'> {{nDeliveredBeforeDeadline}} </td>
            <td class='w3-center'> {{nDeliveredAfterDeadline}} </td>
            <td class='w3-center'> {{nTotal - nDeliveredBeforeDeadline - nDeliveredAfterDeadline}} </td>
            <td class='w3-center'> {{nReceivedFeedback}} </td>
            <td class='w3-center'> {{nNoFeedback}} </td>
          </tr>
        </table>
      </div>
      <div class = 'col-sm-12 row'>
        <div id="deliveryChart" style="width: 450px; height: 500px;" class='w3-center'></div>
        <div id="feedbackChart" style="width: 450px; height: 500px;" class='w3-center'></div>
      </div>
      <div class='col-sm-12 row'>

      </div>

    </div>
    <div class='col-sm-1' style='padding: 0px'></div>
  </div>
</template>


<script>
  import axios from 'axios'
  const path = "http://127.0.0.1:5000/requirements-statistics";
  export default {
    data() {
      return {
        requirementName: 'OOP Requirement',
        requirementType: 'Students',
        nTotal: 12,
        nDeliveredBeforeDeadline: 5,
        nDeliveredAfterDeadline: 7,
        nReceivedFeedback: 2,
        nNoFeedback: 10
      }
    },
    methods: {
      loadCharts: function() {
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(this.drawCharts);
      },
      drawCharts: function() {
        this.drawDeliveredChart();
        this.drawFeedbackChart();
      },
      drawDeliveredChart: function() {

        var data = google.visualization.arrayToDataTable([
          ['Students / Teams', 'Delivery Date'],
          ['After The Deadline',   this.nDeliveredAfterDeadline],
          ['Before The Deadline',  this.nDelivedBeforeDeadline],
          ['Did not Deliver', this.nTotal - this.nDeliveredBeforeDeadline - this.nDeliveredAfterDeadline]
        ]);

        var options = {
          title: 'Delivery Time',
          is3D: true,
          backgroundColor: { fill:'transparent' },
          width:600,
          fontSize: 18
        };

        var chart = new google.visualization.PieChart(document.getElementById('deliveryChart'));

        chart.draw(data, options);
      },
      drawFeedbackChart: function() {

        var data = google.visualization.arrayToDataTable([
          ['', 'Received Feedback'],
          ['Received Feedback',     this.nReceivedFeedback],
          ['Did Not Receive Feedback',   this.nNoFeedback]
        ]);

        var options = {
          title: 'Feedback',
          is3D: true,
          backgroundColor: { fill:'transparent' },
          width:600,
          fontSize: 18
        };

        var chart = new google.visualization.PieChart(document.getElementById('feedbackChart'));

        chart.draw(data, options);
      },
      loadData: function() {
        axios.get(path, {
          params: {
          reqID: this.$parent.reqID
          }
        })
          .then(this.fillData)
          .catch(function(error) {
            console.log(error)
          });
      },
      fillData: function(response) {
        let data = response.data
        this.requirementName = data.requirement_name;
        this.nDeliveredBeforeDeadline = data.delivered_before_deadline;
        this.nDeliveredAfterDeadline = data.delivered_after_deadline;
        this.nNoFeedback = data.no_feedback;
        this.nReceivedFeedback = data.have_feedback;
        if(data.requirement_type == 0) {
          this.requirementType = "Teams";
        }
        else {
          this.requirementType = 'Students';
        }
        this.nTotal = data.n_total;
        this.loadCharts();
      }

    },
    beforeMount() {
      this.loadData();
    }
  }
</script>


<style scoped>
  .container {
    margin-left: 120px;
    width: calc(100% - 120px);
    max-width: calc(100% - 120px);
  }
  @media only screen and (max-width: 600px) {
    .container {
      margin-left: 0;
    }
  }
  #background {
    display: flex;
    justify-content: center;
    align-items: center;
    height:100%;
  }
</style>
