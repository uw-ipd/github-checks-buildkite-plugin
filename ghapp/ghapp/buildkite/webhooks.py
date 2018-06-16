import logging

import attr

from aiohttp import web

from ..signalset import SignalSet

logger = logging.getLogger(__name__)

@attr.s(auto_attribs=True)
class BuildkiteHooks:
    token: str

    signals: SignalSet = attr.Factory(SignalSet)

    async def handler(self, req: web.Request):
        # Get and validate signature
        token = req.headers.get('x-buildkite-token')
        if token:
            if not token == self.token:
                logging.debug("x-buildkite-token: %s", token)
                logging.debug("token: %s", self.token)
                return web.Response(status=401, text="invalid x-buildkite-token")

        # Get body, only application/json
        body = await req.json()

        name = req.headers['x-buildkite-event']
        logger.debug("name: %s", name)

        signal = self.signals.signals.get(name)
        if signal:
            logger.debug("resolved signals: %s", name)
            await signal.send(name = name, body=body)

        return web.Response(status=200)
