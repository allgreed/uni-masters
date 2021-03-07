import matplotlib.pyplot as plt
import numpy as np


DATA = [('TRUE*', 68.21, 68.21, 46.51), ('random*', 46.51, 100, 46.51)] +\
[('tree', 60.16666666666667, 32.114999999999995, 19.322525), ('naïve\n Bayes', 58.5, 32.114999999999995, 18.787274999999998), ('k-NN 3', 60.5, 32.114999999999995, 19.429574999999996), ('k-NN 5', 63.5, 32.114999999999995, 20.393024999999998), ('k-NN 11', 66.0, 32.114999999999995, 21.195899999999998), ('k-NN 21', 67.66666666666666, 32.114999999999995, 21.731149999999992)]

# * theoretical computations

labels, scores, distribution_diff_accuracies, overall_scores = list(zip(*DATA))
scores = [round(s, 2) for s in scores]
distribution_diff_accuracies = [round(s, 2) for s in distribution_diff_accuracies]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, scores, width, label='Score')
rects2 = ax.bar(x + width/2, distribution_diff_accuracies, width, label='Distribution diff accuracy')
ax.plot(overall_scores, "Dm", markersize=10, label="Overall")
ax.hlines(46, -1, len(DATA), "k", label="Benchmark")

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
autolabel(rects2, "%")

fig.tight_layout()
plt.show()
