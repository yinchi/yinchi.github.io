# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pybtex",
#     "pyyaml",
# ]
# ///
"""Regenerate data/en/sections/publications.yaml from yinchi.bib.

yinchi.bib is the single source of truth. Each entry's `pubstate` field
(standard BibTeX field; e.g. `pubstate = {preprint}`) determines whether its
PDF is looked up under static/preprints/ or static/papers/, and is used to
tag the entry accordingly. Absent pubstate defaults to "published".

This file is fully generated -- do not hand-edit; re-run `just pubs` instead.
"""

import calendar
from pathlib import Path

import yaml
from pybtex.database import parse_file

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB_FILE = REPO_ROOT / "yinchi.bib"
OUTPUT_FILE = REPO_ROOT / "data" / "en" / "sections" / "publications.yaml"
PAPERS_DIR = REPO_ROOT / "static" / "papers"
PREPRINTS_DIR = REPO_ROOT / "static" / "preprints"

# Entry types not shown on the site (e.g. patents aren't public-facing here).
EXCLUDED_TYPES = {"patent"}

REQUIRED_FIELDS = ("title", "year")

_MONTH_ABBR = {m.lower(): n for n, m in enumerate(calendar.month_abbr) if n}
_MONTH_NAME = {m.lower(): n for n, m in enumerate(calendar.month_name) if n}


def strip_braces(s: str) -> str:
    """Remove literal BibTeX case-protection braces, e.g. "{Covid-19}" -> "Covid-19"."""
    return s.replace("{", "").replace("}", "")


def month_number(s: str | None) -> int:
    if not s:
        return 0
    return _MONTH_ABBR.get(s.lower()) or _MONTH_NAME.get(s.lower()) or 0


def format_date(year: str, month_field: str | None) -> str:
    m = month_number(month_field)
    if m:
        return f"{calendar.month_name[m]} {year}"
    return year


def initials(parts: list[str]) -> str:
    """"Yin-Chi" -> "Y.-C."; "W." -> "W." (idempotent on already-abbreviated parts)."""
    out = []
    for part in parts:
        segments = [seg for seg in part.split("-") if seg]
        out.append("-".join(f"{seg[0].upper()}." for seg in segments))
    return " ".join(out)


# Matched against the raw (un-abbreviated) BibTeX name parts, as spelled in yinchi.bib
# ("Chan, Yin-Chi"), so this doesn't depend on the initials-formatting logic below.
SITE_OWNER = {"first": ["Yin-Chi"], "last": ["Chan"]}


def is_site_owner(person) -> bool:
    return (
        person.get_part("first") == SITE_OWNER["first"]
        and person.get_part("last") == SITE_OWNER["last"]
    )


def format_author(person) -> str:
    first_middle = person.get_part("first") + person.get_part("middle")
    last = " ".join(person.get_part("last"))
    init = initials(first_middle)
    name = f"{init} {last}".strip()
    # Bolded via markdown; cards/publication.html has a small override to markdownify
    # author names so this renders instead of showing literal "**...**".
    return f"**{name}**" if is_site_owner(person) else name


def publication_venue(fields: dict) -> str:
    for key in ("journal", "booktitle", "publisher"):
        if key in fields:
            return strip_braces(fields[key])
    return ""


def paper_url(citekey: str, pubstate: str) -> str | None:
    directory = PREPRINTS_DIR if pubstate == "preprint" else PAPERS_DIR
    pdf_path = directory / f"{citekey}.pdf"
    if pdf_path.is_file():
        return f"/{directory.name}/{citekey}.pdf"
    return None


def slides_url(citekey: str, pubstate: str) -> str | None:
    directory = PREPRINTS_DIR if pubstate == "preprint" else PAPERS_DIR
    slides_path = directory / f"{citekey}_slides.pdf"
    if slides_path.is_file():
        return f"/{directory.name}/{citekey}_slides.pdf"
    return None


def convert_entry(citekey: str, entry) -> dict | None:
    fields = entry.fields
    missing = [f for f in REQUIRED_FIELDS if f not in fields]
    if missing:
        print(f"WARN: skipping {citekey}, missing required field(s): {missing}")
        return None

    pubstate = fields.get("pubstate", "published")
    doi = fields.get("doi")
    doi_url = f"https://doi.org/{doi}" if doi else fields.get("url")

    pub = {
        "title": strip_braces(fields["title"]),
        "publishedIn": {
            "name": publication_venue(fields),
            "date": format_date(fields["year"], fields.get("month")),
        },
        "authors": [
            {"name": format_author(p)} for p in entry.persons.get("author", [])
        ],
        "paper": {},
        "tags": [pubstate] if pubstate != "published" else [],
    }
    if doi_url:
        pub["publishedIn"]["url"] = doi_url

    url = paper_url(citekey, pubstate)
    pub["paper"]["url"] = url or doi_url

    slides = slides_url(citekey, pubstate)
    if slides:
        pub["paper"]["slidesUrl"] = slides

    return pub


def main() -> None:
    bib = parse_file(str(BIB_FILE))

    entries = [
        (key, e) for key, e in bib.entries.items() if e.type not in EXCLUDED_TYPES
    ]

    def sort_key(item):
        _, e = item
        f = e.fields
        return (int(f.get("year", 0)), month_number(f.get("month")))

    entries.sort(key=sort_key, reverse=True)

    publications = []
    for citekey, entry in entries:
        pub = convert_entry(citekey, entry)
        if pub is not None:
            publications.append(pub)

    output = {
        "section": {
            "name": "Publications",
            "id": "publications",
            # Moved off the homepage entirely -- full list lives at /publications/
            # instead (linked via customMenus in data/en/site.yaml).
            "enable": False,
            "weight": 3,
            "showOnNavbar": False,
        },
        "publications": publications,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as fp:
        fp.write(
            "# Auto-generated by scripts/convert_publications.py from yinchi.bib.\n"
            "# Do not edit by hand -- re-run `just pubs` instead.\n\n"
        )
        yaml.dump(output, fp, sort_keys=False, allow_unicode=True, width=100)

    print(f"Wrote {len(publications)} publication(s) to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
