#masło;chleb;ser;piwo;czipsy
0;     1;    2;  3;   4
data = [
    [1,1,0,0,0],
    [0,1,1,0,0],
    [1,1,1,0,0],
    [0,0,0,1,1],
    [0,1,0,1,0],
    [0,1,0,1,1],
    [1,1,0,1,1],
    [0,1,0,1,1],
    [1,1,1,1,0],
    [1,1,0,1,1],
]

class Rule:
    def __init__(self, x_list, y_list):
        self.x_list = x_list
        self.y_list = y_list 

    def supports_rule(self, row):
        indices = self.x_list + self.y_list
        return all(row[i] for i in indices)

    def supports_x(self, row):
        return all(row[i] for i in self.x_list) 

    def support(self, data):
        return sum(map(self.supports_rule, data)) / len(data)

    def confidence(self, data):
        support_x = sum(map(self.supports_x, data)) / len(data)
        return self.support(data) / support_x

a2 = Rule([1], [3,4])
a3 = Rule([3], [4])
a4 = Rule([4], [3])
a5 = Rule([0, 2], [1])

rules = [(a2, "a2"), (a3, "a3"), (a4, "a4"), (a5, "a5")]

for r, name in rules:
    print(f"{name}: support - {r.support(data)}; confidence - {r.confidence(data)}")

print("my rule: {ser = FALSE} => {piwo = TRUE}")
support = sum(map(lambda r: (not r[2]) and r[3], data)) / len(data)
support_x = sum(map(lambda r: (not r[2]), data)) / len(data)
support_y = sum(map(lambda r: r[3], data)) / len(data)
confidence = support / support_x
lift = confidence / support_y
print("support", support, "confidence", confidence, "lift", lift)
