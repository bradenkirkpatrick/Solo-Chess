import solo_chess
from Timer import Timer

def main():
    t = Timer()
    for n in range(2, 6):
        t.test(t.start(), solo_chess.n_pieces(3, n, solving_alg=solo_chess.is_solvable_with_n_pieces))

if __name__ == "__main__":
    main()