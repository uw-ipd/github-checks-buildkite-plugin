import attr

from aiohttp import Signal
from frozendict import frozendict

@attr.s(auto_attribs=True)
class SignalSet:
    signals: dict = attr.Factory(dict)

    @property
    def frozen(self):
        return isinstance(self.signals, frozendict)

    def add_handler(self, key, handler):
        if self.frozen:
            return RuntimeError("Can not add handler to frozen signal set.")

        if key not in self.signals:
            # Do not set owner
            self.signals[key] = Signal(None)

        self.signals[key].append(handler)

    def freeze(self):
        for k, h in self.signals.items():
            h.freeze()

        self.signals = frozendict(self.signals)
