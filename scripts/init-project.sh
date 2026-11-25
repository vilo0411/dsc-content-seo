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
cp -r .agents "$PROJECT_NAME/"
cp AGENTS.md GEMINI.md "$PROJECT_NAME/"
cp CLAUDE.md "$PROJECT_NAME/"
cp README.md "$PROJECT_NAME/"

# Initialize data and production folders
mkdir -p "$PROJECT_NAME/knowledge/1-brand"
mkdir -p "$PROJECT_NAME/knowledge/2-market"
mkdir -p "$PROJECT_NAME/knowledge/3-seo"
mkdir -p "$PROJECT_NAME/knowledge/4-channels"
mkdir -p "$PROJECT_NAME/knowledge/5-analytics"
mkdir -p "$PROJECT_NAME/knowledge/raw"
mkdir -p "$PROJECT_NAME/knowledge/3-seo/content/0-sources"
mkdir -p "$PROJECT_NAME/knowledge/3-seo/content/1-outlines"
mkdir -p "$PROJECT_NAME/knowledge/3-seo/content/2-drafts"
mkdir -p "$PROJECT_NAME/knowledge/3-seo/content/3-finalized"
mkdir -p "$PROJECT_NAME/knowledge/raw/intel"

# Copy internal templates to knowledge folder
cp -r .agents/templates/* "$PROJECT_NAME/knowledge/" 2>/dev/null || true

echo "✅ Project '$PROJECT_NAME' created successfully with Zen Structure!"
echo "👉 Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. Run '/setup all' to start interactive onboarding."
