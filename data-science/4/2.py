import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

iris = load_iris()
train_inputs, test_inputs, train_classes, test_classes = train_test_split(iris.data, iris.target, train_size=0.7, random_state=1)

print("train data", train_inputs[:10], "...")
print("test data", test_inputs[:10], "...")

tree = DecisionTreeClassifier(random_state=1, max_depth=2)

tree = tree.fit(train_inputs, train_classes)

r = export_text(tree, feature_names=iris.feature_names)
plot_tree(tree, feature_names=iris.feature_names, class_names=iris.target_names)

test_results = tree.predict(test_inputs)
print("score", accuracy_score(test_classes, test_results))

c = confusion_matrix(test_classes, test_results)
class_to_name = dict(enumerate(iris.target_names))
print(c)
for i, t in enumerate(c):
    for j, v in enumerate(t):
        if i != j and v != 0:
            print(f"{v} {class_to_name[i]} missclassified as {class_to_name[j]}")

print(r)
# plt.show()
