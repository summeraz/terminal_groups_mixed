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

groups = ['amino', 'carboxyl', 'cyano', 'hydroxyl', 'nitro', 'nitrophenyl',
          'pyrrole']

fig = plt.figure(1)
ax = plt.subplot(111)

nonpolar_x = []
nonpolar_y = []
polar_x = []
polar_y = []
mixed_x = []
mixed_y = []
for job in project:
    tg1 = job.sp['terminal_groups'][0]
    tg2 = job.sp['terminal_groups'][1]
    polar = [tg for tg in [tg1, tg2] if tg in groups]
    if len(polar) == 0:
        nonpolar_x.append(job.document['COF'])
        nonpolar_y.append(job.document['intercept'])
    elif len(polar) == 1:
        mixed_x.append(job.document['COF'])
        mixed_y.append(job.document['intercept'])
    elif len(polar) == 2:
        polar_x.append(job.document['COF'])
        polar_y.append(job.document['intercept'])
ax.scatter(nonpolar_x, nonpolar_y, color='black', marker='o', s=75)
ax.scatter(mixed_x, mixed_y, color='red', marker='s', s=75)
ax.scatter(polar_x, polar_y, color='cyan', marker='^', s=75)

plt.xlabel('COF')
ax.set_ylabel('Intercept, nN')
'''
plt.xlim([0.05, 0.2])
plt.ylim([0.0, 12.0])
'''
plt.tight_layout()
plt.savefig('cof-intercept.pdf')
