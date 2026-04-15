# The Immutable Ledger — Go-Live Guide

## Recommended Stack

| Layer | Service | Cost |
|---|---|---|
| **Hosting** | Vercel | Free (100GB bandwidth/month) |
| **Source control** | GitHub | Free |
| **Domain** | Cloudflare Registrar | ~$12–15 AUD/year |
| **Ads** | Google AdSense | Free (revenue share) |
| **Donations** | Ko-fi | Free (5% fee on donations) |

**Why Vercel over Netlify/GitHub Pages/AWS:**
- Fastest global CDN of any free tier
- Auto-deploys in ~30 seconds on every git push — Claude Cowork edits the files, you push one command, the site is live
- Clean URLs out of the box (already configured in `vercel.json`)
- Free SSL on custom domain
- No restrictions on AdSense or content

---

## Step 1 — Run the Setup Script

Open Terminal, navigate to the site folder, and run:

```bash
cd ~/path/to/Cowork/The\ Immutable\ Ledger
bash SETUP.sh
```

This initialises git, stages all files, and makes your first commit.

---

## Step 2 — Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `the-immutable-ledger`
3. Set to **Public** (required for Vercel free tier)
4. **Do not** tick "Add README", "Add .gitignore", or choose a licence — the repo must be empty
5. Click **Create repository**

Then run these two commands in your Terminal (replace `YOUR_USERNAME`):

```bash
git remote add origin https://github.com/YOUR_USERNAME/the-immutable-ledger.git
git push -u origin main
```

---

## Step 3 — Deploy to Vercel

1. Go to **https://vercel.com** and sign up (use your GitHub account — single click)
2. Click **Add New → Project**
3. Click **Import** next to `the-immutable-ledger`
4. Framework Preset: **Other**
5. Root Directory: leave as `/`
6. Click **Deploy**

Your site will be live in about 30 seconds at:
**`https://the-immutable-ledger.vercel.app`**

---

## Step 4 — Custom Domain (optional but recommended for AdSense)

### Buy the domain
Cheapest option: **Cloudflare Registrar** (https://dash.cloudflare.com) — at-cost pricing, no markup.
Recommended: `theimmutableledger.com` (~$12 USD/year) or `.com.au` (~$15 AUD/year)

### Connect to Vercel
1. In Vercel → your project → **Settings → Domains**
2. Add your domain
3. Vercel gives you DNS records to add
4. In Cloudflare → DNS → add those records
5. SSL certificate is automatic and free

---

## Step 5 — Google AdSense

> **Note:** AdSense requires a live site with real traffic before approval. Apply once the site has been live for a few weeks and has some visitors.

> **Satire note:** The site clearly labels itself "Satirical publication. All content fictional." in the footer. AdSense generally approves satirical sites — the key is the disclaimer is visible. If AdSense declines, **Media.net** (Yahoo/Bing backed) or **Carbon Ads** are good alternatives for a niche professional audience.

### Application
1. Go to **https://adsense.google.com**
2. Sign in with a Google account
3. Enter your site URL
4. Add the AdSense verification script to the `<head>` of every HTML page
5. Wait for approval (typically 1–2 weeks)

### Replacing Placeholders
Once approved, each `<!-- GOOGLE ADSENSE: replace... -->` comment in the HTML files shows exactly where to paste your `<ins class="adsbygoogle">` tags. There are:
- 1 leaderboard slot per page (below nav)
- 1 in-content slot per article (mid-article)
- 2 right-rail slots per article (300×250 and 300×600)

---

## Step 6 — Donation Button (Ko-fi)

1. Sign up at **https://ko-fi.com** (free — Ko-fi takes 0% on one-off donations, 5% on memberships)
2. Set up your page: "The Immutable Ledger"
3. Copy your Ko-fi button code
4. In `donate.html`, find the `<!-- PAYMENT INTEGRATION: replace this section -->` comment and paste the Ko-fi widget code there

Ko-fi also supports monthly memberships ("The Ledger Supporter" at $5/month) and a shop if you ever want to sell merchandise. Recommended first product: a "The Consultant Left The Building" tote bag.

---

## Step 7 — Private Sponsor Slots

The large dark sponsor banners on the homepage and pre-footer sections are ready for direct sponsors. To activate one:

1. Replace `<div class="ad-sponsor-logo-box">Your Logo Here</div>` with `<img src="sponsor-logo.png" alt="Sponsor Name" style="max-height:80px;">`
2. Update the headline and copy in `<div class="ad-sponsor-copy">`
3. Change the CTA link from `mailto:advertising@...` to the sponsor's URL
4. Commit and push — live in 30 seconds

---

## Ongoing Workflow (Claude Cowork → Live Site)

Once the GitHub + Vercel pipeline is set up, the workflow for new content is:

1. **Ask Claude (in Cowork)** to write a new article or update the site
2. Claude saves the files to your Cowork folder automatically
3. Open Terminal and run:
   ```bash
   cd ~/path/to/Cowork/The\ Immutable\ Ledger
   git add .
   git commit -m "New article: [headline]"
   git push
   ```
4. Vercel auto-deploys — **live in ~30 seconds**

That's it. No servers to manage, no build step, no deployment pipeline to configure.

---

## Cost Summary

| Item | Cost |
|---|---|
| Vercel hosting | $0/month |
| GitHub | $0/month |
| Domain (Cloudflare) | ~$1/month |
| Ko-fi donations | 0% fee |
| Google AdSense | Revenue share (you keep ~68%) |
| **Total fixed cost** | **~$1/month** |

---

## AdSense Revenue Expectations (realistic)

For a niche B2B audience like payments/fintech professionals:

| Monthly visitors | Estimated RPM | Monthly revenue |
|---|---|---|
| 1,000 | $8–15 | $8–15 |
| 5,000 | $8–15 | $40–75 |
| 20,000 | $10–20 | $200–400 |

RPM (revenue per 1,000 impressions) is higher for financial services audiences. Direct sponsorship rates should be significantly higher than AdSense — a presenting sponsor slot on a fintech trade publication targeting 10,000+ monthly readers in Australia would typically command $500–2,000/month in direct deals.
