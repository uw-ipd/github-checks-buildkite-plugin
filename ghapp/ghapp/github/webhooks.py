from typing import Optional, Union

import logging
import hmac
import os

import attr

from aiohttp import web

from ..signalset import SignalSet

logger = logging.getLogger(__name__)

@attr.s(auto_attribs=True)
class GithubHooks:
    SECRET_ENV_VAR = "GITHUB_WEBHOOK_SECRET"

    @staticmethod
    def _resolve_secret(secret: Optional[Union[str, bytes]] = None) -> bytes:
        """Resolve secret from env or target file, falling back to `GITHUB_WEBHOOK_SECRET`."""
        if secret is None:
            logger.debug("Resolving secret from env.")

            secret = os.getenv(GithubHooks.SECRET_ENV_VAR)
            if secret is None:
                raise ValueError("Unable to resolve secret from env: %s" %
                                 GithubHooks.SECRET_ENV_VAR)
            logger.info("Resolved %s to secret.",
                        GithubHooks.SECRET_ENV_VAR)

        if os.path.isfile(secret):
            logger.info("Resolved secret to filename: %s", secret)
            secret = open(secret, "rb").read()

        logger.debug("Resolved secret.", secret)

        if isinstance(secret, str):
            return secret.encode()
        else:
            assert isinstance(secret, bytes)
            return secret

    secret: bytes = attr.ib(
        converter=_resolve_secret.__func__,
        default=attr.Factory(lambda: GithubHooks._resolve_secret()))

    signals: SignalSet = attr.Factory(SignalSet)

    async def handler(self, req: web.Request):
        # Get and validate signature
        sig = req.headers.get('x-hub-signature')
        if sig:
            raw_body = await req.read()

            mac = hmac.new(self.secret, msg=raw_body, digestmod='sha1')
            local_sig = "sha1=" + mac.hexdigest()

            logger.info("x-hub-sig: %s", sig)
            logger.info("payload-sig: %s", local_sig)

            if not sig == local_sig:
                return web.Response(status=401, text="invalid x-hub-signature")

        # Get body and unpack content type
        logger.info("content-type: %s", req.headers["content-type"])
        if req.headers["content-type"] == "application/x-www-form-urlencoded":
            body = (await req.post())["payload"]
        else:
            body = await req.json()

        name = req.headers['x-github-event']
        logger.debug("name: %s", name)

        signal = self.signals.signals.get(name)
        if signal:
            logger.debug("resolved signals: %s", name)
            await signal.send(name = name, body=body)

        return web.Response(status=200)
