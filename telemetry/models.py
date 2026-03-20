from dataclasses import dataclass

@dataclass
class TelemetrySample:
    timestamp: str          # when the reading was taken
    vehicle_id: str         # which scooter (e.g. "SCT-001")
    speed_kmph: float       # speed in km/h
    soc: float              # battery percentage (0-100)
    motor_temp_c: float     # motor temperature in celsius
    lat: float              # GPS latitude
    lon: float              # GPS longitude
    state: str              # "idle", "riding", or "charging"

@dataclass
class Session:
    vehicle_id: str         # which scooter
    session_type: str       # "riding" or "charging" or "idle"
    start_time: str         # when the session started
    end_time: str           # when the session ended
    sample_count: int       # how many samples in this session
    start_soc: float        # battery percentage at start
    end_soc: float          # battery percentage at end
    max_speed: float        # max speed during session
    max_temp: float         # max motor temp during session

@dataclass
class DailyMetrics:
    vehicle_id: str
    date: str
    total_ride_time_min: float
    distance_estimate_km: float
    avg_speed_kmph: float
    soc_drop_pct: float
    max_temp_c: float
    num_rides: int
    num_charges: int

@dataclass
class Anomaly:
    vehicle_id: str
    timestamp: str
    rule: str
    severity: str            # "low", "medium", or "high"
    explanation: str