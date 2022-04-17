
"""
Names of data after different pathways:

data_valid - after removing NAN values 
data_kept - an array containing the data stored from the valid data, but reduced to the features we 
            desire to keep 
            
X_reduced-  after dimension reduction
X_clean - after quantile outlier reduction 
X_quant - after quantization (distinct from quantile elimination)

"""


import numpy as np
import pandas as pd
import os

from datatools import make_clean_data, select_features, \
    remove_quantiles, elbow_method, data_quantization, run_svd,\
    plot_clustering

"""
Set Parameters for Processing of Data 
"""

def run_elbow(data_set,Kmin= 5,Kmax =10,num_K = 2):
    k_search = np.linspace(start=Kmin, stop=Kmax, num= num_K,dtype = int)
    elbow_method(data_set,k_search, method = 'KMeans',plot = True)
    elbow_method(data_set, k_search, method = 'GM', plot = True)
    return None
    
if __name__ == "__main__":
    
    """
    1. Set parameters for this file run
    """

    dataset = 'basic'  #which dataset; options are 'basic', 'all', or 'freq'
    no_change = False  #Run clustering on cleaned (NaN-removed data). No touching the outliers. 
     
    #Choose only one of these; run clustering on quantized data, or outlier-removed data.
    do_quantize = False
    remove_outliers = not do_quantize
    
    #Apply SVD on the data (after quantizing / removing outliers)?
    reduce_dim = False
    
    """
    2. Read In Data
    """
    DATA_PATH = './raw_data/CreditCard_data.csv'

    if os.path.isfile(DATA_PATH):
        print('DATA_PATH is a valid path')
    else:
        raise ValueError('DATA_PATH is not valid path')

    #SAMPLE_SIZE = 10000
    data_raw = pd.read_csv(DATA_PATH)
    
    """
    3. Remove bad data values (NaN) and reduce only to valid dataset
    """
    data_valid, _, _ = make_clean_data(data_raw, verbose=False)
    data_kept, _, _ = select_features(data_valid, which= dataset)
    X = data_kept.values.astype(np.float64) # numpy array ready to be clustered

    """
    4. Elbow Method on Selected Features; Data Otherwise Not Modified 
    """
    
    if no_change:
        
        run_elbow(X)

        """
        5.
            (i)   Remove Outliers or to Quantize All Data; 
            (ii)  Choose Whether To Dimension Reduce; 
            (iii) Run Elbow Method on Resulting Data 
        """

    elif remove_outliers == True:
        
        p = 1 # percent of upper and lower population to be removed
        data_clean, _ = remove_quantiles(data_kept, p)
        assert np.size(data_clean.isna().sum(axis=1).to_numpy().nonzero()[0]) == 0,  "Data still contains NaN"
        X_clean = data_clean.values.astype(np.float64)
        
        if reduce_dim == True: 
            
            #Run SVD and reduce to components which explain at least 99% variance 
            
            desired_var_per = 99
            X_red = run_svd(X_clean, percent_var = desired_var_per)
            
            run_elbow(X_red)
            
        else:
            
            run_elbow(X_clean)
                      
    elif do_quantize:
        """
        Quantize Data- Convert each feature into integer based on membership in the population quantile 
        """
        
        data_quant, percent_zero = data_quantization(data_kept)
        print('Features have at least the following percentage of being zero:\n', percent_zero)
        X_quant = data_quant.values.astype(np.float64)
        
        if reduce_dim == True:
            desired_var_per = 99
            X_red = run_svd(X_quant,percent_var = desired_var_per)
            run_elbow(X_red)
        
        elif reduce_dim == False:
            run_elbow(X_quant)
