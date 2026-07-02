import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import argparse

def load_spikes(filepath):

    data = np.load(filepath)
    return data.T if data.ndim > 1 else data

def compute_firing_rate(spike_times, bin_size=50, t_start=0, t_end=5000):

    bins = np.arange(t_start, t_end, bin_size)
    counts, edges = np.histogram(spike_times, bins=bins)
    rates = counts / bin_size
    bin_centers = edges[1:] + bin_size / 2

    return rates, bin_centers

def compute_isi(spike_times):

    if len(spike_times) < 2:
        return np.array([]), np.nan
    isis = np.diff(spike_times)
    cv = np.std(isis) / np.mean(isis)

    return isis, cv

def compute_mean_isi(spike_times):

    isis, _ = compute_isi(spike_times)
    return np.mean(isis)

def smooth_signal(signal, window=5):

    kernel = np.ones(window)
    return np.convolve(signal, kernel, mode='same')

def plot_summary(spike_times, neuron_id, output_dir="results"):

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    rates, bin_centers = compute_firing_rate(spike_times)
    smoothed = smooth_signal(rates)
    axes[0].plot(bin_centers, smoothed)
    axes[0].set_xlabel("Time (ms)")
    axes[0].set_ylabel("Firing rate (Hz)")
    axes[0].set_title(f"Neuron {neuron_id} firing rate")

    isis, cv = compute_isi(spike_times)
    axes[1].hist(isis, bins=30, color='steelblue')
    axes[1].set_xlabel("ISI (ms)")
    axes[1].set_ylabel("Count")
    cv_str = f"{cv:.2f}" if not np.isnan(cv) else "nan"
    axes[1].set_title(f"ISI distribution (CV={cv_str})")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"neuron_{neuron_id}_summary.png"))
    plt.close()

def compute_population_stats(all_spike_times):

    stats = []
    for neuron_id, spike_times in all_spike_times.items():
        rates, _ = compute_firing_rate(spike_times)
        isis, cv = compute_isi(spike_times)

        stats.append({
            "neuron_id": neuron_id,
            "mean_firing_rate_hz": np.mean(rates),
            "mean_isi_ms": compute_mean_isi(spike_times),
            "isi_cv": cv,
            "n_spikes": len(spike_times),
            "peak_firing_rate_hz": np.max(smooth_signal(rates)),
        })
    return stats

def run_population_analysis(data_dir, output_dir="results"):

    neuron_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".npy")])

    all_spike_times = {}
    for fname in neuron_files:
        neuron_id = fname.replace("neuron_", "").replace(".npy", "")
        spike_times = load_spikes(os.path.join(data_dir, fname))
        all_spike_times[neuron_id] = spike_times

    stats = compute_population_stats(all_spike_times)

    for neuron_id, spike_times in all_spike_times.items():
        plot_summary(spike_times, neuron_id, output_dir)

    if stats:
        with open(os.path.join(output_dir, "population_stats.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=stats[0].keys())
            writer.writeheader()
            writer.writerows(stats)

    print(f"Analyzed {len(stats)} neurons.")
    return stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spike train analysis pipeline")
    parser.add_argument("data_dir", nargs="?", default="data",
                        help="Directory containing .npy spike time files")
    args = parser.parse_args()
    run_population_analysis(args.data_dir)
