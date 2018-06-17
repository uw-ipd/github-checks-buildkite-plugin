import logging
import json
import os
from typing import Optional

import cattr

import aiohttp
import aiorun
import asyncio
import click
from decorator import decorator

from .github.identity import AppIdentity
from .github import checks
from .github.gitcredentials import credential_helper

from .buildkite import jobs
from .handlers import RepoName, job_environ_to_check_action

logger = logging.getLogger(__name__)

#https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-a-github-app
pass_appidentity = click.make_pass_decorator(AppIdentity, ensure=True)


@decorator
def aiomain(coro, *args, **kwargs):
    aiorun.logger.setLevel(51)

    async def main():
        try:
            await coro(*args, **kwargs)
        finally:
            asyncio.get_event_loop().stop()

    return aiorun.run(main())


@click.group()
@click.option(
    '--app_id',
    help=("Integer app id, or path to file containing id. "
          "Resolved from $%s." % AppIdentity.APP_ID_ENV_VAR),
    envvar=AppIdentity.APP_ID_ENV_VAR,
)
@click.option(
    '--private_key',
    help=("App private key, or path to private key file. "
          "Resolved from $%s." % AppIdentity.PRIVATE_KEY_ENV_VAR),
    envvar=AppIdentity.PRIVATE_KEY_ENV_VAR,
)
@click.option(
    '-v',
    '--verbose',
    count=True,
    help="'-v' for logging, '-vv' for debug logging. "
    "Resolved via $GITHUB_APP_AUTH_DEBUG ('1' or '2').",
    envvar="GITHUB_APP_AUTH_DEBUG",
)
@click.pass_context
def main(ctx, app_id, private_key, verbose):
    if verbose:
        logging.basicConfig(
            level=logging.INFO if verbose == 1 else logging.DEBUG,
            format="%(name)s %(message)s",
        )

    ctx.obj = AppIdentity(app_id=app_id, private_key=private_key)


@main.add_command
@click.command(help="Resolve app id/key and check app authentication.")
@pass_appidentity
@aiomain
async def current(appidentity: AppIdentity):
    async with aiohttp.ClientSession(
            headers=appidentity.app_headers(), ) as session:
        async with session.get('https://api.github.com/app', ) as resp:
            resp.raise_for_status()
            print(json.dumps(await resp.json(), indent=2))


@main.add_command
@click.command(help="Generate access token for installation.")
@pass_appidentity
@click.argument('account')
@aiomain
async def token(appidentity, account):
    print(await appidentity.installation_token_for(account))


@main.group(help="git-credential helper implementation.")
def credential():
    pass


@credential.add_command
@click.command(help="Credential storage helper implementation.")
@pass_appidentity
@click.argument('input', type=click.File('r'), default="-")
@click.argument('output', type=click.File('w'), default="-")
@aiomain
async def get(appidentity, input, output):
    # https://git-scm.com/docs/git-credential
    logger.debug("get id: %s input: %s output: %s", appidentity, input, output)
    output.write(await credential_helper(input.read(),
                                         appidentity.installation_token_for))
    output.write("\n")


@credential.command(help="no-op git-credential interface")
def store():
    pass


@credential.command(help="no-op git-credential interface")
def erase():
    pass


@main.group(help="github checks api support")
def check():
    pass


@check.add_command
@click.command()
@pass_appidentity
@click.argument('repo', type=str)
@click.argument('ref', type=str)
@aiomain
async def list(app: AppIdentity, repo: str, ref: str):
    """List current checks on given repo ref."""
    repo = RepoName.parse(repo)

    async with aiohttp.ClientSession(
            headers=await app.installation_headers(repo.owner)) as sesh:
        fetch = checks.GetRuns(owner=repo.owner, repo=repo.repo, ref=ref)
        print(await fetch.execute(sesh))


