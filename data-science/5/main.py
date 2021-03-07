import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score


RS = 1

df = pd.read_csv("./diabetes.csv")
target = df[["class"]].to_numpy().ravel()
data = df.drop(["class"], axis=1)
train_inputs, test_inputs, train_classes, test_classes = train_test_split(data, target, train_size=0.67, random_state=RS)

classifiers = [
    ("tree", DecisionTreeClassifier(random_state=RS, max_depth=5)),
    ("naïve Bayes", GaussianNB()),
    ("k-NN 3", KNeighborsClassifier(n_neighbors=3)),
    ("k-NN 5", KNeighborsClassifier(n_neighbors=5)),
    ("k-NN 11", KNeighborsClassifier(n_neighbors=11)),
]

plot_data = []
for name, c in classifiers:
    test_results = c.fit(train_inputs, train_classes).predict(test_inputs)
    score = accuracy_score(test_classes, test_results)
    c = confusion_matrix(test_classes, test_results)
    _, fp, fn, __ = c.ravel()

    plot_data.append((name, score, fn))

    print("===============================")
    print(name)
    print("score:", score)
    print(c)

labels, scores, false_negatives = list(zip(*plot_data))
scores = [round(s * 100, 2) for s in scores]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, scores, width, label='Score')
rects2 = ax.bar(x + width/2, false_negatives, width, label='False negatives')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(loc='lower right')

def autolabel(rects, suffix=""):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}{}'.format(height, suffix),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rects1, "%")
autolabel(rects2)

fig.tight_layout()
plt.show()
