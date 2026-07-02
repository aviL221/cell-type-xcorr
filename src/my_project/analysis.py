import numpy as np
import pandas as pd
import itertools
from scipy.io import loadmat
>>>>>>>

def compute_correlations(norm_vals):
    """
    Computes correlations for the given norm_vals array.
    """
    
    n_pages = norm_vals.shape[2]
    corrs = np.zeros((norm_vals.shape[0], norm_vals.shape[0], n_pages))
    for i in range(n_pages):
        corrs[:, :, i] = np.corrcoef(norm_vals[:, :, i])
    return corrs

def process_data(norm_vals, corrs):
    # Make condition index array
    conds = np.array([0, 2, 4, 8])
    cond_idx = np.tile(conds, 20)
    
    # Make animal index array
    worms = np.arange(1, 21)
    animal_idx = np.repeat(worms, 4)
    
    # Cull
    # conds = conds(conds~=8);
    # worms = worms(worms>5);
    # inds = cond_idx~=8 & animal_idx>5;
    
    inds = (cond_idx != 8) & (animal_idx > 5)
    
    norm_vals_culled = norm_vals[:, :, inds]
    corrs_culled = corrs[:, :, inds]
    cond_idx_culled = cond_idx[inds]
    animal_idx_culled = animal_idx[inds]
    
    return norm_vals_culled, corrs_culled, cond_idx_culled, animal_idx_culled

def compute_diff_trils(corrs):
    diff_trils = []
    for i in range(corrs.shape[2]):
        tmp = np.tril(corrs[:, :, i], -1)
        tmp[tmp == 0] = np.nan
        # Flatten and append
        diff_trils.append(tmp.flatten())
    
    # Stack along the second dimension (columns)
    return np.column_stack(diff_trils)

def process_neurontable(mat_file_path):
    data = loadmat(mat_file_path)
    # Assuming the mat file contains a struct array 'neurontable'
    # This is a common way to convert MATLAB structs to pandas DataFrames
    neurontable_struct = data['neurontable']
    
    # Extract field names
    field_names = neurontable_struct.dtype.names
    
    # Create a dictionary of lists
    data_dict = {name: neurontable_struct[name].flatten() for name in field_names}
    
    # Create DataFrame
    neurontable = pd.DataFrame(data_dict)
    
    return neurontable

def compute_individual_corrs(corr_tbl, norm_vals):
    """
    Computes individual correlations by row.
    """
    indiv_corr = np.full(len(corr_tbl), np.nan)
    
    for i in range(len(corr_tbl)):
        idx1 = int(corr_tbl.iloc[i]['IDX1']) - 1 # Assuming 1-based indexing in MATLAB
        idx2 = int(corr_tbl.iloc[i]['IDX2']) - 1
        page = int(corr_tbl.iloc[i]['PageNumber']) - 1
        
        # Extract the data
        data1 = norm_vals[idx1, :, page]
        data2 = norm_vals[idx2, :, page]
        
        # Compute correlation
        # 'rows', 'complete' in MATLAB means ignoring NaNs
        mask = ~np.isnan(data1) & ~np.isnan(data2)
        if np.sum(mask) > 1:
            indiv_corr[i] = np.corrcoef(data1[mask], data2[mask])[0, 1]
            
    return indiv_corr

def getPairTableIdx(all_traces,neur_table):
    # neur_table is expected to be a pandas DataFrame
    # out = nchoosek(1:size(Tbl,1),2)
    n = len(neur_table)
    out = np.array(list(itertools.combinations(range(n), 2)))
    
    
    
    # PageNums = (j-1)*4+1:j*4
    PageNums = np.arange((j - 1) * 4 + 1, j * 4 + 1)
    
    num_out = len(out)
    # Create all combinations of (out_idx, ic_idx)
    # out_indices is 0 to len(out)-1
    # ic_indices is 0 to 3
    out_indices = np.repeat(np.arange(num_out), 4)
    ic_indices = np.tile(np.arange(4), num_out)
    
    NeuronNames_G1 = neur_table['ID'].iloc[out[out_indices, 0]].values
    NeuronNames_G2 = neur_table['ID'].iloc[out[out_indices, 1]].values
    
    E = out[out_indices]
    
    # Dataframe = table2array(Tbl(:,3:6))
    # Assuming columns 3-6 are the data columns
    Dataframe = neur_table.iloc[:, 2:6].values
    
    T1 = Dataframe[E[:, 0], ic_indices]
    T2 = Dataframe[E[:, 1], ic_indices]
    
    PageNums_idx = np.tile(PageNums, num_out)
    
    corr_tbl2 = pd.DataFrame({
        'Animal': np.full(len(E), j),
        'name1': NeuronNames_G1,
        'name2': NeuronNames_G2,
        'IDX1': T1,
        'IDX2': T2,
        'condition': PageNums_idx,
    })
    
    return corr_tbl2
>>>>>>>
