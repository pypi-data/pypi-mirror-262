class OutputRendition:
    def __init__(self, name: str, type: str, spec: str) -> None:
        self.name: str = name
        self.spec: str = spec
        self.type: str = type
        self.mp4: str
        self.lang: str = "und"
