<template>
  <v-layout column>
    <v-flex xs12 class="text-xs-center" mt-5>
      <h3>Sign Up</h3>
    </v-flex>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form @submit.prevent="if(password === confirmPassword) { register() } else {alert('Passwords not match with confirmation!')}">
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
          <v-flex>
            <v-text-field
              name="confirmPassword"
              label="Confirm Password"
              id="confirmPassword"
              type="password"
              v-model="confirmPassword"
              ></v-text-field>
          </v-flex>
          <v-flex class="text-xs-center" mt-5>
            <v-btn primary type="submit">Sign Up</v-btn>
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
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    register: function () {
      var router = this.$router
      axios.post('/api/register', {'email': this.email, 'username': this.email, 'password': this.password})
      .then(res => {
        console.log(res.data.register_result)
        alert(res.data.register_result)
        router.push('signin')
      })
      .catch(err => {
        console.log(err)
        alert(err)
      })
    }
  }
}
</script>
