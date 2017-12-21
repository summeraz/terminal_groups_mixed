from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats
import seaborn as sns

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)

groups = ['amino', 'carboxyl', 'cyano', 'hydroxyl', 'nitro', 'nitrophenyl',
          'pyrrole']

variables = ['Avg. Molecular weight', 'Δ Molecular weight', 'Avg. Dipole moment',
             'Δ Dipole moment', 'COF', 'Intercept', 'Avg Nematic order',
             'Δ Nematic order', 'Diff S2', 'Avg Tilt angle', 'Δ Tilt angle',
             'Diff Tilt', 'Interdigitation', 'Δ Interdigitation',
             'Interaction energy', 'Δ Interaction energy', 'Interaction energy QQ',
             'Δ Interaction energy QQ', 'Interaction energy LJ',
             'Δ Interaction energy LJ']

data = [[] for _ in variables]

for job in project.find_jobs():
    for i, var in enumerate(variables):
        if var == 'COF':
            val = job.document['COF']
        elif var == 'Intercept':
            val = job.document['intercept']
        elif var == 'Avg. Molecular weight':
            val = job.document['avg_molecular_weight']
        elif var == 'Avg. Dipole moment':
            val = job.document['avg_dipole_moment']
        elif var == 'Δ Molecular weight':
            val = job.document['delta_molecular_weight']
        elif var == 'Δ Dipole moment':
            val = job.document['delta_dipole_moment']
        elif var == 'Avg Nematic order':
            val = (job.document['S2_top']['15nN'] + job.document['S2_bottom']['15nN']) / 2
        elif var == 'Δ Nematic order':
            avg_high = (job.document['S2_top']['25nN'] + job.document['S2_bottom']['25nN']) / 2
            avg_low = (job.document['S2_top']['5nN'] + job.document['S2_bottom']['5nN']) / 2
            val = avg_high - avg_low
        elif var == 'Diff S2':
            max_val = max(job.document['S2_top']['15nN'], job.document['S2_bottom']['15nN'])
            min_val = min(job.document['S2_top']['15nN'], job.document['S2_bottom']['15nN'])
            val = max_val - min_val
        elif var == 'Avg Tilt angle':
            val = (job.document['tilt_top']['15nN'] + job.document['tilt_bottom']['15nN']) / 2
        elif var == 'Δ Tilt angle':
            avg_high = (job.document['tilt_top']['25nN'] + job.document['tilt_bottom']['25nN']) / 2
            avg_low = (job.document['tilt_top']['5nN'] + job.document['tilt_bottom']['5nN']) / 2
            val = avg_high - avg_low
        elif var == 'Diff Tilt':
            max_val = max(job.document['tilt_top']['15nN'], job.document['tilt_bottom']['15nN'])
            min_val = min(job.document['tilt_top']['15nN'], job.document['tilt_bottom']['15nN'])
            val = max_val - min_val
        elif var == 'Interdigitation':
            val = job.document['interdigitation']['15nN']
        elif var == 'Δ Interdigitation':
            val = job.document['interdigitation']['25nN'] - job.document['interdigitation']['5nN']
        elif var == 'Interaction energy':
            val = job.document['shear_15nN-Etotal'][0]
        elif var == 'Δ Interaction energy':
            val = job.document['shear_25nN-Etotal'][0] - job.document['shear_5nN-Etotal'][0]
        elif var == 'Interaction energy QQ':
            val = job.document['shear_15nN-qq'][0]
        elif var == 'Δ Interaction energy QQ':
            val = job.document['shear_25nN-qq'][0] - job.document['shear_5nN-qq'][0]
        elif var == 'Interaction energy LJ':
            val = job.document['shear_15nN-lj'][0]
        elif var == 'Δ Interaction energy LJ':
            val = job.document['shear_25nN-lj'][0] - job.document['shear_5nN-lj'][0]
        tg1 = job.sp['terminal_groups'][0]
        tg2 = job.sp['terminal_groups'][1]
        polar = [tg for tg in [tg1, tg2] if tg in groups]
        if len(polar) == 1:
            data[i].append(val)

correlation_matrix = np.empty([len(variables), len(variables)])

for i, var1 in enumerate(variables):
    for j, var2 in enumerate(variables):
        slope, intercept, r_val, p_val, err = stats.linregress(data[i], data[j])
        correlation_matrix[i, j] = r_val

np.save('correlation-matrix-mixed', correlation_matrix)
