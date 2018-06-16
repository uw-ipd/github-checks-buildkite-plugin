import os
import contextlib

from ...github.identity import AppIdentity

@contextlib.contextmanager
def set_env(**environ):
    """
    Temporarily set the process environment variables.

    See:
    https://stackoverflow.com/questions/2059482/python-temporarily-modify-the-current-processs-environment

    >>> with set_env(PLUGINS_DIR=u'test/plugins'):
    ...   "PLUGINS_DIR" in os.environ
    True

    >>> "PLUGINS_DIR" in os.environ
    False

    :type environ: dict[str, unicode]
    :param environ: Environment variables to set
    """
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)

def test_appidentity(tmpdir):

    test_key = """
-----BEGIN RSA PRIVATE KEY-----
sekrats
-----END RSA PRIVATE KEY-----
"""
    test_key_file = tmpdir.join("key.pem")
    test_key_file.write_text(test_key, ensure=True, encoding=None)

    test_id = 1663
    test_id_file = tmpdir.join("id")
    test_id_file.write_text(str(test_id), ensure=True, encoding=None)

    with set_env(**{AppIdentity.PRIVATE_KEY_ENV_VAR: test_key, AppIdentity.APP_ID_ENV_VAR: str(test_id)}):
        # Test resolution of id from environment
        i = AppIdentity()
        assert i.private_key == test_key
        assert i.app_id == test_id

        # Test override of variables and type coercion
        i = AppIdentity(app_id = str(test_id + 1))
        assert i.private_key == test_key
        assert i.app_id == test_id + 1

        i = AppIdentity(private_key = test_key.replace("sekrats", "secrets"))
        assert i.private_key == test_key.replace("sekrats", "secrets")
        assert i.app_id == test_id

    with set_env(**{AppIdentity.PRIVATE_KEY_ENV_VAR: str(test_key_file), AppIdentity.APP_ID_ENV_VAR: str(test_id_file)}):
        # Test resolution of id from env filenames
        i = AppIdentity()
        assert i.private_key == test_key
        assert i.app_id == test_id

    # Test resolution of id from filenames
    i = AppIdentity(private_key = str(test_key_file), app_id = str(test_id_file))
