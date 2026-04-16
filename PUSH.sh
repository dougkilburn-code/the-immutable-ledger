#!/bin/bash
# ─────────────────────────────────────────────────────
# The Immutable Ledger — Push latest changes to Vercel
# Run from inside "The Immutable Ledger" folder:
#   bash PUSH.sh
# ─────────────────────────────────────────────────────

set -e

cd "$(dirname "$0")"

echo ""
echo "═══════════════════════════════════════════════"
echo "  THE IMMUTABLE LEDGER — Deploying to Vercel"
echo "═══════════════════════════════════════════════"
echo ""

# Stage all site files
echo "→ Staging all changes..."
git add *.html *.css *.json

# Commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
git commit -m "WSJ-style layout: centre hero, thumbnail rails, tablet breakpoint — $TIMESTAMP"
echo "  Committed."

# Push
echo "→ Pushing to GitHub (Vercel will auto-deploy in ~30 seconds)..."
git push
echo "  Done!"

echo ""
echo "═══════════════════════════════════════════════"
echo "  Deployed!  View live at:"
echo "  https://the-immutable-ledger.vercel.app"
echo "═══════════════════════════════════════════════"
echo ""
