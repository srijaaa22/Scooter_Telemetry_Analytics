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