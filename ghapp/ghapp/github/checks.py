from typing import Optional

import aiohttp
import logging

import attr
import cattr
import enum

from ..cattrs import ignore_optional_none

logger = logging.getLogger(__name__)
api_headers = {"Accept": "application/vnd.github.antiope-preview+json"}


class Status(enum.Enum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"


class Conclusion(enum.Enum):
    success = "success"
    failure = "failure"
    neutral = "neutral"
    cancelled = "cancelled"
    timed_out = "timed_out"
    action_required = "action_required"


@ignore_optional_none
@attr.s(auto_attribs=True)
class Output:
    title: str
    summary: str
    text: Optional[str] = None
    #annotations: List[Annotation]
    #images: List[Image]


@ignore_optional_none
@attr.s(auto_attribs=True)
class RunDetails:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    name: str
    id: Optional[str] = None
    head_sha: Optional[str] = None
    head_branch: Optional[str] = None
    details_url: Optional[str] = None
    external_id: Optional[str] = None
    status: Optional[Status] = None
    started_at: Optional[str] = None
    conclusion: Optional[Conclusion] = None
    completed_at: Optional[str] = None
    output: Optional[Output] = None
    # actions: typing.List[CheckActions]


@attr.s(auto_attribs=True)
class CreateRun:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    owner: str
    repo: str
    run: RunDetails

    def execute(self, session: aiohttp.ClientSession):
        assert self.run.head_branch is not None
        assert self.run.head_sha is not None
        assert self.run.id is None

        url = (f"https://api.github.com"
               f"/repos/{self.owner}/{self.repo}/check-runs")
        body = cattr.unstructure(self.run)

        logger.info('POST %s\n%s', url, body)

        return session.post(url, headers=api_headers, json=body)


@attr.s(auto_attribs=True)
class UpdateRun:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    owner: str
    repo: str
    run: RunDetails

    def execute(self, session: aiohttp.ClientSession):
        assert self.run.id is not None

        assert self.run.head_branch is None
        assert self.run.head_sha is None

        url = (f"https://api.github.com"
               f"/repos/{self.owner}/{self.repo}/check-runs/{self.run.id}")
        body = cattr.unstructure(self.run)

        logger.info('PATCH %s\n%s', url, body)

        return session.patch(url, headers=api_headers, json=body)