@check.add_command
@click.command()
@pass_appidentity
@click.argument('repo', type=str)
@click.argument('branch', type=str)
@click.argument('name', type=str)
@click.option('--sha', type=str, default=None)
@click.option('--output_title', type=str, default=None)
@click.option('--output_summary', type=str, default=None)
@click.option('--output', type=str, default=None)
@aiomain
async def push(
        app: AppIdentity,
        repo: str,
        branch: str,
        sha: str,
        name: str,
        output_title: str,
        output_summary: Optional[str],
        output: Optional[str],
):
    """Push a check to github."""
    repo = RepoName.parse(repo)
    output = load_job_output(output_title, output_summary, output)

    async with aiohttp.ClientSession(
            headers=await app.installation_headers(repo.owner)) as sesh:

        if not sha:
            logging.info("Resolving branch sha: %s", branch)
            ref_url = (
                f"https://api.github.com"
                f"/repos/{repo.owner}/{repo.repo}/git/refs/heads/{branch}"
            )
            logging.debug(ref_url)
            resp = await sesh.get(ref_url)
            logging.info(resp)
            sha = (await resp.json())["object"]["sha"]

        action = checks.CreateRun(
            owner=repo.owner,
            repo=repo.repo,
            run=checks.RunDetails(
                head_branch=branch,
                head_sha=sha,
                name=name,
                status=checks.Status.in_progress,
                output = output,
            ))

        async with action.execute(sesh) as resp:
            logging.debug(resp)

            try:
                resp.raise_for_status()
            except Exception:
                logging.exception((await resp.json())["message"])
                raise

            print(await resp.json())


@check.add_command
@click.command()
@pass_appidentity
@click.argument('repo', type=str)
@click.argument('id', type=str)
@click.argument('name', type=str)
@aiomain
async def update(
        app: AppIdentity,
        repo: str,
        id: str,
        name: str,
):
    """List current checks on given repo ref."""
    repo = RepoName.parse(repo)

    action = checks.UpdateRun(
        owner=repo.owner,
        repo=repo.repo,
        run=checks.RunDetails(
            id=id,
            name=name,
            status=checks.Status.in_progress,
        ))

    async with aiohttp.ClientSession(
            headers=await app.installation_headers(repo.owner)) as sesh:

        async with action.execute(sesh) as resp:
            logging.debug(resp)

            try:
                resp.raise_for_status()
            except Exception:
                logging.exception((await resp.json())["message"])
                raise

            print(await resp.json())


@check.add_command
@click.command()
@pass_appidentity
@click.option('--output_title', type=str, default=None)
@click.option('--output_summary', type=str, default=None)
@click.option('--output', type=str, default=None)
@aiomain
async def from_job_env(
    app: AppIdentity,
    output_title: str,
    output_summary: Optional[str],
    output: Optional[str],
):
    job_env = cattr.structure(dict(os.environ), jobs.JobEnviron)
    logging.info("job_env: %s", job_env)

    repo = RepoName.parse(job_env.BUILDKITE_REPO)

    async with aiohttp.ClientSession(
            headers=await app.installation_headers(repo.owner)) as sesh:

        current_runs = await checks.GetRuns(
            owner=repo.owner,
            repo=repo.repo,
            ref=job_env.BUILDKITE_COMMIT,
        ).execute(sesh)
        logging.info("current_runs: %s", current_runs)

        check_action = job_environ_to_check_action(job_env, current_runs)
        logging.info("action: %s", check_action)

        output = load_job_output(output_title, output_summary, output)
        if output:
            check_action.run.output = output

        await check_action.execute(sesh)

def load_job_output(output_title, output_summary, output):
    """Loads job output (maybe) from files, to be moved to handler layer."""
    def read_if_file(val):
        if os.path.exists(val):
            with open(val, "r") as inf:
                return inf.read()
        else:
            return val

    if output_title:
        assert output_summary
        output = checks.Output(
            title = output_title,
            summary = read_if_file(output_summary),
            text = read_if_file(output) if output else None
        )
    else:
        output = None

