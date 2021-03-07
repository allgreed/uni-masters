import pandas as pd
from pprint import pprint
from apyori import apriori
from collections import defaultdict

_data = pd.read_csv("titanic.csv")
data = _data.drop(_data.columns[0], 1)

print(data.head())

records = []
for i in range(len(data)):
    records.append([str(data.values[i,j]) for j in range(4)])

min_length = 2
association_rules = apriori(records, min_support=0.005, min_confidence=0.8, min_lift=0)
association_results = list(filter(lambda r: len(r[0]) >= 2, association_rules))

rules = []
for i in association_results:
    for rule in i[2]:
        rules.append([tuple(rule[0]), tuple(rule[1]), rule[2], rule[3]])

def compute_support(r):
    lst = r[0] + r[1]
    return sum(all(x in row for x in lst) for row in records) / len(records)

def filter_out(r):
    # if len(r[1]) != 1:
        # return False

    if abs(r[3] - 1) <= .25:
        return False
    
    return True

rules = sorted(filter(filter_out, rules), key=lambda t: t[3], reverse=True)
for r in rules:
    r.append(compute_support(r))

print("Females on the Crew", compute_support([("Female", "Crew"), ()]))
print("Children on the Crew", compute_support([("Child", "Crew"), ()]))


r = [(("Female",), ("Yes",)), (("Child",), ("Yes",))]
for _r in r:
    fys = compute_support([_r[0], _r[1]])
    fyc = fys / compute_support([_r[0], ()])
    fyl = fyc / compute_support([_r[1], ()])
    print(f"{', '.join(_r[0])} -> Yes", fys, fyc, fyl)

print("---------")
print(len(rules))
for x in rules:
    lhs, rhs, confidence, lift, support = x
    print(f"{'{'}{', '.join(lhs)} -> {', '.join(rhs)}{'}'}, lift: {lift:.2f}, confidence: {confidence * 100:.2f}%, support: {support * 100:.2f}%")
    
