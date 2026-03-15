import csv
from models import TelemetrySample
from datetime import datetime

def load_csv(filepath):

    samples = []
    errors = []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            valid, msg = validate_row(row)
            if valid:
                sample = TelemetrySample(
                    timestamp=row["timestamp"],
                    vehicle_id=row["vehicle_id"],
                    speed_kmph=float(row["speed_kmph"]),
                    soc=float(row["soc"]),
                    motor_temp_c=float(row["motor_temp_c"]),
                    lat=float(row["lat"]),
                    lon=float(row["lon"]),
                    state=row["state"]
                )

                samples.append(sample)

            else:

                errors.append({
                    "row": i + 2,
                    "error": msg
                })

    return samples, errors


def validate_row(row):

    reqfields = [
        "timestamp",
        "vehicle_id",
        "speed_kmph",
        "soc",
        "motor_temp_c",
        "lat",
        "lon",
        "state"
    ]

    # check required fields
    for field in reqfields:
        if field not in row or row[field] == "":
            return False, "Missing field: " + field
        
    try:
        datetime.fromisoformat(row["timestamp"])
    except ValueError:
        return False, "Invalid timestamp format"
    
    try:
        speed = float(row["speed_kmph"])
        soc = float(row["soc"])
        motor_temp = float(row["motor_temp_c"])
        lat = float(row["lat"])
        lon = float(row["lon"])
    except ValueError:
        return False, "Non-numeric value in numeric field"

    if speed < 0 or speed > 150:
        return False, "Impossible speed: " + str(speed)

    if soc < 0 or soc > 100:
        return False, "Impossible SOC: " + str(soc)

    if row["state"] not in ["idle", "riding", "charging"]:
        return False, "Invalid state"

    return True, ""

if __name__ == "__main__":

    samples, errors = load_csv("data/sample_telemetry.csv")

    print("Valid samples:", len(samples))
    print("Errors:", len(errors))
