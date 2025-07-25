from pybtex.database import parse_file
import calendar
from pathlib import Path

bib = parse_file('yinchi.bib')

map_short = {s: n for n, s in list(enumerate(calendar.month_abbr)) if n}
map_long = {s: n for n, s in list(enumerate(calendar.month_name)) if n}

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

with open('templates/_publications.md', 'r', encoding='utf-8') as fp:
    preamble = fp.read()

with open('docs/publications.md', 'w', encoding='utf-8') as fp:
    print(preamble, file=fp)
    for k, v in d.items():
        print(f'1. @{k}')
        print(f'1. @{k}', file=fp)
        path = f'papers/{k}.pdf'
        if Path(f'docs/{path}').is_file():
            print(f'    - [PDF]({path})')
            print(f'    - [PDF]({path})', file=fp)
        path = f'papers/{k}_slides.pdf'
        if Path(f'docs/{path}').is_file():
            print(f'    - [Slides]({path})')
            print(f'    - [Slides]({path})', file=fp)


    print('''\

<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.md-content ol').innerHTML = document.querySelector('.md-content ol').innerHTML.replaceAll('Y.-C. Chan', '<b>Y.-C. Chan</b>')
})
</script>
''', file=fp)
