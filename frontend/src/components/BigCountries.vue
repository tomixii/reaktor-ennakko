<template>
    <div class="container">
      <h2>Great powers' CO<sub>2</sub> emissions</h2>
      <pie-chart v-if="loaded" :chart-data="chartData" />
      <br>
      <select v-model="selected" @change="getEmissions()">
        <option v-for="year in years" v-bind:key="year" >
          {{ year }}
        </option>
      </select>
    </div>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'
import VueChartJs from 'vue-chartjs'

function range (start, end) {
  return Array(end - start + 1).fill().map((_, idx) => start + idx)
}

Vue.component('pie-chart', {
  extends: VueChartJs.Pie,
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
        legend: {
          display: true
        },
        tooltips: {
          enabled: true,
          mode: 'single',
          callbacks: {
            label: function (tooltipItems, data) {
              return data.labels[tooltipItems.index] + ': ' + data.datasets[tooltipItems.datasetIndex].data[tooltipItems.index] + '%'
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
  name: 'great-powers-chart',
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
            label: 'Great powers\' CO2 emissions',
            backgroundColor: ['Green', 'Red', 'Blue', 'Yellow', 'Orange', 'Purple', 'Cyan', 'Brown'],
            data: [],
            hoverBackgroundColor: ['Green', 'Red', 'Blue', 'Yellow', 'Orange', 'Purple', 'Cyan', 'Brown']
          }
        ]
      }
      this.loaded = false
      axios.get('/api/greatpowers/' + this.selected)
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
