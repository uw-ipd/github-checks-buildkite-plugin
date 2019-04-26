#!/usr/bin/env bats

load '/usr/local/lib/bats/load.bash'

@test "pre-command" {
  export DCYML=$PWD/hooks/../docker-compose.yml

  stub docker-compose \
    "-f ${DCYML} build ghapp : echo build ghapp" \
    "-f ${DCYML} run --workdir=${PWD} --rm ghapp -v check from-job-env : echo run ghapp" \
    "-f ${DCYML} down  : echo down"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose
}

@test "debug mode" {
  export DCYML=$PWD/hooks/../docker-compose.yml

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG=true

  stub docker-compose \
    "-f ${DCYML} build ghapp : echo build ghapp" \
    "-f ${DCYML} run --workdir=${PWD} --rm ghapp -vv check from-job-env : echo run ghapp" \
    "-f ${DCYML} down  : echo down"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG
}

@test "output title and summary" {
  # Output is only included on post-command hook.
  export DCYML=$PWD/hooks/../docker-compose.yml

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_OUTPUT_TITLE=Test
  export BUILDKITE_PLUGIN_GITHUB_CHECKS_OUTPUT_SUMMARY=summary.md

  stub docker-compose \
    "-f ${DCYML} build ghapp : echo build ghapp" \
    "-f ${DCYML} run --workdir=${PWD} --rm ghapp -v check from-job-env : echo run ghapp" \
    "-f ${DCYML} down  : echo down"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose

  stub docker-compose \
    "-f ${DCYML} build ghapp : echo build ghapp" \
    "-f ${DCYML} run --workdir=${PWD} --rm ghapp -v check from-job-env --output_title Test --output_summary summary.md : echo run ghapp" \
    "-f ${DCYML} down  : echo down"

  run $PWD/hooks/post-command

  assert_success

  unstub docker-compose

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_OUTPUT_TITLE
  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_OUTPUT_SUMMARY

}

@test "BUILDKITE_DOCKER_DEFAULT_VOLUMES support" {
  export DCYML=$PWD/hooks/../docker-compose.yml
  export BUILDKITE_DOCKER_DEFAULT_VOLUMES="buildkite:/buildkite"

  stub docker-compose \
    "-f ${DCYML} build ghapp : echo build ghapp" \
    "-f ${DCYML} run -v buildkite:/buildkite --workdir=${PWD} --rm ghapp -v check from-job-env : echo run ghapp" \
    "-f ${DCYML} down  : echo down"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose

  unset BUILDKITE_DOCKER_DEFAULT_VOLUMES

}
