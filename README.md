# Scooter Telemetry Analytics

## Abstract

This repository presents a comprehensive data analytics pipeline for processing electric scooter telemetry data. The system implements an end-to-end solution for ingesting raw sensor readings, validating data quality, performing temporal sessionization, computing operational metrics, detecting anomalies, and generating multi-format analytical reports. Designed for IoT fleet management applications, this platform enables real-time monitoring of vehicle health, operational efficiency, and predictive maintenance for electric scooter fleets.

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Data Model](#data-model)
7. [Pipeline Components](#pipeline-components)
8. [Usage](#usage)
9. [Testing](#testing)
10. [Output Formats](#output-formats)
11. [Anomaly Detection](#anomaly-detection)
12. [Performance Metrics](#performance-metrics)
13. [Future Work](#future-work)
14. [Contributing](#contributing)
15. [License](#license)

---

## Introduction

### Background

Electric scooters have emerged as a critical component of modern urban transportation infrastructure. Fleet operators managing hundreds or thousands of vehicles require robust telemetry systems to monitor vehicle health, optimize operations, and ensure rider safety. Raw telemetry data from embedded sensors—including GPS coordinates, battery state-of-charge (SOC), motor temperature, and operational state—must be processed, validated, and analyzed to extract actionable insights.

### Project Scope

This project implements a modular ETL (Extract, Transform, Load) pipeline that:

- **Ingests** streaming telemetry data from CSV files
- **Validates** data integrity using rule-based quality checks
- **Sessionizes** temporal data into meaningful operational periods
- **Computes** daily performance metrics for each vehicle
- **Detects** operational anomalies using heuristic rules
- **Generates** both machine-readable (JSON) and human-readable (PNG) reports

### Research Objectives

1. Develop a scalable architecture for processing IoT sensor data
2. Implement robust data validation mechanisms to ensure data quality
3. Design efficient sessionization algorithms for state-based temporal data
4. Create interpretable anomaly detection rules for operational monitoring
5. Generate comprehensive multi-format reports for stakeholder analysis

---

## System Architecture

### High-Level Design

The system follows a **pipeline architecture** with six sequential stages:

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐
│   Raw CSV   │───▶│  Ingestion   │───▶│  Validation    │
│    Data     │    │   & Parse    │    │  & Filtering   │
└─────────────┘    └──────────────┘    └────────────────┘
                                               │
                                               ▼
┌─────────────┐    ┌──────────────┐    ┌────────────────┐
│   Reports   │◀───│   Anomaly    │◀───│ Sessionization │
│ (JSON/PNG)  │    │  Detection   │    │  & Grouping    │
└─────────────┘    └──────────────┘    └────────────────┘
                           ▲
                           │
                    ┌──────────────┐
                    │   Metrics    │
                    │ Computation  │
                    └──────────────┘
```

### Architectural Principles

- **Modularity**: Each processing stage is encapsulated in independent modules
- **Type Safety**: Python dataclasses ensure compile-time type checking
- **Fail-Safe Design**: Validation errors are collected, not raised as exceptions
- **Per-Vehicle Processing**: Each vehicle is analyzed independently for parallelization potential
- **Multi-Format Output**: Reports generated in both JSON (API-friendly) and PNG (human-readable)

---

## Technology Stack

### Development Environment

| Component | Specification |
|-----------|---------------|
| **Operating System** | Windows 11 |
| **IDE** | Visual Studio Code (VS Code) |
| **Python Version** | 3.12.3 (latest stable release) |
| **Package Manager** | pip |

### Core Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| **NumPy** | Latest | Numerical computations and array operations |
| **Matplotlib** | Latest | Data visualization and chart generation |
| **pytest** | Latest | Unit testing framework |

### Python Standard Library Modules

- `dataclasses`: Type-safe data models
- `csv`: CSV file parsing
- `argparse`: Command-line argument parsing
- `datetime`: Timestamp manipulation
- `collections.defaultdict`: Efficient grouping operations
- `glob`: File pattern matching
- `json`: JSON serialization
- `os`: File system operations

---

## Installation

### Prerequisites

- Python 3.8 or higher (tested on Python 3.12.3)
- pip package manager
- Git (for cloning the repository)

### Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/srijaaa22/Scooter_Telemetry_Analytics.git
cd Scooter_Telemetry_Analytics
```

2. **Create Virtual Environment** (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Generate Sample Data**

```bash
python generate_data.py
```

This creates `data/sample_telemetry.csv` with 1,500 synthetic telemetry samples for 3 vehicles (SCT-001, SCT-002, SCT-003).

5. **Verify Installation**

```bash
pytest tests/
```

All 7 tests should pass.

---

## Project Structure

```
Scooter_Telemetry_Analytics/
│
├── data/                          # Input data directory
│   └── sample_telemetry.csv      # Synthetic telemetry (1,500 rows)
│
├── telemetry/                     # Core processing modules
│   ├── __init__.py               # Package initialization
│   ├── models.py                 # Data models (5 dataclasses)
│   ├── ingest.py                 # CSV loading & validation
│   ├── sessionize.py             # Session grouping logic
│   ├── metrics.py                # Daily metrics computation
│   ├── anomaly.py                # Anomaly detection rules
│   └── reports.py                # Report generation (JSON + PNG)
│
├── tests/                         # Testing infrastructure
│   └── test_basics.py            # Unit tests (pytest)
│
├── reports/                       # Output directory
│   ├── SCT-001_summary.json      # Vehicle 1 metrics
│   ├── SCT-001_report.png        # Vehicle 1 visualization
│   ├── SCT-002_summary.json      # Vehicle 2 metrics
│   ├── SCT-002_report.png        # Vehicle 2 visualization
│   ├── SCT-003_summary.json      # Vehicle 3 metrics
│   └── SCT-003_report.png        # Vehicle 3 visualization
│
├── generate_data.py               # Synthetic data generator
├── main.py                        # Pipeline orchestrator
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore patterns
└── README.md                      # This file
```

---

## Data Model

The system defines five core data structures using Python `dataclasses`:

### 1. TelemetrySample

Represents a single sensor reading from a scooter.

```python
@dataclass
class TelemetrySample:
    timestamp: str          # ISO 8601 format (e.g., "2026-08-29T06:00:00")
    vehicle_id: str         # Unique identifier (e.g., "SCT-001")
    speed_kmph: float       # Speed in kilometers per hour (0-150)
    soc: float              # Battery State of Charge (0-100%)
    motor_temp_c: float     # Motor temperature in Celsius
    lat: float              # GPS latitude coordinate
    lon: float              # GPS longitude coordinate
    state: str              # Operational state: "idle", "riding", "charging"
```

### 2. Session

Represents a continuous period of activity in the same operational state.

```python
@dataclass
class Session:
    vehicle_id: str         # Unique identifier
    session_type: str       # "riding", "charging", or "idle"
    start_time: str         # Session start timestamp
    end_time: str           # Session end timestamp
    sample_count: int       # Number of samples in session
    start_soc: float        # Battery SOC at session start
    end_soc: float          # Battery SOC at session end
    max_speed: float        # Maximum speed during session
    max_temp: float         # Maximum motor temperature during session
```

### 3. DailyMetrics

Aggregated performance indicators for a single vehicle over one day.

```python
@dataclass
class DailyMetrics:
    vehicle_id: str
    date: str
    total_ride_time_min: float      # Total minutes in riding state
    distance_estimate_km: float      # Estimated distance traveled
    avg_speed_kmph: float            # Average speed during riding
    soc_drop_pct: float              # Total battery consumption
    max_temp_c: float                # Peak motor temperature
    num_rides: int                   # Number of riding sessions
    num_charges: int                 # Number of charging sessions
```

### 4. Anomaly

Represents a detected operational anomaly.

```python
@dataclass
class Anomaly:
    vehicle_id: str
    timestamp: str
    rule: str               # Detection rule name
    severity: str           # "low", "medium", or "high"
    explanation: str        # Human-readable description
```

---

## Pipeline Components

### 1. Ingestion & Validation (`telemetry/ingest.py`)

**Purpose**: Load CSV data and validate each row for data quality.

**Key Functions**:
- `load_csv(filepath: str) -> Tuple[List[TelemetrySample], List[str]]`
- `validate_row(row: dict) -> Tuple[TelemetrySample, str]`

**Validation Rules**:
1. **Required Fields**: All 8 columns must be present
2. **Timestamp Format**: Must be valid ISO 8601 format
3. **Numeric Parsing**: Speed, SOC, temperature, lat/lon must be parseable as floats
4. **Range Validation**:
   - Speed: 0 ≤ speed ≤ 150 km/h
   - SOC: 0 ≤ soc ≤ 100%
5. **State Validation**: State must be one of {"idle", "riding", "charging"}

**Error Handling**: Invalid rows are logged but do not halt processing. Returns tuple of (valid_samples, error_list).

### 2. Sessionization (`telemetry/sessionize.py`)

**Purpose**: Group consecutive samples with the same operational state into sessions.

**Algorithm**:
1. Sort samples chronologically by timestamp
2. Initialize first session with first sample's state
3. For each subsequent sample:
   - If state matches current session → accumulate statistics
   - If state differs → finalize current session, start new session
4. Finalize last session

**Statistics Tracked**:
- Sample count
- Start/end SOC (battery change during session)
- Maximum speed and temperature

**Use Case**: Identifies distinct operational periods (e.g., "9 AM - 10 AM: Riding session, 15 samples, 5% battery drain, max speed 45 km/h").

### 3. Metrics Computation (`telemetry/metrics.py`)

**Purpose**: Calculate daily Key Performance Indicators (KPIs) for each vehicle.

**Key Function**: `compute_daily_metrics(vehicle_id, date, samples, sessions) -> DailyMetrics`

**Computed Metrics**:

1. **Total Ride Time**: Sum of all riding session durations (minutes)
2. **Distance Estimate**: ∑(speed × Δt) for riding samples
   - Time gaps capped at 0.5 hours to prevent GPS outage errors
3. **Average Speed**: Mean of all riding samples where speed > 0
4. **SOC Drop**: Battery % at first sample - battery % at last sample
5. **Max Temperature**: Peak motor temperature across all samples
6. **Ride Count**: Number of riding sessions
7. **Charge Count**: Number of charging sessions

**Mathematical Formulation**:

```
distance = Σ(speed_i × Δt_i) for all riding samples
  where Δt_i = min(t_{i+1} - t_i, 0.5 hours)

avg_speed = Σ(speed_i) / count(speed_i > 0)
```

### 4. Anomaly Detection (`telemetry/anomaly.py`)

**Purpose**: Identify operational irregularities using rule-based heuristics.

**Detection Rules**:

#### Rule 1: SOC Increase While Riding
- **Condition**: `state == "riding" AND soc[i] > soc[i-1]`
- **Severity**: Medium
- **Explanation**: Battery cannot charge while in use (indicates sensor malfunction)

#### Rule 2: Temperature Spike
- **Condition**: `motor_temp > 80°C`
- **Severity**: High
- **Explanation**: Overheating risk or sensor fault

#### Rule 3: GPS Jump
- **Condition**: `|lat[i] - lat[i-1]| > 0.01 OR |lon[i] - lon[i-1]| > 0.01`
- **Severity**: Medium
- **Explanation**: Impossible location change (GPS signal loss or spoofing)

**Output**: List of `Anomaly` objects with timestamp, rule, severity, and explanation.

### 5. Report Generation (`telemetry/reports.py`)

**Purpose**: Produce multi-format analytical reports.

**Key Function**: `generate_report(vehicle_id, date, samples, metrics, anomalies, out_dir)`

**Output Formats**:

#### JSON Summary (`<vehicle_id>_summary.json`)
```json
{
  "vehicle_id": "SCT-001",
  "date": "2026-08-29",
  "metrics": {
    "total_ride_time_min": 974.17,
    "distance_estimate_km": 530.86,
    "avg_speed_kmph": 32.71,
    "num_rides": 9,
    ...
  },
  "anomaly_count": 208,
  "anomalies": [
    {
      "timestamp": "2026-08-29T06:02:00",
      "rule": "temperature_spike",
      "severity": "high",
      "explanation": "Motor temperature exceeded 80°C (actual: 82.5°C)"
    },
    ...
  ]
}
```

#### PNG Visualization (`<vehicle_id>_report.png`)

Three-panel time-series chart:
1. **Panel 1**: Speed (km/h) vs. sample index (blue line)
2. **Panel 2**: Battery SOC (%) vs. sample index (green line)
3. **Panel 3**: Motor temperature (°C) vs. sample index (red line + 80°C threshold)

**Sample Output**:

![Sample Report for Vehicle SCT-001](reports/SCT-001_report.png)

*Figure 1: Sample telemetry report for vehicle SCT-001 showing speed profile, battery discharge curve, and motor temperature with anomaly threshold (80°C red line). This vehicle completed 9 rides over 974 minutes, traveling an estimated 530.86 km with 208 detected anomalies, primarily temperature spikes.*

---

## Usage

### Basic Execution

Run the entire pipeline with default settings:

```bash
python main.py
```

**Default Configuration**:
- Input directory: `data/`
- Output directory: `reports/`
- Processes all `.csv` files in input directory

### Custom Directories

Specify custom input and output paths:

```bash
python main.py --input raw_data/ --out output_reports/
```

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--input` | str | `data/` | Directory containing CSV files |
| `--out` | str | `reports/` | Directory for generated reports |

### Execution Flow

1. Load all CSV files from input directory
2. For each CSV file:
   - Ingest and validate rows
   - Group samples by vehicle ID
   - For each vehicle:
     - Sessionize temporal data
     - Compute daily metrics
     - Detect anomalies
     - Generate JSON + PNG reports
     - Print summary to console
3. Print completion message

**Console Output Example**:

```
 Loading data/sample_telemetry.csv...
   Loaded 1485 valid rows, found 15 errors.
Processing 3 vehicles...
SCT-001: 9 rides, 0 charges, 208 anomalies → reports/SCT-001_report.png
SCT-002: 7 rides, 2 charges, 156 anomalies → reports/SCT-002_report.png
SCT-003: 8 rides, 1 charges, 182 anomalies → reports/SCT-003_report.png

Done! Reports saved to reports/
```

---

## Testing

### Test Framework

The project uses **pytest** for unit testing with 7 comprehensive tests covering critical pipeline components.

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_basics.py::test_sessionize_groups_same_state
```

### Test Coverage

**File**: `tests/test_basics.py`

#### Ingestion Tests
1. `test_validate_rejects_missing_field`: Validates rejection of rows with missing required fields
2. `test_validate_rejects_out_of_range`: Validates rejection of out-of-range values (e.g., SOC > 100%)

#### Sessionization Tests
3. `test_sessionize_groups_same_state`: Confirms consecutive samples with same state form single session
4. `test_sessionize_splits_on_change`: Confirms state transitions create new sessions

#### Anomaly Detection Tests
5. `test_anomaly_detects_soc_glitch`: Detects battery increase during riding
6. `test_anomaly_detects_temperature_spike`: Detects motor temperature > 80°C
7. `test_anomaly_detects_gps_jump`: Detects impossible location changes

### Test Data Strategy

Uses pytest's `tmp_path` fixture for isolated test files, preventing side effects between tests.

---

## Output Formats

### JSON Report Structure

Machine-readable format for API integration and automated analysis.

**Schema**:
```json
{
  "vehicle_id": "string",
  "date": "YYYY-MM-DD",
  "metrics": {
    "total_ride_time_min": "float",
    "distance_estimate_km": "float",
    "avg_speed_kmph": "float",
    "soc_drop_pct": "float",
    "max_temp_c": "float",
    "num_rides": "int",
    "num_charges": "int"
  },
  "anomaly_count": "int",
  "anomalies": [
    {
      "timestamp": "ISO 8601 string",
      "rule": "string",
      "severity": "low|medium|high",
      "explanation": "string"
    }
  ]
}
```

### PNG Report Features

Human-readable visualization for stakeholder presentations.

**Design Elements**:
- **Shared X-Axis**: Sample index for temporal alignment
- **Color Coding**: Blue (speed), green (battery), red (temperature)
- **Threshold Line**: 80°C danger zone marked on temperature panel
- **Title**: Vehicle ID and date
- **Labels**: Clear axis labels with units
- **Grid**: Subtle gridlines for readability

---

## Anomaly Detection

### Detection Philosophy

Uses **rule-based heuristics** rather than machine learning for:
- **Interpretability**: Stakeholders understand explicit rules
- **Determinism**: Consistent behavior without training data requirements
- **Real-Time Capability**: No model inference overhead

### Current Rules

| Rule ID | Name | Threshold | Severity | Description |
|---------|------|-----------|----------|-------------|
| 1 | SOC Glitch | SOC[i] > SOC[i-1] during riding | Medium | Battery cannot charge while in use |
| 2 | Temperature Spike | motor_temp > 80°C | High | Overheating risk or sensor fault |
| 3 | GPS Jump | Δlat > 0.01° OR Δlon > 0.01° | Medium | Impossible location change (~1 km) |

### Extensibility

New rules can be added by editing `telemetry/anomaly.py` and following the pattern:

```python
# Example: Speed spike detection
if sample.speed_kmph > 100:
    anomalies.append(Anomaly(
        vehicle_id=sample.vehicle_id,
        timestamp=sample.timestamp,
        rule="speed_spike",
        severity="high",
        explanation=f"Unsafe speed: {sample.speed_kmph} km/h"
    ))
```

---

## Performance Metrics

### Sample Dataset Statistics

| Metric | Value |
|--------|-------|
| Total Samples | 1,500 |
| Vehicles | 3 (SCT-001, SCT-002, SCT-003) |
| Samples per Vehicle | 500 |
| Date Range | 2026-08-29 (24 hours) |
| Valid Rows | ~1,485 (99% validation pass rate) |
| Invalid Rows | ~15 (intentional test cases) |

### Vehicle SCT-001 Report Summary

| KPI | Value |
|-----|-------|
| Total Ride Time | 974 minutes (~16 hours) |
| Distance Estimate | 530.86 km |
| Average Speed | 32.71 km/h |
| SOC Drop | 41.7% |
| Max Temperature | 95.0°C |
| Number of Rides | 9 |
| Charging Cycles | 0 |
| Detected Anomalies | 208 |
| Primary Anomaly Type | Temperature spikes (>90%) |

---

## Future Work

### Planned Enhancements

1. **Real-Time Processing**: Integrate with message queues (Kafka/RabbitMQ) for streaming data
2. **Machine Learning Models**: Implement LSTM networks for predictive maintenance
3. **Database Integration**: Store processed data in PostgreSQL/TimescaleDB
4. **Web Dashboard**: Build React frontend for real-time monitoring
5. **Advanced Anomaly Detection**: Add statistical process control (SPC) methods
6. **Multi-Day Analysis**: Extend metrics to weekly/monthly aggregations
7. **API Layer**: RESTful API for querying reports
8. **Geospatial Analysis**: Route reconstruction and geofencing

### Research Directions

- Comparative study of ML vs. rule-based anomaly detection
- Optimization of distance estimation algorithms
- Battery degradation modeling
- Predictive maintenance using survival analysis

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-rule`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest tests/`)
5. Submit a pull request with detailed description

### Code Style

- Follow PEP 8 conventions
- Use type hints for function signatures
- Add docstrings for public functions
- Maintain test coverage above 80%

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Citation

If you use this code in academic research, please cite:

```bibtex
@software{scooter_telemetry_analytics,
  author = {Srija},
  title = {Scooter Telemetry Analytics: An ETL Pipeline for IoT Fleet Management},
  year = {2026},
  url = {https://github.com/srijaaa22/Scooter_Telemetry_Analytics}
}
```

---

## Acknowledgments

- Python Software Foundation for the Python programming language
- NumPy and Matplotlib development teams
- pytest framework maintainers
- Open-source community for inspiration and tools

---

## Contact

For questions, issues, or collaboration inquiries, please open an issue on the GitHub repository:
https://github.com/srijaaa22/Scooter_Telemetry_Analytics/issues

---

**Last Updated**: March 22, 2026
**Version**: 1.0.0
**Python Version**: 3.12.3
**Status**: Production Ready
