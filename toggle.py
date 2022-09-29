class Toggle:
    def __init__(self, status: bool = True) -> None:
        self.status = status
        self.toggled = False

    def toggle(self) -> None:
        self.status = not self.status
        self.toggled = not self.toggled
        