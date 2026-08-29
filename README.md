# High Performance AI Lab

A static, markdown-driven home for the lab. Built with Astro and deployed
to GitHub Pages at <https://highperformanceailab.com> — this
repository is the org-domain repository, so the site serves from the
domain root.

## Run it locally

```bash
npm install
npm run dev
```

Run `npm run build` to validate all project frontmatter and produce the static site in `dist/`.
Run `npm run check:social` after a build to verify that every page has complete
Open Graph and X card metadata and that the 1200×630 preview is published.

## Add a product

Products are flagship offerings shown in the homepage **Platform** section (a FIG-numbered bento with metrics). Add one Markdown file to [`src/content/products`](src/content/products). At least one should set `featured: true`.

```md
---
name: "Ferrite"
tagline: "One-line pitch."
description: "What it does and why it matters."
eyebrow: "01 — Inference Engine"
category: "Platform"
url: "https://github.com/owner/repo" # optional
command: "ferrite serve model.gguf" # optional, shown as a terminal line
accent: "teal" # teal | cyan | violet | amber | rose
order: 1
featured: true
features:
  - code: "01"
    label: "Short feature title"
    detail: "One sentence of detail."
metrics:
  - value: "75.6"      # numbers animate as counters
    label: "tok/s decode · model · device"
---

Optional body notes for future detail pages.
```

## Add a project


Add one Markdown file to [`src/content/projects`](src/content/projects). The next build validates it and places it in the project gallery automatically.

```md
---
title: "project-name"
tagline: "The shortest, strongest reason this project should exist."
eyebrow: "07 — Short project type"
description: "One crisp sentence about what it does and why it matters."
url: "https://github.com/owner/repository" # optional
category: "systems" # systems | tools | education
tags: ["Rust", "Metal", "Inference"]
order: 7
stackOrder: 7 # position in the system map
stackAction: "Extend" # short verb: Run, Observe, Teach...
stackRole: "What this project contributes to the stack"
accent: "cobalt" # oxide | cobalt | citron | violet | moss | amber
icon: "checkpoint" # lattice | checkpoint | proof | curriculum | neural-die | trace
status: "open source"
metric: "42 tok/s" # optional
metricLabel: "model · device · conditions" # optional
command: "cargo run --release" # optional
featured: false
---

Longer project notes can live here for future detail pages.
```

The schema is defined in [`src/content.config.ts`](src/content.config.ts). Gallery markup is in [`src/components/ProjectCard.astro`](src/components/ProjectCard.astro).

## Add an article or news item

Add a Markdown file to `src/content/articles`. Its body becomes a standalone article page. Set an optional `url` when the item should point to an external publication instead.

```md
---
title: "A useful, specific headline"
description: "The one-sentence reason to read it."
publishedAt: 2026-07-27
kind: "article" # article | news | field-note
author: "High Performance AI Lab"
tags: ["Inference", "Metal"]
readingTime: "6 min"
featured: false
---

Write the article in Markdown here.
```

## Add a team member

Add one Markdown file to `src/content/team`. The homepage orders profiles by the `order` field.

```md
---
name: "Full name"
role: "Role or research focus"
bio: "A concise description of their work."
initials: "FN"
location: "City, Country"
order: 2
accent: "moss"
github: "https://github.com/username" # optional
website: "https://example.com" # optional
---
```

## Deploy

The workflow in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) builds and publishes the site on every push to `main`. In the GitHub repository settings, set **Pages → Source** to **GitHub Actions**.

The workflow detects both GitHub user/organization sites and project sites, and configures Astro's base path accordingly.

## License

MIT OR Apache-2.0, at your option (see `LICENSE-MIT` and `LICENSE-APACHE`).
