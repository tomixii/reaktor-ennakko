<template>
  <div id="app">
    <h1>CO2 emissions</h1>
    <router-view/>

  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<script>
import Top20 from './components/Top20.vue'

export default {
  name: 'App',
  components: {
		Top20
	}
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
