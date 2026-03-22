import os
import json
import matplotlib.pyplot as plt
from typing import List
from dataclasses import asdict
from .models import TelemetrySample, DailyMetrics, Anomaly

def generate_report(vehicle_id: str, date_str: str, samples: List[TelemetrySample], metrics: DailyMetrics, anomalies: List[Anomaly], out_dir: str) -> None:
    """Generates a JSON summary and a 3-panel PNG chart for a single vehicle."""
    
    # Ensure the output directory exists
    os.makedirs(out_dir, exist_ok=True)
    
    # generate json summary
    summary = {
        "metrics": asdict(metrics),
        "anomaly_count": len(anomalies),
        "anomalies": [asdict(a) for a in anomalies]
    }
    
    json_path = os.path.join(out_dir, f"{vehicle_id}_summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
        
    # generate png chart
    x = range(len(samples))
    speeds = [s.speed_kmph for s in samples]
    socs = [s.soc for s in samples]
    temps = [s.motor_temp_c for s in samples]
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"Daily Report: {vehicle_id} — {date_str}", fontsize=14)
    
    # Top Panel: Speed (Blue)
    ax1.plot(x, speeds, color='blue')
    ax1.set_ylabel('Speed (km/h)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Middle Panel: Battery SOC (Green)
    ax2.plot(x, socs, color='green')
    ax2.set_ylabel('Battery SOC (%)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Bottom Panel: Motor Temperature (Red)
    ax3.plot(x, temps, color='red')
    ax3.set_ylabel('Motor Temp (°C)')
    ax3.axhline(y=80, color='red', linestyle='--', label='Danger (80°C)') # Add danger threshold line
    ax3.set_xlabel('Sample Index')
    ax3.legend(loc='upper right')
    ax3.grid(True, linestyle='--', alpha=0.6)
    
    plt.tight_layout()
    
    png_path = os.path.join(out_dir, f"{vehicle_id}_report.png")
    plt.savefig(png_path)
    plt.close(fig)