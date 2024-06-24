__pragma__("skip")  # noqa
from typing import Any

m: Any = print  # noqa
window = document = console = Object = setTimeout = m
__pragma__("noskip")  # noqa

encoder = __new__(TextEncoder)


class State:
    game = None
    board = None
    white = {"addr": None, "name": None, "time": 0}
    black = {"addr": None, "name": None, "time": 0}
    request = {"addr": None, "name": None, "time": 0}
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


def send_update(update: dict) -> None:
    json = window.JSON.stringify(update)
    window.console.log("channel -> " + json)
    window.channel.send(encoder.encode(json))
    window.webxdc.sendUpdate(update, "")


def accept_request(request) -> None:
    State.white["addr"] = request["addr"]
    State.white["name"] = request["name"]
    State.white["time"] = request["time"]
    update = {
        "payload": {"accept": request},
        "summary": get_summary(),
    }
    send_update(update)


def join_game() -> None:
    addr = window.webxdc.selfAddr
    name = window.webxdc.selfName
    if not State.black["addr"] or (
        not State.white["addr"] and State.black["addr"] != addr
    ):
        now = __new__(Date)
        update = {
            "payload": {"addr": addr, "name": name, "time": now.valueOf()},
            "info": normalize_name(name) + " wants to play Othello",
        }
        send_update(update)
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
    info = f"{normalize_name(window.webxdc.selfName)} surrenders, {winner} wins"
    update: dict = {"payload": {"surrender": addr}, "summary": info, "info": info}
    send_update(update)


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
