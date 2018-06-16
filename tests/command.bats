#!/usr/bin/env bats

load '/usr/local/lib/bats/load.bash'

@test "pre-command" {

  stub echo-env \
    ":"
  stub docker-compose \
    "build ghapp : echo build ghapp" \
    "run ghapp : echo run ghapp"

  run $PWD/hooks/pre-command

  assert_success

  unstub echo-env
  unstub docker-compomse
}

@test "debug mode" {

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG=true



  stub echo-env \
    ":"
  stub docker-compose \
    "build ghapp : echo build ghapp" \
    "run ghapp -v : echo run ghapp -v"

  run $PWD/hooks/pre-command

  assert_success

  unstub echo-env
  unstub docker-compomse

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG

}
