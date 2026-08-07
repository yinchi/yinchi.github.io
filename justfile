# Default: list all available tasks in an interactive menu.
default:
    just --choose

# Local dev server with live reload.
serve:
    hugo server -w

# Production-equivalent build, mirrors what CI runs.
build:
    hugo --gc --minify

# Scaffold a new blog post.
new-post title:
    hugo new content/posts/{{title}}.md

# Regenerate Toha publications data from yinchi.bib (script added in Phase B step 7).
pubs:
    uv run scripts/convert_publications.py

# Build + check for broken internal links.
check: build
    htmltest

# Remove Hugo's build caches.
clean:
    rm -rf public resources
