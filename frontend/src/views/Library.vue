<template>
  <v-layout row>
    <v-flex xs12 sm6 offset-sm3 mt-1>
       <v-card>
        <v-progress-linear v-if="loading" v-bind:indeterminate="true"></v-progress-linear>
        <v-list three-line v-if="!notFound">
          <template v-for="item in items">
            <v-subheader v-if="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" v-bind:inset="item.inset"></v-divider>
            <v-list-tile avatar v-else v-bind:key="item.clean_id" @click="">
              <v-list-tile-avatar>
                <!--img v-bind:src="item.avatar"/-->
                <v-icon color="brown lighten-1">clipboard_text</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content v-on:click="openInNewTab(item.link)">
                <v-list-tile-title v-html="item.title"></v-list-tile-title>
                <v-list-tile-sub-title v-html="item.abstract"></v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn icon ripple v-on:click="removeFromLibrary(item.clean_id)" title="Remove from library">
                  <v-icon color="cyan accent-3">delete</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>
          </template>
        </v-list>
        <v-flex v-if="notFound" text-xs-center text-sm-center text-md-center text-lg-center text-xl-center>
          <h3>No items in your library.</h3>
          <v-btn v-on:click="goToSearch()">Search something and add items from its results!</v-btn>
        </v-flex>
        <v-progress-linear v-if="loading" v-bind:indeterminate="true"></v-progress-linear>
      </v-card>
     <v-pagination v-bind:length="totalPages" v-model="page" v-if="!notFound" circle></v-pagination>
    </v-flex>
  </v-layout>
</template>


<script>
  import * as axios from 'axios'
  export default {
    data () {
      return {
        page: 1,
        loading: false,
        empty: true
      }
    },
    computed: {
      items () {
        var store = this.$store
        var lastResult = store.getters.lastLibResult
        if ((lastResult.answer.page !== this.page) || this.empty) {
          this.empty = false
          this.changePage()
        }
        var itms = [{ header: 'Library of user: ' + lastResult.query }]
        var ans = lastResult.answer.items
        var i
        for (i = 0; i < ans.length; i++) {
          itms.push(ans[i])
          itms.push({ divider: true, inset: true })
        }
        return itms
      },
      totalPages () {
        var lastResult = this.$store.getters.lastLibResult
        var totalPages = lastResult.answer.pages
        return totalPages
      },
      currentPage () {
        var lastResult = this.$store.getters.lastLibResult
        var currentPage = lastResult.answer.page
        return currentPage
      },
      notFound () {
        if (this.empty) {
          this.changePage()
          this.empty = false
        }
        return this.$store.getters.lastLibResult.answer.items.length === 0
      }
    },
    methods: {
      openInNewTab: function (url) {
        var win = window.open(url, '_blank')
        win.focus()
      },
      goToSearch: function () {
        this.$router.push('search')
      },
      changePage: function () {
        var store = this.$store
        var username = store.getters.username
        this.loading = true
        axios.get('/api/library/list?username=' + username + '&page=' + this.page)
        .then(res => {
          console.log(res)
          store.commit('lastLibResult', res.data)
          this.loading = false
        })
        .catch(err => {
          this.loading = false
          alert(err)
          console.log(err)
        })
      },
      removeFromLibrary: function (cleanId) {
        var store = this.$store
        var username = store.getters.username
        this.loading = true
        axios.post('/api/library/remove/', {'username': username, 'clean_id': cleanId})
        .then(res => {
          console.log(res)
          this.loading = false
        })
        .catch(err => {
          this.loading = false
          alert(err)
          console.log(err)
        })
        this.changePage()
      }
    }
  }
</script>
