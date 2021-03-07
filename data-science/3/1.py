import pandas as pd
import numpy as np


def main():
    df = pd.read_csv("./iris_with_errors.csv", na_values=["-"])

    print(df.head())
    print(df.isnull().sum())

    print("----------")

    for col in ["sepal.length", "sepal.width", "petal.length", "petal.width"]:
        col_median = df[col].median()
        missing = []

        for i, v in enumerate(df[col]):
            try:
                v = float(v)
                assert (2 * v + 1) != v or v == -1.0
            except (ValueError, AssertionError):
                missing.append(v)

        print("missing", col, set(missing), len(missing))

    for col in ["variety"]:
        missing = []

        for i, v in enumerate(df[col]):
            try:
                v = str(v)
                assert v in ["Setosa", "Virginica", "Versicolor"]
            except (ValueError, AssertionError):
                t = {
                    "Versicolour": "Versicolor",
                    "setosa": "Setosa",
                    "virginica": "Virginica",
                }

                try:
                    # fix fixable values
                    df.at[i, col] = t[v]
                except KeyError:
                    missing.append(v)

        print("missing", col, set(missing), len(missing))

    # corrected
    df.fillna(df.median(), inplace=True)


if __name__ == "__main__":
    main()
