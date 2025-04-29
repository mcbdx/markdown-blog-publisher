# Markdown Blog Publisher CLI

This is a simple command-line tool I built to manage and publish my blog posts written in Markdown. It converts Markdown to HTML, extracts frontmatter metadata, and publishes both the metadata and content to a database.

I use this CLI to manage content for my personal platform, allowing me to write blogs in [Obsidian](https://obsidian.md), version them, and publish them seamlessly.

---

## Features

- Convert Markdown to HTML (with code highlighting)
- Extract and parse frontmatter as Python dictionaries
- Publish metadata and content to your database via SQLAlchemy
- Version control content — only one active version per blog
- CLI flags to run full publish, metadata-only, or dry-run mode

---

## File Structure

```bash
.
├── content/sample.md      # Sample blog post with frontmatter
├── sample.html            # Output HTML generated from Markdown
├── generate_html.py       # Markdown → HTML + metadata extractor
├── publish_utils.py       # Utilities to publish data to DB
├── publish_blog.py        # Main CLI logic
```
---
## Sample Usage
`python publish_blog.py -f content/sample.md --dry-run`

