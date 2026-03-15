from models import TelemetrySample, Session


def _build_session(session_samples, state):
    return Session(
        vehicle_id=session_samples[0].vehicle_id,
        session_type=state,
        start_time=session_samples[0].timestamp,
        end_time=session_samples[-1].timestamp,
        sample_count=len(session_samples),
        start_soc=session_samples[0].soc,
        end_soc=session_samples[-1].soc,
        max_speed=max(s.speed_kmph for s in session_samples),
        max_temp=max(s.motor_temp_c for s in session_samples),
    )


def sessionize(samples):
    if len(samples) == 0:
        return []

    sessions = []
    curr_state = samples[0].state
    session_samples = [samples[0]]

    for i in range(1, len(samples)):
        if samples[i].state == curr_state:
            session_samples.append(samples[i])
        else:
            print(f"Session: {curr_state}, {len(session_samples)} samples")
            sessions.append(_build_session(session_samples, curr_state))
            curr_state = samples[i].state
            session_samples = [samples[i]]

    # Final session
    print(f"Session: {curr_state}, {len(session_samples)} samples")
    sessions.append(_build_session(session_samples, curr_state))

    return sessions


if __name__ == "__main__":
    from ingest import load_csv

    samples, errors = load_csv("data/sample_telemetry.csv")

    print("Samples loaded:", len(samples))
    print("Errors:", len(errors))

    vehicles = {}
    for s in samples:
        vid = s.vehicle_id
        if vid not in vehicles:
            vehicles[vid] = []
        vehicles[vid].append(s)

    vehicle_id = list(vehicles.keys())[0]
    vehicle_samples = vehicles[vehicle_id]

    print("Testing vehicle:", vehicle_id)

    vehicle_samples.sort(key=lambda x: x.timestamp)

    sessions = sessionize(vehicle_samples)

    print("Sessions created:", len(sessions))