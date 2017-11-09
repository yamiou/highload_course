<template id="d3__chart">
  <svg :view-box.camel="viewBox" preserveAspectRatio="xMidYMid meet">
    <g class="d3__stage" :style="stageStyle">
      <d3__axis
                v-for="(axis, index) in _.uniq(axes)"
                :key="index"
                :axis="axis"
                :layout="layout"
                :scale="scale"
                ></d3__axis>
      <g ref="d3__stage"></g>
    </g>
  </svg>
</template>

<template id="d3__axis">
  <g :class="[classList]" ref="axis" :style="style"></g>
</template>

<script>
var response = {
  "data": {
    "flipbooks": {
      "rawData": [
        ["2017-03-01T01:00:00", 1, 3],
        ["2017-03-02T01:00:00", 2, 6],
        ["2017-03-03T01:00:00", 2, 6],
        ["2017-03-04T01:00:00", 2, 6],
        ["2017-03-05T01:00:00", 2, 6],
        ["2017-03-06T01:00:00", 4, 6],
        ["2017-03-07T01:00:00", 9, 7],
        ["2017-03-08T01:00:00", 18, 14],
        ["2017-03-09T01:00:00", 23, 16],
        ["2017-03-10T01:00:00", 24, 16],
        ["2017-03-11T01:00:00", 24, 16],
        ["2017-03-12T01:00:00", 24, 16],
        ["2017-03-13T01:00:00", 25, 18],
        ["2017-03-14T01:00:00", 26, 19],
        ["2017-03-15T01:00:00", 30, 21],
        ["2017-03-16T01:00:00", 32, 23],
        ["2017-03-17T01:00:00", 32, 23],
        ["2017-03-18T01:00:00", 32, 23],
        ["2017-03-19T01:00:00", 32, 23],
        ["2017-03-20T01:00:00", 32, 23],
        ["2017-03-21T01:00:00", 32, 25],
        ["2017-03-22T01:00:00", 32, 26],
        ["2017-03-23T01:00:00", 32, 28],
        ["2017-03-24T01:00:00", 32, 29],
        ["2017-03-25T01:00:00", 32, 29],
        ["2017-03-26T01:00:00", 32, 29],
        ["2017-03-27T01:00:00", 32, 29],
        ["2017-03-28T01:00:00", 35, 29],
        ["2017-03-29T01:00:00", 35, 29],
        ["2017-03-30T01:00:00", 35, null],
        ["2017-03-31T01:00:00", 35, null]
      ]
    }
  }
};
var chartData = response.data.flipbooks.rawData;

// Parse the data and split it into series
var columns = ['Timestamp', 'Previous', 'Current'],
  offset = 1;
var c = columns.slice(offset).map(function(id, index) {
  return {
    id: id,
    values: chartData.map(function(d) {
      return {
        timestamp: d3.utcParse("%Y-%m-%dT%H:%M:%S")(d[0]).setHours(0, 0, 0, 0),
        value: d[index + offset]
      }
    })
  }
});

// Component: SVG parent and stage
Vue.component('d3__chart', {
  template: '#d3__chart',
  props: {
    axes: {
      type: Array,
      default: function() {
        return ['left', 'bottom'];
      },
      validator: function(v) {
        return !_.difference(v, ['left', 'right', 'top', 'bottom']).length
      }
    },
    layout: Object,
    chartData: Array
  },
  computed: {

    // SVG viewbox
    viewBox: function() {
      var outerWidth = this.layout.width + this.layout.marginLeft + this.layout.marginRight,
        outerHeight = this.layout.height + this.layout.marginTop + this.layout.marginBottom;
      return '0 0 ' + outerWidth + ' ' + outerHeight;
    },

    // Stage
    stageStyle: function() {
      return {
        'transform': 'translate(' + this.layout.marginLeft + 'px,' + this.layout.marginTop + 'px)'
      }
    }
  },
  mounted: function() {
    this.draw();
  },
  data: function() {
    return {
      scale: {
        x: this.getScaleX(),
        y: this.getScaleY(),
        color: d3.scaleOrdinal()
          .range(['#159078', '#999999'])
          .domain(['Current', 'Previous'])
      },
    }
  },
  methods: {

    // Get x-axis scale
    getScaleX: function() {
      return d3.scaleTime()
        .range([0, this.layout.width])
        .domain(d3.extent(chartData, function(d) {
          return d3.utcParse("%Y-%m-%dT%H:%M:%S")(d[0]).setHours(0, 0, 0, 0)
        }));
    },

    // Get y-axis scale
    getScaleY: function() {
      return d3.scaleLinear()
        .range([this.layout.height, 0])
        .domain([
          0,
          d3.max(this.chartData, function(d) {
            return d3.max(d.values, function(e) {
              return e.value;
            })
          })
        ]);
    },

    // Draw chart
    draw: function() {

      // Define transition
      var t = d3.transition().duration(500);

      // Define scale
      var scale = this.scale;

      // Define stage
      var $stage = d3.select(this.$refs.d3__stage);

      // Draw lines
      // Plotter
      var line = d3.line().x(function(d) {
          return scale.x(d.timestamp);
        })
        .y(function(d) {
          return scale.y(d.value);
        });

      // Update
      var $line = $stage
        .selectAll('.line')
        .data(this.chartData);

      // Exit
      $line.exit().remove();

      // Enter
      var $line = $line.enter()
        .append('path')
        .attr('d', function(d) {
          return line(d.values.filter(function(e) {
            return typeof e.value !== typeof null;
          }));
        })
        .merge($line)
        .attr('class', 'line')
        .transition(t)
        .attr('d', function(d) {
          return line(d.values.filter(function(e) {
            return typeof e.value !== typeof null;
          }));
        })
        .style('fill', 'none')
        .style('stroke', function(d) {
          return scale.color(d.id);
        })
        .style('stroke-width', 2);

      // Draw area
      // Plotter
      var area = d3.area()
        .x(function(d) {
          return scale.x(d.timestamp);
        })
        .y0(scale.y(0))
        .y1(function(d) {
          return scale.y(d.value);
        });

      // Update
      var $area = $stage
        .selectAll('.area')
        .data(this.chartData);

      // Exit
      $area.exit().remove();

      // Enter
      var $area = $area.enter()
        .append('path')
        .attr('d', function(d) {
          return area(d.values.filter(function(e) {
            return typeof e.value !== typeof null;
          }));
        })
        .style('fill', function(d) {
          return scale.color(d.id);
        })
        .style('fill-opacity', 0.25)
        .style('stroke', 'none')
        .merge($area)
        .attr('class', 'area')
        .transition(t)
        .attr('d', function(d) {
          return area(d.values.filter(function(e) {
            return typeof e.value !== typeof null;
          }));
        });

      // Draw point series
      // Update
      var $points = $stage
        .selectAll('.series')
        .data(this.chartData);

      // Exit
      $points.exit().remove();

      // Enter
      var $points = $points.enter()
        .append('g')
        .attr('class', 'series')
        .merge($points)
        .style('stroke', function(d) {
          return scale.color(d.id);
        });

      // Draw points
      // Update
      var $point = $points
        .selectAll('.point')
        .data(function(d) {
          return d.values.filter(function(e) {
            return typeof e.value !== typeof null;
          })
        });

      // Exit
      $point.exit().remove();

      // Enter
      var $point = $point
        .enter()
        .append('circle')
        .attr('class', 'point')
        .attr('cx', function(d) {
          return scale.x(d.timestamp);
        })
        .attr('cy', function(d) {
          return scale.y(d.value);
        })
        .attr('r', 4)
        .style('fill', '#fff')
        .style('stroke-width', 2)
        .merge($point)
        .transition(t)
        .attr('cx', function(d) {
          return scale.x(d.timestamp);
        })
        .attr('cy', function(d) {
          return scale.y(d.value);
        });

    }
  },
  watch: {
    // Watch for layout changes
    layout: {
      deep: true,
      handler: function(val, oldVal) {
        this.scale.x = this.getScaleX();
        this.scale.y = this.getScaleY();
        this.draw();
      }
    },
    chartData: {
      deep: true,
      handler: function(val, oldVal) {
        this.scale.x = this.getScaleX();
        this.scale.y = this.getScaleY();
        this.draw();
      }
    }
  }
});

