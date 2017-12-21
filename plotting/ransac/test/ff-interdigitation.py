import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn import linear_model, datasets

fig = plt.figure(1)
ax = plt.subplot(111)

interdigitation = np.loadtxt('shear_25nN-interdigitation.txt')[::2][:,1]
friction = np.loadtxt('friction_25nN.txt')[:,1]

X = np.array([[val] for val in interdigitation])
lr = linear_model.LinearRegression()
lr.fit(X, friction)
_, _, r_all, _, _ = stats.linregress(interdigitation, friction)

ransac = linear_model.RANSACRegressor(random_state=92)
ransac.fit(X, friction)
inlier_mask = ransac.inlier_mask_
outlier_mask = np.logical_not(inlier_mask)

_, _, r_ransac, _, _ = stats.linregress(interdigitation[inlier_mask], friction[inlier_mask])

line_X = np.linspace(interdigitation.min(), interdigitation.max(), 10)[:, np.newaxis]
line_y = lr.predict(line_X)
line_y_ransac = ransac.predict(line_X)

print("Pearson correlations (Linear regression, RANSAC):")
print(r_all, r_ransac)

plt.scatter(X[inlier_mask], friction[inlier_mask], color='yellowgreen', marker='.',
    s=75)
plt.scatter(X[outlier_mask], friction[outlier_mask], color='red', marker='.', s=75)
plt.plot(line_X, line_y, color='navy', label='LR ({:.3f})'.format(r_all))
plt.plot(line_X, line_y_ransac, color='cornflowerblue', 
    label='RANSAC ({:.3f})'.format(r_ransac))

plt.xlabel('Interdigitation')
ax.set_ylabel('Friction')
plt.legend()
plt.tight_layout()
plt.savefig('friction-interdigitation.pdf')
