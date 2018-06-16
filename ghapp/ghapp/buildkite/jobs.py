from typing import Optional

import enum
import attr
from ..cattrs import ignore_unknown_attribs


class JobEvent(enum.Enum):
    activated = "job.activated"
    started = "job.started"
    finished = "job.finished"

class State(enum.Enum):
    scheduled = "scheduled"
    running = "running"
    passed = "passed"
    failed = "failed"
    blocked = "blocked"
    canceled = "canceled"
    canceling = "canceling"
    skipped = "skipped"
    not_run = "not_run"


@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class Job:
    id: str
    name: str
    state: State

    build_url: str
    web_url: str
    log_url: str

    created_at: Optional[str] = None
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None


@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class Build:
    id: str
    message: str
    state: State

    url: str
    web_url: str

    commit: str
    branch: str
    tag: Optional[str] = None
    pull_request: Optional[str] = None

    created_at: Optional[str] = None
    scheduled_at: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None


@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class Pipeline:
    id: str
    url: str
    web_url: str

    name: str
    description: str
    slug: str
    repository: str


@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class JobHook:
    event: JobEvent
    job: Job
    build: Build
    pipeline: Pipeline
