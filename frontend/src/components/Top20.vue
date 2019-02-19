<template>
    <div class="container">
      <p>Select year:</p>
      <select v-model="selected" @change="getEmissions()">
        <option disabled value="">Select year</option>
        <option v-for="year in years" >
          {{ year }}
        </option>
      </select>
      <bar-chart v-if="loaded" :chart-data="chartData" :chart-labels="chartLabels"/>
    </div>
</template>

<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.18/vue.min.js"></script>

<script>
import axios from 'axios'
import Vue from 'vue'
import VueChartJs from 'vue-chartjs'

function range(start, end) {
  return Array(end - start + 1).fill().map((_, idx) => start + idx)
}

Vue.component('bar-chart', {
  extends: VueChartJs.HorizontalBar,
  mixins: [VueChartJs.mixins.reactiveProp],
  props: {
        chartData: {
          type: Array | Object,
          required: false
        },
        chartLabels: {
          type: Array,
          required: true
        }
  },
  data: function () {
    return {
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: false
            }
          }],
          xAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              display: true
            }
          }]
        },
        legend: {
          display: false
        },
        tooltips: {
          enabled: true,
          mode: 'single',
          callbacks: {
            label: function (tooltipItems, data) {
              return tooltipItems.xLabel
            }
          }
        },
        responsive: true,
        maintainAspectRatio: false,
        backgroundColor: "#123456"
      }
    }
  },
  mounted () {
    // this.chartData is created in the mixin
    this.renderChart({
          labels: this.chartLabels,
          datasets: [
            {
              data: this.chartData,
            }
          ]
        },this.options)

  }
})

export default {
  data: () => ({
    loaded: false,
    chartLabels: [],
    chartData: [],
    selected: '2014',
    years: range(1960, 2014)
  }),
  async mounted () {
    this.getEmissions()
  },
  methods: {
    getEmissions () {
      this.chartData = []
      this.chartLabels = []
      this.loaded = false
      const path = 'http://localhost:5000/api/co2/'+this.selected+'/1/20'
      axios.get(path)
        .then(response => {
          var emissions = response.data
          if (emissions !== undefined) {
            for (var i = 0; i < emissions.length; i++) {
              this.chartLabels.push(emissions[i][0])
              this.chartData.push(emissions[i][1])
            }
            console.log(this.chartData)
            this.loaded = true
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}

</script>
