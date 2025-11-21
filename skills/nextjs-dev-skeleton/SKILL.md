---
name: Next.js Dev Skeleton
description: Bootstrap Next.js projects with development environment including ESLint (absolute imports, auto-sorted), Prettier (Tailwind integration), shadcn/ui, and VSCode settings. Use when starting new Next.js projects, standardizing existing codebases, or setting up team development environments. Triggers on mentions of next.js + new project / dev setup, eslint config, prettier config, absolute imports, import sorting, or shadcn setup.
---

# Next.js Dev Skeleton

## Instructions

### Prerequisites

- Next.js project initialized (with App Router)
- pnpm installed

### Workflow: Bootstrap Development Environment

1. **Copy configuration files**:

```bash
# Copy all config files to project root
cp ./resources/.prettierrc.js .
cp ./resources/eslint.config.ts .
cp ./resources/tailwind.config.ts .
cp ./resources/components.json .

# Copy VSCode settings
mkdir -p .vscode
cp ./resources/.vscode/settings.json .vscode/
cp ./resources/.vscode/extensions.json .vscode/
```

2. **Install required dependencies**:

```bash
# ESLint plugins
pnpm add -D eslint-plugin-unused-imports @eslint/eslintrc @eslint/js \
  @typescript-eslint/eslint-plugin @typescript-eslint/parser \
  eslint-plugin-import eslint-plugin-jsx-a11y eslint-plugin-n \
  eslint-plugin-no-relative-import-paths eslint-plugin-prettier \
  eslint-plugin-promise eslint-plugin-react eslint-plugin-react-hooks \
  eslint-plugin-simple-import-sort eslint-plugin-jsx-a11y @types/eslint-plugin-jsx-a11y

# Prettier plugins
pnpm add -D prettier prettier-plugin-tailwindcss

# Tailwind required
pnpm add -D @tailwindcss/typography

# Tailwind optional, like animations
pnpm add -D tailwindcss-animate

# shadcn/ui cli
pnpm add -D @ui-shadcn/cli
```

3. **Add package.json scripts** (if not present):

```json
{
  "scripts": {
    "worker": "RUN_MODE=worker dotenv -e .env -- bin/worker.js",
    "worker:dev": "NODE_OPTIONS='--inspect=9231' RUN_MODE=worker dotenv -e .env -- tsx watch bin/worker.ts",
    "dev": "NODE_OPTIONS='--inspect=9229' next dev --turbopack",
    "build": "eslint . --fix && NODE_ENV=production next build",
    "start": "next start",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "typecheck": "tsc --noEmit --incremental false",
    "test": "jest --env=jsdom --passWithNoTests",
    "test:all": "run-p typecheck lint test",
    "test:coverage": "jest --env=jsdom --coverage --passWithNoTests",
    "test:unit": "jest --env=jsdom --passWithNoTests",
    "shadcn:add": "shadcn add",
    "shadcn:remove": "shadcn remove",
    // and if drizzle db with postgres:
    "drizzle:generate": "dotenv -e .env -- drizzle-kit generate",
    "drizzle:migrate": "dotenv -e .env -- tsx lib/db/migrate.ts",
    "drizzle:studio": "dotenv -e .env -- drizzle-kit studio",
    "drizzle:push": "dotenv -e .env -- drizzle-kit push",
    "drizzle:pull": "dotenv -e .env -- drizzle-kit pull",
    "drizzle:check": "dotenv -e .env -- drizzle-kit check",
    "drizzle:up": "dotenv -e .env -- drizzle-kit up",
    "db:reset": "pnpm db:stop && rm -rf ./data/postgres && pnpm db:start && pnpm drizzle:generate && sleep 1 && pnpm drizzle:migrate",
    "db:seed": "dotenv -e .env -- tsx lib/db/seed.ts",
    "db:start": "docker compose up -d",
    "db:stop": "docker compose down"
  }
}
```

4. **Verify setup**:

```bash
# Test ESLint
pnpm lint

# Test Prettier
pnpm format:check

# Open in VSCode and install recommended extensions
code .
```

### Key Features

**ESLint Configuration** - See [resources/eslint.config.ts](resources/eslint.config.ts):

- **Absolute imports enforced**: All imports use `@/` prefix (no `../../../`)
- **Auto-sorted imports**: Groups by node: � external � @/ � relative
- **No semicolons**: Aligned with Prettier for consistency
- **React hooks rules**: Prevents common React pitfalls
- **TypeScript strict**: Consistent type imports, no inferrable types
- **Unused imports removed**: Auto-cleanup on save

