
<template>
  <div id="app">
    <b-navbar fixed="top" type="dark" variant="dark">
      <b-navbar-brand href="#">CO<sub>2</sub> Emissions Hub</b-navbar-brand>
      <b-navbar-toggle target="nav_collapse" />

        <b-navbar-nav>
          <b-nav-item
            v-for="tab in tabs"
            v-bind:key="tab.name"
            v-bind:class="['tab-button', { active: currentTab.name === tab.name }]"
            v-on:click="currentTab = tab"
          >{{ tab.name }}</b-nav-item>
        </b-navbar-nav>
    </b-navbar>
    <br>
    <component
      v-bind:is="currentTab.component"
      class="tab"
    ></component>
  </div>
</template>

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<script>
import Top20 from './components/Top20.vue'
import BigCountries from './components/BigCountries.vue'
import Vue from 'vue/dist/vue.esm.js'

var tabs = [
  {
    name: 'Top list',
    component: Top20
  },
  {
    name: 'Great powers',
    component: BigCountries
  }
]

export default {
  name: 'App',
  data() {
    return {
      tabs: tabs,
      currentTab: tabs[0]
    }
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
