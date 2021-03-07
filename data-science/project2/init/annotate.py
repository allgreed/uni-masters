from multiprocessing import Pool
import os.path


from stockfish import Stockfish

with open("positions/manifest") as f:
    manifest = list(map(lambda s: s.rstrip(), f.readlines()))

def compute_annotation(f):
    fname = f.replace("positions/", "annotations/")
    if os.path.isfile(fname):
        return

    with open(f) as _f:
        line = _f.read().rstrip()

    fen, move = line.split(";")
    compute_annotation.stockfish.set_fen_position(fen)
    best = compute_annotation.stockfish.get_best_move()
    annotation = "1" if move in best else "0"

    with open(fname, "w+") as f:
        f.write(";".join((fen, move, annotation)))


def init_worker(function):
    function.stockfish = Stockfish(parameters={"Threads": 1, "MultiPV": 3}, depth=18)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == "__main__":
    batches = list(chunks(manifest, 100))
    total = len(batches)    
    with Pool(initializer=init_worker, initargs=(compute_annotation,)) as p:
        for i, b in enumerate(batches):
            p.map(compute_annotation, b)
            print("batch {} out of {} - {:.2f}% done!".format(i, total, i / total * 100))
