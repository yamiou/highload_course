<template>
  <v-layout column>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form @submit.prevent="submitQuery()">
        <v-layout column>
          <v-flex>
            <v-text-field
              name="query"
              id="query"
              v-model="query"
              type="text"
              placeholder="Input your query here"
              required></v-text-field>
          </v-flex>
          <v-flex class="text-xs-center" mt-5>
            <v-btn primary type="submit">Find articles!</v-btn>
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
      query: ''
    }
  },
  methods: {
    submitQuery: function () {
      var store = this.$store
      axios.get('/api/search?query=' + this.query)
      .then(res => {
        console.log(res)
        store.commit('lastResult', res.data)
      })
      .catch(err => {
        alert(err)
        console.log(err)
      })
      this.$router.push('results')
    }
  }
}
</script>
