<template>
  <v-layout column>
    <v-flex xs12 sm6 offset-sm3 mt-3>
      <form>
        <v-layout column>
          <v-flex>
            <v-text-field
              name="query"
              id="query"
              type="text"
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
