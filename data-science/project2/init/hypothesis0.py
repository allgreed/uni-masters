import chess.pgn
from stockfish import Stockfish

# TODO: dehardcode this
stockfish = Stockfish("/nix/store/gfrsm7wdvrx1a8ck61zalbr35iiri6wp-stockfish-11/bin/stockfish", parameters={"Threads": 2, "MultiPV": 3}, depth=18)

pgn = open("./g_kasparov_some_recent_games.pgn")
first_game = chess.pgn.read_game(pgn)
board = first_game.board()

x = first_game.headers["Black"] == "Kasparov, Garry"
print("----------")
total = 0
best = 0
prediction = None
da_fen = None
for i, move in enumerate(first_game.mainline_moves()):
    board.push(move)
    if i % 2 == x:
        total += 1
        if str(move) in prediction:
            best += 1
        else:
            print("suboptimal move", i // 2 + x, da_fen, move, prediction)
    else:
        fen = board.fen()
        stockfish.set_fen_position(fen)
        da_fen = fen
        prediction = stockfish.get_best_move()
print("fin", total, best, best / (total) * 100)    
