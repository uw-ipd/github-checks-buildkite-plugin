import logging
import hmac

import attr

from aiohttp import web

from ..signalset import SignalSet

logger = logging.getLogger(__name__)

@attr.s(auto_attribs=True)
class GithubHooks:
    secret: bytes

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
