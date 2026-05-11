#!/bin/bash

# SEO Writer Agent - Project Initializer (Zen Structure)
# Usage: ./setup.sh [project_name]

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup.sh [project_name]"
    exit 1
fi

echo "🚀 Initializing SEO Project: $PROJECT_NAME..."

# Create project directory
mkdir -p "$PROJECT_NAME"

# Copy engine core
cp -r .antigravity "$PROJECT_NAME/"
cp .cursorrules "$PROJECT_NAME/"
cp CLAUDE.md "$PROJECT_NAME/"
cp README.md "$PROJECT_NAME/"

# Initialize data and production folders
mkdir -p "$PROJECT_NAME/knowledge/1-brand"
mkdir -p "$PROJECT_NAME/knowledge/2-market"
mkdir -p "$PROJECT_NAME/knowledge/3-pipeline"
mkdir -p "$PROJECT_NAME/knowledge/raw"
mkdir -p "$PROJECT_NAME/content/blog/0-raw"
mkdir -p "$PROJECT_NAME/content/blog/1-outlines"
mkdir -p "$PROJECT_NAME/content/blog/2-user-review"
mkdir -p "$PROJECT_NAME/content/blog/3-finalized"

# Copy internal templates to knowledge folder
cp -r .antigravity/internal-templates/* "$PROJECT_NAME/knowledge/" 2>/dev/null || true

echo "✅ Project '$PROJECT_NAME' created successfully with Zen Structure!"
echo "👉 Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Run '/setup all' to start interactive onboarding."
