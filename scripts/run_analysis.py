import * from my_project.analysis
#required data to import 
#   1. calcium traces for all neurons
#   2. mapping of each neuron to its group identities
#   3. mapping of each neuron to its trace
#combine all traces into one matrix
all_traces
#construct cross-correlation table from all calcium traces
all_corrs = compute_correlations(all_traces)
#build corrtable with each pair and both neuron's indices for cross-correlation table and indices for group identity