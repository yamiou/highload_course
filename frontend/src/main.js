// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
// import VueD3 from 'vue-d3'
import Vuetify from 'vuetify'
import * as d3 from 'd3'

import App from './App'
import router from './router'
import { store } from './store'

Vue.prototype.$d3 = d3
Vue.use(Vuetify)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
