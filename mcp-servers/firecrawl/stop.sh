#!/usr/bin/env bash
set -e

docker compose --env-file ./.env down

echo "Firecrawl MCP server stopped"
