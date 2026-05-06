class StateNotFoundException(Exception):

    def __init__(self, state: str):

        self.state = state