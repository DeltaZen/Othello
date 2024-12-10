__pragma__("skip")  # noqa
from typing import Any

m: Any = print  # noqa
window = document = console = m
__pragma__("noskip")  # noqa

from othello.components import BoardComponent, HomeComponent
from othello.game import Othello
from othello.util import State as S
from othello.util import accept_request

decoder = __new__(TextDecoder)


def receive_update(update) -> None:
    payload = update["payload"]
    if payload["move"]:
        S.game.move(*payload["move"])
    elif payload["surrender"]:
        S.surrender_addr = payload["surrender"]
        S.game.surrender()
    elif payload["addr"]:
        if not S.black["addr"] or S.black["time"] > payload["time"]:
            if S.black["addr"] != payload["addr"]:
                S.request["addr"] = S.black["addr"]
                S.request["name"] = S.black["name"]
                S.request["time"] = S.black["time"]
            S.black["addr"] = payload["addr"]
            S.black["name"] = payload["name"]
            S.black["time"] = payload["time"]
        elif not S.request["addr"] or S.request["time"] > payload["time"]:
            if S.black["addr"] != payload["addr"]:
                S.request["addr"] = payload["addr"]
                S.request["name"] = payload["name"]
                S.request["time"] = payload["time"]
    elif payload["accept"]:
        white = payload["accept"]
        if not S.white["addr"] or S.white["time"] > white["time"]:
            S.white["addr"] = white["addr"]
            S.white["name"] = white["name"]
            S.white["time"] = white["time"]

    if update["serial"] == update["max_serial"]:
        if not S.white["addr"] and S.request["addr"] and window.webxdc.selfAddr == S.black["addr"]:
            accept_request(S.request)
        m.redraw()


def process_realtime_data(raw_data) -> None:
    json_data = decoder.decode(raw_data)
    window.console.log("channel <- " + json_data)
    update = window.JSON.parse(json_data)
    receive_update(update)


def init_realtime() -> None:
    window.channel = window.webxdc.joinRealtimeChannel()
    window.channel.setListener(process_realtime_data)


def _main() -> None:
    S.game = Othello()
    root = document.getElementById("root")
    m.mount(
        root,
        {"view": lambda: m(BoardComponent if S.white["addr"] else HomeComponent)},
    )

    window.webxdc.setUpdateListener(receive_update, 0).then(init_realtime)


def main():
    window.addEventListener("load", _main)