// Component: Chart axes
Vue.component('d3__axis', {
  template: '#d3__axis',
  props: {
    axis: {
      type: String,
      validator: function(v) {
        return ['left', 'right', 'top', 'bottom'].indexOf(v) > -1
      }
    },
    layout: Object,
    scale: Object
  },
  //props: ['axis', 'layout', 'scale'],
  data: function() {
    return {
      // Return class list
      classList: ['axis'].concat(this.getAxisClasses())
    }
  },
  mounted: function() {
    this.drawAxis();
  },
  computed: {
    style: function() {
      return {
        transform: this.getAxisTransform()
      }
    }
  },
  methods: {

    // Return a class list containg the appropriate labels for axes
    getAxisClasses: function() {
      var axis = {
        top: 'x',
        bottom: 'x',
        left: 'y',
        right: 'y'
      };
      return [this.axis, axis[this.axis]];
    },

    // Draw axis
    drawAxis: function() {

      var t = d3.transition(500);
      var $axis = d3.select(this.$refs.axis);
      var scale = this.scale;
      var axisGenerator = {
        top: d3.axisTop(scale.x).tickFormat(d3.timeFormat("%b %d")),
        right: d3.axisRight(scale.y),
        bottom: d3.axisBottom(scale.x).tickFormat(d3.timeFormat("%b %d")),
        left: d3.axisLeft(scale.y)
      }

      // Transition the axis, and then call/construct it
      $axis.transition(t).call(axisGenerator[this.axis]);
    },

    // Return necessary axis transformation for proper positioning
    getAxisTransform: function() {

      var axisOffset = {
        top: {
          x: 0,
          y: 0
        },
        right: {
          x: this.layout.width,
          y: 0
        },
        bottom: {
          x: 0,
          y: this.layout.height
        },
        left: {
          x: 0,
          y: 0
        }
      };

      return 'translate(' + axisOffset[this.axis].x + 'px, ' + axisOffset[this.axis].y + 'px)';
    }
  },
  watch: {
    // Changes to scale means we have to redraw the line!
    scale: {
      deep: true,
      handler: function(val, oldVal) {
        this.drawAxis();
      }
    }
  }
});

// Initialize chart
var d3Vis = new Vue({
  el: '#chart',
  data: {
    layout: {
      width: 800,
      height: 250,
      marginTop: 45,
      marginRight: 35,
      marginBottom: 50,
      marginLeft: 50,
    },
    chartData: c,
    axes: ['left', 'bottom']
  }
});


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
  }
}

</script>

<style>
body {
  line-height: 1.75;
}

header {
  margin-bottom: 1.5rem;
}

h1 {
  margin-bottom: .5rem;
  text-align: center;
  & + span.byline {
    display: block;
    text-align: center;
  }
}

section {
  margin-bottom: 1.5rem;
  &.content {
    padding: 0 1.5rem;
  }
}

svg {
  background-color: #eee;
  width: 100%;
}

code {
  background-color: #f5f5f5;
  color: #e96900;
  padding: 3px 5px;
  margin: 0 2px;
  border-radius: 4px;
  white-space: nowrap;
}
</style>
