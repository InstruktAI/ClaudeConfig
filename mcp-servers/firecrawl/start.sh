#!/usr/bin/env bash
set -e

#  "firecrawl": {
#     "type": "http",
#     "comments": "Firecrawl is started as a docker compose stack in mcp-servers/firecrawl.",
#     "url": "http://localhost:3333/v1"
#   },

docker compose --env-file ./.env up -d

echo "Firecrawl MCP server started on http://localhost:3333/v1"