---
name: GitHub Workflows
description: Creates production-ready GitHub Actions workflows with Docker builds, deployment automation, and ARM64 optimization. Use when setting up CI/CD pipelines, implementing Docker builds, configuring deployment workflows, optimizing build caching, or debugging GitHub Actions issues. Triggers on mentions of workflows, GitHub Actions, CI/CD, Docker build, deployment, self-hosted runners, or workflow optimization.
---

# GitHub Workflows

## Instructions

### Prerequisites

- Repository with Dockerfile
- Docker registry credentials (Docker Hub, GitHub Container Registry, etc.)
- For deployment: API endpoint or deployment target configured

### Workflow: Build Pipeline

1. **Create build workflow** at `.github/workflows/build.yaml`:

```yaml
name: Build

on:
  push:
    branches:
      - main

env:
  TARGET_REGISTRY: docker.io
  TARGET_REGISTRY_USER: <username>
  IMAGE_NAME: <org>/<image-name>

jobs:
  build:
    timeout-minutes: 15
    runs-on: [self-hosted, linux, ARM64]  # Or: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.TARGET_REGISTRY }}
          username: ${{ env.TARGET_REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/arm64
          push: true
          cache-from: type=local,src=/var/lib/docker-cache
          cache-to: type=local,dest=/var/lib/docker-cache,mode=max
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

2. **Configure cache directory** (self-hosted runners only):
   ```bash
   mkdir -p /var/lib/docker-cache
   chown runner:runner /var/lib/docker-cache
   ```

3. **Configure secrets** in repository settings:
   - `REGISTRY_TOKEN`: Docker registry authentication token

### Workflow: Deployment Pipeline

1. **Create deploy workflow** at `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  workflow_run:
    workflows: ['Build']
    types: [completed]
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - name: Deploy with retry
        uses: nick-fields/retry-action@v3
        with:
          timeout_minutes: 5
          max_attempts: 3
          retry_wait_seconds: 30
          command: |
            response=$(curl -s -w "\n%{http_code}" \
              'https://${{ secrets.API_HOST }}/update-upstream/<project>' \
              -H 'Authorization: Bearer ${{ secrets.API_KEY }}')

            http_code=$(echo "$response" | tail -n1)
            body=$(echo "$response" | sed '$d')

            if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
              echo "✅ Deployment successful (HTTP $http_code)"
              exit 0
            else
              echo "❌ Deployment failed (HTTP $http_code): $body"
              exit 1
            fi
```

2. **Configure deployment secrets**:
   - `API_HOST`: Deployment API hostname (without https://)
   - `API_KEY`: API authentication bearer token

### Secure Build-Time Secrets

When build process needs credentials (e.g., database access for code generation):

**In Dockerfile**:
```dockerfile
RUN --mount=type=secret,id=POSTGRES_PASSWORD,required \
    POSTGRES_PASSWORD=$(cat /run/secrets/POSTGRES_PASSWORD) \
    pnpm build
```

**In GitHub Actions**:
```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    secrets: |
      "POSTGRES_USER=${{ secrets.POSTGRES_USER }}"
      "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}"
```

Secrets mounted with `--mount=type=secret` never persist in image layers.

### Cache Strategy

**Self-hosted runners** (recommended):
```yaml
cache-from: type=local,src=/var/lib/docker-cache
cache-to: type=local,dest=/var/lib/docker-cache,mode=max
```

**GitHub-hosted runners**:
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

## Examples

### Example 1: Setting Up Basic Build Workflow

User request:
```
Set up GitHub Actions to build and push my Docker image on every push to main
```

You would:
1. Create `.github/workflows/build.yaml` in the repository
2. Configure environment variables for registry and image name
3. Add build job with:
   - Checkout code
   - Set up Docker Buildx
   - Login to registry
   - Extract metadata for tags
   - Build and push with local cache (for self-hosted) or GHA cache (for GitHub-hosted)
4. Test the workflow with a commit to main branch

### Example 2: Adding Deployment Workflow

User request:
```
Add deployment that triggers when the build completes successfully
```

You would:
1. Create `.github/workflows/deploy.yml` triggered by `workflow_run` event
2. Add condition to only run if build workflow succeeded
3. Configure deployment step with:
   - Retry logic using `nick-fields/retry-action@v3`
   - HTTP response validation
   - Proper error handling
4. Add optional failure notifications
5. Test by pushing to main and verifying deployment triggers after successful build

### Example 3: Optimizing Build Cache for Self-Hosted Runner

User request:
```
Our builds are taking 8 minutes on our Raspberry Pi runner, how can we speed them up?
```

You would:
1. Verify current build configuration lacks caching
2. Add local disk cache configuration:
   ```yaml
   cache-from: type=local,src=/var/lib/docker-cache
   cache-to: type=local,dest=/var/lib/docker-cache,mode=max
   ```
3. SSH into runner and create cache directory:
   ```bash
   mkdir -p /var/lib/docker-cache
   chown runner:runner /var/lib/docker-cache
   ```
4. Trigger a build and verify cache is created
5. Run second build and confirm time reduction (expect 1-3 min for code-only changes)

### Example 4: Securing Build-Time Secrets

User request:
```
My Next.js app needs database credentials during build. How do I pass them securely?
```

You would:
1. Verify Dockerfile uses `--mount=type=secret` pattern (correct approach)
2. Configure GitHub Actions workflow to pass secrets:
   ```yaml
   - name: Build and push
     uses: docker/build-push-action@v6
     with:
       secrets: |
         "POSTGRES_USER=${{ secrets.POSTGRES_USER }}"
         "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}"
   ```
3. Explain why this is secure (secrets don't persist in layers)
4. Ensure runtime secrets use environment variables instead
