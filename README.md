# Solar Site Analyzer

A full-stack web application for identifying and analyzing potential sites for solar panel installations using spatial data analysis.

## 🌐 Live Demo

- **Frontend**: [https://solar-analyzer.vercel.app/](https://solar-analyzer.vercel.app/)
- **Backend API**: [http://136.111.17.239:8000/api/](http://136.111.17.239:8000/api/)

## 🚀 Features Implemented

### Core Functionality

- **Interactive Map**: Display solar sites with color-coded markers based on suitability scores
- **Site Dashboard**: View statistics, top sites, and score distributions
- **Suitability Analysis**: Calculate scores based on solar irradiance, area, grid distance, slope, and infrastructure
- **Custom Analysis**: Adjust factor weights and recalculate scores in real-time
- **Site Comparison**: Compare multiple sites side-by-side
- **Data Export**: Export site data as CSV

### Technical Implementation

- **Responsive Design**: Works on both desktop and mobile devices
- **Real-time Calculations**: Instant score updates with custom weights
- **Spatial Visualization**: Geographic display of site data
- **RESTful API**: Clean API design with proper error handling

## 🛠 Tech Stack

### Backend

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: MySQL (Aiven cloud) / SQLite (local development)
- **Production Server**: Gunicorn
- **Deployment**: GCP VM with Docker

### Frontend

- **Framework**: Vue 3 + TypeScript
- **State Management**: Pinia
- **Routing**: Vue Router
- **Maps**: Leaflet
- **Charts**: Chart.js
- **HTTP Client**: Axios
- **Deployment**: Vercel

## 📦 Project Structure

```
solar-site-analyzer/
├── backend/                 # Django REST API
│   ├── solar_app/          # Main application
│   ├── config/             # Django settings
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Vue.js application
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page components
│   │   ├── stores/         # Pinia state management
│   │   └── services/       # API services
│   └── package.json
└── README.md
```

## 🔧 Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:

   ```bash
   cd backend
   ```

2. **Create virtual environment and install dependencies**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with:

   ```env
   DEBUG=False
   SECRET_KEY=your-secret-key
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=your-database-host
   DB_PORT=your-database-port
   ```

4. **Run migrations and start server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**:

   ```bash
   cd frontend
   ```

2. **Install dependencies**:

   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

## 🗄 Database

The application comes pre-loaded with sample solar site data including:

- Site locations (latitude/longitude)
- Solar irradiance data
- Area measurements
- Grid distances
- Terrain slopes
- Infrastructure proximity

## 📊 Suitability Scoring

Sites are scored (0-100) using weighted factors:

| Factor           | Weight | Description                     |
| ---------------- | ------ | ------------------------------- |
| Solar Irradiance | 35%    | Daily solar energy (kWh/m²/day) |
| Land Area        | 25%    | Available area for installation |
| Grid Distance    | 20%    | Distance to power grid (km)     |
| Terrain Slope    | 15%    | Ground slope in degrees         |
| Infrastructure   | 5%     | Distance to roads (km)          |

## 🚀 Deployment

### Backend Deployment (GCP VM)

- Deployed on Google Cloud Platform VM instance
- Uses Gunicorn as production WSGI server
- Docker containerization for consistent environments
- Environment variables managed via `.env` file

### Frontend Deployment (Vercel)

- Automatic deployments from Git repository
- Environment variables configured in Vercel dashboard
- Continuous deployment on push to main branch

### Database (Aiven)

- MySQL database hosted on Aiven cloud platform
- Secure connection with SSL

## 🔌 API Endpoints

- `GET /api/sites/` - List all sites with filters
- `GET /api/analysis-results/` - Get suitability analysis results
- `GET /api/analysis-results/top_sites/` - Get top recommended sites
- `GET /api/analysis-results/statistics/` - Get overall statistics
- `POST /api/analyze/calculate/` - Calculate custom suitability scores
- `GET /api/export/` - Export site data as CSV(not implemented)

## 🎯 Usage

1. **View Dashboard**: See overview of sites and statistics
2. **Explore Map**: Click on site markers to view details
3. **Custom Analysis**: Adjust weights and calculate new scores
4. **Compare Sites**: Select multiple sites for comparison
5. **Export Data**: Download site data for further analysis

## 📝 Note

This is a demo application with pre-loaded sample data. No authentication is required to use the application. All data is reset periodically.
