# DTUMOS (Digital Twin for Large-scale Urban Mobility Operating System)

**Urban Mobility Simulation and Optimization System**

DTUMOS is a comprehensive digital twin system for simulating and optimizing large-scale urban mobility operations. The system provides advanced passenger-vehicle matching optimization based on real operational data, along with powerful visualization and analysis capabilities for simulation results.

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
- Process real operational data from urban mobility systems
- Filter data within defined geographic boundaries
- Normalize passenger and vehicle data for simulation

### 2. **Vehicle Simulation**
- Configurable fleet size
- Shift-based work schedule simulation
- Time-based operation pattern reproduction
- Realistic vehicle behavior modeling

### 3. **Optimized Dispatch**
- Optimal dispatch algorithm using OR-Tools
- Cost matrix-based passenger-vehicle matching
- MIP (Mixed Integer Programming) based optimization
- Scalable to large-scale urban environments

### 4. **Result Visualization**
- Interactive dashboard generation
- Time-series operation status charts
- Map-based spatial analysis
- Fleet operation efficiency analysis
- Real-time performance monitoring

---

## 📁 Project Structure

```
DTUMOS/
├── main.py                          # Main execution script
├── requirements.txt                 # Python package dependencies
├── data/                           # Data directory
│   ├── etc/                        # Raw data files
│   │   ├── Seongnam_Taxi_20240418.csv  # Example dataset
│   │   └── seongnam_boundary.geojson   # Example boundary file
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

# Fleet Configuration
NUM_TAXIS = 950                       # Number of vehicles in simulation
USE_SHIFT = True                      # Enable shift-based scheduling
RANDOM_SEED = 42                      # Random seed for reproducibility

# Simulation Configuration
base_configs['dispatch_mode'] = 'in_order'  # Dispatch mode
base_configs['matrix_mode'] = 'haversine_distance'  # Distance calculation method
base_configs['target_region'] = 'Your City, Country'  # Target region
```

---

## ⚙️ Configuration Options

### Dispatch Mode
- `in_order`: Sequential dispatch (FIFO-based)
- `optimization`: Optimization-based dispatch using OR-Tools

### Matrix Mode (Distance Calculation)
- `haversine_distance`: Straight-line distance using Haversine formula
- `osrm`: Actual road distance using OSRM (Open Source Routing Machine)

### Time Configuration
- Time is specified in **minutes from midnight**
- Examples:
  - `1080` = 18:00 (6:00 PM)
  - `1260` = 21:00 (9:00 PM)
  - `0` = 00:00 (midnight)

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
- Data validation and normalization

### 2. **Engine Module**
- `simulator.py`: Main simulation logic and orchestration
- `config_manager.py`: Configuration management and validation
- `state_updater.py`: Passenger/vehicle state updates
- `io_manager.py`: Result saving and loading

**Simulation Process:**
1. Initial data loading and validation
2. Time-step based iterative simulation
3. Passenger request processing
4. Vehicle dispatch and state updates
5. Result recording and persistent storage

### 3. **Dispatch Module**
- `dispatch_algorithms.py`: OR-Tools based optimization
- `cost_matrix.py`: Passenger-vehicle cost matrix calculation
- `dispatch_flow.py`: Dispatch flow control and coordination

**Optimization Algorithm:**
- MIP (Mixed Integer Programming) based
- Cost minimization objective function
- Constraints:
  - Each vehicle is assigned at most 1 passenger at a time
  - Each passenger is assigned exactly 1 vehicle
- Scalable for large-scale fleet operations

### 4. **Analytics Module**
- `dashboard.py`: Automatic dashboard generation
- `service_charts.py`: Service metric charts and KPIs
- `fleet_charts.py`: Fleet operation charts
- `spatial_charts.py`: Map-based spatial analysis

**Generated Charts:**
- Time-series waiting passenger count
- Vehicle utilization rate
- Service success/failure rate
- Regional demand heatmap
- Fleet distribution analysis

### 5. **Routing Module**
- `osrm_client.py`: OSRM (Open Source Routing Machine) API client
- Real-world road network routing
- Distance and time estimation

