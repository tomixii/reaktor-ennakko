<template>
  <div>
    <p>Top 20</p>

    <p>Finland emissions 2005: {{ emissions }} kt</p>
    <button @click="getEmissions">get emissions</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      emissions: 0
    }
  },
  methods: {
    getEmissions () {
      const path = `http://localhost:5000/api/co2/finland/2007`
      axios.get(path)
        .then(response => {
          this.emissions = response.data.value
          console.log('moi')
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getEmissions()
  }
}
</script>
