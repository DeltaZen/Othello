__pragma__("skip")  # noqa
from typing import Any

m: Any = print  # noqa
window = document = console = Object = setTimeout = m
__pragma__("noskip")  # noqa


class State:
    game = None
    board = None
    white = dict(addr=None, name=None)
    black = dict(addr=None, name=None)
    request = dict(join=None, addr=None, name=None)
    surrender_addr = None
    replay_mode = False


class Observable:
    def __init__(self) -> None:
        self._observers = []

    def add_observer(self, observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer) -> None:
        self._observers.remove(observer)

    def notify_all(self) -> None:
        for observer in self._observers:
            observer.update()


def create_element(tag, attributes, *children):
    element = document.createElement(tag)
    Object.entries(attributes).forEach(
        lambda entry: element.setAttribute(entry[0], entry[1])
    )
    element.append(*children)
    return element


def normalize_name(name: str) -> str:
    return name[:16] + "…" if len(name) > 16 else name


def is_my_turn() -> bool:
    addr = window.webxdc.selfAddr
    if State.game.turn == State.game.BLACK:
        return addr == State.black["addr"]
    return addr == State.white["addr"]


def is_observer() -> bool:
    return window.webxdc.selfAddr not in (State.black["addr"], State.white["addr"])


def get_summary() -> str:
    game = State.game
    BLACK = game.BLACK
    WHITE = game.WHITE
    if game.game_over():
        status = "Game over, "
        score = game.score()
        if score[BLACK] == score[WHITE]:
            status += "it's a draw!"
        else:
            winner = normalize_name(
                State.black["name"]
                if score[BLACK] > score[WHITE]
                else State.white["name"]
            )
            status += f"{winner} wins"
    else:
        status = "Turn: " + normalize_name(
            State.black["name"] if game.turn == BLACK else State.white["name"]
        )
    return status


def accept_request(request) -> None:
    State.white["addr"] = request["addr"]
    State.white["name"] = request["name"]
    desc = "Othello: " + normalize_name(request["name"]) + " joined the game"
    update = {
        "payload": {
            "whiteAddr": request["addr"],
            "whiteName": request["name"],
        },
        "summary": get_summary(),
    }
    window.webxdc.sendUpdate(update, desc)


def join_game() -> None:
    addr = window.webxdc.selfAddr
    name = window.webxdc.selfName
    update = {}
    if not State.black["addr"]:
        update["payload"] = {"blackAddr": addr, "blackName": name}
        update["summary"] = normalize_name(name) + " is waiting for an opponent"
        window.webxdc.sendUpdate(update, "Othello: " + update["summary"])
    elif not State.white["addr"] and State.black["addr"] != addr:
        update["payload"] = {"join": State.black["addr"], "addr": addr, "name": name}
        update["summary"] = normalize_name(name) + " requested to join game"
        window.webxdc.sendUpdate(update, "Othello: " + update["summary"])
    else:
        console.log("Warning: ignoring call to join_game()")


def surrender() -> None:
    if State.surrender_addr:
        console.log("Warning: ignoring call to surrender()")
        return

    addr = window.webxdc.selfAddr
    winner = normalize_name(
        State.white["name"] if addr == State.black["addr"] else State.black["name"]
    )
    update: dict = {
        "payload": {"surrender": addr},
        "summary": f"{normalize_name(window.webxdc.selfName)} surrenders, {winner} wins",
    }
    window.webxdc.sendUpdate(update, "Othello: " + update["summary"])


def replay() -> str:
    State.replay_mode = True
    game = State.game
    history = game.history
    game.reset()
    i = 0  # noqa

    def run_turn():
        def _run_turn():
            game.move(*history[i])  # noqa
            m.redraw()
            i += 1  # noqa
            if i < len(history):
                run_turn()
            else:
                if State.surrender_addr:
                    game.surrender()
                State.replay_mode = False
                m.redraw()

        setTimeout(_run_turn, 1500)

    run_turn()
