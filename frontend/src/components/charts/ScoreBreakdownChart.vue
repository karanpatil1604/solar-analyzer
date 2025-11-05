<template>
  <div class="chart-container">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { Radar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  RadialLinearScale,
  LineElement,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, PointElement, RadialLinearScale, LineElement)

interface Props {
  scores: {
    solar: number
    area: number
    grid: number
    slope: number
    infrastructure: number
  }
  siteName: string
}

const props = defineProps<Props>()

const chartData = {
  labels: ['Solar Irradiance', 'Area', 'Grid Distance', 'Slope', 'Infrastructure'],
  datasets: [
    {
      label: props.siteName,
      data: [
        props.scores.solar,
        props.scores.area,
        props.scores.grid,
        props.scores.slope,
        props.scores.infrastructure,
      ],
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgb(54, 162, 235)',
      pointBackgroundColor: 'rgb(54, 162, 235)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(54, 162, 235)',
    },
  ],
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      angleLines: {
        display: true,
      },
      suggestedMin: 0,
      suggestedMax: 100,
    },
  },
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
