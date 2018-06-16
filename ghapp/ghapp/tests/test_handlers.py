import os
import json

import pytest

import cattr

from ..buildkite import jobs
from ..github import checks

from ..handlers import job_hook_to_check_action, job_env_to_run_details


@pytest.fixture
def test_events():
    bd = os.path.dirname(__file__)

    return {
        "job.finished": json.load(open(bd + "/buildkite.job.finished.json")),
        "job.started": json.load(open(bd + "/buildkite.job.started.json")),
    }


def test_job_conversion(test_events):
    events = {
        k: cattr.structure(e, jobs.JobHook)
        for k, e in test_events.items()
    }

    init = job_hook_to_check_action(events["job.started"], [])
    assert isinstance(init, checks.CreateRun)

    conclude = job_hook_to_check_action(events["job.finished"], [init.run])
    assert isinstance(conclude, checks.UpdateRun)

    just_finished = job_hook_to_check_action(events["job.finished"], [])
    assert isinstance(just_finished, checks.CreateRun)


@pytest.fixture
def test_environs():
    return dict(
        post_timeout={
            'BUILDKITE':
            'true',
            'BUILDKITE_AGENT_DEBUG':
            'false',
            'BUILDKITE_AGENT_ENDPOINT':
            'https://agent.buildkite.com/v3',
            'BUILDKITE_AGENT_ID':
            '6931eb79-bcdc-4d8f-b0c6-97aa7aa91643',
            'BUILDKITE_AGENT_META_DATA_DOCKER':
            '1.13.1',
            'BUILDKITE_AGENT_META_DATA_HOST':
            'mako',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DEVICE':
            'GeForce_GTX_1050"',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DOCKER':
            '2.0.3',
            'BUILDKITE_AGENT_META_DATA_QUEUE':
            'default',
            'BUILDKITE_AGENT_NAME':
            'mako',
            'BUILDKITE_AGENT_PID':
            '7',
            'BUILDKITE_AGENT_TAGS':
            '"queue=default,host=mako,docker=1.13.1,nvidia_docker=2.0.3,nvidia_device=GeForce_GTX_1050"',
            'BUILDKITE_ARTIFACT_PATHS':
            '',
            'BUILDKITE_BIN_PATH':
            '/usr/local/bin',
            'BUILDKITE_BRANCH':
            'master',
            'BUILDKITE_BUILD_CHECKOUT_PATH':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'BUILDKITE_BUILD_CREATOR':
            'Alex Ford',
            'BUILDKITE_BUILD_CREATOR_EMAIL':
            'fordas@uw.edu',
            'BUILDKITE_BUILD_ID':
            'deefbbee-3bca-476f-b411-ae5d5573c11c',
            'BUILDKITE_BUILD_NUMBER':
            '17',
            'BUILDKITE_BUILD_PATH':
            '/buildkite/builds',
            'BUILDKITE_BUILD_URL':
            'https://buildkite.com/uw-ipd/test-checks/builds/17',
            'BUILDKITE_COMMAND':
            'sleep 120',
            'BUILDKITE_COMMAND_EVAL':
            'true',
            'BUILDKITE_COMMAND_EXIT_STATUS':
            '-1',
            'BUILDKITE_COMMIT':
            'e275658387fd2d5e0452c51c910fe214e391432b',
            'BUILDKITE_CONFIG_PATH':
            '',
            'BUILDKITE_ENV_FILE':
            '/tmp/job-env-063a5b46-02bc-444d-b394-ee3a6b1cca42248448946',
            'BUILDKITE_GIT_CLEAN_FLAGS':
            '-fxdq',
            'BUILDKITE_GIT_CLONE_FLAGS':
            '-v',
            'BUILDKITE_GIT_SUBMODULES':
            'true',
            'BUILDKITE_HOOKS_PATH':
            '/buildkite/hooks',
            'BUILDKITE_JOB_ID':
            '063a5b46-02bc-444d-b394-ee3a6b1cca42',
            'BUILDKITE_LABEL':
            'Teen Sleep',
            'BUILDKITE_LAST_HOOK_EXIT_STATUS':
            '0',
            'BUILDKITE_LOCAL_HOOKS_ENABLED':
            'true',
            'BUILDKITE_MESSAGE':
            'Get that teen sleep.',
            'BUILDKITE_ORGANIZATION_SLUG':
            'uw-ipd',
            'BUILDKITE_PIPELINE_DEFAULT_BRANCH':
            'master',
            'BUILDKITE_PIPELINE_PROVIDER':
            'github',
            'BUILDKITE_PIPELINE_SLUG':
            'test-checks',
            'BUILDKITE_PLUGINS':
            '[{"github.com/asford/github-checks-buildkite-plugin#f5a689":{"debug":true}}]',
            'BUILDKITE_PLUGINS_ENABLED':
            'true',
            'BUILDKITE_PLUGINS_PATH':
            '/buildkite/plugins',
            'BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG':
            'true',
            'BUILDKITE_PROJECT_PROVIDER':
            'github',
            'BUILDKITE_PROJECT_SLUG':
            'uw-ipd/test-checks',
            'BUILDKITE_PULL_REQUEST':
            'false',
            'BUILDKITE_PULL_REQUEST_BASE_BRANCH':
            '',
            'BUILDKITE_PULL_REQUEST_REPO':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_ID':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_NUMBER':
            '',
            'BUILDKITE_REPO':
            'https://github.com/asford/test_checks',
            'BUILDKITE_RETRY_COUNT':
            '0',
            'BUILDKITE_SCRIPT_PATH':
            'sleep 120',
            'BUILDKITE_SHELL':
            '/bin/bash -e -c',
            'BUILDKITE_SOURCE':
            'webhook',
            'BUILDKITE_SSH_KEYSCAN':
            'true',
            'BUILDKITE_TAG':
            '',
            'BUILDKITE_TIMEOUT':
            '1',
            'BUILDKITE_TRIGGERED_FROM_BUILD_ID':
            '',
            'CI':
            'true',
            'CUDA_DEVICE_ORDER':
            'PCI_BUS_ID',
            'CUDA_VISIBLE_DEVICES':
            '1',
            'GITHUB_APP_AUTH_ID':
            '/buildkite-secrets/buildkite-agent.id',
            'GITHUB_APP_AUTH_KEY':
            '/buildkite-secrets/buildkite-agent.private-key.pem',
            'GIT_TERMINAL_PROMPT':
            '0',
            'HOME':
            '/root',
            'HOSTNAME':
            '6a08f8bc81ff',
            'OLDPWD':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'PATH':
            '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'PWD':
            '/buildkite/plugins/github-com-asford-github-checks-buildkite-plugin-f5a689',
            'SHLVL':
            '2',
            '_':
            '/usr/bin/python3'
        },
        pre_success={
            'BUILDKITE':
            'true',
            'BUILDKITE_AGENT_DEBUG':
            'false',
            'BUILDKITE_AGENT_ENDPOINT':
            'https://agent.buildkite.com/v3',
            'BUILDKITE_AGENT_ID':
            '6931eb79-bcdc-4d8f-b0c6-97aa7aa91643',
            'BUILDKITE_AGENT_META_DATA_DOCKER':
            '1.13.1',
            'BUILDKITE_AGENT_META_DATA_HOST':
            'mako',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DEVICE':
            'GeForce_GTX_1050"',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DOCKER':
            '2.0.3',
            'BUILDKITE_AGENT_META_DATA_QUEUE':
            'default',
            'BUILDKITE_AGENT_NAME':
            'mako',
            'BUILDKITE_AGENT_PID':
            '7',
            'BUILDKITE_AGENT_TAGS':
            '"queue=default,host=mako,docker=1.13.1,nvidia_docker=2.0.3,nvidia_device=GeForce_GTX_1050"',
            'BUILDKITE_ARTIFACT_PATHS':
            '',
            'BUILDKITE_BIN_PATH':
            '/usr/local/bin',
            'BUILDKITE_BRANCH':
            'master',
            'BUILDKITE_BUILD_CHECKOUT_PATH':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'BUILDKITE_BUILD_CREATOR':
            'Alex Ford',
            'BUILDKITE_BUILD_CREATOR_EMAIL':
            'fordas@uw.edu',
            'BUILDKITE_BUILD_ID':
            'c9fb2bb8-99d5-41d9-aa3d-27ef919f91f3',
            'BUILDKITE_BUILD_NUMBER':
            '15',
            'BUILDKITE_BUILD_PATH':
            '/buildkite/builds',
            'BUILDKITE_BUILD_URL':
            'https://buildkite.com/uw-ipd/test-checks/builds/15',
            'BUILDKITE_COMMAND':
            'sleep 3',
            'BUILDKITE_COMMAND_EVAL':
            'true',
            'BUILDKITE_COMMIT':
            'df998e034720a29ecc301e3d1cc80a3dad085492',
            'BUILDKITE_CONFIG_PATH':
            '',
            'BUILDKITE_ENV_FILE':
            '/tmp/job-env-c498dd9c-77d0-42de-be6d-811d9c5156cc739700638',
            'BUILDKITE_GIT_CLEAN_FLAGS':
            '-fxdq',
            'BUILDKITE_GIT_CLONE_FLAGS':
            '-v',
            'BUILDKITE_GIT_SUBMODULES':
            'true',
            'BUILDKITE_HOOKS_PATH':
            '/buildkite/hooks',
            'BUILDKITE_JOB_ID':
            'c498dd9c-77d0-42de-be6d-811d9c5156cc',
            'BUILDKITE_LABEL':
            'Sleepy',
            'BUILDKITE_LOCAL_HOOKS_ENABLED':
            'true',
            'BUILDKITE_MESSAGE':
            'Update plugin.',
            'BUILDKITE_ORGANIZATION_SLUG':
            'uw-ipd',
            'BUILDKITE_PIPELINE_DEFAULT_BRANCH':
            'master',
            'BUILDKITE_PIPELINE_PROVIDER':
            'github',
            'BUILDKITE_PIPELINE_SLUG':
            'test-checks',
            'BUILDKITE_PLUGINS':
            '[{"github.com/asford/github-checks-buildkite-plugin#f5a689":{"debug":true}}]',
            'BUILDKITE_PLUGINS_ENABLED':
            'true',
            'BUILDKITE_PLUGINS_PATH':
            '/buildkite/plugins',
            'BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG':
            'true',
            'BUILDKITE_PROJECT_PROVIDER':
            'github',
            'BUILDKITE_PROJECT_SLUG':
            'uw-ipd/test-checks',
            'BUILDKITE_PULL_REQUEST':
            'false',
            'BUILDKITE_PULL_REQUEST_BASE_BRANCH':
            '',
            'BUILDKITE_PULL_REQUEST_REPO':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_ID':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_NUMBER':
            '',
            'BUILDKITE_REPO':
            'https://github.com/asford/test_checks',
            'BUILDKITE_RETRY_COUNT':
            '0',
            'BUILDKITE_SCRIPT_PATH':
            'sleep 3',
            'BUILDKITE_SHELL':
            '/bin/bash -e -c',
            'BUILDKITE_SOURCE':
            'webhook',
            'BUILDKITE_SSH_KEYSCAN':
            'true',
            'BUILDKITE_TAG':
            '',
            'BUILDKITE_TIMEOUT':
            'false',
            'BUILDKITE_TRIGGERED_FROM_BUILD_ID':
            '',
            'CI':
            'true',
            'CUDA_DEVICE_ORDER':
            'PCI_BUS_ID',
            'CUDA_VISIBLE_DEVICES':
            '1',
            'GITHUB_APP_AUTH_ID':
            '/buildkite-secrets/buildkite-agent.id',
            'GITHUB_APP_AUTH_KEY':
            '/buildkite-secrets/buildkite-agent.private-key.pem',
            'GIT_TERMINAL_PROMPT':
            '0',
            'HOME':
            '/root',
            'HOSTNAME':
            '6a08f8bc81ff',
            'OLDPWD':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'PATH':
            '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'PWD':
            '/buildkite/plugins/github-com-asford-github-checks-buildkite-plugin-f5a689',
            'SHLVL':
            '2',
            '_':
            '/usr/bin/python3'
        },
        post_success={
            'BUILDKITE':
            'true',
            'BUILDKITE_AGENT_DEBUG':
            'false',
            'BUILDKITE_AGENT_ENDPOINT':
            'https://agent.buildkite.com/v3',
            'BUILDKITE_AGENT_ID':
            '6931eb79-bcdc-4d8f-b0c6-97aa7aa91643',
            'BUILDKITE_AGENT_META_DATA_DOCKER':
            '1.13.1',
            'BUILDKITE_AGENT_META_DATA_HOST':
            'mako',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DEVICE':
            'GeForce_GTX_1050"',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DOCKER':
            '2.0.3',
            'BUILDKITE_AGENT_META_DATA_QUEUE':
            'default',
            'BUILDKITE_AGENT_NAME':
            'mako',
            'BUILDKITE_AGENT_PID':
            '7',
            'BUILDKITE_AGENT_TAGS':
            '"queue=default,host=mako,docker=1.13.1,nvidia_docker=2.0.3,nvidia_device=GeForce_GTX_1050"',
            'BUILDKITE_ARTIFACT_PATHS':
            '',
            'BUILDKITE_BIN_PATH':
            '/usr/local/bin',
            'BUILDKITE_BRANCH':
            'master',
            'BUILDKITE_BUILD_CHECKOUT_PATH':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'BUILDKITE_BUILD_CREATOR':
            'Alex Ford',
            'BUILDKITE_BUILD_CREATOR_EMAIL':
            'fordas@uw.edu',
            'BUILDKITE_BUILD_ID':
            'c9fb2bb8-99d5-41d9-aa3d-27ef919f91f3',
            'BUILDKITE_BUILD_NUMBER':
            '15',
            'BUILDKITE_BUILD_PATH':
            '/buildkite/builds',
            'BUILDKITE_BUILD_URL':
            'https://buildkite.com/uw-ipd/test-checks/builds/15',
            'BUILDKITE_COMMAND':
            'sleep 3',
            'BUILDKITE_COMMAND_EVAL':
            'true',
            'BUILDKITE_COMMAND_EXIT_STATUS':
            '0',
            'BUILDKITE_COMMIT':
            'df998e034720a29ecc301e3d1cc80a3dad085492',
            'BUILDKITE_CONFIG_PATH':
            '',
            'BUILDKITE_ENV_FILE':
            '/tmp/job-env-c498dd9c-77d0-42de-be6d-811d9c5156cc739700638',
            'BUILDKITE_GIT_CLEAN_FLAGS':
            '-fxdq',
            'BUILDKITE_GIT_CLONE_FLAGS':
            '-v',
            'BUILDKITE_GIT_SUBMODULES':
            'true',
            'BUILDKITE_HOOKS_PATH':
            '/buildkite/hooks',
            'BUILDKITE_JOB_ID':
            'c498dd9c-77d0-42de-be6d-811d9c5156cc',
            'BUILDKITE_LABEL':
            'Sleepy',
            'BUILDKITE_LAST_HOOK_EXIT_STATUS':
            '0',
            'BUILDKITE_LOCAL_HOOKS_ENABLED':
            'true',
            'BUILDKITE_MESSAGE':
            'Update plugin.',
            'BUILDKITE_ORGANIZATION_SLUG':
            'uw-ipd',
            'BUILDKITE_PIPELINE_DEFAULT_BRANCH':
            'master',
            'BUILDKITE_PIPELINE_PROVIDER':
            'github',
            'BUILDKITE_PIPELINE_SLUG':
            'test-checks',
            'BUILDKITE_PLUGINS':
            '[{"github.com/asford/github-checks-buildkite-plugin#f5a689":{"debug":true}}]',
            'BUILDKITE_PLUGINS_ENABLED':
            'true',
            'BUILDKITE_PLUGINS_PATH':
            '/buildkite/plugins',
            'BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG':
            'true',
            'BUILDKITE_PROJECT_PROVIDER':
            'github',
            'BUILDKITE_PROJECT_SLUG':
            'uw-ipd/test-checks',
            'BUILDKITE_PULL_REQUEST':
            'false',
            'BUILDKITE_PULL_REQUEST_BASE_BRANCH':
            '',
            'BUILDKITE_PULL_REQUEST_REPO':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_ID':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_NUMBER':
            '',
            'BUILDKITE_REPO':
            'https://github.com/asford/test_checks',
            'BUILDKITE_RETRY_COUNT':
            '0',
            'BUILDKITE_SCRIPT_PATH':
            'sleep 3',
            'BUILDKITE_SHELL':
            '/bin/bash -e -c',
            'BUILDKITE_SOURCE':
            'webhook',
            'BUILDKITE_SSH_KEYSCAN':
            'true',
            'BUILDKITE_TAG':
            '',
            'BUILDKITE_TIMEOUT':
            'false',
            'BUILDKITE_TRIGGERED_FROM_BUILD_ID':
            '',
            'CI':
            'true',
            'CUDA_DEVICE_ORDER':
            'PCI_BUS_ID',
            'CUDA_VISIBLE_DEVICES':
            '1',
            'GITHUB_APP_AUTH_ID':
            '/buildkite-secrets/buildkite-agent.id',
            'GITHUB_APP_AUTH_KEY':
            '/buildkite-secrets/buildkite-agent.private-key.pem',
            'GIT_TERMINAL_PROMPT':
            '0',
            'HOME':
            '/root',
            'HOSTNAME':
            '6a08f8bc81ff',
            'OLDPWD':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'PATH':
            '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'PWD':
            '/buildkite/plugins/github-com-asford-github-checks-buildkite-plugin-f5a689',
            'SHLVL':
            '2',
            '_':
            '/usr/bin/python3'
        },
        pre_failure={
            'BUILDKITE':
            'true',
            'BUILDKITE_AGENT_DEBUG':
            'false',
            'BUILDKITE_AGENT_ENDPOINT':
            'https://agent.buildkite.com/v3',
            'BUILDKITE_AGENT_ID':
            '6931eb79-bcdc-4d8f-b0c6-97aa7aa91643',
            'BUILDKITE_AGENT_META_DATA_DOCKER':
            '1.13.1',
            'BUILDKITE_AGENT_META_DATA_HOST':
            'mako',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DEVICE':
            'GeForce_GTX_1050"',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DOCKER':
            '2.0.3',
            'BUILDKITE_AGENT_META_DATA_QUEUE':
            'default',
            'BUILDKITE_AGENT_NAME':
            'mako',
            'BUILDKITE_AGENT_PID':
            '7',
            'BUILDKITE_AGENT_TAGS':
            '"queue=default,host=mako,docker=1.13.1,nvidia_docker=2.0.3,nvidia_device=GeForce_GTX_1050"',
            'BUILDKITE_ARTIFACT_PATHS':
            '',
            'BUILDKITE_BIN_PATH':
            '/usr/local/bin',
            'BUILDKITE_BRANCH':
            'master',
            'BUILDKITE_BUILD_CHECKOUT_PATH':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'BUILDKITE_BUILD_CREATOR':
            'Alex Ford',
            'BUILDKITE_BUILD_CREATOR_EMAIL':
            'fordas@uw.edu',
            'BUILDKITE_BUILD_ID':
            'c9fb2bb8-99d5-41d9-aa3d-27ef919f91f3',
            'BUILDKITE_BUILD_NUMBER':
            '15',
            'BUILDKITE_BUILD_PATH':
            '/buildkite/builds',
            'BUILDKITE_BUILD_URL':
            'https://buildkite.com/uw-ipd/test-checks/builds/15',
            'BUILDKITE_COMMAND':
            'exit 1',
            'BUILDKITE_COMMAND_EVAL':
            'true',
            'BUILDKITE_COMMIT':
            'df998e034720a29ecc301e3d1cc80a3dad085492',
            'BUILDKITE_CONFIG_PATH':
            '',
            'BUILDKITE_ENV_FILE':
            '/tmp/job-env-382571ad-af38-40d1-b418-46af6b438ae1893225573',
            'BUILDKITE_GIT_CLEAN_FLAGS':
            '-fxdq',
            'BUILDKITE_GIT_CLONE_FLAGS':
            '-v',
            'BUILDKITE_GIT_SUBMODULES':
            'true',
            'BUILDKITE_HOOKS_PATH':
            '/buildkite/hooks',
            'BUILDKITE_JOB_ID':
            '382571ad-af38-40d1-b418-46af6b438ae1',
            'BUILDKITE_LABEL':
            'Error',
            'BUILDKITE_LOCAL_HOOKS_ENABLED':
            'true',
            'BUILDKITE_MESSAGE':
            'Update plugin.',
            'BUILDKITE_ORGANIZATION_SLUG':
            'uw-ipd',
            'BUILDKITE_PIPELINE_DEFAULT_BRANCH':
            'master',
            'BUILDKITE_PIPELINE_PROVIDER':
            'github',
            'BUILDKITE_PIPELINE_SLUG':
            'test-checks',
            'BUILDKITE_PLUGINS':
            '[{"github.com/asford/github-checks-buildkite-plugin#f5a689":{"debug":true}}]',
            'BUILDKITE_PLUGINS_ENABLED':
            'true',
            'BUILDKITE_PLUGINS_PATH':
            '/buildkite/plugins',
            'BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG':
            'true',
            'BUILDKITE_PROJECT_PROVIDER':
            'github',
            'BUILDKITE_PROJECT_SLUG':
            'uw-ipd/test-checks',
            'BUILDKITE_PULL_REQUEST':
            'false',
            'BUILDKITE_PULL_REQUEST_BASE_BRANCH':
            '',
            'BUILDKITE_PULL_REQUEST_REPO':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_ID':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_NUMBER':
            '',
            'BUILDKITE_REPO':
            'https://github.com/asford/test_checks',
            'BUILDKITE_RETRY_COUNT':
            '0',
            'BUILDKITE_SCRIPT_PATH':
            'exit 1',
            'BUILDKITE_SHELL':
            '/bin/bash -e -c',
            'BUILDKITE_SOURCE':
            'webhook',
            'BUILDKITE_SSH_KEYSCAN':
            'true',
            'BUILDKITE_TAG':
            '',
            'BUILDKITE_TIMEOUT':
            'false',
            'BUILDKITE_TRIGGERED_FROM_BUILD_ID':
            '',
            'CI':
            'true',
            'CUDA_DEVICE_ORDER':
            'PCI_BUS_ID',
            'CUDA_VISIBLE_DEVICES':
            '1',
            'GITHUB_APP_AUTH_ID':
            '/buildkite-secrets/buildkite-agent.id',
            'GITHUB_APP_AUTH_KEY':
            '/buildkite-secrets/buildkite-agent.private-key.pem',
            'GIT_TERMINAL_PROMPT':
            '0',
            'HOME':
            '/root',
            'HOSTNAME':
            '6a08f8bc81ff',
            'OLDPWD':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'PATH':
            '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'PWD':
            '/buildkite/plugins/github-com-asford-github-checks-buildkite-plugin-f5a689',
            'SHLVL':
            '2',
            '_':
            '/usr/bin/python3'
        },
        post_failure={
            'BUILDKITE':
            'true',
            'BUILDKITE_AGENT_DEBUG':
            'false',
            'BUILDKITE_AGENT_ENDPOINT':
            'https://agent.buildkite.com/v3',
            'BUILDKITE_AGENT_ID':
            '6931eb79-bcdc-4d8f-b0c6-97aa7aa91643',
            'BUILDKITE_AGENT_META_DATA_DOCKER':
            '1.13.1',
            'BUILDKITE_AGENT_META_DATA_HOST':
            'mako',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DEVICE':
            'GeForce_GTX_1050"',
            'BUILDKITE_AGENT_META_DATA_NVIDIA_DOCKER':
            '2.0.3',
            'BUILDKITE_AGENT_META_DATA_QUEUE':
            'default',
            'BUILDKITE_AGENT_NAME':
            'mako',
            'BUILDKITE_AGENT_PID':
            '7',
            'BUILDKITE_AGENT_TAGS':
            '"queue=default,host=mako,docker=1.13.1,nvidia_docker=2.0.3,nvidia_device=GeForce_GTX_1050"',
            'BUILDKITE_ARTIFACT_PATHS':
            '',
            'BUILDKITE_BIN_PATH':
            '/usr/local/bin',
            'BUILDKITE_BRANCH':
            'master',
            'BUILDKITE_BUILD_CHECKOUT_PATH':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'BUILDKITE_BUILD_CREATOR':
            'Alex Ford',
            'BUILDKITE_BUILD_CREATOR_EMAIL':
            'fordas@uw.edu',
            'BUILDKITE_BUILD_ID':
            'c9fb2bb8-99d5-41d9-aa3d-27ef919f91f3',
            'BUILDKITE_BUILD_NUMBER':
            '15',
            'BUILDKITE_BUILD_PATH':
            '/buildkite/builds',
            'BUILDKITE_BUILD_URL':
            'https://buildkite.com/uw-ipd/test-checks/builds/15',
            'BUILDKITE_COMMAND':
            'exit 1',
            'BUILDKITE_COMMAND_EVAL':
            'true',
            'BUILDKITE_COMMAND_EXIT_STATUS':
            '1',
            'BUILDKITE_COMMIT':
            'df998e034720a29ecc301e3d1cc80a3dad085492',
            'BUILDKITE_CONFIG_PATH':
            '',
            'BUILDKITE_ENV_FILE':
            '/tmp/job-env-382571ad-af38-40d1-b418-46af6b438ae1893225573',
            'BUILDKITE_GIT_CLEAN_FLAGS':
            '-fxdq',
            'BUILDKITE_GIT_CLONE_FLAGS':
            '-v',
            'BUILDKITE_GIT_SUBMODULES':
            'true',
            'BUILDKITE_HOOKS_PATH':
            '/buildkite/hooks',
            'BUILDKITE_JOB_ID':
            '382571ad-af38-40d1-b418-46af6b438ae1',
            'BUILDKITE_LABEL':
            'Error',
            'BUILDKITE_LAST_HOOK_EXIT_STATUS':
            '0',
            'BUILDKITE_LOCAL_HOOKS_ENABLED':
            'true',
            'BUILDKITE_MESSAGE':
            'Update plugin.',
            'BUILDKITE_ORGANIZATION_SLUG':
            'uw-ipd',
            'BUILDKITE_PIPELINE_DEFAULT_BRANCH':
            'master',
            'BUILDKITE_PIPELINE_PROVIDER':
            'github',
            'BUILDKITE_PIPELINE_SLUG':
            'test-checks',
            'BUILDKITE_PLUGINS':
            '[{"github.com/asford/github-checks-buildkite-plugin#f5a689":{"debug":true}}]',
            'BUILDKITE_PLUGINS_ENABLED':
            'true',
            'BUILDKITE_PLUGINS_PATH':
            '/buildkite/plugins',
            'BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG':
            'true',
            'BUILDKITE_PROJECT_PROVIDER':
            'github',
            'BUILDKITE_PROJECT_SLUG':
            'uw-ipd/test-checks',
            'BUILDKITE_PULL_REQUEST':
            'false',
            'BUILDKITE_PULL_REQUEST_BASE_BRANCH':
            '',
            'BUILDKITE_PULL_REQUEST_REPO':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_ID':
            '',
            'BUILDKITE_REBUILT_FROM_BUILD_NUMBER':
            '',
            'BUILDKITE_REPO':
            'https://github.com/asford/test_checks',
            'BUILDKITE_RETRY_COUNT':
            '0',
            'BUILDKITE_SCRIPT_PATH':
            'exit 1',
            'BUILDKITE_SHELL':
            '/bin/bash -e -c',
            'BUILDKITE_SOURCE':
            'webhook',
            'BUILDKITE_SSH_KEYSCAN':
            'true',
            'BUILDKITE_TAG':
            '',
            'BUILDKITE_TIMEOUT':
            'false',
            'BUILDKITE_TRIGGERED_FROM_BUILD_ID':
            '',
            'CI':
            'true',
            'CUDA_DEVICE_ORDER':
            'PCI_BUS_ID',
            'CUDA_VISIBLE_DEVICES':
            '1',
            'GITHUB_APP_AUTH_ID':
            '/buildkite-secrets/buildkite-agent.id',
            'GITHUB_APP_AUTH_KEY':
            '/buildkite-secrets/buildkite-agent.private-key.pem',
            'GIT_TERMINAL_PROMPT':
            '0',
            'HOME':
            '/root',
            'HOSTNAME':
            '6a08f8bc81ff',
            'OLDPWD':
            '/buildkite/builds/mako/uw-ipd/test-checks',
            'PATH':
            '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
            'PWD':
            '/buildkite/plugins/github-com-asford-github-checks-buildkite-plugin-f5a689',
            'SHLVL':
            '2',
            '_':
            '/usr/bin/python3'
        },
    )


