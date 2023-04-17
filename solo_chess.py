from Piece import Piece
from Timer import timer
import itertools

def is_solvable_for_two_pieces(ps):
    p1, p2 = ps
    return p1.can_take(p2) or p2.can_take(p1)

def is_solo_solvable_for_two_pieces(ps):
    p1, p2 = ps
    if p1.can_take(p2) or p2.can_take(p1):
        return not p1.can_take(p2) and p2.can_take(p1)
    
piece_count_to_solving_function = {2:is_solvable_for_two_pieces}
def is_solvable(ps, solving_alg=None):
    if solving_alg:
        return solving_alg(ps)
    return piece_count_to_solving_function[len(ps)](ps)

def is_solvable_highest_dom_takes_lowest_dom(ps):
    ps_sorted_by_dom = list()
    for i in range:
      for p in ps:
          if p.piece_type == i:
            ps_sorted_by_dom.append(p)
    flag = True
    while flag:
        num_ps = len(ps_sorted_by_dom)
        for i in range(num_ps):
            j = num_ps - 1 
            while j > i:
                if ps_sorted_by_dom[j].can_take(ps_sorted_by_dom[i]):
                    ps_sorted_by_dom[j].take(ps_sorted_by_dom[i])
                    ps_sorted_by_dom.pop(i)
                    break
                j-=1
            if num_ps != len(ps_sorted_by_dom):
                break

        if num_ps == len(ps_sorted_by_dom):
            return False

        if len(ps_sorted_by_dom) == 1:
            return True

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
        
    
################################################################################
def n_pieces(n, num_pieces, switch=True, solving_alg=None):
    sa = itertools.combinations(itertools.product(range(n), range(n)), num_pieces)
    sb = itertools.product(range(1, 6), repeat=num_pieces)
    s = list(itertools.product(sa, sb))
    del sa, sb
    solved_puzzles, unsolved_puzzles = solve_puzzle(s, solving_alg)
    
    if switch:
        a, b = len(solved_puzzles), len(solved_puzzles) + len(unsolved_puzzles)
        print(f"On a {n}x{n} board with {num_pieces} pieces")
        print(f"{a}/{b}")
        print(f"The puzzles are solved {round(a / b * 100, 2)}% of the time")
    return unsolved_puzzles

################################################################################

def solve_puzzle(s, solving_alg, option=None):
    if option == "c1d1toc1":
        print("no")
    else:
        return default_puzzle_solver(s, solving_alg)

def default_puzzle_solver(s, solving_alg):
    solved_puzzles = list()
    unsolved_puzzles = list()
    for i in range(len(s)):
        combo = s[i]
        pieces = list()
        combo_coords, combo_pieces = combo
        combo_pieces = list(combo_pieces)
        combo_coords = list(combo_coords)
        i = 0
        for i in range(len(combo_pieces)):
            x, y = combo_coords[i]
            p = combo_pieces[i]
            pieces.append(Piece(x, y, p))
            i += 1
        
        if is_solvable(pieces, solving_alg):
            u = []
            for i in pieces:
                u.append([i.x, i.y, i.piece_type])
            solved_puzzles.append(u)
        else:
            u = []
            for i in pieces:
                u.append([i.x, i.y, i.piece_type])
            unsolved_puzzles.append(u)
    return solved_puzzles, unsolved_puzzles
