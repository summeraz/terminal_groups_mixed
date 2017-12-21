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
for job in project:
    tg1 = job.sp['terminal_groups'][0]
    tg2 = job.sp['terminal_groups'][1]
    cof = job.document['COF']
    intercept = job.document['intercept']
    if cof < 0.1:
        print(tg1, tg2, cof, intercept)
    if tg1 == 'cyano' or tg2 == 'cyano':
        cyano_x.append(job.document['COF'])
        cyano_y.append(job.document['intercept'])
    else:
        all_x.append(job.document['COF'])
        all_y.append(job.document['intercept'])
ax.scatter(all_x, all_y, color='black', marker='o', s=75)
ax.scatter(cyano_x, cyano_y, color='red', marker='s', s=75)

plt.xlabel('COF')
ax.set_ylabel('Intercept, nN')
'''
plt.xlim([0.05, 0.2])
plt.ylim([0.0, 12.0])
'''
plt.tight_layout()
plt.savefig('cof-intercept-cyano.pdf')
