from rx.subject import Subject


class _InteractiveFake:
    def __init__(self):
        self.__speechStream = Subject()

    @property
    def speechStream(self):
        return self.__speechStream


# Doing this here so it's accessible from the interpreter
interactiveFake = _InteractiveFake()


def connectToNVDA():
    return interactiveFake