def test_check_from_job_env(test_environs):
    start_check = job_env_to_run_details(cattr.structure(test_environs["pre_success"], jobs.JobEnviron))

    assert start_check.name == "Sleepy"
    assert start_check.external_id == "c498dd9c-77d0-42de-be6d-811d9c5156cc"
    assert start_check.head_sha == "df998e034720a29ecc301e3d1cc80a3dad085492"
    assert start_check.head_branch == "master"
    assert start_check.details_url == "https://buildkite.com/uw-ipd/test-checks/builds/15#c498dd9c-77d0-42de-be6d-811d9c5156cc"
    assert start_check.external_id == "c498dd9c-77d0-42de-be6d-811d9c5156cc"
    assert start_check.started_at is not None
    assert start_check.status == checks.Status.in_progress
    assert start_check.conclusion is None
    assert start_check.completed_at is None
    assert start_check.output is None

    end_check = job_env_to_run_details(cattr.structure(test_environs["post_success"], jobs.JobEnviron))

    assert end_check.name == "Sleepy"
    assert end_check.head_sha == "df998e034720a29ecc301e3d1cc80a3dad085492"
    assert end_check.head_branch == "master"
    assert end_check.details_url == "https://buildkite.com/uw-ipd/test-checks/builds/15#c498dd9c-77d0-42de-be6d-811d9c5156cc"
    assert end_check.external_id == "c498dd9c-77d0-42de-be6d-811d9c5156cc"
    assert end_check.started_at is None
    assert end_check.status == checks.Status.completed
    assert end_check.conclusion == checks.Conclusion.success
    assert end_check.completed_at is not None
    assert end_check.output is None

    fail_check = job_env_to_run_details(cattr.structure(test_environs["post_failure"], jobs.JobEnviron))

    assert fail_check.name == "Error"
    assert fail_check.head_sha == "df998e034720a29ecc301e3d1cc80a3dad085492"
    assert fail_check.head_branch == "master"
    assert fail_check.details_url == "https://buildkite.com/uw-ipd/test-checks/builds/15#382571ad-af38-40d1-b418-46af6b438ae1"
    assert fail_check.external_id == "382571ad-af38-40d1-b418-46af6b438ae1"
    assert fail_check.started_at is None
    assert fail_check.status == checks.Status.completed
    assert fail_check.conclusion == checks.Conclusion.failure
    assert fail_check.completed_at is not None
    assert fail_check.output is None

    timeout_check = job_env_to_run_details(cattr.structure(test_environs["post_timeout"], jobs.JobEnviron))

    assert timeout_check.name == "Teen Sleep"
    assert timeout_check.head_sha == "e275658387fd2d5e0452c51c910fe214e391432b"
    assert timeout_check.head_branch == "master"
    assert timeout_check.details_url == "https://buildkite.com/uw-ipd/test-checks/builds/17#063a5b46-02bc-444d-b394-ee3a6b1cca42"
    assert timeout_check.external_id == "063a5b46-02bc-444d-b394-ee3a6b1cca42"
    assert timeout_check.started_at is None
    assert timeout_check.status == checks.Status.completed
    assert timeout_check.conclusion == checks.Conclusion.timed_out
    assert timeout_check.completed_at is not None
    assert timeout_check.output is None
