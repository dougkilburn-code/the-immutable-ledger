# Publishing Workflow

This is your plain-English guide to publishing a new article on The Immutable Ledger.

---

## How it works

You write articles in Notion. When you're ready to publish, you flip a status switch.
One command on your Mac pulls the article, generates the HTML, updates the homepage,
and pushes it live to Vercel. You don't touch any code.

---

## One-time setup (do this once)

### 1. Install Python packages

Open Terminal and run:

```
pip3 install notion-client python-dotenv
```

### 2. Create your .env file

In the repo folder, copy the example file:

```
cp .env.example .env
```

Open `.env` in any text editor and paste your Notion integration token after `NOTION_TOKEN=`.

The database ID is already filled in for you.

Your `.env` file should look like this:

```
NOTION_TOKEN=secret_abc123...
NOTION_DATABASE_ID=6ee8941088a24e4f8b1da35cedda1529
```

### 3. Make the publish script executable

```
chmod +x publish.sh
```

---

## Writing an article in Notion

1. Open **The Immutable Ledger → Immutable Ledger Articles** database in Notion
2. Click **New** to create a new article
3. Fill in the properties:
   - **Title** — the full headline
   - **Slug** — short URL name, lowercase, hyphens only (e.g. `bnpl-new-product`)
   - **Date** — publication date
   - **Category** — pick one: Payments, Technology, Agentic AI, Crypto, Regulation, Consumer, Conferences
   - **Summary** — one sentence shown on the homepage card
   - **HeroImage** — filename from `img/clean_images/`, e.g. `article-bnpl.jpg`
   - **Author** — byline name
4. Write the article body in the page content area (below the properties)
5. When ready, change **Status** from **Not started** to **In progress**

> The script pulls articles with Status = **In progress**. After publishing, it automatically sets them to **Done**.

---

## Publishing (every time)

Open Terminal, navigate to the repo folder, and run:

```
./publish.sh
```

That's it. The script will:
- Pull your ready articles from Notion
- Generate the HTML files
- Add them to the homepage in the right category section
- Validate everything looks correct
- Commit and push to GitHub
- Vercel deploys automatically within about 30 seconds

---

## After publishing

- Check the live site to confirm the article appeared correctly
- The homepage card is added at the top of the category section automatically
- If you want the article featured in the hero/top-of-page slot, edit `index.html` manually

---

## Status meanings

| Notion Status | Meaning |
|---|---|
| Not started | Draft — not ready |
| In progress | Ready to Publish — script will pick this up |
| Done | Published — already live |

---

## Troubleshooting

**"NOTION_TOKEN not set"** — check your `.env` file exists and the token is pasted correctly

**"No articles ready to publish"** — make sure Status is set to **In progress** in Notion

**Article appeared but hero image is broken** — check the HeroImage field matches a file in `img/clean_images/`

**Article not appearing in the right category** — check the Category field is set correctly in Notion
