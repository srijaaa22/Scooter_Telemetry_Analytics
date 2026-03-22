import argparse
import os
import glob
from collections import defaultdict

from telemetry.ingest import load_csv
from telemetry.sessionize import sessionize
from telemetry.metrics import compute_daily_metrics
from telemetry.anomaly import detect_anomalies
from telemetry.reports import generate_report

def process_file(filepath: str, out_dir: str):
    """Processes a single CSV file through the entire pipeline."""
    print(f"\n Loading {filepath}...")
    
    # 1. Ingest & Validate
    samples, errors = load_csv(filepath)
    print(f"   Loaded {len(samples)} valid rows, found {len(errors)} errors.")
    
    if not samples:
        print(" No valid samples to process. Skipping.")
        return

    # 2. Group by Vehicle ID
    vehicles = defaultdict(list)
    for sample in samples:
        vehicles[sample.vehicle_id].append(sample)
        
    print(f"Processing {len(vehicles)} vehicles...")

    # 3. Process each vehicle independently
    for vehicle_id, vehicle_samples in vehicles.items():
        vehicle_samples.sort(key=lambda s: s.timestamp)
        
        report_date = vehicle_samples[0].timestamp.split('T')[0]
        
        sessions = sessionize(vehicle_samples)
        metrics = compute_daily_metrics(vehicle_id, report_date, vehicle_samples, sessions)
        anomalies = detect_anomalies(vehicle_samples)
        
        generate_report(vehicle_id, report_date, vehicle_samples, metrics, anomalies, out_dir)
        
        print(f"{vehicle_id}: {metrics.num_rides} rides, {metrics.num_charges} charges, {len(anomalies)} anomalies → {out_dir}{vehicle_id}_report.png")

def main():
    parser = argparse.ArgumentParser(description = "Electric Scooter Telemetry Pipeline")
    parser.add_argument("--input", type = str, default = "data/", help = "Directory containing raw CSV files")
    parser.add_argument("--out", type = str, default = "reports/", help = "Directory to save generated reports")
    args = parser.parse_args()

    search_pattern = os.path.join(args.input, "*.csv")
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print(f"No CSV files found in {args.input}. Did you run generate_data.py first?")
        return

    for filepath in csv_files:
        process_file(filepath, args.out)

    print(f"\nDone! Reports saved to {args.out}")

if __name__ == "__main__":
    main()