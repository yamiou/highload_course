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
    authorize: function () {
      this.$store.commit('authorized')
      this.$router.push('search')
    },
    submitQuery: function () {
      var store = this.$store
      axios.get('/api/search/')
      .then(res => {
        console.log(res)
        store.commit('lastResult', res.data)
      })
      .catch(err => {
        console.log(err)
      })
      this.$router.push('results')
    }
  }
}
</script>
