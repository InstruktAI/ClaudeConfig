# LLM Coding Directives (Unified Edition)

Purpose: Define what to produce — not why. Apply in every project unless configuration explicitly overrides.

## 0. Project Awareness

1. Always follow the project's existing configuration (pyproject, tsconfig, eslint, ruff, etc.).
2. Use only approved dependencies, import patterns, naming, and formatting.
3. Mirror the repository's structure and conventions.
4. Don't introduce new frameworks or architectural patterns.
5. **When debugging log files**: Truncate log files before operations to easily find relevant output (e.g., `: > /var/log/app.log`).

## 1. Architecture & Structure

1. Prefer functions over classes in all languages.
2. One clear responsibility per module, function, or class.
3. Separate business logic, infrastructure, and UI.
4. Depend on abstractions, not implementations.
5. Avoid circular dependencies.
6. Prefer composition over inheritance.
7. Keep the public surface small and explicit.

## 2. Functions & Behavior

1. Use pure functions for business logic, no hidden side effects.
2. Parameters and return types must be explicit.
3. Maximum of 4 parameters; use structured objects for more.
4. Apply Command-Query Separation: read or write, never both.
5. Default to explicit typing and deterministic outputs.

## 3. Typing & Contracts

1. Always type everything.

    - TypeScript: strict types, no `any`.
    - Python: strict, modern type hints (`list`, `dict`, `|` syntax), no `Any`.

2. Define structured data models (interfaces, dataclasses, schemas).
3. Enforce invariants so illegal states are unrepresentable.
4. Validate at system boundaries; fail early and clearly.
5. Never return `None` or `null` for errors; raise or return Result/Option.

## 4. State & Dependencies

1. Prefer module-level state over class instance state.
2. Use immutable data for shared state.
3. Avoid global mutable state except defined singletons.
4. Initialize state explicitly, never on import.
5. Pass dependencies explicitly; don’t hide them in globals.
6. Don’t create Manager, Service, or Helper classes unless truly required.

## 5. Error Handling & Reliability

1. Fail fast with clear diagnostics.
2. Never swallow exceptions silently.
3. Validate early and close to input.
4. Commands change state; queries do not.
5. Keep recovery logic explicit and minimal.

## 6. Simplicity & Abstraction

1. Keep it simple: the simplest working solution first.
2. Never duplicate code. Extract to components/functions on second use.
3. Simple extraction beats complex abstraction. Extract now, refine later.
4. Build only for current requirements (YAGNI).
5. Keep files and functions short and clear.

## 7. Async / Concurrency

1. Use async/await over callbacks.
2. Aggregate concurrent operations with gather or Promise.all.
3. Use explicit async context managers for resources.

## 8. Language Patterns

### Python

-   Use dict-based dispatch over long if/elif chains.
-   Use generators for streaming or large data.
-   Use context managers for resource handling.
-   Prefer dataclasses and protocols for structure.
-   Avoid mutable defaults, star imports, or classes used for namespacing.

### TypeScript

-   Use const assertions for literals.
-   Prefer discriminated unions for state.
-   Use type guards and strict null checks.
-   Use interfaces for shapes, types for unions or aliases.
-   Avoid enum, any, default exports, and class-based namespacing.

## 9. Testing

1. Test behavior, not implementation.
2. One assertion per test; name tests for expected outcome.
3. Mock only at architectural boundaries.
4. Don’t test private or internal methods directly.
5. Focus on edge cases more than happy paths.

## 10. Output Discipline

1. Conform to existing naming and formatting automatically.
2. Output only the required files or blocks; no commentary.
3. Don't add unused imports or extra utilities.
4. Never contradict the project's configuration.

## 11. Git Commits

**Git is version control, not a backup tool. Commits must be atomic, complete, and working.**

1. **Format**: `type(scope): subject` (commitizen)
   - Types: feat, fix, refactor, style, docs, test, chore, perf
   - Subject: imperative, lowercase, no period, max 72 chars
2. **Attribution footer**:
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

### Commit Standards

**Atomic commits (Unix philosophy): Do ONE thing completely and well.**

- ✅ "feat(auth): add JWT validation" - complete feature
- ✅ "fix(api): handle null response" - one bug
- ❌ "fix bugs and add features" - not atomic
- ❌ "WIP" or "quick save" - not complete

**Pre-commit hooks enforce tests/linting/formatting automatically.**

Only commit when:
- Change is atomic and complete
- Code works (hooks will verify)
- No debug/temp code

Use rsync or git stash for WIP, not commits.

## 12. Logging & Observability

1. Add logging at key execution points: boundaries, state changes, errors.
2. Use appropriate log levels:
   - DEBUG: detailed diagnostic info for troubleshooting
   - INFO: significant events (startup, config loaded, operation completed)
   - WARNING: recoverable issues, degraded behavior
   - ERROR: failures requiring attention
   - CRITICAL: system-threatening failures
3. Log input validation failures and all error paths.
4. Include relevant context (IDs, paths, values) in messages for traceability.
5. **When debugging**: Truncate log files before operations to isolate relevant output (e.g., `: > /var/log/app.log`).
6. Never log sensitive data (passwords, tokens, PII, API keys).
7. Use single-line text format; formatters are already configured. **Never use JSON logging**.

## Final Self-Check Before Emitting Code

-   [ ] Follows project config and linter
-   [ ] Uses functions, not classes, by default
-   [ ] All types explicit and modern
-   [ ] No extra abstractions or side effects
-   [ ] Dependencies explicit, not hidden
-   [ ] Fail-fast logic present
-   [ ] Logging added at key points with appropriate levels
-   [ ] Simple, short, and testable
