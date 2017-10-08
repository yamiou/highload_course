import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import HelloD3 from '@/components/HelloD3'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/d3',
      name: 'Hello D3',
      component: HelloD3
    }
  ]
})