**Prettier Configuration** - See [resources/.prettierrc.js](resources/.prettierrc.js):

- **Tailwind class sorting**: Automatic class order via plugin
- **No semicolons**: Matches ESLint config
- **120 char line width**: Wider for modern displays
- **Single quotes**: Consistent with modern JS

**Tailwind Configuration** - See [resources/tailwind.config.ts](resources/tailwind.config.ts):

- **Font family CSS vars**: Use `--font-sans`, `--font-serif`, `--font-mono`
- **Custom animations**: `caret-blink`, `glow-effect` keyframes
- **Typography plugin**: For rich text content
- **Animate plugin**: Pre-built animations

**shadcn/ui Configuration** - See [resources/components.json](resources/components.json):

- **Style**: new-york (more refined than default)
- **Base color**: stone (neutral palette)
- **RSC enabled**: Server Components ready
- **Icon library**: Lucide React

**VSCode Settings** - See [resources/.vscode/settings.json](resources/.vscode/settings.json):

- **Format on save**: ESLint + Prettier auto-fix
- **Tailwind IntelliSense**: Enhanced CSS class completion
- **Drizzle auto-migration**: � Runs migrations when schema.ts changes (disable if unwanted)
- **Language-specific formatters**: Python, Shell, YAML, etc.

**VSCode Extensions** - See [resources/.vscode/extensions.json](resources/.vscode/extensions.json):

- Tailwind CSS IntelliSense
- ESLint
- Prettier
- Drizzle ORM
- GitHub Actions
- TypeScript

### Important Warnings

� **Drizzle auto-migration** (line 52-58 in `.vscode/settings.json`):

```json
"emeraldwalk.runonsave": {
  "commands": [{
    "match": "lib/db/schema.ts",
    "cmd": "pnpm drizzle:generate && pnpm drizzle:migrate"
  }]
}
```

This automatically generates and runs migrations when you save `lib/db/schema.ts`. **Remove this if**:

- You don't use Drizzle ORM
- You want manual migration control
- You're working with production databases

� **Absolute imports enforcement**: All relative imports (except same folder) will error. This is intentional but requires:

- `@/` alias configured in `tsconfig.json`
- All imports converted from relative to absolute

## Examples

### Example 1: Bootstrap New Next.js Project

User request:

```
Set up a new Next.js project with best practices for development
```

You would:

1. Initialize Next.js: `pnpm create next-app@latest`
2. Copy all config files from skill resources to project root
3. Install required dependencies (ESLint plugins, Prettier, Tailwind plugins)
4. Add lint/format scripts to package.json
5. Open in VSCode, install recommended extensions
6. Run `pnpm lint:fix` to auto-fix existing code
7. Verify imports are sorted and absolute paths enforced

### Example 2: Add to Existing Next.js Project

User request:

```
Our Next.js project has inconsistent import styles and no linting. Help standardize it.
```

You would:

1. Check if project already has ESLint/Prettier configs (may need to merge or replace)
2. Copy skill configs, preserving any custom rules if needed
3. Install all dependencies
4. Run `pnpm lint:fix` to auto-fix import sorting and absolute paths
5. Review changed files for any breaking imports
6. Commit changes: "Standardize dev environment with absolute imports and auto-formatting"
7. Update team README with new conventions

### Example 3: Disable Drizzle Auto-Migration

User request:

```
I don't want migrations running automatically when I edit my schema
```

You would:

1. Open `.vscode/settings.json`
2. Remove the `emeraldwalk.runonsave` section (lines 52-59)
3. Explain alternative workflow: `pnpm drizzle:generate` then `pnpm drizzle:migrate` manually
4. Optionally add these as separate package.json scripts for convenience

### Example 4: Configure Absolute Imports

User request:

```
ESLint is erroring on all my relative imports after adding your config
```

You would:

1. Verify `tsconfig.json` has `@/*` path alias:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./*"]
       }
     }
   }
   ```
2. Run `pnpm lint:fix` to auto-convert relative to absolute imports
3. Fix any remaining manual imports that can't be auto-fixed
4. Explain benefit: No more `../../../components` hell, consistent imports across codebase

### Example 5: Team Onboarding

User request:

```
New team member needs to set up their dev environment
```

You would:

1. Ensure they have pnpm installed: `npm install -g pnpm`
2. Clone repo and run: `pnpm install`
3. Open in VSCode: Install recommended extensions (prompt appears automatically)
4. Run `pnpm lint` to verify ESLint works
5. Make a small change and save file - verify auto-formatting happens
6. Explain key conventions: absolute imports, no semicolons, sorted imports
7. Point them to config files if they want to understand specifics
