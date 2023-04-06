class Piece():
    def __init__(self, x, y, piece_type):
        self.x = x
        self.y = y
        self.piece_type = piece_type
    def take(self, other):
        self.x = other.x
        self.y = other.y
    def can_take(self, other):
        if other.piece_type == 'King':
            return False
        if moves[self.piece_type](self.x, self.y, other.x, other.y):
            return True
        return False
    def is_king(self) -> bool:
        return self.piece_type == "King"
    def clone(self):
        return Piece(self.x, self.y, self.piece_type)
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.piece_type == __o.piece_type
    def __ne__(self, __o: object) -> bool:
        if self.x != __o.x:
            return True
        if self.y != __o.y:
            return True
        if self.piece_type != __o.piece_type:
            return True
        return False
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.piece_type})"

class Pieces():
    def clone_all(pieces:list) -> list:
        out = list()
        for piece in pieces:
            out.append(piece.clone())
        yield out
    def can_take(p1, p2) -> bool:
        if p2[2] == 'King':
            return False
        if moves[p1[2]](p1[0], p1[1], p2[0], p2[1]):
            return True
        return False

moves = {
    'Rook':   lambda x1, y1, x2, y2: x1 == x2 or y1 == y2, 
    'Knight': lambda x1, y1, x2, y2: abs(x1-x2) + abs(y1-y2) == 3 and abs(x1-x2) > 0,
    'Bishop': lambda x1, y1, x2, y2: abs(x1 - x2) == abs(y1 - y2),
    'King':   lambda x1, y1, x2, y2: abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1,
    'Pawn':   lambda x1, y1, x2, y2: abs(x1 - x2) == 1 and y1 - y2 == -1,
    'Queen':  lambda x1, y1, x2, y2: moves['Rook'](x1, y1, x2, y2) or moves['Bishop'](x1, y1, x2, y2)
}
################################################################################

from re import X
import itertools

################################################################################
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
    for i in "Pawn", "Knight", "Bishop", "Rook", "Queen":
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

def is_solvable_with_n_pieces_a1(pieces:list):
    s = itertools.permutations(pieces, 2)
    takes = []
    for p1, p2 in s:
        if Pieces.can_take(p1, p2):
            takes.append((p1, p2))
    del s
    if len(pieces) == 2:
        return Pieces.can_take(p1, p2) or Pieces.can_take(p2, p1)
    for p1, p2 in takes:
        attempt = pieces.copy()
        attempt.remove(p1)
        attempt.remove(p2)
        p2[2] = p1[2]
        attempt.append(p2)
        if is_solvable_with_n_pieces_a1(attempt):
            return True
    return False
        
    
################################################################################
def n_pieces(n, num_pieces, switch=True, solving_alg=None):
    pieces = ['Rook', 'Bishop', 'Queen', 'Knight', 'Pawn']
    sa = itertools.combinations(itertools.product(range(n), range(n)), num_pieces)
    sb = itertools.product(pieces, repeat=num_pieces)
    s = list(itertools.product(sa, sb))
    del pieces, sa, sb
    solved_puzzles, unsolved_puzzles = solve_puzzle(s, solving_alg)
    
    if switch:
        a, b = len(solved_puzzles), len(solved_puzzles) + len(unsolved_puzzles)
        print(f"On a {n}x{n} board with {num_pieces} pieces")
        print(f"{a}/{b}")
        print(f"The puzzles are solved {round(a / b * 100, 2)}% of the time")
    return unsolved_puzzles

def n_pieces_a1(n, num_pieces, switch=True, solving_alg=None):
    pieces = ['Rook', 'Bishop', 'Queen', 'Knight', 'Pawn']
    sa = itertools.combinations(itertools.product(range(n), range(n)), num_pieces)
    sb = itertools.product(pieces, repeat=num_pieces)
    s = list(itertools.product(sa, sb))
    del pieces, sa, sb
    solved_puzzles, unsolved_puzzles = solve_puzzle_a1(s, solving_alg)
    
    if switch:
        a, b = len(solved_puzzles), len(solved_puzzles) + len(unsolved_puzzles)
        print(f"On a {n}x{n} board with {num_pieces} pieces")
        print(f"{a}/{b}")
        print(f"The puzzles are solved {round(a / b * 100, 2)}% of the time")
    return unsolved_puzzles

################################################################################

def solve_puzzle(s, solving_alg):
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


def solve_puzzle_a1(s, solving_alg):
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
            pieces.append([x, y, p])
            i += 1
        if is_solvable(pieces, solving_alg):
            solved_puzzles.append(pieces)
        else:
            unsolved_puzzles.append(pieces)
    return solved_puzzles, unsolved_puzzles
################################################################################

import time
class timer():
    def __init__(self):
        self.time = time.process_time()
    def start(self):
        self.time = time.process_time()
    def get(self):
        return time.process_time() - self.time
    def print(self):
        print("time: " + str(self.get()))

################################################################################

def main():
    t = timer()
    # t.start()
    # unsolved_puzzles1 = n_pieces_a1(3, 3, solving_alg=is_solvable_with_n_pieces_a1)
    # print(f"Calculated in {t.get()} seconds")
    for n in range(2, 7):
        t.start()
        n_pieces(3, n, solving_alg=is_solvable_with_n_pieces)
        print(f"Calculated in {t.get()} seconds")
        # unsolved_puzzles_intersection = [x for x in unsolved_puzzles1 if not x in unsolved_puzzles2]
        # print(unsolved_puzzles_intersection[0]) #normal solver more accurate than fast solver therefore it is wrong

    #t.start()
    # n_pieces(4, 5, solving_alg=is_solvable_highest_dom_takes_lowest_dom)
    # print(f"Calculated in {t.get()} seconds")
if __name__ == "__main__":
    main()