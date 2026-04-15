#!/bin/bash
# ─────────────────────────────────────────────────────
# The Immutable Ledger — GitHub + Vercel Setup Script
# Run this from inside the "The Immutable Ledger" folder
# in your Terminal: bash SETUP.sh
# ─────────────────────────────────────────────────────

set -e

echo ""
echo "═══════════════════════════════════════════════"
echo "  THE IMMUTABLE LEDGER — Setup Script"
echo "═══════════════════════════════════════════════"
echo ""

# 1. Clean up any broken .git folder from the sandbox
if [ -d ".git" ]; then
  echo "→ Removing previous incomplete .git folder..."
  rm -rf .git
  echo "  Done."
fi

# 2. Initialise fresh git repo
echo "→ Initialising git repository..."
git init
git branch -m main
echo "  Done."

# 3. Set git identity (edit these if needed)
git config user.name "Doug Kilburn"
git config user.email "dougkilburn@icloud.com"

# 4. Stage all site files
echo "→ Staging files..."
git add *.html *.css *.json .gitignore
echo "  Done."

# 5. Initial commit
echo "→ Creating initial commit..."
git commit -m "Initial publish: The Immutable Ledger v1.0"
echo "  Done."

echo ""
echo "═══════════════════════════════════════════════"
echo "  Git setup complete!"
echo ""
echo "  NEXT STEPS:"
echo ""
echo "  1. Create a new repo at https://github.com/new"
echo "     Name it: the-immutable-ledger"
echo "     Set it to: Public (required for free Vercel)"
echo "     Do NOT add README or .gitignore — the repo should be empty"
echo ""
echo "  2. Run these two commands (replace YOUR_GITHUB_USERNAME):"
echo ""
echo "     git remote add origin https://github.com/YOUR_GITHUB_USERNAME/the-immutable-ledger.git"
echo "     git push -u origin main"
echo ""
echo "  3. Go to https://vercel.com → New Project → Import from GitHub"
echo "     Select: the-immutable-ledger"
echo "     Framework: Other (static)"
echo "     Click Deploy"
echo ""
echo "  4. Your site will be live at:"
echo "     https://the-immutable-ledger.vercel.app"
echo ""
echo "  5. See GO-LIVE-GUIDE.md for Google AdSense and domain setup"
echo "═══════════════════════════════════════════════"
echo ""
