import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from analysis import (
    compute_firing_rate, compute_isi, compute_mean_isi, smooth_signal
)

def test_firing_rate_basic():

    spike_times = np.linspace(50, 950, 10)
    rates, centers = compute_firing_rate(spike_times, bin_size=100, t_start=0, t_end=1000)
    assert np.allclose(rates, 0.01), f"Expected 0.01, got {rates}"

def test_firing_rate_bins():
    spike_times = np.array([100., 200., 300.])
    rates, centers = compute_firing_rate(spike_times, bin_size=100, t_start=0, t_end=500)
    assert len(rates) == len(centers)

def test_isi_regular():

    spike_times = np.arange(0, 1000, 50).astype(float)
    isis, cv = compute_isi(spike_times)
    assert cv < 0.01, f"CV too high: {cv}"

def test_isi_unsorted():
    spike_times = np.array([300., 100., 200., 500., 400.])
    isis, cv = compute_isi(spike_times)
    assert cv > 0

def test_isi_single_spike():
    isis, cv = compute_isi(np.array([100.0]))
    assert len(isis) == 0
    assert np.isnan(cv)

def test_smooth_signal():
    signal = np.ones(10)
    smoothed = smooth_signal(signal, window=5)
    assert smoothed[5] == 5.0, f"Expected 5.0, got {smoothed[5]}"

def test_compute_mean_isi_empty():
    result = compute_mean_isi(np.array([100.0]))
    assert result != 0

print("All tests passed.")
