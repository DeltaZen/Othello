__pragma__("skip")  # noqa
from typing import Any

m: Any = None  # noqa
window = document = console = m
__pragma__("noskip")  # noqa

from othello.game import BLACK, WHITE
from othello.util import State as S
from othello.util import (
    create_element,
    get_summary,
    is_my_turn,
    is_observer,
    send_update,
)


class OthelloBoard:
    def __init__(self, container_id: str) -> None:
        self.container = document.getElementById(container_id)
        self.board: list = []
        for x in range(8):
            row = []
            self.board.append(row)
            rowdiv = create_element("div", {"class": "row"})
            for y in range(8):
                piece = create_element("div", {"class": "piece"})
                if S.game.board[x][y]:
                    piece.classList.add(S.game.board[x][y])
                cell = create_element("div", {"class": "cell"}, piece)
                cell.addEventListener("click", _move(x, y))
                rowdiv.append(cell)
                row.append({"cell": cell, "piece": piece})
            self.container.append(rowdiv)
        self.set_highlight()
        S.game.add_observer(self)

    def update(self) -> None:
        if S.game.last_move:
            x, y = S.game.last_move
            if S.game.board[x][y]:
                self.board[x][y].piece.classList.add(S.game.board[x][y])

            for x, row in enumerate(S.game.board):
                for y, cell in enumerate(row):
                    self.board[x][y].cell.classList.remove("highlight")
                    self.board[x][y].piece.classList.remove("reversed")
        else:  # game started/reset
            for x, row in enumerate(S.game.board):
                for y, cell in enumerate(row):
                    self.board[x][y].cell.classList.remove("highlight")
                    self.board[x][y].piece.classList.remove("reversed")
                    self.board[x][y].piece.classList.remove(BLACK, WHITE)
                    if cell:
                        self.board[x][y].piece.classList.add(cell)

        for x, y in S.game.last_flipped:
            self.board[x][y].piece.classList.toggle(WHITE)
            self.board[x][y].piece.classList.toggle(BLACK)
            self.board[x][y].piece.classList.add("reversed")

        self.set_highlight()

    def set_highlight(self) -> None:
        highlight = not S.game.surrendered and (
            is_my_turn() or is_observer() or S.replay_mode
        )
        moves = S.game.moves() if highlight else []
        for x, y in moves:
            self.board[x][y].cell.classList.add("highlight")


def _move(x: int, y: int) -> Any:
    return lambda: move(x, y)


def move(x: int, y: int) -> None:
    if S.replay_mode or S.game.game_over():
        return

    if not is_my_turn():
        return

    if S.game.move(x, y):
        update = {"payload": {"move": (x, y)}, "summary": get_summary()}
        if S.game.game_over():
            update["info"] = update["summary"]
        send_update(update)
