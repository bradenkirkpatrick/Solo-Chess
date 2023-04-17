import solo_chess
from Timer import timer

def main():
    t = timer()
    for n in range(2, 7):
        t.test(t.start(), solo_chess.n_pieces(3, n, solving_alg=solo_chess.is_solvable_with_n_pieces))

if __name__ == "__main__":
    main()