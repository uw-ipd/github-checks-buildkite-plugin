from typing import Optional, Union, List

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
            id = current_checks_by_id[check_details.external_id].id,
            run=check_details,
        )

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
