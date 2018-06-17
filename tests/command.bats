#!/usr/bin/env bats

load '/usr/local/lib/bats/load.bash'

@test "pre-command" {

  stub docker-compose \
    "build ghapp : echo build ghapp" \
    "run --rm ghapp -v check from_job_env : echo run ghapp -v"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose
}

@test "debug mode" {

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG=true

  stub docker-compose \
    "build ghapp : echo build ghapp" \
    "run --rm ghapp -vv check from_job_env : echo run ghapp -vv"

  run $PWD/hooks/pre-command

  assert_success

  unstub docker-compose

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG

}
