import pytest
from telemetry.models import TelemetrySample
from telemetry.ingest import load_csv
from telemetry.sessionize import sessionize
from telemetry.anomaly import detect_anomalies

# INGESTION TESTS

def test_validate_rejects_missing_field(tmp_path):
    file = tmp_path / "missing.csv"
    # Provide the correct headers, but leave the speed_kmph value empty between the commas!
    # Notice the empty space before 95.0 -> SCT-1,,95.0
    file.write_text("timestamp,vehicle_id,speed_kmph,soc,motor_temp_c,lat,lon,state\n2026-02-28T06:00:00,SCT-1,,95.0,35.0,12.0,77.0,idle")
    
    samples, errors = load_csv(str(file))
    assert len(samples) == 0  
    assert len(errors) == 1   

def test_validate_rejects_out_of_range(tmp_path):
    file = tmp_path / "out_of_range.csv"
    # Correct headers, SOC is 150.0
    file.write_text("timestamp,vehicle_id,speed_kmph,soc,motor_temp_c,lat,lon,state\n2026-02-28T06:00:00,SCT-1,10.0,150.0,35.0,12.0,77.0,riding")
    
    samples, errors = load_csv(str(file))
    assert len(samples) == 0
    assert len(errors) == 1


# SESSIONIZATION TESTS

def test_sessionize_groups_same_state():
    # 3 consecutive riding samples
    samples = [
        TelemetrySample("2026-02-28T06:00:00", "SCT-1", 10.0, 95.0, 35.0, 12.0, 77.0, "riding"),
        TelemetrySample("2026-02-28T06:05:00", "SCT-1", 15.0, 94.0, 36.0, 12.0, 77.0, "riding"),
        TelemetrySample("2026-02-28T06:10:00", "SCT-1", 20.0, 93.0, 37.0, 12.0, 77.0, "riding"),
    ]
    sessions = sessionize(samples)
    
    assert len(sessions) == 1
    assert sessions[0].session_type == "riding"
    assert sessions[0].sample_count == 3

def test_sessionize_splits_on_change():
    # 2 riding samples followed by 1 idle sample
    samples = [
        TelemetrySample("2026-02-28T06:00:00", "SCT-1", 10.0, 95.0, 35.0, 12.0, 77.0, "riding"),
        TelemetrySample("2026-02-28T06:05:00", "SCT-1", 15.0, 94.0, 36.0, 12.0, 77.0, "riding"),
        TelemetrySample("2026-02-28T06:10:00", "SCT-1", 0.0, 93.0, 37.0, 12.0, 77.0, "idle"),
    ]
    sessions = sessionize(samples)
    
    assert len(sessions) == 2             
    assert sessions[0].session_type == "riding"
    assert sessions[1].session_type == "idle"


# ANOMALY TESTS

def test_anomaly_detects_soc_glitch():
    # Battery SOC goes UP from 90 to 95 while riding (impossible without charging)
    samples = [
        TelemetrySample("2026-02-28T06:00:00", "SCT-1", 10.0, 90.0, 35.0, 12.0, 77.0, "riding"),
        TelemetrySample("2026-02-28T06:05:00", "SCT-1", 15.0, 95.0, 36.0, 12.0, 77.0, "riding"),
    ]
    
    anomalies = detect_anomalies(samples)
    assert len(anomalies) == 1
    assert anomalies[0].rule == "soc increase while riding"
    assert anomalies[0].severity == "Medium"