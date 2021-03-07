import chess.pgn


def main(write=True, output_is_white=False):
    pgn = open("./all_kasparov_games.pgn")
    games = []
    i = 0
    while True:
        try:
            maybe_game = chess.pgn.read_game(pgn)
        except UnicodeDecodeError:
            print(i)
            raise

        i += 1

        if not maybe_game:
            break

        games.append(maybe_game)

    white_mapping = {}
    for i, g in enumerate(games):
        for d in extract_data(g, i):
            move_id, fen, player_move, is_white = d

            white_mapping[i] = is_white

            if write:
                with open(f"./positions/{i}_{move_id}.csv", "w") as f:
                    f.write(f"{fen};{player_move}\n")

    if output_is_white:
        print(white_mapping)

def extract_data(game, game_id=-1):
    data = []

    board = game.board()
    x =  "Kasparov" in game.headers["Black"]

    fen, play_move, move_id = (None,) * 3
    for i, move in enumerate(game.mainline_moves()):
        board.push(move)

        if i % 2 == x and i == 0:
            continue

        if i % 2 == x:
            move_number = i // 2 + x
            player_move = str(move)
            data.append((move_number, fen, player_move, not x))
        else:
            fen = board.fen()


    return data

if __name__ == "__main__":
    # main()
    main(False, True)
