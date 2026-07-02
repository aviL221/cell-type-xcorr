# Project: Spike Train Analysis

## What this code does
[Fill in after reading analysis.py — one paragraph in your own words]
This code analyzes spike timeseries data. 
Computes firing rates for small bins of the total time series.
Computes ISIs for a list of spike times.
Computes the mean ISI for a list of spike times.
Gives a smooth version of the signal.
Makes a plot summary.
Computes population stats for the case of multiple neurons.


## Known issues
[Fill in during diagnosis phase — numbered list]
1. incorrect import in test_analysis.py
2. 

## Conventions to enforce
- Spike times: milliseconds (ms)
- Firing rates: Hz
- All output goes to results/
- Use numpy throughout; no pandas
- Run with pytest, not `python test_analysis.py`

## Progress
- [ ] generate_data.py runs successfully
- [ ] analysis.py runs without crashing
- [ ] Firing rates look correct (~5–40 Hz expected range)
- [ ] ISI CVs are reasonable (0.2–1.5 expected range)
- [ ] All test assertions are correct (not just passing)
- [ ] Tests run via pytest

## Decisions made
[Fill in as you go — e.g. "Fixed firing rate unit bug by dividing by bin_size / 1000.0", "Chose not to fix X because..."]
