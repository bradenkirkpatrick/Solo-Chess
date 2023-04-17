from Piece import Piece
import itertools

def is_solvable_for_two_pieces(ps):
    p1, p2 = ps
    return p1.can_take(p2) or p2.can_take(p1)
    
def is_solvable(ps, solving_alg):
    return solving_alg(ps)

def is_solvable_with_n_pieces(pieces:list):
    s = itertools.permutations(pieces, 2)
    takes = []
    for p1, p2 in s:
        if p1.can_take(p2):
            takes.append((p1, p2))
    del s
    if len(pieces) == 2:
        return p1.can_take(p2) or p2.can_take(p1)
    for p1, p2 in takes:
        attempt = list()
        for i in pieces:
            if p1 == i:
                p1 = i.clone()
                attempt.append(p1)
            elif p2 == i:
                p2 = i.clone()
                attempt.append(p2)
            else:
                attempt.append(i.clone())
        p1.take(p2)
        attempt.remove(p2)
        if is_solvable_with_n_pieces(attempt):
            return True
    return False
        
def n_pieces(n, num_pieces, switch=True, solving_alg=None):
    sa = itertools.combinations(itertools.product(range(n), range(n)), num_pieces)
    sb = itertools.product(range(1, 6), repeat=num_pieces)
    s = list(itertools.product(sa, sb))
    del sa, sb
    solved_puzzles, unsolved_puzzles = solve_puzzle(s, solving_alg)
    
    if switch:
        if solving_alg == list_puzzle_solver:
            solved_puzzles, puzzles = len(solved_puzzles), len(solved_puzzles) + len(unsolved_puzzles)
        print(f"On a {n}x{n} board with {num_pieces} pieces")
        print(f"{solved_puzzles}/{puzzles}")
        print(f"The puzzles are solved {round(a / b * 100, 2)}% of the time")
    return unsolved_puzzles

def solve_puzzle(s, solving_alg, option=None):
    if option == "int solver":
        return int_puzzle_solver()
    return list_puzzle_solver(s, solving_alg)

def list_puzzle_solver(s, solving_alg):
    solved_puzzles = list()
    unsolved_puzzles = list()
    for combo_coords, combo_pieces in s:
        pieces = list()
        combo_pieces = list(combo_pieces)
        combo_coords = list(combo_coords)
        entry = []
        i = 0
        for i in range(len(combo_pieces)):
            x, y = combo_coords[i]
            p = combo_pieces[i]
            entry.append((x, y, p))
            pieces.append(Piece(x, y, p))
            i += 1
        
        if is_solvable(pieces, solving_alg):
            solved_puzzles.append(entry)
        else:
            unsolved_puzzles.append(entry)
    return solved_puzzles, unsolved_puzzles

def int_puzzle_solver(s, solving_alg):
    solved_puzzles = 0
    unsolved_puzzles = 0
    for combo_coords, combo_pieces in s:
        pieces = list()
        combo_pieces = list(combo_pieces)
        combo_coords = list(combo_coords)
        i = 0
        for i in range(len(combo_pieces)):
            x, y = combo_coords[i]
            p = combo_pieces[i]
            pieces.append(Piece(x, y, p))
            i += 1
        
        if is_solvable(pieces, solving_alg):
            solved_puzzles += 1
        else:
            unsolved_puzzles += 1
    return solved_puzzles, unsolved_puzzles
