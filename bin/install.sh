#!/usr/bin/env bash
set -e

echo "========================================="
echo "  Claude Code Hooks - Installation"
echo "========================================="
echo ""

# Determine project root
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if .env exists and is complete
ENV_COMPLETE=false
if [ -f .env ]; then
  if grep -q "^ENGINEER_NAME=.\+" .env && grep -q "^ENGINEER_EMAIL=.\+" .env; then
    ENV_COMPLETE=true
  fi
fi

# Interactive configuration
if [ "$ENV_COMPLETE" = false ]; then
  echo "→ Configuration"
  echo ""

  if [ ! -f .env ]; then
    cp .env.example .env
    echo "  ✓ Created .env from template"
  fi

  echo "Let's set up your environment..."
  echo ""

  # Engineer details
  read -p "Your name: " ENGINEER_NAME
  read -p "Your email: " ENGINEER_EMAIL

  # Update .env
  sed -i '' "s/^ENGINEER_NAME=.*/ENGINEER_NAME=$ENGINEER_NAME/" .env
  sed -i '' "s/^ENGINEER_EMAIL=.*/ENGINEER_EMAIL=$ENGINEER_EMAIL/" .env

  echo ""
  echo "  ✓ Engineer details saved"
  echo ""

  # Optional: API keys
  echo "API Keys (all optional - press Enter to skip):"
  echo ""

  read -p "OpenAI API key (optional, for TTS and LLM): " OPENAI_KEY
  if [ -n "$OPENAI_KEY" ]; then
    sed -i '' "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env
    echo "  ✓ OpenAI key saved"
  fi

  read -p "ElevenLabs API key (optional, for TTS): " ELEVENLABS_KEY
  if [ -n "$ELEVENLABS_KEY" ]; then
    sed -i '' "s/^ELEVENLABS_API_KEY=.*/ELEVENLABS_API_KEY=$ELEVENLABS_KEY/" .env
    echo "  ✓ ElevenLabs key saved"
  fi

  read -p "Anthropic API key (optional, for LLM): " ANTHROPIC_KEY
  if [ -n "$ANTHROPIC_KEY" ]; then
    sed -i '' "s/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$ANTHROPIC_KEY/" .env
    echo "  ✓ Anthropic key saved"
  fi

  read -p "Limitless API key (optional, for Limitless MCP server): " LIMITLESS_KEY
  if [ -n "$LIMITLESS_KEY" ]; then
    sed -i '' "s/^LIMITLESS_API_KEY=.*/LIMITLESS_API_KEY=$LIMITLESS_KEY/" .env
    echo "  ✓ Limitless key saved"
  fi

  read -p "Firecrawl API key (optional, for Firecrawl MCP server): " FIRECRAWL_KEY
  if [ -n "$FIRECRAWL_KEY" ]; then
    sed -i '' "s/^FIRECRAWL_API_KEY=.*/FIRECRAWL_API_KEY=$FIRECRAWL_KEY/" .env
    echo "  ✓ Firecrawl key saved"
  fi

  echo ""
else
  echo "→ Using existing .env configuration"
  echo ""
fi

# Load environment variables
set -a
source .env
set +a

# Create id.md from template if needed
if [ ! -f id.md ]; then
  if [ -z "$ENGINEER_NAME" ] || [ -z "$ENGINEER_EMAIL" ]; then
    echo "⚠️  Cannot create id.md: ENGINEER_NAME or ENGINEER_EMAIL not set"
    echo "   Edit .env and run 'make install' again"
    echo ""
  else
    echo "→ Creating id.md..."
    sed -e "s/{ENGINEER_NAME}/$ENGINEER_NAME/g" \
        -e "s|{ENGINEER_EMAIL}|$ENGINEER_EMAIL|g" \
        id.md.example > id.md
    echo "  ✓ id.md created"
    echo ""
  fi
else
  echo "→ id.md already exists (preserved)"
  echo ""
fi

# Configure ccstatusline (Claude CLI status line)
CCSTATUS_DIR="$HOME/.config/ccstatusline"
CCSTATUS_FILE="$CCSTATUS_DIR/settings.json"

