<template>
  <div class="site-map">
    <div v-if="loading" class="map-loading">Loading map...</div>
    <div v-else class="map-container">
      <l-map
        ref="map"
        :zoom="zoom"
        :center="center"
        @ready="onMapReady"
        @update:center="centerUpdated"
        @update:zoom="zoomUpdated"
      >
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
        />

        <l-marker
          v-for="site in sitesWithScores"
          :key="site.site"
          :lat-lng="[site.latitude, site.longitude]"
          @click="onMarkerClick(site)"
        >
          <l-icon
            :icon-url="getMarkerIcon(site.total_suitability_score)"
            :icon-size="[32, 32]"
            :icon-anchor="[16, 32]"
          />
          <l-tooltip>
            <div class="site-tooltip">
              <strong>{{ site.site_name }}</strong>
              <br>Score: {{ formatScore(site.total_suitability_score) }}
              <br>Region: {{ site.region }}
            </div>
          </l-tooltip>
        </l-marker>
      </l-map>
    </div>

    <!-- Site Details Modal -->
    <div v-if="selectedSite" class="modal-overlay" @click="selectedSite = null">
      <div class="modal-content" @click.stop>
        <button class="close-button" @click="selectedSite = null">×</button>
        <SiteDetails :site="selectedSite" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { LMap, LTileLayer, LMarker, LIcon, LTooltip } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';
import type { AnalysisResult } from '@/types';
import SiteDetails from './SiteDetails.vue';

interface Props {
  sites: AnalysisResult[];
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
});
const formatScore = (score: any) => (typeof score === 'number' ? score.toFixed(2) : 'N/A')

const emit = defineEmits<{
  siteSelected: [site: AnalysisResult]
}>();

const map = ref();
const zoom = ref(7);
const center = ref<[number, number]>([11.0, 77.0]); // Center on Tamil Nadu
const selectedSite = ref<AnalysisResult | null>(null);

const sitesWithScores = computed(() =>
  props.sites.filter(site => site.total_suitability_score != null)
);

const getMarkerIcon = (score: number) => {
  if (score >= 80) return '/marker-excellent.png';
  if (score >= 60) return '/marker-good.png';
  if (score >= 40) return '/marker-fair.png';
  if (score >= 20) return '/marker-poor.png';
  return '/marker-very-poor.png';
};

const onMapReady = () => {
  console.log('Map is ready');
};

const centerUpdated = (center: [number, number]) => {
  console.log('Center updated:', center);
};

const zoomUpdated = (zoom: number) => {
  console.log('Zoom updated:', zoom);
};

const onMarkerClick = (site: AnalysisResult) => {
  selectedSite.value = site;
  emit('siteSelected', site);
};

// Create marker icons (you can replace with actual images)
onMounted(() => {
  // In a real app, you'd have actual marker images
  // For now, we'll use colored circles generated programmatically
});
</script>

<style scoped>
.site-map {
  position: relative;
  height: 100%;
  width: 100%;
}

.map-container {
  height: 600px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.map-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: #f5f5f5;
  border-radius: 8px;
}

.site-tooltip {
  text-align: center;
  min-width: 150px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #333;
}
</style>
