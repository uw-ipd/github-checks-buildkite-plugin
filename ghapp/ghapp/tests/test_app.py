import pytest
import os
import hmac

from ..app import Main, BuildkiteHooks, GithubHooks


@pytest.fixture
def github_ping_body():
    with open(os.path.dirname(__file__) + "/github.ping.json", "rb") as inf:
        return inf.read()


@pytest.fixture
def github_ping_secret(github_ping_body):
    return "github"


@pytest.fixture
def buildkite_ping_body():
    with open(os.path.dirname(__file__) + "/buildkite.ping.json", "rb") as inf:
        return inf.read()


@pytest.fixture
def buildkite_ping_secret():
    return "buildkite"


async def test_zen(
        test_client,
        github_ping_body,
        github_ping_secret,
        buildkite_ping_body,
        buildkite_ping_secret,
        monkeypatch,
):
    monkeypatch.setenv(GithubHooks.SECRET_ENV_VAR, github_ping_secret)
    monkeypatch.setenv(BuildkiteHooks.SECRET_ENV_VAR, buildkite_ping_secret)

    client = await test_client(lambda loop: Main.setup(loop=loop).app)

    resp = await client.get('/')
    assert resp.status == 404

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "The mind is a blank canvas."

    resp = await client.post(
        "/webhooks/github",
        headers={
            "X-GitHub-Event":
            "ping",
            "X-Hub-Signature":
            'sha1=' + hmac.new(
                github_ping_secret.encode(), msg=github_ping_body,
                digestmod='sha1').hexdigest(),
            "content-type":
            "application/json",
        },
        data=github_ping_body)
    assert resp.status == 200, await resp.text()

    resp = await client.get('/zen')
    assert resp.status == 200
    text = await resp.text()
    assert text == "Practicality beats purity."

    resp = await client.post(
        "/webhooks/buildkite",
        headers={
            "X-Buildkite-Event": "ping",
            "X-Buildkite-Token": buildkite_ping_secret,
            "content-type": "application/json",
        },
        data=buildkite_ping_body)
    assert resp.status == 200, await resp.text()
