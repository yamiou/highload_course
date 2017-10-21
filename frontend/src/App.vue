<template>
  <v-app>
    <v-navigation-drawer temporary v-model="sidebar">
      <v-list>
        <v-list-tile
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>{{ item.title }}</v-list-tile-content>
    </v-list-tile>
  </v-list>
    </v-navigation-drawer>
    <v-toolbar fixed>
      <span class="hidden-sm-and-up">
        <v-toolbar-side-icon @click.stop="sidebar = !sidebar">
        </v-toolbar-side-icon>
      </span>
      <v-toolbar-title>
        <router-link to="/" tag="span" style="cursor: pointer">
          {{ appTitle }}
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-xs-only">
        <v-btn
          flat
          v-for="item in menuItems"
          v-if="item.visible"
          :key="item.title"
          :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
      </v-btn>
    </v-toolbar-items>
    </v-toolbar>

    <main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </main>

  </v-app>
</template>
<script>
  export default {
    data () {
      return {
        sidebar: false
      }
    },
    computed: {
      appTitle () {
        return this.$store.getters.appTitle
      },
      menuItems () {
        return [
            { title: 'Library', path: '/library', icon: 'home', visible: this.$store.getters.authorized },
            { title: 'Search', path: '/search', icon: 'search', visible: true },
            { title: 'Sign Up', path: '/signup', icon: 'face', visible: !this.$store.getters.authorized },
            { title: 'Sign In', path: '/signin', icon: 'lock_open', visible: !this.$store.getters.authorized }
        ]
      }
    }
  }
</script>
<style lang="stylus">
  @import './stylus/main'
</style>
