<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-sheet color="white" elevation="10">
          <v-slider
            v-model="radar"
            min="0"
            max="100"
            label="Radar"
            color="primary"
          ></v-slider>
        </v-sheet>
      </v-col>
      <v-col cols="12" md="6">
        <v-sheet color="white" elevation="10">
          <highcharts :options="areaGraphOptions"></highcharts>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-sheet color="white" elevation="10">
          <highcharts :options="gaugeGraphOptions"></highcharts>
        </v-sheet>
      </v-col>
      <v-col cols="12" md="6">
        <v-sheet color="white" elevation="10">
          <v-card>
            <v-card-title>Water Reserves</v-card-title>
            <v-card-text>
              <v-progress-linear
                :value="percentage"
                :color="percentage > 100 ? 'error' : 'primary'"
                height="25"
              ></v-progress-linear>
            </v-card-text>
          </v-card>
        </v-sheet>
      </v-col>
    </v-row>
    <v-dialog v-model="overflowDetected" max-width="300">
      <v-card>
        <v-card-title class="headline">Overflow Detected</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="overflowDetected = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, watch } from "@vue/composition-api";
import Highcharts from "highcharts";
import HighchartsVue from "highcharts-vue";

export default {
  components: {
    highcharts: HighchartsVue,
  },
  setup() {
    const radar = ref(0);
    const reserve = ref(0);
    const percentage = ref(0);
    const overflowDetected = ref(false);

    const areaGraphOptions = ref({
      chart: { zoomType: "x" },
      title: { text: "Water Reserves (10 min)", align: "left" },
      xAxis: { type: "datetime" },
      yAxis: { title: { text: "Water level" } },
      series: [
        {
          name: "Water",
          data: [],
        },
      ],
      tooltip: { shared: true },
    });

    const gaugeGraphOptions = ref({
      chart: { type: "solidgauge" },
      title: { text: "Water Reserves", align: "left" },
      yAxis: {
        min: 0,
        max: 1000,
        tickPixelInterval: 72,
        tickPosition: "inside",
        tickColor: Highcharts.defaultOptions.chart.backgroundColor || "#FFFFFF",
        tickLength: 20,
        tickWidth: 2,
        minorTickInterval: null,
        labels: {
          distance: 20,
          style: {
            fontSize: "14px",
            fontFamily: "Roboto",
          },
        },
      },
      tooltip: { shared: true },
      pane: {
        startAngle: -90,
        endAngle: 89.9,
        background: null,
        center: ["50%", "75%"],
        size: "110%",
      },
      series: [
        {
          type: "gauge",
          name: "Water Capacity",
          data: [0],
          tooltip: { valueSuffix: " Gal" },
          dataLabels: {
            format: "{y} Gal",
            borderWidth: 0,
            color:
              (Highcharts.defaultOptions.title &&
                Highcharts.defaultOptions.title.style &&
                Highcharts.defaultOptions.title.style.color) ||
              "#333333",
            style: { fontSize: "16px" },
          },
          dial: {
            radius: "80%",
            backgroundColor: "gray",
            baseWidth: 12,
            baseLength: "0%",
            rearLength: "0%",
          },
          pivot: { backgroundColor: "gray", radius: 6 },
        },
      ],
    });

    return {
      radar,
      reserve,
      percentage,
      overflowDetected,
      areaGraphOptions,
      gaugeGraphOptions,
    };
  },
};
</script>

