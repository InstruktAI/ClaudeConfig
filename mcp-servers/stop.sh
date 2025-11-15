#!/usr/bin/env bash
set -e

for server in */ ; do
  if [ -f "$server/stop.sh" ]; then
    echo "Stopping MCP server: $server"
    (cd "$server" && bash stop.sh)
  fi
done

echo "All MCP servers stopped"
