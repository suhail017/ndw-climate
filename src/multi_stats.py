
import numpy as np


def compute_eigvals_pvalues(dlam, slam):
    """
    Computes the p-value of each eigenvalue given the data eigenvalues and the surrogate eigenvalues 
    from slam.shape[0] surrogates.  It is required that dlam.shape[0] == slam.shape[1].
    """
    # compute each p-val
    Nsurr = slam.shape[0]
    p_vals = np.zeros_like(dlam, dtype = np.float64)
    
    for i in range(len(p_vals)):
        p_vals[i] = float(np.sum(dlam[i] <= slam[:,i])) / Nsurr
        
    return p_vals
        

def bonferroni_test(p_vals, sig_level, Nsurr):
    """
    Run a Bonferroni-corrected multiple hypothesis test.
    """
    Nhyp = len(p_vals)
    bonf_level = sig_level / Nhyp
    
    if bonf_level < 1.0 / Nsurr:
        raise "Will not run Bonferroni, not enough surrogates used for the test!"
    
    return p_vals < bonf_level


def fdr_test(p_vals, sig_level, Nsurr):
    """
    Run an FDR corrected multiple hypothesis test on the p-values, given the number
    of surrogates generated (to upper-bound the p-values of components where 
    lambda(i) > slambda(j,i) for all j.)
    """
    Nhyp = len(p_vals)
    sndx = np.argsort(p_vals)
    
    bonf_level = sig_level / Nhyp
    
    if bonf_level < 1.0 / Nsurr:
        raise "Will not run FDR, not enough surrogates used for the test!"
    
    h = np.zeros((Nhyp,), dtype = np.bool)
    
    # test the p-values in order of p-values (smallest first)
    for i in range(Nhyp):
        
        # select the hypothesis with the i-th lowest p-value
        hndx = sndx[i]
        
        # check if we have violated the FDR condition
        if p_vals[hndx] > (i+1)*bonf_level:
            break
        
        # the hypothesis is true
        h[hndx] = True
            
    return h


def sidak_test(p_vals, sig_level, Nsurr):
    """
    Run an FDR-corrected multiple hypothesis test on the p-values, given the number
    of surrogates generated (to upper-bound the p-values of components where 
    lambda(i) > slambda(j,i) for all j.)
    """
    Nhyp = len(p_vals)
    sndx = np.argsort(p_vals)
    
    bonf_level = sig_level / Nhyp
    
    if bonf_level < 1.0 / Nsurr:
        raise "Will not run Sidak test, not enough surrogates used for the test!"
    
    h = np.zeros((Nhyp,), dtype = np.bool)

    levels = (1 - (1 - sig_level)) ** (1.0 / np.arange(Nhyp, 0, -1))
    nz = np.nonzero(p_vals[sndx] < levels)[0]
    if nz.size > 0:
        last = nz[-1]
        h[sndx[:last+1]] = True
    
    return h


def holm_test(p_vals, sig_level, Nsurr):
    """
    Run a Holm multiple testing procedure on data.
    """
    Nhyp = len(p_vals)
    sndx = np.argsort(p_vals)
    
    bonf_level = sig_level / Nhyp
    
    if bonf_level < 1.0 / Nsurr:
        raise "Will not run Holm test, not enough surrogates used for the test!"

    h = np.zeros((Nhyp,), dtype = np.bool)

    # test the p-values in order of p-values (smallest first)
    for i in range(Nhyp):
        
        # select the hypothesis with the i-th lowest p-value
        hndx = sndx[i]
        
        # check if we have violated the FDR condition
        if p_vals[hndx] > sig_level / (Nhyp - i):
            break
        
        # the hypothesis is true
        h[hndx] = True
            
    return h



