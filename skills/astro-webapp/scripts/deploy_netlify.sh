#!/bin/bash

# Deploy Astro site to Netlify
# Usage: ./deploy_netlify.sh [production|staging]

set -e

ENVIRONMENT=${1:-production}
BUILD_DIR="dist"

echo "🚀 Deploying to Netlify ($ENVIRONMENT)"

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "📦 Installing Netlify CLI..."
    npm install -g netlify-cli
fi

# Build the project
echo "🔨 Building project..."
npm run build

# Check if build was successful
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Build failed: $BUILD_DIR directory not found"
    exit 1
fi

# Deploy based on environment
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🌍 Deploying to production..."
    netlify deploy --prod --dir=$BUILD_DIR
elif [ "$ENVIRONMENT" = "staging" ]; then
    echo "🔧 Deploying to staging (draft)..."
    netlify deploy --dir=$BUILD_DIR
else
    echo "❌ Unknown environment: $ENVIRONMENT"
    echo "Usage: $0 [production|staging]"
    exit 1
fi

echo "✅ Deployment complete!"
echo ""
echo "📝 Remember to set environment variables in Netlify:"
echo "   - PUBLIC_WEB3FORMS_KEY"
echo "   - PUBLIC_SITE_URL"
