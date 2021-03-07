import pandas as pd


def main():
    df = pd.read_csv("./iris.csv", na_values=["-"])
    myPredict(df, myPredictRow)
    

def myPredictRow(sl, sw, pl, pw):
    if sl < 5.5:
        return "setosa"
    else:
        if pl < 3.4:
            return "versicolor"
        else:
            return "virginica"


def myPredict(df, predictor):
    total = len(df)
    correct = sum(row.species == predictor(row.sepal_length, row.sepal_width, row.petal_length, row.petal_width) for _, row in df.iterrows())

    print(correct / total * 100, "%")
    
if __name__ == "__main__":
    main()
