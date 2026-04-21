#!/bin/bash
# publish.sh — The Immutable Ledger one-command publishing workflow
# ---------------------------------------------------------------
# Pulls Ready to Publish articles from Notion, validates, commits and pushes.
# Run this from the repo root: ./publish.sh

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  THE IMMUTABLE LEDGER — Publishing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check .env exists
if [ ! -f ".env" ]; then
  echo "ERROR: .env file not found."
  echo "Copy .env.example to .env and add your NOTION_TOKEN."
  exit 1
fi

# Check Python packages
python3 -c "import notion_client, dotenv" 2>/dev/null || {
  echo "Installing required Python packages…"
  pip3 install notion-client python-dotenv --quiet
}

echo ""
echo "Step 1: Pulling from Notion…"
python3 scripts/notion_to_html.py

echo ""
echo "Step 2: Validating content…"
python3 scripts/validate_content.py

echo ""
echo "Step 3: Committing and pushing to GitHub…"
git add .
git commit -m "Publish content update $(date +%Y-%m-%d)"
git push

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done. Vercel will deploy automatically."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
