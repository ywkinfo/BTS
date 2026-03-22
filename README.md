# BTS Volvio Hub

Static Spanish-language content hub about BTS's 2026 comeback, built as a dependency-free multi-page site.

## Run locally

Use any static file server. A simple option:

```bash
cd /Users/peter/BTS
python3 -m http.server 4173
```

Then open [http://localhost:4173](http://localhost:4173).

## Structure

- `index.html`: landing page and reading routes
- `pages/`: 12 editorial pages for comeback, timeline, members, tour, and future outlook
- `styles/site.css`: shared visual system and responsive layout
- `scripts/site.js`: mobile navigation and small enhancements

## Editorial defaults

- Language: Spanish
- Audience: Mexico and LATAM first, Spain second
- Tone: neutral, explanatory, beginner-friendly
- Format: static hub pages, no comments or membership features

## Content notes

- Pages use official and high-trust public sources linked in each article.
- Dates are written explicitly to avoid ambiguity for event-driven pages.

## Launch checklist

- If you deploy through the included GitHub Pages workflow, the placeholder domain `https://bts-volvio.example` is replaced automatically at build time.
- If you deploy some other way, replace that placeholder production domain in canonical tags, `sitemap.xml`, `robots.txt`, and JSON-LD before going live.
- Add your real analytics/Search Console setup after the production domain is connected.

## GitHub Pages

This repo now includes a GitHub Pages workflow at `.github/workflows/deploy-pages.yml`.

### Default GitHub Pages URL behavior

- If your repository is named `<owner>.github.io`, the workflow builds for `https://<owner>.github.io`
- Otherwise it builds for `https://<owner>.github.io/<repository>`

The workflow computes the correct public URL and rewrites the placeholder production domain during the build, so canonical tags, structured data, and `sitemap.xml` stay correct for GitHub Pages.

### How to publish

1. Push this project to a **public GitHub repository**.
2. In GitHub, open `Settings` > `Pages`.
3. Under `Build and deployment`, choose `GitHub Actions` as the source.
4. Push to `main` or `master`, or run the `Deploy to GitHub Pages` workflow manually.

### Optional custom domain

If you want to build the site for a custom domain, add a repository variable named `PAGES_CUSTOM_DOMAIN` with a value like `example.com`.

This will make the workflow build canonical tags and sitemap entries for that domain.
You should still configure the custom domain in `Settings` > `Pages` on GitHub.

### Local Pages-style build

You can preview the built output with:

```bash
cd /Users/peter/BTS
python3 tools/build_pages.py --site-url https://example.com --output-dir _site
cd _site
python3 -m http.server 4173
```