### 6. **Utils Module**
- `distance_utils.py`: Haversine distance calculation and utilities
- Geographic coordinate processing

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
- `pandas`: Data processing and manipulation
- `numpy`: Numerical computation
- `geopandas`: Geographic data processing
- `folium`: Interactive map visualization
- `plotly`: Interactive charts and graphs
- `ortools`: Optimization algorithms (Google OR-Tools)
- `osmnx`: OpenStreetMap road network data
- `matplotlib`: Static chart generation
- `shapely`: Geometric operations

See `requirements.txt` for complete package list

---

## 🔍 Core Algorithms

### OR-Tools Based Dispatch Optimization

**Objective Function:**
```
Minimize: Σ cost[i,j] × x[i,j]
          i,j
```

Where:
- `x[i,j]` is a binary decision variable (1 if vehicle i is assigned to passenger j, 0 otherwise)
- `cost[i,j]` is the cost of assigning vehicle i to passenger j (distance or time)

**Constraints:**
```
Σ x[i,j] ≤ 1  for all i  (Each vehicle is assigned at most 1 passenger)
j

Σ x[i,j] = 1  for all j  (Each passenger is assigned exactly 1 vehicle)
i

x[i,j] ∈ {0, 1}  for all i,j
```

**Cost Matrix:**
- Distance or time between vehicles and passengers
- Uses Haversine distance or OSRM route distance
- Dynamically computed based on current vehicle positions

---

## 📖 Simulation Process

```
1. Data Loading
   ↓
2. Preprocessing (Passengers/Vehicles)
   ├─ Load raw operational data
   ├─ Filter by geographic boundaries
   ├─ Normalize timestamps
   └─ Generate vehicle schedules
   ↓
3. Simulation Initialization
   ├─ Initialize vehicle states
   ├─ Load passenger requests
   └─ Setup data structures
   ↓
4. [Time Loop] - Iterate through each time step
   ├─ Extract new passenger requests
   ├─ Update vehicle states (position, availability)
   ├─ Execute dispatch algorithm
   ├─ Match passengers and vehicles
   ├─ Update trip records
   └─ Record metrics
   ↓
5. Result Analysis and Visualization
   ├─ Calculate KPIs
   ├─ Generate charts
   └─ Create spatial visualizations
   ↓
6. Dashboard Generation
   └─ Export interactive HTML dashboard
```

---

## 🎯 Simulation Metrics

The simulation records the following key performance indicators:

- **waiting_passenger_cnt**: Number of waiting passengers at each time step
- **fail_passenger_cnt**: Cumulative number of passengers who failed to get service
- **empty_vehicle_cnt**: Number of available/idle vehicles
- **driving_vehicle_cnt**: Number of vehicles currently in service
- **iter_time(second)**: Computation time for each simulation step

### Additional Analysis Metrics:
- Service success rate
- Average waiting time
- Vehicle utilization rate
- Distance traveled (empty vs. occupied)
- Demand patterns by time and location

---

## 🔧 Customization

### Adding Custom Datasets

1. Prepare your data in CSV format with required columns
2. Update the boundary file (GeoJSON) for your target region
3. Modify configuration in `main.py`:
   ```python
   RAW_DATA_PATH = "data/etc/your_data.csv"
   BOUNDARY_PATH = "data/etc/your_boundary.geojson"
   base_configs['target_region'] = 'Your City, Country'
   ```

### Extending Dispatch Algorithms

Implement custom dispatch logic in `modules/dispatch/dispatch_algorithms.py`

---

## 🤝 Contributing

Bug reports, feature suggestions, and Pull Requests are welcome!

### How to Contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

Please check the repository for license information.

---

## 📧 Contact

If you have any questions about the project, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- **OSRM** (Open Source Routing Machine) - Routing engine
- **OR-Tools** (Google Optimization Tools) - Optimization algorithms
- **OpenStreetMap** - Geographic data

---

## 📚 Publications

If you use DTUMOS in your research, please cite appropriately.

---

**Last Updated**: 2024-04-18
