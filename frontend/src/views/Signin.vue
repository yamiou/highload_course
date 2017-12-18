<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Sign In</h3>
    </v-flex>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form @submit.prevent="authorize()">
        <v-layout column>
          <v-flex>
            <v-text-field
              name="email"
              label="Email"
              id="email"
              type="email"
              v-model="email"
              required></v-text-field>
          </v-flex>
          <v-flex>
            <v-text-field
              name="password"
              label="Password"
              id="password"
              type="password"
              v-model="password"
              required></v-text-field>
          </v-flex>
          <v-flex class="text-xs-center" mt-5>
            <v-btn primary type="submit">
              Sign In
            </v-btn>
          </v-flex>
        </v-layout>
      </form>
    </v-flex>
  </v-layout>
</template>


<script>
import * as axios from 'axios'
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    getUserName: function () {
      var store = this.$store
      axios.get('/api/auth/me')
      .then(res => {
        var data = res.data.me
        store.commit('username', data['username'])
      })
      .catch(err => {
        console.log(err)
        alert(err)
      })
    },
    authorize: function () {
      var store = this.$store
      var router = this.$router
      axios.post('/api/auth/', {'username': this.email, 'password': this.password})
      .then(res => {
        var data = res.data
        console.log(res)
        axios.defaults.headers.common['authorization2'] = 'Bearer ' + data.access_token
        store.commit('authorized')
        store.commit('access_token', data.access_token)
        store.commit('username', this.email)
        // this.getUserName()
        router.push('search')
      })
      .catch(err => {
        console.log(err)
        alert(err)
      })
    }
  }
}
</script>
