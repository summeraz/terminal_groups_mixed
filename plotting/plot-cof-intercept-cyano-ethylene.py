import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import signac
from scipy import stats

project = signac.get_project()
df_index = pd.DataFrame(project.index())
df_index = df_index.set_index(['_id'])
statepoints = {doc['_id']: doc['statepoint'] for doc in project.index()}
df = pd.DataFrame(statepoints).T.join(df_index)

fig = plt.figure(1)
ax = plt.subplot(111)

all_x = []
all_y = []
cyano_x = []
cyano_y = []
ethylene_x = []
ethylene_y = []
both_x = []
both_y = []
for job in project:
    tg1 = job.sp['terminal_groups'][0]
    tg2 = job.sp['terminal_groups'][1]
    cyano_count = [tg for tg in [tg1, tg2] if tg == 'cyano']
    ethylene_count = [tg for tg in [tg1, tg2] if tg == 'ethylene']
    cof = job.document['COF']
    intercept = job.document['intercept']
    if len(cyano_count) == 1 and len(ethylene_count) == 1:
        both_x.append(job.document['COF'])
        both_y.append(job.document['intercept'])
    elif len(cyano_count) == 1:
        cyano_x.append(job.document['COF'])
        cyano_y.append(job.document['intercept'])
        print(tg1, tg2, cof, intercept)
    elif len(ethylene_count) == 1:
        ethylene_x.append(job.document['COF'])
        ethylene_y.append(job.document['intercept'])
        print(tg1, tg2, cof, intercept)
    else:
        all_x.append(job.document['COF'])
        all_y.append(job.document['intercept'])
ax.scatter(all_x, all_y, color='black', marker='o', s=75)
ax.scatter(cyano_x, cyano_y, color='red', marker='s', s=75)
ax.scatter(ethylene_x, ethylene_y, color='blue', marker='^', s=75)
ax.scatter(both_x, both_y, color='gold', marker='*', s=75)

plt.xlabel('COF')
ax.set_ylabel('Intercept, nN')
'''
plt.xlim([0.05, 0.2])
plt.ylim([0.0, 12.0])
'''
plt.tight_layout()
plt.savefig('cof-intercept-cyano-ethylene.pdf')
