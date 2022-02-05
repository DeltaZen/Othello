__pragma__("skip")  # noqa
from typing import Any

m: Any = print  # noqa
window = document = console = m
__pragma__("noskip")  # noqa

from othello.board import OthelloBoard
from othello.game import BLACK, WHITE
from othello.util import State as S
from othello.util import join_game, normalize_name, replay, surrender


class HomeComponent:
    @staticmethod
    def view() -> Any:
        document.getElementById("root").style["align-items"] = "center"
        container = m(
            "div#home", m("div.logo", [m("h1", "OTHELLO"), m("h1", "OTHELLO")])
        )

        if S.black["addr"] == window.webxdc.selfAddr:
            container.children.push(m("h3.sub", "Waiting for opponent..."))
        else:
            if S.black["addr"]:
                if S.request["addr"]:
                    if S.request["addr"] == window.webxdc.selfAddr:
                        status = [
                            "Waiting for ",
                            get_tag(BLACK),
                            " to accept...",
                        ]
                    else:
                        status = [
                            get_tag(WHITE),
                            " requested to join ",
                            get_tag(BLACK),
                        ]
                else:
                    status = [
                        get_tag(BLACK),
                        " is waiting for opponent...",
                    ]
                container.children.push(m("h3.sub", status))

            if not S.request["addr"]:
                container.children.push(
                    m(
                        "a#join-btn",
                        {"class": "btn", "onclick": join_game},
                        "Join Game" if S.black["addr"] else "Start Game",
                    )
                )

        return container


class BoardComponent:
    @staticmethod
    def view() -> Any:
        document.getElementById("root").style["align-items"] = ""
        score = S.game.score()
        container = m(
            "div#game",
            [
                m(
                    "h3.sub",
                    [
                        get_tag(BLACK),
                        f" {score.black} : {score.white} ",
                        get_tag(WHITE),
                    ],
                ),
                m("div#board.board"),
                m("h3.sub", get_status()),
            ],
        )
        turn = S.black["addr"] if S.game.turn == BLACK else S.white["addr"]
        if S.game.game_over():
            container.children.push(
                m("a", {"class": "btn", "onclick": replay}, "Replay")
            )
        elif window.webxdc.selfAddr == turn and not S.replay_mode:
            container.children.push(
                m(
                    "a",
                    {"class": "btn", "onclick": surrender},
                    "Surrender",
                )
            )
        return container

    @staticmethod
    def oncreate():
        S.board = OthelloBoard("board")


def get_tag(color) -> Any:
    if color == BLACK:
        return m(f"div.tag.{BLACK}", normalize_name(S.black["name"]))
    if color == WHITE:
        return m(
            f"div.tag.{WHITE}",
            normalize_name(S.white["name"] or S.request["name"]),
        )
    return None


def get_status():
    if S.game.game_over():
        status = ["Game over, "]
        if S.game.surrendered:
            if S.surrender_addr == S.black["addr"]:
                name = get_tag(BLACK)
                winner = get_tag(WHITE)
            else:
                name = get_tag(WHITE)
                winner = get_tag(BLACK)
            status.extend([name, " surrenders, ", winner, " wins"])
        else:
            score = S.game.score()
            if score[BLACK] == score[WHITE]:
                status.append("it's a draw!")
            else:
                winner = get_tag(BLACK if score[BLACK] > score[WHITE] else WHITE)
                status.extend([winner, " wins"])
    else:
        status = ["Turn: ", get_tag(S.game.turn)]
    return status
