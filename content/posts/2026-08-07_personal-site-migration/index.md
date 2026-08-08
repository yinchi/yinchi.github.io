---
title: "Migrating my personal site to Hugo"
date: 2026-08-08
tags: ["web", "Hugo"]
---

I got bored of my old personal website, which was built using [MkDocs](https://www.mkdocs.org/), and decided to migrate to [Hugo](https://gohugo.io/). The main reason for this migration was to refresh the look and feel of my personal website using a more modern and responsive theme. I eventually settled on the [Toha](https://themes.gohugo.io/themes/toha/) theme, which describes itself as "A Hugo theme for a personal portfolio with minimalist design and responsiveness."

The main difference I saw right away is that Hugo uses Go templates for its pages, which allows for more flexibility in customizing the layout and design of the website. For me, this included a bunch of tweaks to the Toha theme, stored as custom override HTML Go templates in `layouts/`:

- An "About Me" page, rather than stuffing all that content into the homepage.
- Allowing Markdown for publication author lists so I can bold my own name.
- Customized card layouts for publications and projects.
- Renaming page titles, e.g. "Blog Posts" instead of just "Posts".
- ...and many more tweaks

I also removed the sidebar from various pages, as we already have a top navigation bar and no sidebar was more visually appealing.

## Layouts

Most of Toha's page types share a common `baseof.html` template: a `navbar`/`sidebar`/`content`/`toc` block structure, with the actual page content living in a `content-section` column sized to sit alongside the sidebar. To remove the sidebar while not breaking page layouts altogether, I ended up bypassing `baseof.html` completely for the pages I cared about, replacing them with full rewrites in the `layouts/` directory of my project.

The one genuine priority surprise was the blog's tag pages. The override file `layouts/_default/list.html` works perfectly for the main Blog Posts page (`/posts/`), and since that same template generically handles anything Hugo treats as a "list" of pages, I assumed it would also cover tag pages like `/tags/tag1/` for free. It didn't: Hugo resolves templates by matching the *most specific* file it can find under `layouts/` before ever falling back to `_default/`, and Toha ships its own `layouts/tags/list.html` &mdash; based on the old `baseof.html` structure.  To fix this, I had to copy that file into my own `layouts/tags/list.html`, even though the overrides are essentially identical in both files (I eventually customized the page titles for tag pages as well, but that was a separate change).

## SCSS

The above changes and custom layouts broke CSS styling in some places. Toha uses SCSS for its styling, so I had to override some of the default styles in `assets/styles/override.scss`. This took a lot of trial and error.  One example: `.card .card-head` does not apply to card headers in the "Skills" section of the About Me page ([`/about#skills`]({{< ref "about.md#skills" >}})), because those headers are styled with `.skills-section .card .card-head` instead, and three CSS classes combined have higher specificity than two. So I had to add a special rule for that section, even though the styling is the same as the default card header styling.

The above customizations were only possible with the help of Claude Code, which had to dig deep into the Toha theme's Go templates and SCSS to figure out how to make the changes I wanted.  There were many attempts to get the SCSS right, but we eventually got it working.  Another issue we had: we had to remove a useless `search/` page that was part of the Toha theme, but in the process accidentally removed the font files as well &mdash; which broke the site on GitHub Pages only, while the local build worked fine!

## Internal link resolution and Hugo shortcodes

Toha provides a `{{</* ref */>}}` shortcode to resolve internal links, and an `{{</* img */>}}` shortcode to resolve image paths. There are two issues here:

1. The `{{</* ref */>}}` shortcode only works for pages that have a Hugo Page object. This is fine for most pages, but not for files under `static/`, which have no Page object, for example my CV (a .pdf file).
2. The `{{</* img */>}}` shortcode is not subpath-aware, so it will break if the site is hosted at a subpath, for example `https://yinchi.dev/me/` instead of `https://yinchi.dev/`.

For the first issue, the solution was to create a new shortcode, `{{</* relurl */>}}`.  However, this connects to the second issue: how to make `{{</* relurl */>}}` and `{{</* img */>}}` subpath-aware?

The solution was to use a helper function, `get-local-path`, defined in `layouts/partials/helpers/get-local-path.html`, which resolves internal paths against the subpath-aware baseURL.  This allows me to link to a static file using `{{</* relurl "/path/to/file" */>}}` without worrying about whether the site is hosted at the domain root or a subpath.  The same applies to images, e.g. `{{</* img "/images/foo.png" */>}}` will resolve correctly regardless of the hosting path. I had originally created this helper function to resolve the subpath-awareness issue independently of Hugo's shortcode processor: specifically, for the About Me page's CV link (`layouts/about-page/single.html`), and the Publications page's PDF and slides download buttons (`layouts/partials/cards/publication.html`). These don't need a shortcode wrapper at all, since they're plain Go templates rather than Markdown content &mdash; they can call the helper function's underlying partial directly.

An interesting thing I learned about Hugo shortcodes in the process: Hugo renders shortcodes in multiple stages:

1. First, every shortcode in a page is executed and its result stashed, while the code itself is replaced on the page with a placeholder token.
2. [Goldmark](https://github.com/yuin/goldmark/) then renders the Markdown file into HTML, retaining the placeholders. This means that Goldmark never sees any shortcodes or the content generated from them using the Go templates; it only sees the placeholder tokens.
3. A final pass afterwards swaps each placeholder back out for its real, pre-computed result, wherever it landed in the page.

For this reason, while it is possible to generate a render hook to process raw Markdown links, e.g. `[link text](path/to/file)`, this conflicts with the multi-stage rendering process and breaks link resolution for shortcodes like `{{</* ref */>}}`.  The solution was to abandon the render-hook approach and instead create the new `{{</* relurl */>}}` shortcode as mentioned above.

A further complication was found when writing this post: to describe shortcode syntax, we need to escape the shortcodes themselves, e.g. `{{</** ref **/>}}` with asterisks which Hugo strips out (while skipping the actual shortcode rendering).

## Publications list

The publications list is generated from a BibTeX file using a Python script. PEP 723 allows us to declare Python dependencies directly in a single-file script, which we ran using `uv run scripts/convert_publications.py`. The script generates a `data/en/sections/publications.yaml`, which is then used by Hugo to generate the [Publications]({{< ref "publications.md" >}}) page.  The key Python dependency is [pybtex](https://pybtex.org/), which parses the BibTeX file and allows us to extract the relevant fields for each publication; this package was also used in my previous MkDocs-based website, but the surrounding ecosystem is much simpler (`.bib` file to `.yaml` and Hugo handles the rest).

## CV

Along the way, I also updated my [CV]({{< relurl "/Yin-Chi_Chan_CV.pdf" >}}) using a YAML-based CV generator (Typst with the [RenderCV](https://typst.app/universe/package/rendercv/) template), as opposed to LaTeX before (with the [moderncv](https://ctan.org/pkg/moderncv) package).  The simpler build now uses a simple `uv run rendercv` command to generate the PDF &mdash; no more fiddling with LaTeX packages and templates. Unlike the Toha template above, I found the RenderCV template to be quite visually appealing out of the box, with only minor configuration needed to get the look I wanted.  A [just](https://just.systems/man/en/) recipe was used to copy the generated PDF to the `static/` folder of my site's working directory for Hugo to serve.

## Deployment and DNS

Simpler than I expected.  Bought a domain name from Cloudflare Registrar, and pointed it to my GitHub Pages site.  The GitHub Actions workflow file is largely based on Hugo's own [GitHub Pages deployment guide](https://gohugo.io/hosting-and-deployment/hosting-on-github/#github-actions), so all that remained was point my new domain name to the GitHub Pages site. This only required a pair of CNAME records in Cloudflare's DNS settings, as Cloudflare does something called [CNAME flattening](https://developers.cloudflare.com/dns/cname-flattening/) to allow a CNAME record at the root of the domain.

The trickier part was with GitHub itself: rename the old site's repository, deactivate Pages for it, then rename the new site's repository to the newly freed name, and activate Pages for it.  This is because despite the custom domain name, I still wanted to use `yinchi.github.io` as the repository name for the new site, as that is the expected repository name for a domain-root GitHub Pages site.

## Final remarks

Overall, I am quite happy with the new look and feel of my personal website.  The Toha theme is visually appealing, and the Hugo framework is much more flexible than MkDocs.  On the other hand, customizing the Toha theme was not trivial, and required a lot of trial and error to get the SCSS and Go template / shortcode logic right, but the end result is worth it.  I hope you enjoy the new look and feel of my personal website!