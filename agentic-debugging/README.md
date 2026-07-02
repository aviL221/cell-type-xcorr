# Spike Train Analysis — Agentic Code Rescue
**NRT Data Analysis Boot Camp · July 1, 2026**

---

## What this code does

This is a Python pipeline for analyzing extracellular neural recordings from 5 simulated neurons. Given spike times (the times at which each neuron fired an action potential), the code computes:

- **Firing rates** — how often each neuron fires, in Hz, using histograms
- **Inter-spike intervals (ISIs)** — the time between consecutive spikes, and their coefficient of variation (CV), which measures how regular or irregular the firing pattern is

It then plots these summaries and saves them to a `results/` directory.

The code has bugs. Finding and fixing them is the point.

---

## Setup

**1. Install dependencies**
```bash
pip install numpy matplotlib pytest
```

**2. Generate synthetic spike data (do this first)**
```bash
python generate_data.py
```

This creates `data/`, containing one `.npy` file per neuron. **You must run this before `analysis.py`** — the analysis script reads these files and will crash if they don't exist.

**3. Run the analysis**
```bash
python analysis.py
```

If everything is working, this writes plots and a summary CSV to `results/`. If it crashes, that's a bug (or there are several).

**4. Run the tests**
```bash
pytest tests/
```

Note: `python tests/test_analysis.py` will appear to succeed even if the tests are broken. Always use `pytest`.

---

## Today's session

### Step 1: Read before you touch anything

Open `analysis.py` and `tests/test_analysis.py` and read through them manually. Don't run anything yet, don't ask the agent yet. Write down your initial impressions:

- What does each function do?
- Does anything look suspicious?
- What would you expect the output to look like?

Open `agent.md` — it's already in the project. Fill in "What this code does" in your own words.

### Step 2: Agent-assisted audit

Open Cline in this directory. Give the agent a task like:

> "Read `analysis.py` and `tests/test_analysis.py` carefully. List every bug, code quality issue, and potential scientific error you can find. Do not fix anything yet. Write your findings in agent.md under 'Known issues'."

Do not accept any edits during this phase — diagnosis only.

Read the agent's output critically. Compare it to your own notes. The agent may find things you missed; it will also miss things you noticed.

### Step 3: Fix iteratively

Fix one bug at a time. After each fix:

1. **Before accepting the agent's change:** review every line of the diff. In Cline, click the diff view on any proposed edit before accepting it. Or run `git diff` in the terminal after accepting. Either way — you are responsible for what goes into the codebase.
2. Accept or reject the change, then run `python analysis.py`
3. Run `pytest tests/`
4. Look at the output numbers — do they make sense?
5. Commit: `git add -A && git commit -m "fix: [what you fixed]"`
6. Update agent.md under "Decisions made"

**Good order to fix in:** Start with crashes (things that raise exceptions), then move to silent wrong output (things that run but produce incorrect results), then scientific precision issues.

### Step 4: Fix the tests

Run `pytest tests/` and look at the test assertions. Ask yourself: are these tests correct, or are some of them passing because of bugs?

The tests were written at the same time as the bugs. Some of them are lying. Find the ones that pass for the wrong reason and fix the assertions.

### Step 5: Partner swap

Swap your `agent.md` with a partner. Read theirs and ask: if I picked this up tomorrow with no other context, could I understand what they did and why?

---

## Minimum deliverable

If you're running short on time, aim for this:

- [ ] Fix the firing rate calculation so reported rates are in the correct range (~5–40 Hz)
- [ ] Fix the corresponding test assertion to match the correct value
- [ ] Write one new test that would have caught a bug that was previously silent

Everything beyond this is a bonus.

---

## What correct output looks like

When the bugs are fixed, running `analysis.py` should produce a `results/` directory with:

- Firing rate plots — rates should be roughly **5–40 Hz** per neuron
- ISI histograms — CVs should be roughly **0.2–1.5** (0 = perfectly regular, >1 = bursty)
- `population_stats.csv` — a table with one row per neuron

If your firing rates are in the range of 0.001–0.04 Hz, there is still a unit conversion bug. If your smoothed signals look 5x larger than the raw values, there is still a normalization bug.

---

## Things to keep in mind

**Read every diff.** When the agent proposes a change, read it before you accept it. You are responsible for what goes into the codebase.

**Running ≠ correct.** `analysis.py` can run without errors and still produce numbers that are 1000x off. Always sanity-check the output values against what you'd expect biologically.

**Tests passing ≠ correct.** Some tests in this repo pass because of bugs, not despite them. A passing test suite is evidence, not proof.

**Commit before you change anything.** `git init && git add . && git commit -m "initial state"` gives you an undo button.

---

## Where to get help

- Your agent.md — write it well and it'll help you
- Your partner — explain the bug out loud; this often surfaces the fix
- Your instructor — especially for scientific/domain questions the agent can't answer
- The agent — for code mechanics, not for deciding whether the numbers make biological sense
