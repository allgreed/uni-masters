import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("./miasta.csv")
print(df)

newdf = df.append(dict(zip(df.columns, [2010,460,555,405])), ignore_index=True)
gda_people = newdf["Gdansk"]
years = newdf["Rok"]

plt.plot(years, gda_people, "-ro")
plt.xlabel("Lata")
plt.ylabel("Liczba ludności [w tys.]")
plt.title("Ludnosc w miastach Polski")
plt.show()

colors = ["r", "g", "b"]

for index, c in enumerate(df.columns[1:]):
    plt.plot(years, newdf[c], f"-{colors[index]}o", label=c)
plt.xlabel("Lata")
plt.ylabel("Liczba ludności [w tys.]")
plt.title("Ludnosc w miastach Polski")
plt.legend()
plt.show()
