

import sklearn.neighbors
import scipy.special


import pygsp.filters
from graph_coarsening.coarsening_utils import *
import graph_coarsening.graph_utils
from mssi.utils import *

def ms_coars(st_data, batch_key = 'batch', spatial_key = 'spatial', n_scales = 5):
    
    cord = st_data.obsm[spatial_key]
    
    if(batch_key not in st_data.obs.columns):
            batch = np.zeros(cord.shape[0]).astype('int')
    else:
        batch = np.asarray(st_data.obs[batch_key])
            
    batch_coars_dict = {}
    batch_graph_dict = {}
    for val in np.unique(batch):
        cord_batch = cord[batch == val]
        
        AdjMat = sklearn.neighbors.kneighbors_graph(cord_batch, n_neighbors = 8, include_self = True)

        AdjMat.setdiag(0)
        AdjMat.eliminate_zeros()

        G = graphs.Graph(AdjMat + AdjMat.T)
        S = graph_coarsening.graph_utils.get_S(G).T
        
        batch_coars_ops = []
        batch_graph_obj = []
        for scale in range(n_scales):

            G.estimate_lmax()
            C, Gc, Call, Gall = coarsen(G, K = 10, r = 0.5, method='variation_neighborhood')
            batch_coars_ops.append(C)
            batch_graph_obj.append(G)
            G = Gc
        
        batch_coars_dict[val] = batch_coars_ops 
        batch_graph_dict[val] = batch_graph_obj 
    
    if(len(batch_coars_dict.values()) == 1):
        return(list(batch_coars_dict.values())[0], list(batch_graph_dict.values())[0])
    
    return(batch_coars_dict, batch_graph_dict)

def MSSI(self, true_df, predicted_df, coars_ops, batch = None):

    true_df = scale_max(true_df)
    predicted_df = scale_max(predicted_df)

    coeffs = [0.0448, 0.2856, 0.3001, 0.2363, 0.1333]

    if(batch is None):
        batch = np.zeros(shape = (raw.shape[0])).astype('int')
        coars_ops = {0: coars_ops}

    mssi = pd.DataFrame(np.zeros((1, predicted_df.shape[-1])), index = ['MSSI'], columns = predicted_df.columns)

    for val in np.unique(batch):
        
        true_batch_scale = [np.asarray(raw)[batch == val]]
        predicted_batch_scale = [np.asarray(impute)[batch == val]]

        mssi_batch = np.ones(impute.shape[-1])

        for ind, ops in enumerate(coars_ops[val]):
            for col_ind in range(true_batch[-1].shape[-1]):
                
                true_batch_col = true_batch[-1][:, col_ind]
                predicted_batch_col = predicted_batch[-1][:, col_ind]

                l_scale, c_scale, s_scale = cal_ssim(true_batch_col, 
                                                     predicted_batch_col, 
                                                     max(true_batch_col.max(), predicted_batch_col.max()))
                c_scale, s_scale = max(c_scale, 0), max(s_scale, 0)

                mssi_batch[col_ind] = mssi_batch[col_ind] * np.power(c_scale, coeffs[ind]) * np.power(s_scale, coeffs[ind])
                
                if(ind == len(coars_ops[val]) - 1):
                    mssi_batch[col_ind] = mssi_batch[col_ind] * l_scale

            true_batch_scale = coarsen_vector(true_batch_scale, ops)
            predicted_batch_scale = coarsen_vector(predicted_batch_scale, ops)


        mssi = mssi + mssi_batch * np.mean(batch == val)

    return ms_ssim
