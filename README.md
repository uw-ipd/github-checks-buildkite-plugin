# Git Checks Buildkite Plugin 

A [Buildkite plugin](https://buildkite.com/docs/agent/v3/plugins) for uploading pipeline status via the Github [checks API](https://developer.github.com/v3/checks/).


## Example

Checks are limited to displaying markdown formatted output, which this plugin
will faithfully pipe from your build via the checks API. For example, this script:

```bash
# pytest.sh
{
  echo '# pytest'
  echo '```'
  pytest -v
  echo '```'
} > pytest_summary.md
```

can be reported via:

```yml
  - label: Pytest
    command: test.sh
    plugins:
      - uw-ipd/github-checks#v0.0.2:
          output_title: pytest
          output_summary: pytest_summary.md
```

See this plugin's [pipeline.yml](.buildkite/pipeline.yml) and
[checks](https://github.com/uw-ipd/github-checks-buildkite-plugin/pull/6/checks)
for details.

## Setup

The plugin interacts with Github via application credentials, which are best
managed by [creating a private application](https://developer.github.com/apps/building-github-apps/creating-a-github-app/).
Feel free to direct webhooks to [`/dev/null`](https://devnull-as-a-service.com/dev/null).
The application *requires* read/write permissions for the checks API.

Make an application id and private-key available to your `buildkite-agent` by
whatever means necessary, remembering that a `private-key.pem` is serious
sekrat business. The `GITHUB_APP_AUTH_ID` and `GITHUB_APP_AUTH_KEY` environment
variables can be used to indicate a file containing the key/id (ideal) or
directly specify the id/key value (not so ideal) as env vars.

Now that you've gone to the trouble of registering an app, why not simplify
your private-repo access credentials? Check out
[git-credential-github-app-auth](https://github.com/uw-ipd/git-credential-github-app-auth).

The hook uses `docker-compose` to manage setup and execution. To upload local
build products the current working directory _must_ be available as a docker
mount. Set `BUILDKITE_DOCKER_DEFAULT_VOLUMES` in your agent environment hook
to ensure that that `BUILDKITE_BUILD_CHECKOUT_PATH` is available. (eg. `export
BUILDKITE_DOCKER_DEFAULT_VOLUMES=/buildkite/builds:/buildkite/builds`)

## Configuration

### `output_title` (optional str)
### `output_summary` (optional path or str)
### `output_details` (optional path or str)

Specify check report output, as either inline strings *or* paths of build
products relative to the build root. If `output_title` is specified then
`output_summary` must be provided. Both the summary and details are rendered as
markdown.

### `app_id` (optional path or str)

Override the Github application id, otherwise defaulting to the agent
environment value `GITHUB_APP_AUTH_ID`.

### `private_key` (optional path or str)

Override the Github application private key, otherwise defaulting to the agent
environment value `GITHUB_APP_AUTH_KEY`.

### `debug` (optional boolean)

Enable debug-level logging of plugin actions.

## License

MIT (see [LICENSE](LICENSE))
