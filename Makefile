.PHONY: help install format lint test clean start-mcp stop-mcp

help:
	@echo "Available targets:"
	@echo "  make install   - Complete project installation"
	@echo "  make format    - Format code with black and isort"
	@echo "  make lint      - Run pylint and mypy checks"
	@echo "  make test      - Run pytest tests"
	@echo "  make clean     - Remove generated files and caches"
	@echo "  make start-mcp - Start all MCP servers"
	@echo "  make stop-mcp  - Stop all MCP servers"

install:
	@./bin/install.sh

format:
	@echo "Formatting code..."
	@./bin/format.sh
	@echo "✓ Code formatted"

lint:
	@echo "Running lint checks..."
	@./bin/lint.sh
	@echo "✓ Lint checks passed"

test:
	@echo "Running tests..."
	@./bin/test.sh
	@echo "✓ Tests passed"

clean:
	@echo "Cleaning generated files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@rm -rf .mypy_cache 2>/dev/null || true
	@rm -rf .tmp 2>/dev/null || true
	@echo "✓ Cleaned generated files"

start-mcp:
	@echo "Starting MCP servers..."
	@cd mcp-servers && ./start.sh
	@echo "✓ MCP servers started"

stop-mcp:
	@echo "Stopping MCP servers..."
	@cd mcp-servers && ./stop.sh
	@echo "✓ MCP servers stopped"
