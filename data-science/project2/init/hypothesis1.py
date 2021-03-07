import chess.pgn
import numpy as np
from stockfish import Stockfish

# TODO: dehardcode this
stockfish = Stockfish("/nix/store/gfrsm7wdvrx1a8ck61zalbr35iiri6wp-stockfish-11/bin/stockfish", parameters={"Threads": 2, "MultiPV": 3}, depth=18)

def main():
    pgn = open("./g_kasparov_some_recent_games.pgn")
    games = []
    while True:
        maybe_game = chess.pgn.read_game(pgn)

        if not maybe_game:
            break

        games.append(maybe_game)

    # game_scores = list(map(compute_game_accuracy, games))
    # print(game_scores)

    game_scores = [(31, 22), (55, 35), (19, 12), (42, 28), (49, 36), (65, 38), (48, 33), (37, 22), (36, 18), (39, 29), (27, 13), (27, 12), (60, 46), (31, 22), (6, 4), (44, 22), (29, 19), (37, 24), (62, 35), (52, 35), (77, 53), (70, 30), (32, 25), (47, 24), (4, 2)]

    sensible_game_scores = (filter(lambda t: t[0] > 10, game_scores))
    percentages = list(map(lambda t: t[1] / t[0] * 100, sensible_game_scores))

    mean, std, median, _min, _max = np.mean(percentages), np.std(percentages), np.median(percentages), min(percentages), max(percentages)
    print(len(percentages), mean, std, median, _min, _max)

def compute_game_accuracy(game):
    board = game.board()
    x = game.headers["Black"] == "Kasparov, Garry"
    total = 0
    best = 0
    prediction = None
    for i, move in enumerate(game.mainline_moves()):
        board.push(move)
        if i % 2 == x:
            total += 1
            if not prediction:
                print("best move is falsy o.0", "i:", i, "move:", move, "prediction:", prediction)
                continue
            if str(move) in prediction:
                best += 1
        else:
            stockfish.set_fen_position(board.fen())
            prediction = stockfish.get_best_move()
    print((total, best))        
    return (total, best)

if __name__ == "__main__":
    main()
