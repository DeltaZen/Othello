__pragma__("skip")  # noqa
from typing import Any

m: Any = print  # noqa
window = document = console = m
__pragma__("noskip")  # noqa


from othello.components import BoardComponent, HomeComponent
from othello.game import Othello
from othello.util import State as S
from othello.util import accept_request


def receive_update(update) -> None:
    payload = update["payload"]
    if payload["move"]:
        S.game.move(*payload["move"])
    elif payload["surrender"]:
        S.surrender_addr = payload["surrender"]
        S.game.surrender()
    elif payload["blackAddr"] and not S.black["addr"]:
        S.black["addr"] = payload["blackAddr"]
        S.black["name"] = payload["blackName"]
    elif (
        not S.request["addr"] and payload["join"] and payload["join"] == S.black["addr"]
    ):
        S.request["join"] = payload["join"]
        S.request["addr"] = payload["addr"]
        S.request["name"] = payload["name"]
    elif payload["whiteAddr"] and not S.white["addr"]:
        S.white["addr"] = payload["whiteAddr"]
        S.white["name"] = payload["whiteName"]

    if update["serial"] == update["max_serial"]:
        if (
            not S.white["addr"]
            and S.request["addr"]
            and window.webxdc.selfAddr == S.black["addr"]
        ):
            accept_request(S.request)
        m.redraw()


def _main() -> None:
    S.game = Othello()
    root = document.getElementById("root")
    m.mount(
        root,
        {"view": lambda: m(BoardComponent if S.white["addr"] else HomeComponent)},
    )

    window.webxdc.setUpdateListener(receive_update, 0)


def main():
    window.addEventListener("load", _main)
