import numpy as np
import os

np.random.seed(42)
os.makedirs("data", exist_ok=True)

neurons = {
    "01": {"rate": 20, "cv": 0.3},
    "02": {"rate": 5,  "cv": 1.0},
    "03": {"rate": 40, "cv": 0.2},
    "04": {"rate": 10, "cv": 1.5},
    "05": {"rate": 15, "cv": 0.8},
}

for nid, params in neurons.items():
    rate_hz = params["rate"]
    cv = params["cv"]
    duration_ms = 5000

    mean_isi = 1000 / rate_hz
    std_isi = cv * mean_isi

    if cv > 0:
        k = 1 / cv**2
        theta = mean_isi / k
        isis = np.random.gamma(k, theta, size=int(rate_hz * duration_ms / 1000 * 2))
    else:
        isis = np.ones(int(rate_hz * duration_ms / 1000 * 2)) * mean_isi

    spike_times = np.cumsum(isis)
    spike_times = spike_times[spike_times < duration_ms]

    np.save(f"data/neuron_{nid}.npy", spike_times)
    print(f"Neuron {nid}: {len(spike_times)} spikes, ~{rate_hz} Hz")

print("Data generation complete.")
