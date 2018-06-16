# Git Checks Buildkite Plugin 

A [Buildkite plugin](https://buildkite.com/docs/agent/v3/plugins) for uploading pipeline status via the Github [checks API](https://developer.github.com/v3/checks/).


## Example

The following pipeline will run `yarn install` and `yarn run test` inside a Docker container using the [node:7 Docker image](https://hub.docker.com/_/node/):

```yml
steps:
  - label: sleep
    command: sleep 15
    plugins:
      uw-ipd/github-checks#master
```

## Configuration

## License

MIT (see [LICENSE](LICENSE))