if [ ! -f "$CCSTATUS_FILE" ]; then
  echo "→ Installing ccstatusline configuration..."
  mkdir -p "$CCSTATUS_DIR"
  cp ccstatusline.json "$CCSTATUS_FILE"
  echo "  ✓ ccstatusline.json installed to ~/.config/ccstatusline/settings.json"
  echo ""
else
  echo "→ ccstatusline configuration already exists"
  read -p "  Overwrite with ClaudeConfig version? (y/N): " OVERWRITE
  if [ "$OVERWRITE" = "y" ] || [ "$OVERWRITE" = "Y" ]; then
    cp ccstatusline.json "$CCSTATUS_FILE"
    echo "  ✓ ccstatusline.json updated"
  else
    echo "  ⊘ Keeping existing ccstatusline configuration"
  fi
  echo ""
fi

# 1. Create Python virtual environment
echo "→ Creating Python virtual environment..."
python3 -m venv .venv
echo "  ✓ Virtual environment created"
echo ""

# 2. Activate venv and upgrade pip
echo "→ Activating virtual environment and upgrading pip..."
source .venv/bin/activate
pip install --upgrade pip -q
echo "  ✓ pip upgraded"
echo ""

# 3. Install package in editable mode
echo "→ Installing package in editable mode..."
pip install -e . -q
echo "  ✓ Package installed (editable)"
echo ""

# 4. Install runtime dependencies
echo "→ Installing runtime dependencies..."
pip install -r requirements.txt -q
echo "  ✓ Runtime dependencies installed"
echo ""

# 5. Install development/test dependencies
echo "→ Installing development dependencies..."
pip install -r requirements-test.txt -q
echo "  ✓ Development dependencies installed"
echo ""

# 6. Install pre-commit hooks
echo "→ Installing pre-commit hooks..."
pre-commit install > /dev/null 2>&1
echo "  ✓ Pre-commit hooks installed"
echo ""

# 7. Merge MCP server configurations
echo "→ Merging MCP server configurations..."
source_servers=$(jq -r '.mcpServers' mcp.json)

# Filter out firecrawl if API key not configured
if [ -z "$FIRECRAWL_API_KEY" ] || [ "$FIRECRAWL_API_KEY" = "your_firecrawl_api_key_here" ]; then
  source_servers=$(echo "$source_servers" | jq 'del(.firecrawl)')
  echo "  ⊘ Skipping Firecrawl (no API key configured)"
else
  # Interpolate FIRECRAWL_API_KEY value
  source_servers=$(echo "$source_servers" | jq --arg key "$FIRECRAWL_API_KEY" \
    '.firecrawl.env.FIRECRAWL_API_KEY = $key')
fi

# Filter out limitless if API key not configured
if [ -z "$LIMITLESS_API_KEY" ] || [ "$LIMITLESS_API_KEY" = "your_limitless_api_key_here" ]; then
  source_servers=$(echo "$source_servers" | jq 'del(.limitless)')
  echo "  ⊘ Skipping Limitless (no API key configured)"
else
  # Interpolate LIMITLESS_API_KEY value
  source_servers=$(echo "$source_servers" | jq --arg key "$LIMITLESS_API_KEY" \
    '.limitless.env.LIMITLESS_API_KEY = $key')
fi

jq --argjson servers "$source_servers" \
  '.mcpServers = (.mcpServers // {}) * $servers' \
  ~/.claude.json > ~/.claude.json.tmp
mv ~/.claude.json.tmp ~/.claude.json
echo "  ✓ MCP servers merged into ~/.claude.json"
echo ""

# 8. Test configuration
echo "→ Testing configuration..."
.venv/bin/python scripts/test_config.py
TEST_RESULT=$?
echo ""

if [ $TEST_RESULT -eq 0 ]; then
  echo "========================================="
  echo "  ✓ Installation complete!"
  echo "========================================="
else
  echo "========================================="
  echo "  ⚠️  Installation complete with warnings"
  echo "========================================="
fi
echo ""
echo "Next step:"
echo "  Run 'make start-mcp' to start MCP servers"
echo ""
