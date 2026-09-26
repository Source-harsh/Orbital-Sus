import time
from simulator import SpacecraftSimulator

def run_automated_demo():
    sim = SpacecraftSimulator(satellite_id="SAT-01")
    print("================================================================")
    print("   SPACECRAFT CYBER-PHYSICAL SIMULATOR & THREAT INJECTOR        ")
    print("================================================================")
    print("Streaming telemetry to backend at http://127.0.0.1:8000/api/telemetry...\n")

    # Sequence of scenarios to run automatically
    schedule = [
        ("NORMAL", 5),                      # Run NORMAL for 5 seconds
        ("CYBER_ATTACK", 8),                # Inject CYBER ATTACK for 8 seconds
        ("ENVIRONMENTAL_DISTURBANCE", 5),   # Inject SOLAR FLARE for 5 seconds
        ("HARDWARE_FAULT", 6),              # Inject HARDWARE FAULT for 6 seconds
        ("NORMAL", 5)                       # Return to NORMAL
    ]

    for scenario, duration in schedule:
        sim.inject_scenario(scenario)
        for _ in range(duration):
            payload = sim.step()
            sim.send_telemetry(payload)
            time.sleep(1)

    print("\n[SIMULATOR] Simulation run complete.")

if __name__ == "__main__":
    run_automated_demo()
