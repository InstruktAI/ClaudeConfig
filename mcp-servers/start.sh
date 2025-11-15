#!/usr/bin/env bash
set -e

for server in */ ; do
  if [ -f "$server/start.sh" ]; then
    echo "Starting MCP server: $server"
    (cd "$server" && bash start.sh) &
  fi
done

echo "All MCP servers started in background"