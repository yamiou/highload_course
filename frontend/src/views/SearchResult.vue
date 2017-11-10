<template>
  <v-layout row>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <v-card>
        <v-list three-line>
          <template v-for="item in items">
            <v-subheader v-if="item.header" v-text="item.header"></v-subheader>
            <v-divider v-else-if="item.divider" v-bind:inset="item.inset"></v-divider>
            <v-list-tile avatar v-else v-bind:key="item.clean_id" @click="">
              <v-list-tile-avatar>
                <!--img v-bind:src="item.avatar"/-->
                <v-icon>question_answer</v-icon>
              </v-list-tile-avatar>
              <v-list-tile-content v-on:click="openInNewTab(item.link)">
                <v-list-tile-title v-html="item.title"></v-list-tile-title>
                <v-list-tile-sub-title v-html="item.abstract"></v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </template>
        </v-list>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
  export default {
    data () {
      return {
      }
    },
    computed: {
      items () {
        var lastResult = this.$store.getters.lastResult
        var itms = [{ header: lastResult.query }]
        var ans = lastResult.answer
        var i
        for (i = 0; i < ans.length; i++) {
          itms.push(ans[i])
          itms.push({ divider: true, inset: true })
        }
        return itms
      }
    },
    methods: {
      openInNewTab: function (url) {
        var win = window.open(url, '_blank')
        win.focus()
      }
    }
  }
</script>
