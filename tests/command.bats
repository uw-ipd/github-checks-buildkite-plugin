#!/usr/bin/env bats

load '/usr/local/lib/bats/load.bash'

# Uncomment to enable stub debug output:
# export DOCKER_STUB_DEBUG=/dev/tty

@test "Run command" {
  export BUILDKITE_COMMAND='command1 "a string"'

  unset BUILDKITE_COMMAND
}
