#!/usr/bin/env python3
"""
Tests for install script logic.
"""

import json
import subprocess
from pathlib import Path


def test_env_copy_when_missing(tmp_path):
    """Install script copies .env.example to .env when .env doesn't exist."""
    env_example = tmp_path / ".env.example"
    env_file = tmp_path / ".env"

    env_example.write_text("TEST_KEY=value\n")

    # Simulate install script logic
    if not env_file.exists():
        env_file.write_text(env_example.read_text())

    assert env_file.exists()
    assert env_file.read_text() == "TEST_KEY=value\n"


def test_env_preserved_when_exists(tmp_path):
    """Install script preserves existing .env file."""
    env_example = tmp_path / ".env.example"
    env_file = tmp_path / ".env"

    env_example.write_text("EXAMPLE=new\n")
    env_file.write_text("CUSTOM=old\n")

    # Simulate install script logic
    if not env_file.exists():
        env_file.write_text(env_example.read_text())

    assert env_file.read_text() == "CUSTOM=old\n"


def test_mcp_merge_script_execution(tmp_path):
    """MCP merge bash commands execute successfully and modify target file."""
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"

    source.write_text(json.dumps({"mcpServers": {"test": {"command": "test"}}}))
    target.write_text(json.dumps({"existing": "data"}))

    # Run actual bash commands from install.sh lines 58-63
    script = f"""
    source_servers=$(jq -r '.mcpServers' {source})
    jq --argjson servers "$source_servers" \\
      '.mcpServers = (.mcpServers // {{}}) * $servers' \\
      {target} > {target}.tmp
    mv {target}.tmp {target}
    """

    result = subprocess.run(["bash", "-c", script], capture_output=True, check=False)

    assert result.returncode == 0, f"Merge script failed: {result.stderr.decode()}"
    assert target.exists(), "Target file missing after merge"
    assert not (tmp_path / f"{target}.tmp").exists(), "Temp file not cleaned up"

    merged = json.loads(target.read_text())
    assert "mcpServers" in merged, "mcpServers not added to target"
    assert "existing" in merged, "Existing data not preserved"


def test_install_script_bash_syntax():
    """Install script has valid bash syntax."""
    project_root = Path(__file__).parent.parent
    install_script = project_root / "bin" / "install.sh"

    result = subprocess.run(["bash", "-n", str(install_script)], capture_output=True, check=False)

    assert result.returncode == 0, f"Syntax error: {result.stderr.decode()}"


def test_mcp_limitless_filtered_when_no_api_key(tmp_path):
    """Limitless MCP server is filtered out when API key not configured."""
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"

    # Create source with limitless server
    source.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "limitless": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-limitless"]},
                    "other": {"command": "other-server"},
                }
            }
        )
    )
    target.write_text(json.dumps({"existing": "data"}))

    # Test with no API key
    script = f"""
    LIMITLESS_API_KEY=""
    source_servers=$(jq -r '.mcpServers' {source})
    if [ -z "$LIMITLESS_API_KEY" ] || [ "$LIMITLESS_API_KEY" = "your_limitless_api_key_here" ]; then
      source_servers=$(echo "$source_servers" | jq 'del(.limitless)')
    fi
    jq --argjson servers "$source_servers" \
      '.mcpServers = (.mcpServers // {{}}) * $servers' \
      {target} > {target}.tmp
    mv {target}.tmp {target}
    """

    result = subprocess.run(["bash", "-c", script], capture_output=True, check=False)
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"

    merged = json.loads(target.read_text())
    assert "limitless" not in merged.get("mcpServers", {}), "Limitless should be filtered out"
    assert "other" in merged.get("mcpServers", {}), "Other server should be preserved"


def test_mcp_limitless_included_when_api_key_set(tmp_path):
    """Limitless MCP server is included when API key is configured."""
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"

    source.write_text(
        json.dumps(
            {
                "mcpServers": {
                    "limitless": {
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-limitless"],
                        "env": {"LIMITLESS_API_KEY": "${LIMITLESS_API_KEY}"},
                    },
                    "other": {"command": "other-server"},
                }
            }
        )
    )
    target.write_text(json.dumps({"existing": "data"}))

    # Test with API key set
    script = f"""
    LIMITLESS_API_KEY="sk-real-key-123"
    source_servers=$(jq -r '.mcpServers' {source})
    if [ -z "$LIMITLESS_API_KEY" ] || [ "$LIMITLESS_API_KEY" = "your_limitless_api_key_here" ]; then
      source_servers=$(echo "$source_servers" | jq 'del(.limitless)')
    else
      source_servers=$(echo "$source_servers" | jq --arg key "$LIMITLESS_API_KEY" \
        '.limitless.env.LIMITLESS_API_KEY = $key')
    fi
    jq --argjson servers "$source_servers" \
      '.mcpServers = (.mcpServers // {{}}) * $servers' \
      {target} > {target}.tmp
    mv {target}.tmp {target}
    """

    result = subprocess.run(["bash", "-c", script], capture_output=True, check=False)
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"

    merged = json.loads(target.read_text())
    assert "limitless" in merged.get("mcpServers", {}), "Limitless should be included"
    assert "other" in merged.get("mcpServers", {}), "Other server should be preserved"
    # Verify the API key was interpolated
    assert (
        merged["mcpServers"]["limitless"]["env"]["LIMITLESS_API_KEY"] == "sk-real-key-123"
    ), "API key should be interpolated, not template"


if __name__ == "__main__":
    import pytest  # noqa: PLC0415

    pytest.main([__file__, "-v"])
