from functools import partial
from pprint import pprint
from typing import Dict
from collections import Counter

import chess
import torch
from torch import nn
from torch.nn import functional as F
from torch import optim
from torch.utils import data as data_utils
import numpy as np
import pandas as pd


np.random.seed(2)
RS = 2


def main():
    raw_data = pd.read_csv("2k_annotated.csv", sep=";")
    # raw_data = pd.read_csv("everything_annotated.csv", sep=";")
    print(raw_data.head())
    avg = raw_data["is_best"].sum() / raw_data["is_best"].size
    print("is_best avg: ", avg)


    # TODO: add cache for all
    data = raw_data.apply(process_row, index=[""], axis=1)

    print(data.head())

    
    data_target = torch.tensor(data['is_best'].values.astype(np.int64))
    data_inputs = torch.tensor(data.drop('is_best', axis = 1).values.astype(np.float32)) 
    dataset = data_utils.TensorDataset(data_inputs, data_target) 

    train, test = train_val_dataset(dataset, test_size=((80 - 2) / 80))

    BS = 1000

    labels = np.array(list(map(lambda i: dataset[i][1].item(), train.indices)))
    labels = labels.astype(int)

    c = Counter(labels.tolist())
    majority_class_count, minority_class_count = c[1], c[0]

    majority_weight = 1/majority_class_count
    minority_weight = 1/minority_class_count
    sample_weights = np.array([minority_weight, majority_weight])
    weights = sample_weights[labels]
    sampler = data_utils.WeightedRandomSampler(weights=weights, num_samples=len(train), replacement=True)

    train_loader = data_utils.DataLoader(dataset=train, batch_size=BS, sampler=sampler)
    test_loader = data_utils.DataLoader(dataset=test, batch_size=BS, shuffle=False)

    net = Network()
    # print(net)

    optimiser = optim.Adam(net.parameters(), lr=5e-3)

    # there's a great tutorial by sentdex on YT
    EPOCHS = 100

    for epoch in range(EPOCHS):
        for data in train_loader:
            X, y = data
            bs = len(X)
            net.zero_grad()
            output = net(X)

            loss = F.nll_loss(output, y)
            loss.backward()
            optimiser.step()
        print("epoch", epoch, loss)

    with torch.no_grad():
        evaluate(net, train_loader, avg)
        evaluate(net, test_loader, avg)

class Network(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.fc1 = nn.Linear(64, 64)
        self.autoencoder_in = nn.Linear(64, 256)
        self.autoencoder_out = nn.Linear(256, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 16)
        self.output = nn.Linear(16, 2)

    def forward(self, x):
        f = [
            self.fc1,
            F.relu,
            self.autoencoder_in,
            self.autoencoder_out,
            F.relu,
            self.fc2,
            F.relu,
            self.fc3,
            F.relu,
            self.fc4,
            F.relu,
            self.output,
            partial(F.log_softmax, dim=1),
        ]

        for func in f:
            x = func(x)

        return x


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


def normalize_piece_encoding(x):
    # TODO: dehardcode?
    return (x + 9.5 ) / 19

def make_board_array(fen, is_white) -> Dict:
    board = chess.Board(fen)

    _x = map(lambda s: piece_to_number(board.piece_at(s), is_white), chess.SQUARES)
    x = map(normalize_piece_encoding, _x)
    return list(x)


# https://discuss.pytorch.org/t/how-to-split-dataset-into-test-and-validation-sets/33987/5
def train_val_dataset(dataset, test_size=0.25):
    train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=test_size)
    train = data_utils.Subset(dataset, train_idx)
    test = data_utils.Subset(dataset, val_idx)
    return (train, test)

def evaluate(net, loader, avg):
    correct, total, positive, fp, fn = 0, 0, 0, 0, 0 

    for data in loader:
        X, y = data
        output = net(X)

        for tx, ty in zip(output, y):
            value = torch.argmax(tx)
            target = ty.item()
            prediction = value

            if prediction == target:
                correct += 1
            else:
                if target:
                    fn += 1
                else:
                    fp += 1

            if prediction:
                positive += 1
            total += 1

    acc = correct / total
    distribution = positive / total
    avg_diff_accuracy = 1 - abs(distribution - avg * 1)
    print("acc:", correct / total)
    print("distribution:", positive / total)
    print("avg_diff accuracy:", avg_diff_accuracy)
    print("total", avg_diff_accuracy * acc)
    print(f"fp {fp} ({fp / total * 100:.2f}%), fn {fn} ({fn / total * 100:.2f}%)")
    print("----")

if __name__ == "__main__":
    main()

# TODO:
# encoding and fragments inspired by: https://towardsdatascience.com/creating-a-chess-ai-using-deep-learning-d5278ea7dcf
