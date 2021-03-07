import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix, accuracy_score

RS = 1

df = pd.read_csv("./diabetes.csv")
target = df[["class"]].to_numpy().ravel()
data = df.drop(["class"], axis=1)
# normalized_data = data
normalized_data = normalize(data, axis=0)
train_inputs, test_inputs, train_classes, test_classes = train_test_split(normalized_data, target, train_size=0.67, random_state=RS)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(8,5,3), max_iter=200, random_state=RS)

model = clf.fit(train_inputs, train_classes)
test_results = model.predict(test_inputs)
score = accuracy_score(test_classes, test_results)
c = confusion_matrix(test_classes, test_results)
print(score)
print(c)
