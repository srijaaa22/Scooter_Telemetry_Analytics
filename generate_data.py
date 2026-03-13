import random 
from datetime import datetime, timedelta
import csv
from pathlib import Path

def generate_vehicle_day(vehicle_id,date):

    dt=datetime.fromisoformat( date + "T06:00:00-05:00")

    soc = random.uniform(80,100)
    lat=12.9716
    lon=77.5946
    temp=35.0
    state="idle"

    rows=[]

    for i in range(500):
        r=random.random()
        if state == "idle" and r<0.06:
            state = 'riding'
        elif state == "riding" and  r<0.04:
            state = 'idle'
        elif state == "idle" and soc<35 and r<0.1:
            state = 'charging'
        elif state == "charging" and soc>90 and r<0.2:
            state = 'idle'

        if state == 'riding':
            speed = random.uniform(10,55)
            soc -= random.uniform(0.05,0.2)
            temp += random.uniform(0,0.7)
            lat += random.uniform(-0.001,0.001)
            lon += random.uniform(-0.001,0.001)

        elif state == 'charging':
            speed = 0.0
            soc += random.uniform(0.15,0.6)
            temp -= random.uniform(0.0,0.4)
    
        else :
            speed = 0.0
            soc -= random.uniform(0.0,0.03)
            temp -= random.uniform(0.0,0.15)

        soc = max(0, min(100, soc))
        temp = max(30, min(95, temp))
    
        d={"timestamp":dt.isoformat(), 
           "vehicle_id":vehicle_id, 
           "speed_kmph":round(speed,1), 
           "soc":round(soc,1),
           "motor_temp_c": round(temp,1),
           "lat":round(lat,6), 
           "lon":round(lon,6), 
           "state":state}
        
        if random.random()<0.02:
            c=random.choice(["missing speed","impossible speed","soc","lat"])
            if c == 'missing speed':
                d["speed_kmph"] = ""
            elif c == 'impossible speed':
                d["speed_kmph"] = random.randint(180,200)
            elif c == 'soc':
                d["soc"] = random.randint(101,150)
            else:
                d["lat"] +=0.5
        rows.append(d)
        dt+=timedelta(minutes=random.randint(1,5))

    return rows

def main():
    Path("data").mkdir(parents=True, exist_ok=True)
    
    all_rows=[]
    for i in ["SCT-001", "SCT-002", "SCT-003"]:
        rows = generate_vehicle_day(i, "2026-08-29")
        all_rows.extend(rows)
        print(i, "generated", len(rows), "rows")

    print("Total rows:", len(all_rows))

    file_path = Path("data/sample_telemetry.csv")

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

    print("Wrote", len(all_rows), "rows to", file_path)

if __name__ == "__main__":
    main()