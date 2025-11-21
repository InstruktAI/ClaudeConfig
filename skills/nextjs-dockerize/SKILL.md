---
name: Next.js Dockerize
description: Creates production-ready Docker setups for self-hosted Next.js applications with multi-stage builds, standalone output optimization, and ARM64 support. Use when dockerizing Next.js apps, deploying to Raspberry Pi or ARM servers, optimizing Next.js Docker images, implementing database migrations in containers, or debugging Next.js standalone output. Triggers on mentions of Next.js Docker, self-hosting, standalone output, Raspberry Pi deployment, or Docker optimization.
---

# Next.js Dockerize

## Instructions

### Prerequisites

- Next.js application (App Router or Pages Router)
- Docker installed locally
- For database apps: Database migration tool (e.g., Drizzle, Prisma)

### Workflow: Dockerize Next.js Application

1. **Configure Next.js for standalone output** in `next.config.ts`:

```typescript
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'standalone',

  // Include additional files not auto-traced by Next.js
  experimental: {
    outputFileTracingIncludes: {
      '/': [
        './lib/**/*', // Database utilities
        './drizzle.config.ts', // Database config (if using Drizzle)
      ],
    },
  },
};

export default nextConfig;
```

2. **Create multi-stage Dockerfile**:

```dockerfile
# syntax=docker.io/docker/dockerfile:1

FROM node:22 AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app

COPY pnpm-lock.yaml* package.json* ./
RUN corepack enable pnpm && pnpm i --frozen-lockfile

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN corepack enable pnpm
RUN --mount=type=secret,id=POSTGRES_USER,required \
    --mount=type=secret,id=POSTGRES_PASSWORD,required \
    --mount=type=secret,id=POSTGRES_DB,required \
    --mount=type=secret,id=POSTGRES_HOST,required \
    POSTGRES_USER=$(cat /run/secrets/POSTGRES_USER) \
    POSTGRES_PASSWORD=$(cat /run/secrets/POSTGRES_PASSWORD) \
    POSTGRES_DB=$(cat /run/secrets/POSTGRES_DB) \
    POSTGRES_HOST=$(cat /run/secrets/POSTGRES_HOST) \
    pnpm build

# Transpile additional TypeScript files (e.g., database utilities)
RUN npx tsc -p tsconfig.db.json && npx tsc-alias -p tsconfig.db.json

# Production image, copy all the files and run next
FROM node:22-slim AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy database utilities for migrations
COPY --from=builder --chown=nextjs:nodejs /app/lib ./lib
COPY --from=builder --chown=nextjs:nodejs /app/start.sh ./

RUN chown -R nextjs:nodejs /app

USER nextjs
ENV HOME=/app

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["./start.sh"]
```

3. **Create start script** at `start.sh`:

```bash
#!/bin/sh
set -e

# When using Postgres with individual environment variables:
# Construct DATABASE_URL from separate PostgreSQL env vars
if [ -n "$POSTGRES_USER" ] && [ -n "$POSTGRES_PASSWORD" ] && [ -n "$POSTGRES_DB" ] && [ -n "$POSTGRES_HOST" ]; then
    export DATABASE_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:5432/$POSTGRES_DB"
    echo "DATABASE_URL constructed from environment variables"
else
    echo "Warning: PostgreSQL environment variables not fully set, using existing DATABASE_URL if available"
fi

# When using database migrations:
# Run migrations using compiled JavaScript (no need for `npx drizzle-kit` at all)
echo "Running database migrations..."
node lib/db/migrate.js

# When supporting multiple run modes (web server vs background workers):
# Start the appropriate service based on RUN_MODE environment variable
case "${RUN_MODE:-server}" in
  "worker")
    echo "Starting background workers..."
    exec node bin/worker.js
    ;;
  *)
    echo "Starting Next.js web server..."
    exec node server.js
    ;;
esac
```

