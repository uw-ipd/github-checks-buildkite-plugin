import attr
from .cattrs import ignore_unknown_attribs

@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class Ping:
    zen: str

@attr.attrs(slots=True, auto_attribs=True)
class Mind:
    thought: str = "The mind is a blank canvas."

    def listen(self, ping: Ping):
        self.thought = ping.zen
