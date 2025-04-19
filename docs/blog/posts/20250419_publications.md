---
date: 2025-04-19
author: yinchi
slug: automating-my-publications-page
categories:
  - Python
---

# Automating my publications page

I wanted to create a new personal website using [MkDocs](https://www.mkdocs.org/), as my old website was based on [Academic Pages](https://academicpages.github.io/), a Ruby-based template, and I am infinitely more familiar with Python.  As part of this migration, I wanted a way to automate my [Publications](/publications) page from a BibTeX file.

<!-- more -->

The first part of the answer was to use a plugin: [mkdocs-bibtex](https://pypi.org/project/mkdocs-bibtex/).  This allows me to write Markdown code such as

`@mypaper`

which the plugin automatically converts into something like:

```
@ChanProcess2024
```

!!! warning

    As it turns out, `mkdocs-bibtex` will automatically convert reference labels even in code blocks, so I cannot use the actual label for this paper or any other paper in my BibTeX file.  `@` followed by anything **not** in my BibTeX file is fine, though.

Next, I needed to point MkDocs to my bibliography file and style file, in `mkdocs.yml`:

```yml
plugins:
  - bibtex:
      bib_file: yinchi.bib
      csl_file: ieee-with-url.csl
```

## Generating the Markdown file

Then, I needed a script to convert my BibTeX file into a Markdown file.  The [pybtex](https://pybtex.org/) Python package seems to do the job:

```py
from pybtex.database import parse_file
import calendar
from pathlib import Path

bib = parse_file('yinchi.bib')
```

To sort my references chronologically, I first needed to extract the year and months, converting both into integers first:

```py
def month(s: str | None):
    if s is None: return 0
    if s.title() in map_short: return map_short[s]
    elif s.title() in map_long: return map_long[s]
    else: return 0

def y_m(bib, key):
    y = int(bib.entries[key].fields['year'])
    m = month(bib.entries[key].fields.get('month', None))
    return (y, m)

d = {k: y_m(bib, k) for k in bib.entries.keys() if bib.entries[k].type not in ['patent']}
d = dict(sorted(d.items(), key=lambda i: i[1], reverse=True))
```

It was then just a matter of writing the sorted BibTeX entries to a file:

```py
with open('docs/publications.md', 'w', encoding='utf-8') as fp:

    # Stuff that goes before the list
    print('# Publications', file=fp)
    print(file=fp)
    print('Google Scholar profile: [link](https://scholar.google.com/citations?user=NJEB3swAAAAJ)', file=fp)
    print(file=fp)

    # The publications list
    # Just use `1.` for each entry, Markdown will handle the numbering
    for k, v in d.items():
        print(f'1. @{k}')
        print(f'1. @{k}', file=fp)

        # Link to files if present
        path = f'papers/{k}.pdf'
        if Path(f'docs/{path}').is_file():
            print(f'    - [PDF]({path})')
            print(f'    - [PDF]({path})', file=fp)
        path = f'papers/{k}_slides.pdf'
        if Path(f'docs/{path}').is_file():
            print(f'    - [Slides]({path})')
            print(f'    - [Slides]({path})', file=fp)
```

## Displaying my name in bold

Displaying my name in bold required a bit of DOM manipulation:

```py
    print('''\

<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.md-content ol').innerHTML = document.querySelector('.md-content ol').innerHTML.replaceAll('Y.-C. Chan', '<b>Y.-C. Chan</b>')
})
</script>
''', file=fp)
```

The above works since the Publications page has only one `<ol>` element.

That's it!  The setup still has some quirks, such as pybtex/mkdocs-bibtex not parsing months in the `.bib` file correctly (other than May which doesn't use an abbreviation), but it's... usable, I guess?
