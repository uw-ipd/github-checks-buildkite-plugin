import pytest

from ...github.gitcredentials import credential_helper

pytestmark = pytest.mark.asyncio


async def test_credential_helper():
    async def test_token(name):
        return {"test": "testtoken", "test2": "testtoken2"}.get(name)

    ssh = """
host=github.com
protocol=ssh
    """.strip()

    assert ssh == await credential_helper(ssh, test_token)

    no_path = """
host=github.com
protocol=https
    """.strip()

    assert no_path == await credential_helper(no_path, test_token)

    test_repo = """
host=github.com
protocol=https
path=test/repo
    """.strip()
    test_repo_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert test_repo_expected == await credential_helper(test_repo, test_token)

    test2_repo = """
host=github.com
protocol=https
path=test2/repo
    """.strip()
    test2_repo_expected = """
host=github.com
protocol=https
path=test2/repo
username=x-access-token
password=testtoken2
    """.strip()

    assert test2_repo_expected == await credential_helper(
        test2_repo, test_token)

    override_name = """
host=github.com
protocol=https
path=test/repo
username=user
    """.strip()
    override_name_expected = """
host=github.com
protocol=https
path=test/repo
username=x-access-token
password=testtoken
    """.strip()

    assert override_name_expected == await credential_helper(
        override_name, test_token)

    invalid_input = """
host=github.com
wat
    """.strip()
    with pytest.raises(ValueError):
        await credential_helper(invalid_input, test_token)
