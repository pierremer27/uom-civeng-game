from game.state import State


def start(config: dict):
    state = State(config)

    # Update the game every frame
    while state.active:
        state.update()
