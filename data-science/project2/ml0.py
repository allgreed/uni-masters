from typing import Dict

import chess
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.metrics import confusion_matrix, accuracy_score


def main():
    RS = 1

    raw_data = pd.read_csv("2k_annotated.csv", sep=";")
    # raw_data = pd.read_csv("everything_annotated.csv", sep=";")
    # TODO: add move number!
    print(raw_data.head())
    avg = raw_data["is_best"].sum() / raw_data["is_best"].size
    print("is_best avg: ", avg)

    processed_data = raw_data.apply(process_row, index=['foo', 'bar'], axis=1)

    print(processed_data.head())

    target = processed_data[["is_best"]].to_numpy().ravel()
    data = processed_data.drop(["is_best"], axis=1)

    train_inputs, test_inputs, train_classes, test_classes = train_test_split(data, target, train_size=0.7, random_state=RS)

    classifiers = [
        ("tree", DecisionTreeClassifier(random_state=RS)),
        ("naïve Bayes", GaussianNB()),
        ("k-NN 3", KNeighborsClassifier(n_neighbors=3)),
        ("k-NN 5", KNeighborsClassifier(n_neighbors=5)),
        # ("k-NN 11", KNeighborsClassifier(n_neighbors=11)),
        # ("k-NN 21", KNeighborsClassifier(n_neighbors=21)),
    ]

    plot_data = []

    for name, c in classifiers:
        test_results = c.fit(train_inputs, train_classes).predict(test_inputs)
        score = accuracy_score(test_classes, test_results) * 100
        c = confusion_matrix(test_classes, test_results)
        tp, fp, fn, _ = c.ravel()

        c_avg = (tp + fp) / sum(c.ravel())
        avg_diff_accuracy = 100 - abs(c_avg - avg * 100)
        overall_accuracy = score * avg_diff_accuracy / 100

        print("===============================")
        print(name)
        print("score:", score)
        print(c)
        print(f"fp: {fp}, fn: {fn}")
        print(tp + fp, sum(c.ravel()))
        print("avg diff accuracy = {:.2f}%".format(avg_diff_accuracy))
        print(f"TRUE ACCURACY = {overall_accuracy:.2f}%")

        plot_data.append((name, score, avg_diff_accuracy, overall_accuracy))

    print(plot_data)

BOARD_INDEX = chess.SQUARE_NAMES

# https://en.wikipedia.org/wiki/Chess_piece_relative_value#Alternative_valuations - using AlphaZero system
PIECE_TO_NUMBER = {
    'p' : 1,
    'n' : 3.05,
    'b' : 3.33,
    'r' : 5.63,
    'q' : 9.5,
    'k' : (3.05 + 3.33 / 2), # interpolating Gik's valuation, I have to put something here...
} 

def piece_to_number(piece, is_white):
    if piece is None:
        return 0

    symbol = piece.symbol()

    number = PIECE_TO_NUMBER[symbol.lower()]
    sing = -1 if symbol.islower() else 1
    white_sign = -1 if is_white else 1
    return sing * white_sign * number

def process_row(row, index):
    fen = row["fen"]
    is_best = row["is_best"]
    is_white = row["is_white"]

    return pd.Series([is_best] + make_board_array(fen, is_white), index=["is_best"] + BOARD_INDEX)

def make_board_array(fen, is_white) -> Dict:
    board = chess.Board(fen)

    # TODO: encode castling right + en passants + is there more info in FEN? o.0
    x =map(lambda s: piece_to_number(board.piece_at(s), is_white), chess.SQUARES)
        
    # TODO: unfuck this - there shouldn't be tons of conversions needed
    lst = normalize([list(x)])
    
    return list(lst[0])

if __name__ == "__main__":
    main()
