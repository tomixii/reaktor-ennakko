<template>
    <div class="container">
      <h2>Top countries by CO<sub>2</sub> emissions per capita (t)</h2>
      <bar-chart v-if="loaded" :chart-data="chartData" />
      <select v-model="selected" @change="getEmissions()">
        <option v-for="year in years" v-bind:key="year">
          {{ year }}
        </option>
      </select>
    </div>
</template>

<script src="https://cdnjs.cloudflare.com/ajax/libs/vue/1.0.18/vue.min.js"></script>

<script>
import axios from 'axios'
import Vue from 'vue'
import VueChartJs from 'vue-chartjs'

function range (start, end) {
  return Array(end - start + 1).fill().map((_, idx) => start + idx)
}

Vue.component('bar-chart', {
  extends: VueChartJs.HorizontalBar,
  mixins: [VueChartJs.mixins.reactiveProp],
  props: {
    chartData: {
      type: Object,
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
              return tooltipItems.xLabel + ' t'
            }
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.options)
  }
})

export default {
  name: 'top20-chart',
  data: () => ({
    loaded: false,
    chartData: {},
    selected: '2014',
    years: range(1960, 2014)
  }),
  async mounted () {
    this.getEmissions()
  },
  methods: {
    getEmissions () {
      this.chartData = {
        labels: [],
        datasets: [
          {
            label: 'CO2 emissions per capita (t)',
            backgroundColor: '#c45850',
            data: []
          }
        ]
      }
      this.loaded = false
      const path = 'http://localhost:5000/api/co2percapita/'+this.selected
      axios.get(path)
        .then(response => {
          var emissions = response.data
          if (emissions !== undefined) {
            for (var i = 0; i < emissions.length; i++) {
              this.chartData.labels.push(emissions[i][0])
              this.chartData.datasets[0].data.push(emissions[i][1])
            }
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
