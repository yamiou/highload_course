<template>
  <v-container align-content-center='true' justify-center='true' width='100%' height='100%'>
    <svg
    xmlns="http://www.w3.org/2000/svg"
    width="500"
    height="500"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:svg="http://www.w3.org/2000/svg"
    xml:space="preserve"
    viewBox="0 0 500 500">
  </svg>
  </v-container>
</template>

<script>
import resize from 'vue-resize-directive'
const props = {}

const directives = {
  resize
}

export default {
  name: 'Home',
  props,
  directives,
  data () {
    return {}
  },
  mounted () {
    const d3 = this.$d3
    // const size = this.getSize()
    const svg = d3.select('svg')
    //      .attr('width', size.width)
    //      .attr('height', size.height)
    // var bbox = svg.getBBox()

    // svg.setAttribute('width', bbox.x + bbox.width + 'px')
    // svg.setAttribute('height', bbox.y + bbox.height + 'px')

    // var width = svg.outerWidth()  // attr('width')
    // var height = svg.outerHeight()  // attr('height')

    var color = d3.scaleOrdinal(d3.schemeCategory20)

    var simulation = d3.forceSimulation()
          .force('link', d3.forceLink().id(function (d) { return d.id }))
          .force('charge', d3.forceManyBody())
          // .force('center', d3.forceCenter(width / 2, height / 2))

    d3.json('/static/miserables.json', function (error, graph) {
      if (error) throw error

      var link = svg.append('g')
          .attr('class', 'links')
          .selectAll('line')
          .data(graph.links)
          .enter().append('line')
          .attr('stroke-width', function (d) { return Math.sqrt(d.value) })

      var node = svg.append('g')
          .attr('class', 'nodes')
          .selectAll('circle')
          .data(graph.nodes)
          .enter().append('circle')
          .attr('r', 5)
          .attr('fill', function (d) { return color(d.group) })
          .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended))

      node.append('title')
            .text(function (d) { return d.id })

      simulation
            .nodes(graph.nodes)
            .on('tick', ticked)

      simulation.force('link')
            .links(graph.links)

      function ticked () {
        link
              .attr('x1', function (d) { return d.source.x })
              .attr('y1', function (d) { return d.source.y })
              .attr('x2', function (d) { return d.target.x })
              .attr('y2', function (d) { return d.target.y })

        node
              .attr('cx', function (d) { return d.x })
              .attr('cy', function (d) { return d.y })
      }
    })

    function dragstarted (d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    }

    function dragged (d) {
      d.fx = d3.event.x
      d.fy = d3.event.y
    }

    function dragended (d) {
      if (!d3.event.active) simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    }
  }
}
</script>

<style>
.treeclass .nodetree  circle {
  fill: #999;
  r: 2.5;
}
.treeclass .node--internal circle {
  cursor: pointer;
  fill:  #555;
  r: 3;
}
.treeclass .nodetree text {
  font: 10px sans-serif;
  cursor: pointer;
}
.treeclass .nodetree.selected text {
  font-weight: bold;
}
.treeclass .node--internal text {
  text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
}
.treeclass .linktree {
  fill: none;
  stroke: #555;
  stroke-opacity: 0.4;
  stroke-width: 1.5px;
}
</style>
