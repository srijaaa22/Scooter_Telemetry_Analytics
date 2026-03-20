import math
from models import TelemetrySample, Anomaly

def detect_anomalies(samples: list[TelemetrySample]) -> list[Anomaly]:
    anomalies = []
    for i in range(1, len(samples)):
        prev = samples[i-1]
        curr = samples[i]
        if curr.state == 'riding' and curr.soc > prev.soc:
            anomalies.append(Anomaly(vehicle_id=curr.vehicle_id,
                                     timestamp=curr.timestamp,
                                     rule="soc increase while riding",
                                     severity='Medium',
                                     explanation=f"SOC increased from {prev.soc}% to {curr.soc}% while riding — possible sensor glitch"))
            
        if curr.motor_temp_c > 80:
            anomalies.append(Anomaly(vehicle_id=curr.vehicle_id,
                                     timestamp=curr.timestamp,
                                     rule="temperature spike",
                                     severity="High",
                                     explanation=f"Motor temp {curr.motor_temp_c}°C exceeds 80°C threshold"))
            
        if math.fabs(prev.lat-curr.lat) > 0.01 or math.fabs(prev.lon-curr.lon) > 0.01:
            anomalies.append(Anomaly(vehicle_id=curr.vehicle_id,
                                     timestamp=curr.timestamp,
                                     rule="gps_jump",
                                     severity="Medium",
                                     explanation=f"Sudden GPS jump detected between {prev.timestamp} and {curr.timestamp}"))
            
    return anomalies