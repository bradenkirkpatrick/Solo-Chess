
QUEEN = 5
ROOK = 4
BISHOP = 3
KNIGHT = 2
PAWN = 1
KING = -1
PIECES = range(1, 6)

moves = {
    ROOK:   lambda x1, y1, x2, y2: x1 == x2 or y1 == y2, 
    KNIGHT: lambda x1, y1, x2, y2: abs(x1-x2) + abs(y1-y2) == 3 and abs(x1-x2) > 0,
    BISHOP: lambda x1, y1, x2, y2: abs(x1 - x2) == abs(y1 - y2),
    KING:   lambda x1, y1, x2, y2: abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1,
    PAWN:   lambda x1, y1, x2, y2: abs(x1 - x2) == 1 and y1 - y2 == -1,
    QUEEN:  lambda x1, y1, x2, y2: moves[ROOK](x1, y1, x2, y2) or moves[BISHOP](x1, y1, x2, y2)
}

class Piece():
    def __init__(self, x, y, piece_type):
        self.x = x
        self.y = y
        self.piece_type = piece_type
    def take(self, other):
        self.x = other.x
        self.y = other.y
    def can_take(self, other):
        if other.piece_type == KING:
            return False
        if moves[self.piece_type](self.x, self.y, other.x, other.y):
            return True
        return False
    def is_king(self) -> bool:
        return self.piece_type == KING
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
