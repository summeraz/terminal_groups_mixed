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

all_x = []
all_y = []
for job in project:
    tg1 = job.sp['terminal_groups'][0]
    tg2 = job.sp['terminal_groups'][1]
    if tg1 in groups and tg2 in groups:
        all_x.append((job.document['tilt_top']['15nN'] + \
                      job.document['tilt_bottom']['15nN']) / 2)
        all_y.append(job.document['intercept'])
ax.scatter(all_x, all_y, color='black', marker='o', s=75)

plt.xlabel('Avg. Tilt Angle, degrees')
ax.set_ylabel('Intercept, nN')
'''
plt.xlim([0.05, 0.2])
plt.ylim([0.0, 12.0])
'''
plt.tight_layout()
plt.savefig('tilt-intercept-polar.pdf')
