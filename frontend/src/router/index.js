import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  // { path: '/', component: 'Visualization' },
  { path: '/', component: 'SearchQuery' },
  { path: '/visualization', component: 'Visualization' },
  { path: '/signin', component: 'Signin' },
  { path: '/signup', component: 'Signup' },
  { path: '/library', component: 'Library' },
  { path: '/results', component: 'SearchResult' },
  { path: '/search', component: 'SearchQuery' }
]

const routes = routerOptions.map(route => {
  return {
    path: route.path,
    component: () => import(`../views/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes
})
