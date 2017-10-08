<template>
  <div class='hellod3'>
    <h1>{{ msg }}</h1>
    <svg width="200" height="200">
    </svg>
  </div>
</template>

<script>
export default {
  name: 'hellod3',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add 'scoped' attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
</style>
