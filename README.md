# ClaudeConfig

Automated installer and global/user configuration for Claude Code with hooks, TTS, LLM integration, and MCP server management.

[![Claude](./assets/Claude.png)](./assets/Claude.png)

> **Acknowledgments**: This project builds upon the excellent work by [IndyDevDan's claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability).
>
> _(Though we respectfully disagreed with the UV approach and went with good old venv + pip instead 😏)_

## Features

### 🎯 Interactive Installation Wizard

- One-command setup: `make install`
- Interactive prompts for engineer details and API keys
- Automatic environment file creation and configuration
- Preserves existing settings on re-runs

### 🔊 Text-to-Speech (TTS) Integration

- Multi-service support with automatic fallback chain
- Supported services:
  - macOS `say` (free, no API key required)
  - OpenAI TTS (high quality)
  - ElevenLabs (premium quality)
  - pyttsx3 (offline fallback)
- FIFO queue for sequential playback
- Background processing for non-blocking operation

### 🤖 LLM Integration

- Completion message generation (OpenAI/Anthropic)
- Summary generation for task completion
- Automatic fallback to preset messages when no API key configured

### 🪝 Claude Code Hooks

Automated lifecycle hooks for:

- **Session Start/End**: TTS announcements and logging
- **Stop**: Task completion messages with optional summarization
- **Subagent Stop**: Subagent completion notifications
- **Notification**: Custom notification handling
- **User Prompt Submit**: Pre-commit hooks and validation

### 🔌 MCP Server Management

- Automatic MCP server configuration merging
- Conditional server inclusion based on API key availability
- Installed MCP servers:
  - **Context7** - Up-to-date library documentation
  - **Firecrawl** - Web scraping and crawling (requires API key)
  - **Limitless** - Memory and context enhancement (requires API key)
  - **Playwright** - Browser automation and testing

### 📊 Event Observability (Optional)

- Hook event streaming to observability server
- Disabled by default (`SEND_EVENTS=false`)
- When enabled, sends hook events to `http://localhost:4000/events`
- Requires [IndyDevDan's observability server](https://github.com/disler/claude-code-hooks-multi-agent-observability)

### 🧪 Testing & Quality

- 27 passing tests covering core functionality
- Pre-commit hooks for code quality
- Black + isort formatting
- Pylint + mypy type checking
- 10/10 pylint score

## Installation

```bash
# Clone the repository to ~/.claude
git clone git@github.com:InstruktAI/ClaudeConfig.git ~/.claude
cd ~/.claude

# Run the interactive installer
make install

# Start MCP servers
make start-mcp
```

The installer will:

1. Prompt for engineer name and email
2. Optionally collect API keys (OpenAI, ElevenLabs, Anthropic, Limitless, Firecrawl)
3. Install ccstatusline configuration (makes Claude CLI look nicer)
4. Create virtual environment and install dependencies
5. Install pre-commit hooks
6. Merge MCP server configurations to `~/.claude.json`
7. Generate `id.md` with your identity
8. Test configuration and verify all hooks work correctly

## Configuration

### Environment Variables (.env)

All configuration is managed through `.env`:

```bash
# Identity
ENGINEER_NAME=Your Name
ENGINEER_EMAIL=your.email@example.com

# Logging
LOG_LEVEL=info  # debug, info, warn, error

# TTS Configuration
TTS_SERVICE=elevenlabs,openai,macos,pyttsx3  # Priority chain
OPENAI_API_KEY=sk-...
OPENAI_VOICE=nova
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_VOICE_ID=...
MACOS_VOICE="Samantha"  # Use quotes for voices with spaces

# LLM Configuration
ANTHROPIC_API_KEY=sk-ant-...

# MCP Servers
LIMITLESS_API_KEY=sk-...

# Event Observability (disabled by default)
# Set to "true" to send hook events to observability server
# Requires: https://github.com/disler/claude-code-hooks-multi-agent-observability
SEND_EVENTS=false
```

### TTS Service Priority

Configure multiple TTS services with automatic fallback:

```bash
# Try ElevenLabs first, fallback to macOS if unavailable
TTS_SERVICE=elevenlabs,macos

# OpenAI only (no fallback)
TTS_SERVICE=openai
```

Services are tried in order until one succeeds.

### Skip TTS for Specific Events

You can disable TTS notifications for specific hook events:

```bash
# Skip TTS for session start and end events
TTS_SKIP_HOOK_EVENTS=SessionStart,SessionEnd

# Available events: SessionStart, SessionEnd, Stop, SubagentStop, Notification
```

When TTS is skipped, a debug log entry is recorded instead.

## Project Structure

```
~/.claude/
├── bin/
│   └── install.sh           # Interactive installation wizard
├── hooks/                   # Claude Code event hooks
│   ├── session_start.py     # Session start with TTS
│   ├── session_end.py       # Session end with stats
│   ├── stop.py              # Task completion with LLM
│   ├── subagent_stop.py     # Subagent completion
│   └── notification.py      # Custom notifications
├── utils/                   # Shared utilities
│   ├── tts/                 # TTS service implementations
│   ├── llm/                 # LLM service implementations
│   ├── tts_manager.py       # TTS orchestration
│   ├── llm_manager.py       # LLM orchestration
│   ├── logging_helper.py    # Unified logging
│   └── tts_queue_runner.py  # FIFO queue processor
├── tests/                   # Test suite
├── mcp-servers/             # MCP server stack
├── .env.example             # Environment template
├── id.md.example            # Identity file template
└── mcp.json                 # MCP server definitions
```

## Development

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Clean build artifacts
make clean

# Test configuration (runs during install)
python scripts/test_config.py
```

### Configuration Tester

The installer runs an automated configuration test at the end to verify:

- ✓ Environment variables are configured
- ✓ TTS is set up correctly
- ✓ All hooks execute successfully

You'll see see and hear output demonstrating each hook. If any issues are found, the installer will complete with warnings.

## Hook System

Hooks are triggered by Claude Code events and configured in `settings.json`:

### Available Hooks

- `SessionStart`: TTS announcement when session starts
- `SessionEnd`: TTS announcement + session statistics
- `Stop`: Task completion message (with optional LLM summary)
- `SubagentStop`: Subagent completion notification
- `Notification`: Custom notification handling
- `UserPromptSubmit`: Pre-commit validation

## MCP Server Management

The installer intelligently handles MCP servers:

1. **Conditional Installation**: Firecrawl and Limitless only installed if API keys provided
2. **API Key Interpolation**: Replaces template variables with actual values
3. **Non-Destructive**: Preserves existing MCP server configurations in `~/.claude.json`
4. **Installed Servers**:
   - Context7 (always) - Library documentation
   - Firecrawl (conditional) - Web scraping
   - Limitless (conditional) - Memory enhancement
   - Playwright (always) - Browser automation

## License

GPL-3.0-only

## Author

Maurice Faber <maurice@instrukt.ai>
