<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  type ChartData,
  type ChartOptions,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

interface Props {
  distribution: {
    excellent: number
    good: number
    fair: number
    poor: number
    veryPoor: number
  }
}

const props = defineProps<Props>()

const labels = [
  'Excellent (80-100)',
  'Good (60-79)',
  'Fair (40-59)',
  'Poor (20-39)',
  'Very Poor (0-19)',
]

const datasetValues = computed(() => [
  props.distribution.excellent,
  props.distribution.good,
  props.distribution.fair,
  props.distribution.poor,
  props.distribution.veryPoor,
])

// ✅ Reactive Chart Data
const chartData = computed<ChartData<'bar'>>(() => ({
  labels,
  datasets: [
    {
      label: 'Number of Sites',
      data: datasetValues.value,
      backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545'],
      borderWidth: 1,
    },
  ],
}))

// ✅ Smart Tooltip + Animations + Axis Formatting
const chartOptions = computed<ChartOptions<'bar'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Site Suitability Distribution',
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const total = datasetValues.value.reduce((a, b) => a + b, 0)
          const count = context.raw as number
          const pct = total ? ((count / total) * 100).toFixed(1) : '0'
          return `${count} sites (${pct}%)`
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0, // Always integer
      },
      title: {
        display: true,
        text: 'Number of Sites',
      },
    },
    x: {
      ticks: {
        maxRotation: 0,
        minRotation: 0,
      },
      title: {
        display: true,
        text: 'Score Range',
      },
    },
  },
  animation: {
    duration: 700,
    easing: 'easeOutQuart',
  },
}))
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 330px;
  width: 100%;
}
@media (max-width: 600px) {
  .chart-container {
    height: 260px;
  }
}
</style>
