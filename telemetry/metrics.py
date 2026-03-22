import numpy as np
from datetime import datetime
from typing import List
from .models import TelemetrySample, Session, DailyMetrics

def compute_daily_metrics(vehicle_id: str, date_str: str, samples: List[TelemetrySample], sessions: List[Session]) -> DailyMetrics:
    if not samples:
        return DailyMetrics(vehicle_id, date_str, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0)

    speed_array = np.array([s.speed_kmph for s in samples])
    temp_array = np.array([s.motor_temp_c for s in samples])

    distance_km = 0.0
    for i in range(len(samples) - 1):
        current = samples[i]
        next_sample = samples[i+1]
        
        if current.state == 'riding' and next_sample.state == 'riding':
            t1 = datetime.fromisoformat(current.timestamp)
            t2 = datetime.fromisoformat(next_sample.timestamp)
          
            hours_delta = (t2 - t1).total_seconds() / 3600.0
            
            if hours_delta <= 0.5:
                distance_km += current.speed_kmph * hours_delta
    
    riding_speeds = speed_array[speed_array > 0]
    avg_speed = float(np.mean(riding_speeds)) if len(riding_speeds) > 0 else 0.0
    
    total_ride_min = 0.0
    num_rides = 0
    num_charges = 0
    
    for session in sessions:
        if session.session_type == 'riding':
            num_rides += 1
            t1 = datetime.fromisoformat(session.start_time)
            t2 = datetime.fromisoformat(session.end_time)
            total_ride_min += (t2 - t1).total_seconds() / 60.0
        elif session.session_type == 'charging':
            num_charges += 1

    soc_drop = samples[0].soc - samples[-1].soc
    max_temp = float(np.max(temp_array))

    return DailyMetrics(
        vehicle_id=vehicle_id,
        date=date_str,
        total_ride_time_min=round(total_ride_min, 2),
        distance_estimate_km=round(distance_km, 2),
        avg_speed_kmph=round(avg_speed, 2),
        soc_drop_pct=round(soc_drop, 2),
        max_temp_c=round(max_temp, 2),
        num_rides=num_rides,
        num_charges=num_charges
    )