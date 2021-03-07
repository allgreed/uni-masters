import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

features = ['sepal length', 'sepal width', 'petal length', 'petal width']
data = pd.read_csv("./iris.csv", names=features + ['target'])
x = data.loc[:, features].values

# normalized
x = pd.DataFrame(StandardScaler().fit_transform(x), index=range(len(x)), columns=features, dtype="float64")
initial_variance = sum(x.var())

def pca(n):
    return pd.DataFrame(data=PCA(n_components=n).fit_transform(x))

final = None
columns = len(features)
for n in range(columns, 0, -1):
    df = pca(n)
    variance_loss = 1 - (sum(df.var()) / initial_variance)
    if variance_loss > 0.2:
        break
    final = n, df
    print(f"columns removed: {columns - n},  variance_loss: {round(variance_loss * 100, 2)}%")

n, df = final
print("\nmax columns removed at <20% variance loss =", n)

finalDf = pd.concat([df, data[['target']]], axis = 1)
print("\n", finalDf)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 0', fontsize = 12)
ax.set_ylabel('Principal Component 0', fontsize = 12)
targets = ['setosa', 'versicolor', 'virginica']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 0]
               , finalDf.loc[indicesToKeep, 1]
               , c = color
               , s = 50)
ax.legend(targets, loc="lower right")
ax.grid()

plt.show()
