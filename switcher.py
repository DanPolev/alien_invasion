class Switcher:
    def __init__(self, status: bool = True) -> None:
        self.status = status

    def switch(self) -> None:
        self.status = not self.status
        