from othello.util import Observable

BLACK = "black"
WHITE = "white"
EMPTY = ""

_SIZE = 8
_DIRECTIONS = [(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]


class Othello(Observable):
    def __init__(self) -> None:
        super().__init__()
        self.BLACK = BLACK
        self.WHITE = WHITE
        self.history = []
        self.turn = BLACK
        self.surrendered = False
        self.last_move: tuple = None
        self.last_flipped = []
        self.reset()

    @staticmethod
    def _is_on_board(x: int, y: int) -> bool:
        return 0 <= x < _SIZE and 0 <= y < _SIZE

    def _is_valid(self, disk: str, x: int, y: int) -> bool:
        """Returns True if the move is valid, False otherwise"""
        if not self._is_on_board(x, y) or self.board[x][y] != EMPTY:
            return False
        other_disk = WHITE if disk == BLACK else BLACK
        for xdir, ydir in _DIRECTIONS:
            newx, newy = x + xdir, y + ydir
            while (
                self._is_on_board(newx, newy) and self.board[newx][newy] == other_disk
            ):
                newx += xdir
                newy += ydir
            if (
                self._is_on_board(newx, newy)
                and self.board[newx][newy] == disk
                and (newx - xdir != x or newy - ydir != y)
            ):
                return True
        return False

    def _get_flipped(self, disk: str, x: int, y: int) -> list:
        if not self._is_on_board(x, y) or self.board[x][y] != EMPTY:
            return []

        other_disk = WHITE if disk == BLACK else BLACK
        flipped = []
        for xdir, ydir in _DIRECTIONS:
            newx, newy = x + xdir, y + ydir
            while (
                self._is_on_board(newx, newy) and self.board[newx][newy] == other_disk
            ):
                newx += xdir
                newy += ydir
            if not self._is_on_board(newx, newy) or self.board[newx][newy] != disk:
                continue
            while True:
                newx -= xdir
                newy -= ydir
                if newx == x and newy == y:
                    break
                flipped.append((newx, newy))
        return flipped

    def _can_move(self, disk: str) -> bool:
        """Returns True if the player with the given disk can move, False otherwise"""
        for x in range(_SIZE):
            for y in range(_SIZE):
                if self._is_valid(disk, x, y):
                    return True
        return False

    def reset(self) -> None:
        self.board = [[EMPTY for y in range(_SIZE)] for x in range(_SIZE)]
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE

        self.history = []
        self.turn = BLACK
        self.surrendered = False
        self.last_move: tuple = None
        self.last_flipped = []

        self.notify_all()

    def surrender(self) -> None:
        self.surrendered = True
        self.notify_all()

    def score(self) -> dict:
        """Get white and black scores"""
        b, w = 0, 0
        for row in self.board:
            for d in row:
                if d == BLACK:
                    b += 1
                elif d == WHITE:
                    w += 1
        return {BLACK: b, WHITE: w}

    def game_over(self) -> bool:
        """Returns True if the game is over, False otherwise"""
        return self.surrendered or (
            not self._can_move(BLACK) and not self._can_move(WHITE)
        )

    def move(self, x: int, y: int) -> bool:
        flipped = self._get_flipped(self.turn, x, y)
        if len(flipped) == 0:
            return False
        self.last_move = (x, y)
        self.last_flipped = flipped
        self.history.append(self.last_move)
        self.board[x][y] = self.turn
        for i, j in flipped:
            self.board[i][j] = self.turn
        next_turn = WHITE if self.turn == BLACK else BLACK
        if self._can_move(next_turn):
            self.turn = next_turn
        self.notify_all()
        return True

    def moves(self, disk: str = None) -> list:
        if disk is None:
            disk = self.turn
        moves = []
        for x in range(_SIZE):
            for y in range(_SIZE):
                if self._is_valid(disk, x, y):
                    moves.append((x, y))
        return moves
