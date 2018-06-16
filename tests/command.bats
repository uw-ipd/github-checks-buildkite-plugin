#!/usr/bin/env bats

load '/usr/local/lib/bats/load.bash'

@test "pre-command" {

  stub echo-env \
    ":"
  stub setup-venv \
    ":"
  stub ghapp \
    "current : echo current"

  run $PWD/hooks/pre-command

  assert_success

  unstub echo-env
  unstub setup-venv
  unstub ghapp
}

@test "debug mode" {

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG=true


  stub echo-env \
    ":"
  stub setup-venv \
    ":"
  stub ghapp \
    "-v current : echo current"

  run $PWD/hooks/pre-command

  assert_success

  unstub echo-env
  unstub setup-venv
  unstub ghapp

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_DEBUG

}

@test "override keys" {

  export BUILDKITE_PLUGIN_GITHUB_CHECKS_APP_ID=1
  export BUILDKITE_PLUGIN_GITHUB_CHECKS_PRIVATE_KEY=key.pem


  stub echo-env \
    ":"
  stub setup-venv \
    ":"
  stub ghapp \
    "--app_id 1 --private_key key.pem current : echo current"

  run $PWD/hooks/pre-command

  assert_success

  unstub echo-env
  unstub setup-venv
  unstub ghapp

  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_APP_ID
  unset BUILDKITE_PLUGIN_GITHUB_CHECKS_PRIVATE_KEY
}
