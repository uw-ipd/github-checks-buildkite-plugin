from typing import Optional
import os

import logging

import attr

from aiohttp import web

from ..signalset import SignalSet

logger = logging.getLogger(__name__)

@attr.s(auto_attribs=True)
class BuildkiteHooks:
    SECRET_ENV_VAR = "BUILDKITE_WEBHOOK_SECRET"

    @staticmethod
    def _resolve_secret(secret: Optional[str] = None):
        """Resolve secret from env or target file, falling back to `GITHUB_WEBHOOK_SECRET`."""
        if secret is None:
            logger.debug("Resolving secret from env.")

            secret = os.getenv(BuildkiteHooks.SECRET_ENV_VAR)
            if secret is None:
                raise ValueError("Unable to resolve secret from env: %s" %
                                 BuildkiteHooks.SECRET_ENV_VAR)
            logger.info("Resolved %s to secret.",
                        BuildkiteHooks.SECRET_ENV_VAR)

        if os.path.isfile(secret):
            logger.info("Resolved secret to filename: %s", secret)
            secret = open(secret, "r").read()

        logger.debug("Resolved secret.", secret)

        return secret

    secret: bytes = attr.ib(
        converter=_resolve_secret.__func__,
        default=attr.Factory(lambda: BuildkiteHooks._resolve_secret()))

    signals: SignalSet = attr.Factory(SignalSet)

    async def handler(self, req: web.Request):
        # Get and validate signature
        token = req.headers.get('x-buildkite-token')
        if token:
            if not token == self.secret:
                logging.debug("x-buildkite-token: %s", token)
                logging.debug("secret: %s", self.secret)
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
