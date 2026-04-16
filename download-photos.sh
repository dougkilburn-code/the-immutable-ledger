#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# The Immutable Ledger — Photo Downloader
# Run this ONCE from Terminal, from inside the site folder:
#   bash download-photos.sh
#
# Downloads 15 unique themed photos from Unsplash's keyword API.
# Photos are saved to img/ and committed to git automatically.
# ─────────────────────────────────────────────────────────────────

cd "$(dirname "$0")"
mkdir -p img

echo "Downloading themed photos for The Immutable Ledger..."
echo ""

# Each curl follows redirects (-L) and saves to a specific filename.
# Unsplash keyword URLs return a relevant real photograph.

download() {
  local keyword="$1"
  local filename="$2"
  local path="img/$filename"
  printf "  %-40s → %s\n" "$keyword" "$filename"
  curl -s -L --max-time 15 \
    "https://source.unsplash.com/820x480/?${keyword}" \
    -o "$path"
  # Verify we got a real image (not an error page)
  local size
  size=$(wc -c < "$path" 2>/dev/null || echo 0)
  if [ "$size" -lt 5000 ]; then
    echo "    ⚠ Warning: $filename looks too small ($size bytes) — may have failed"
  else
    echo "    ✓ $(( size / 1024 ))KB"
  fi
}

# ── CONFERENCES & PEOPLE (30%) ────────────────────────────────────
download "conference,keynote,audience,stage"      "photo-conference.jpg"
download "fireside,chat,speakers,stage,interview" "photo-fireside.jpg"
download "business,meeting,boardroom,corporate"   "photo-boardroom.jpg"
download "luxury,hotel,ballroom,gala,event"       "photo-summit.jpg"

# ── BANKING & FINANCE (40%) ──────────────────────────────────────
download "bank,building,classical,institution"    "photo-bank.jpg"
download "payment,terminal,contactless,card"      "photo-payment.jpg"
download "money,currency,cash,finance"            "photo-money.jpg"
download "bitcoin,cryptocurrency,coin,digital"    "photo-crypto.jpg"
download "stock,market,trading,chart,finance"     "photo-trading.jpg"
download "shopping,retail,bags,consumer"          "photo-shopping.jpg"

# ── TECHNOLOGY (30%) ─────────────────────────────────────────────
download "server,rack,datacenter,technology"      "photo-servers.jpg"
download "coding,laptop,programming,developer"    "photo-coding.jpg"
download "circuit,board,chip,electronics"         "photo-circuit.jpg"
download "cloud,computing,sky,abstract"           "photo-cloud.jpg"
download "robot,artificial,intelligence,ai"       "photo-robot.jpg"

echo ""
echo "Download complete. Adding to git..."
git add img/photo-*.jpg
git commit -m "Add themed article photos — $(date '+%Y-%m-%d %H:%M')"
echo ""
echo "✓ Photos committed. Run 'git push' to deploy to Vercel."
