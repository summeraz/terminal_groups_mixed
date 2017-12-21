from scipy import stats

def correlation(x, y):
    slope, intercept, r_val, p_val, err = stats.linregress(x, y)
    return r_val

def filtergraph():
