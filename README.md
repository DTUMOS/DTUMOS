# DTUMOS (Dynamic Taxi-based Urban Mobility Operation System)

**Seongnam Taxi Simulation System**

DTUMOS is a comprehensive taxi operation simulation and optimization system for Seongnam City, Gyeonggi Province, South Korea. The system optimizes passenger-vehicle matching based on real taxi data and provides visualization and analysis of simulation results.

---

## 📋 Table of Contents

- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration Options](#configuration-options)
- [Module Description](#module-description)
- [Visualization](#visualization)
- [Requirements](#requirements)
- [Core Algorithms](#core-algorithms)
- [Simulation Process](#simulation-process)
- [Simulation Metrics](#simulation-metrics)

---

## 🚀 Key Features

### 1. **Data Preprocessing**
- Process real taxi operation data
- Filter data within Seongnam city boundaries
- Normalize passenger and vehicle data

### 2. **Vehicle Simulation**
- Configurable number of taxis
- Shift-based work schedule simulation
- Time-based operation pattern reproduction

### 3. **Optimized Dispatch**
- Optimal dispatch algorithm using OR-Tools
- Cost matrix-based passenger-vehicle matching
- MIP (Mixed Integer Programming) based optimization

### 4. **Result Visualization**
- Interactive dashboard generation
- Time-series operation status charts
- Map-based spatial analysis
- Vehicle operation efficiency analysis

---

## 📁 Project Structure

```
DTUMOS/
├── main.py                          # Main execution script
├── requirements.txt                 # Python package dependencies
├── data/                           # Data directory
│   ├── etc/                        # Raw data
│   │   ├── Seongnam_Taxi_20240418.csv
│   │   └── seongnam_boundary.geojson
│   └── agents/                     # Preprocessed agent data
│       ├── passenger/              # Passenger data
│       └── vehicle/                # Vehicle data
├── modules/                        # Core modules
│   ├── preprocess/                # Data preprocessing
│   │   ├── passenger_preprocessor.py
│   │   ├── vehicle_preprocessor.py
│   │   └── data_preprocessor.py
│   ├── engine/                    # Simulation engine
│   │   ├── simulator.py          # Main simulator
│   │   ├── config_manager.py     # Configuration management
│   │   ├── io_manager.py         # I/O management
│   │   └── state_updater.py      # State updates
│   ├── dispatch/                  # Dispatch algorithms
│   │   ├── dispatch_algorithms.py # Optimization algorithms
│   │   ├── cost_matrix.py        # Cost matrix calculation
│   │   └── dispatch_flow.py      # Dispatch flow control
│   ├── routing/                   # Route calculation
│   │   └── osrm_client.py        # OSRM client
│   ├── analytics/                 # Analysis and visualization
│   │   ├── dashboard.py          # Dashboard generation
│   │   ├── service_charts.py     # Service charts
│   │   ├── fleet_charts.py       # Fleet operation charts
│   │   └── spatial_charts.py     # Spatial analysis charts
│   └── utils/                     # Utilities
│       └── distance_utils.py     # Distance calculation
└── visualization/                 # Visualization resources
    ├── dashboard/                 # Dashboard HTML/JS
    └── simulation/                # Simulation visualization
```

---

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DTUMOS
```

### 2. Create and Activate Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### Basic Execution

```bash
python main.py
```

### Main Configuration Parameters (modify in main.py)

```python
# Data Configuration
BASE_DATE = "2024-04-18"              # Simulation date
TIME_RANGE_START = 1080               # Start time in minutes (18:00)
TIME_RANGE_END = 1260                 # End time in minutes (21:00)

# Vehicle Configuration
NUM_TAXIS = 950                       # Number of taxis in simulation
USE_SHIFT = True                      # Enable shift-based scheduling
RANDOM_SEED = 42                      # Random seed for reproducibility

# Simulation Configuration
base_configs['dispatch_mode'] = 'in_order'  # Dispatch mode
base_configs['matrix_mode'] = 'haversine_distance'  # Distance calculation method
```

---

## ⚙️ Configuration Options

### Dispatch Mode
- `in_order`: Sequential dispatch
- `optimization`: Optimization-based dispatch using OR-Tools

### Matrix Mode (Distance Calculation)
- `haversine_distance`: Straight-line distance using Haversine formula
- `osrm`: Actual road distance using OSRM

### Time Configuration
- Time is specified in **minutes**
- Examples:
  - `1080` = 18:00 (6:00 PM)
  - `1260` = 21:00 (9:00 PM)

---

## 📦 Module Description

### 1. **Preprocess Module**
- `passenger_preprocessor.py`: Passenger data preprocessing and filtering
- `vehicle_preprocessor.py`: Vehicle data generation and schedule configuration
- `data_preprocessor.py`: Integrated data preprocessing

**Key Functions:**
- Data filtering within regional boundaries
- Time-based data cropping
- Shift schedule generation

### 2. **Engine Module**
- `simulator.py`: Main simulation logic
- `config_manager.py`: Configuration management and validation
- `state_updater.py`: Passenger/vehicle state updates
- `io_manager.py`: Result saving and loading

**Simulation Process:**
1. Initial data loading
2. Time-step based iterative simulation
3. Passenger request processing
4. Vehicle dispatch and state updates
5. Result recording and saving

### 3. **Dispatch Module**
- `dispatch_algorithms.py`: OR-Tools based optimization
- `cost_matrix.py`: Passenger-vehicle cost matrix calculation
- `dispatch_flow.py`: Dispatch flow control

**Optimization Algorithm:**
- MIP (Mixed Integer Programming) based
- Cost minimization objective function
- Constraints:
  - Each vehicle is assigned at most 1 passenger
  - Each passenger is assigned exactly 1 vehicle

### 4. **Analytics Module**
- `dashboard.py`: Automatic dashboard generation
- `service_charts.py`: Service metric charts
- `fleet_charts.py`: Fleet operation charts
- `spatial_charts.py`: Map-based spatial analysis

**Generated Charts:**
- Time-series waiting passenger count
- Vehicle utilization rate
- Service success/failure rate
- Regional demand heatmap

### 5. **Routing Module**
- `osrm_client.py`: OSRM (Open Source Routing Machine) API client

### 6. **Utils Module**
- `distance_utils.py`: Haversine distance calculation and utilities

---

## 📊 Visualization

### View Results After Simulation

```bash
# 1. Open HTML Dashboard
open ./visualization/dashboard/assets/html/index_<simulation_name>.html

# 2. Or Run Interactive Dashboard with npm
cd visualization/simulation
npm install
npm run dev
```

### Generated Result Files

```
simul_result/
└── scenario_base/
    └── <timestamp>/
        ├── passenger_marker.json    # Passenger marker data
        ├── trip.json               # Trip records
        ├── record.csv              # Simulation records
        └── result.json             # Comprehensive results
```

---

## 📝 Requirements

### Python Version
- Python 3.8 or higher

### Key Packages
- `pandas`: Data processing
- `numpy`: Numerical computation
- `geopandas`: Geographic data processing
- `folium`: Map visualization
- `plotly`: Interactive charts
- `ortools`: Optimization algorithms
- `osmnx`: Road network data
- `matplotlib`: Chart generation

See `requirements.txt` for complete package list

---

## 🔍 Core Algorithms

### OR-Tools Based Dispatch Optimization

**Objective Function:**
```
Minimize: Σ cost[i,j] × x[i,j]
```

**Constraints:**
```
Σ x[i,j] ≤ 1  (Each vehicle i is assigned at most 1 passenger)
j

Σ x[i,j] = 1  (Each passenger j is assigned exactly 1 vehicle)
i
```

**Cost Matrix:**
- Distance or time between vehicles and passengers
- Uses Haversine distance or OSRM route distance

---

## 📖 Simulation Process

```
1. Data Loading
   ↓
2. Preprocessing (Passengers/Vehicles)
   ↓
3. Simulation Initialization
   ↓
4. [Time Loop]
   ├─ Extract new passenger requests
   ├─ Update vehicle states
   ├─ Execute dispatch algorithm
   ├─ Match passengers and vehicles
   └─ Record results
   ↓
5. Result Analysis and Visualization
   ↓
6. Dashboard Generation
```

---

## 🎯 Simulation Metrics

The simulation records the following metrics:

- **waiting_passenger_cnt**: Number of waiting passengers
- **fail_passenger_cnt**: Number of passengers who failed to get a ride
- **empty_vehicle_cnt**: Number of empty vehicles
- **driving_vehicle_cnt**: Number of vehicles in operation
- **iter_time(second)**: Execution time for each time step

---

## 🤝 Contributing

Bug reports, feature suggestions, and Pull Requests are welcome!

---

## 📄 License

Please check the repository for license information.

---

## 📧 Contact

If you have any questions about the project, please open an issue.

---

## 🙏 Acknowledgments

- OSRM (Open Source Routing Machine)
- OR-Tools (Google Optimization Tools)
- Seongnam City Taxi Data Provider

---

**Last Updated**: 2024-04-18
