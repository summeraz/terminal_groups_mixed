import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#plt.rcParams["font.weight"] = "bold"
sns.set(font_scale=2)

variables = ['Avg. Molecular weight', 'Δ Molecular weight', 'Avg. Dipole moment',
             'Δ Dipole moment', 'COF', 'Intercept', 'Avg Nematic order',
             'Δ Nematic order', 'Diff S2', 'Avg Tilt angle', 'Δ Tilt angle',
             'Diff Tilt', 'Interdigitation', 'Δ Interdigitation',
             'Interaction energy', 'Δ Interaction energy', 'Interaction energy QQ',
             'Δ Interaction energy QQ', 'Interaction energy LJ',
             'Δ Interaction energy LJ']
correlation_matrix = np.load('correlation-matrix-ransac.npy')

fig, ax = plt.subplots(figsize=(18,18))
ax = sns.heatmap(correlation_matrix, xticklabels=variables, yticklabels=variables,
                 annot=True, cmap='coolwarm', vmin=-1.0, vmax=1.0, center=0.0,
                 square=True, annot_kws={'size': 11, 'weight': 'semibold'},
                 cbar_kws={'ticks': [-1, -0.5, 0, 0.5, 1], 'shrink': 0.74})
ax.tick_params(labelsize=16)
plt.xticks(rotation=-45, ha='left')
plt.tight_layout()
plt.savefig('correlation-heatmap-ransac.pdf')