**Simplified version** (when you don't need workers or custom migrations):

```bash
#!/bin/sh
set -e

echo "Running database migrations..."
node lib/db/migrate.js

echo "Starting Next.js server..."
exec node server.js
```

Make executable:

```bash
chmod +x start.sh
```

4. **Create `.dockerignore`** - See [resources/.dockerignore](resources/.dockerignore) for comprehensive template

5. **For local development** (optional):

Copy [resources/docker-compose.yml](resources/docker-compose.yml) to run Postgres database locally:

```bash
# Create .env file for local development
cp resources/.env.example .env
# Edit .env with your credentials

# Start Postgres database
docker-compose up -d

# Run Next.js in development mode (not in Docker)
npm run dev
```

**Note**: Local development uses `npm run dev` against a running Postgres database. Docker is only for production deployment.

6. **Build production image**:

```bash
docker build -t myapp:latest .
```

### Optional: Database Configuration

**Drizzle ORM** - See [resources/drizzle.config.ts](resources/drizzle.config.ts) for example configuration:
- Schema at `./lib/db/schema.ts`
- Migrations output to `./lib/db/migrations`
- Uses `DATABASE_URL` environment variable

**TypeScript compilation** - For database utilities that need transpilation, create `tsconfig.db.json`:

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "module": "commonjs",
    "outDir": "./lib",
    "rootDir": "./lib"
  },
  "include": ["lib/**/*"],
  "exclude": ["node_modules"]
}
```

### Key Points

**Development vs Production**:
- Local dev: Use `npm run dev` with docker-compose for Postgres only (via `.env` file)
- Production: Full Docker build and deployment with build-time secrets

**Standalone output** (`output: 'standalone'`):
- Reduces image from 1.5GB to 300-400MB
- Traces only required dependencies
- Creates minimal production bundle

**Build secrets** (`--mount=type=secret`):
- Secrets only available during RUN command
- Never persisted in image layers
- Safe for build-time credentials in CI/CD

**Multi-stage build**:
- `deps`: Install dependencies (cached separately)
- `builder`: Build application
- `runner`: Minimal production image (node:22-slim)

**Security**:
- Runs as non-root user (nextjs:nodejs)
- Slim base image reduces attack surface
- Secrets handled securely

**Start script patterns**:
- Construct `DATABASE_URL` from individual Postgres env vars (when using separate credentials)
- Run migrations before server starts (ensures schema is up-to-date)
- Support multiple run modes with `RUN_MODE` env var (server/worker pattern for background jobs)

## Examples

### Example 1: Dockerizing a Basic Next.js App

User request:

```
I want to self-host my Next.js app on my Raspberry Pi instead of using Vercel
```

You would:

1. Add `output: 'standalone'` to `next.config.ts`
2. Create Dockerfile using the template above
3. Copy `.dockerignore` from [resources/.dockerignore](resources/.dockerignore)
4. Build and run: `docker build -t myapp:latest . && docker run -p 3000:3000 myapp:latest`
5. Verify standalone output reduced image size from ~1.5GB to ~300MB

### Example 2: Setting Up Local Development with Database

User request:

```
I need to set up local development with a Postgres database
```

You would:

1. Copy [resources/docker-compose.yml](resources/docker-compose.yml) to project root
2. Copy [resources/.env.example](resources/.env.example) to `.env` and configure credentials
3. Start Postgres: `docker-compose up -d`
4. Run app in development: `npm run dev`
5. Verify connection and migrations work locally

### Example 3: Securing Build-Time Database Credentials (Production)

User request:

```
My build process needs database access to generate types from the schema in CI/CD
```

You would:

1. Verify Dockerfile uses `--mount=type=secret` pattern (shown in workflow above)
2. In CI/CD (GitHub Actions), configure secrets and pass them during build:
   ```yaml
   - name: Build and push
     uses: docker/build-push-action@v6
     with:
       secrets: |
         "POSTGRES_USER=${{ secrets.POSTGRES_USER }}"
         "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}"
   ```
3. Explain why this is secure (secrets never persist in image layers)
4. For local development, credentials come from `.env` file instead

### Example 4: Optimizing Image Size

User request:

```
My Next.js Docker image is 1.8GB, how can I reduce it?
```

You would:

1. Verify `output: 'standalone'` is configured
2. Ensure Dockerfile uses multi-stage build with `node:22-slim` runner
3. Use comprehensive `.dockerignore` from [resources/.dockerignore](resources/.dockerignore)
4. Rebuild and verify: `docker build -t myapp:optimized . && docker images myapp`
5. Confirm 60-75% size reduction to 300-400MB

### Example 5: Supporting Multiple Run Modes (Server + Worker)

User request:

```
I need to run background jobs separately from my web server using the same Docker image
```

You would:

1. Use the RUN_MODE case statement from workflow step 3 (full version of start.sh)
2. Create worker entry point at `bin/worker.js`
3. In production orchestration (Docker Swarm, K8s), deploy two services:
   - Web service: `RUN_MODE=server` with exposed ports
   - Worker service: `RUN_MODE=worker` without exposed ports
4. Both containers use same image but run different processes based on env var

### Example 6: Troubleshooting "Module not found" Errors

User request:

```
My app builds fine locally but crashes in Docker with "Cannot find module './lib/db'"
```

You would:

1. Add `'./lib/**/*'` to `outputFileTracingIncludes` in next.config.ts
2. Verify file is copied in Dockerfile: `COPY --from=builder --chown=nextjs:nodejs /app/lib ./lib`
3. If TypeScript, verify transpilation: `RUN npx tsc -p tsconfig.db.json`
4. Rebuild and test
