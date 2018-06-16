import logging
from typing import Callable, Awaitable
from .identity import AppIdentity

import aiohttp

logger = logging.getLogger(__name__)


async def credential_helper(credential_input: str,
                      get_token_for_account: Callable[[str], Awaitable[str]]) -> str:
    logger.info("credential_input: %s", credential_input)

    cvals = dict(l.strip().split("=", 1) for l in credential_input.split("\n")
                 if l.strip())
    logger.debug("cvals: %s", cvals)

    if not cvals.get("host", None) == "github.com":
        logger.debug("Host does not match github.com")
        return credential_input
    if not cvals.get("protocol", "").startswith("http"):
        logger.debug("Protocol does not match http*")
        return credential_input

    if not cvals.get("path", ""):
        logger.debug("Not path provided.")
        return credential_input

    account = cvals.get("path", "").split("/")[0]
    token = await get_token_for_account(account)
    if not token:
        return credential_input

    cvals["username"] = "x-access-token"
    cvals["password"] = token

    return "\n".join("=".join(i) for i in cvals.items())
