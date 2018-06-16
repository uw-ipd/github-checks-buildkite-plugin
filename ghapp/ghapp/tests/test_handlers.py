import os
import json

import pytest

import cattr

from ..buildkite import jobs
from ..github import checks

from ..handlers import job_hook_to_check_action

@pytest.fixture
def test_events():
    bd = os.path.dirname(__file__)

    return {
        "job.finished": json.load(open(bd + "/buildkite.job.finished.json")),
        "job.started": json.load(open(bd + "/buildkite.job.started.json")),
    }

def test_job_conversion(test_events):
    events = {
        k : cattr.structure(e, jobs.JobHook)
        for k, e in test_events.items()
    }

    init = job_hook_to_check_action(events["job.started"], [])
    assert isinstance(init, checks.CreateRun)

    conclude = job_hook_to_check_action(events["job.finished"], [init.run])
    assert isinstance(conclude, checks.UpdateRun)

    just_finished = job_hook_to_check_action(events["job.finished"], [])
    assert isinstance(just_finished, checks.CreateRun)
