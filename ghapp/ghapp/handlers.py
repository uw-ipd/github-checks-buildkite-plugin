import datetime

import attr
import cattr
from .cattrs import ignore_unknown_attribs

from typing import Optional, Union, List, Dict

from .buildkite import jobs
from .github import checks

import giturlparse


def buildkite_state_github_status(state: jobs.State) -> checks.Status:
    return {
        jobs.State.scheduled: checks.Status.queued,
        jobs.State.running: checks.Status.in_progress,
        jobs.State.canceling: checks.Status.in_progress,
        jobs.State.blocked: checks.Status.in_progress,
    }.get(state, checks.Status.completed)


def buildkite_state_github_conclusion(
        state: jobs.State) -> Optional[checks.Conclusion]:
    return {
        jobs.State.passed: checks.Conclusion.success,
        jobs.State.failed: checks.Conclusion.failure,
        jobs.State.blocked: checks.Conclusion.action_required,
        jobs.State.canceled: checks.Conclusion.cancelled,
        jobs.State.skipped: checks.Conclusion.neutral,
        jobs.State.not_run: checks.Conclusion.neutral,
    }.get(state, None)


def job_hook_to_check_action(
        job_hook: jobs.JobHook,
        checks_for_commit: List[checks.RunDetails],
) -> Union[checks.CreateRun, checks.UpdateRun]:
    check_details = job_to_run_details(job_hook.job)

    repo = giturlparse.parse(job_hook.pipeline.repository)

    current_checks_by_id = {
        check.external_id: check
        for check in checks_for_commit
    }

    if check_details.external_id not in current_checks_by_id:
        action = checks.CreateRun(
            owner=repo.owner,
            repo=repo.repo,
            run=check_details,
        )
        action.run.head_sha = job_hook.build.commit
        action.run.head_branch = job_hook.build.branch
    else:
        action = checks.UpdateRun(
            owner=repo.owner,
            repo=repo.repo,
            run=check_details,
        )
        action.run.id = current_checks_by_id[check_details.external_id].id

    return action


def job_to_run_details(job: jobs.Job) -> checks.RunDetails:
    return checks.RunDetails(
        name=job.name,
        details_url=job.web_url,
        external_id=job.id,
        status=buildkite_state_github_status(job.state),
        started_at=job.started_at,
        conclusion=buildkite_state_github_conclusion(job.state),
        completed_at=job.finished_at,
        output=None,
    )


def job_env_to_run_details(environ: Dict[str, str]) -> checks.RunDetails:
    job: BuildkiteJobEnviron = \
        cattr.structure(environ, BuildkiteJobEnviron)
    assert job.BUILDKITE
    assert job.CI

    now = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    if job.BUILDKITE_COMMAND_EXIT_STATUS is None:
        status = checks.Status.in_progress

        started_at = now
        completed_at = None

        conclusion = None
    else:
        status = checks.Status.completed

        started_at = None
        completed_at = now

        if job.BUILDKITE_COMMAND_EXIT_STATUS == 0:
            conclusion = checks.Conclusion.success
        elif job.BUILDKITE_TIMEOUT:
            conclusion = checks.Conclusion.timed_out
        else:
            conclusion = checks.Conclusion.failure

    return checks.RunDetails(
        name=job.BUILDKITE_LABEL,
        head_sha=job.BUILDKITE_COMMIT,
        head_branch=job.BUILDKITE_BRANCH,
        details_url=f"{job.BUILDKITE_BUILD_URL}#{job.BUILDKITE_JOB_ID}",
        external_id=job.BUILDKITE_JOB_ID,
        status=status,
        started_at=started_at,
        completed_at=completed_at,
        conclusion=conclusion,
    )


@ignore_unknown_attribs
@attr.s(auto_attribs=True)
class BuildkiteJobEnviron:
    CI: bool
    BUILDKITE: bool

    BUILDKITE_LABEL: str

    BUILDKITE_BRANCH: str
    BUILDKITE_COMMIT: str

    BUILDKITE_BUILD_ID: str
    BUILDKITE_BUILD_NUMBER: str
    BUILDKITE_BUILD_URL: str

    BUILDKITE_JOB_ID: str
    BUILDKITE_COMMAND: str
    BUILDKITE_TIMEOUT: bool
    BUILDKITE_COMMAND_EXIT_STATUS: Optional[int] = None
