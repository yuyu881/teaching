"""Render the teaching portal as a static GitHub Pages site."""

import argparse
from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
from string import Template
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
TAIPEI = timezone(timedelta(hours=8))


def render_cards(subjects):
    cards = []
    for index, subject in enumerate(subjects):
        for material in subject["materials"]:
            url = urlsplit(material["url"])
            if url.scheme != "https" or url.netloc != "yuyu881.github.io":
                raise ValueError(f"Unapproved teaching URL: {material['url']}")
            subject_id = escape(subject["id"])
            title = escape(material["title"])
            description = escape(material["description"])
            href = escape(material["url"])
            hidden = " hidden" if index else ""
            cards.append(
                f'<li class="card" data-subject="{subject_id}"{hidden}>\n'
                f"  <h3>{title}</h3>\n"
                f"  <p>{description}</p>\n"
                f'  <a class="entry" href="{href}" aria-label="進入網頁：{title}">'
                '進入網頁 <span aria-hidden="true">→</span></a>\n'
                "</li>"
            )
    return "\n".join(cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog.json")
    args = parser.parse_args()
    built_at = datetime.fromisoformat(os.environ["DEPLOYED_AT"])
    if built_at.utcoffset() is None:
        raise ValueError("DEPLOYED_AT must include a timezone")
    built_at = built_at.astimezone(TAIPEI)
    subjects = json.loads(args.catalog.read_text(encoding="utf-8"))
    if not subjects or len({subject["id"] for subject in subjects}) != len(subjects):
        raise ValueError("Provide at least one subject and unique subject IDs")
    options = "\n".join(
        f'<option value="{escape(subject["id"])}">{escape(subject["name"])}</option>'
        for subject in subjects
    )
    count = len(subjects[0]["materials"])
    template = Template((ROOT / "index.template.html").read_text(encoding="utf-8"))
    html = template.substitute(
        subject_options=options,
        initial_count=count,
        cards=render_cards(subjects),
        empty_state="hidden" if count else "",
        year=built_at.year,
        iso_time=built_at.isoformat(timespec="seconds"),
        display_time=built_at.strftime("%Y-%m-%d %H:%M Asia/Taipei"),
    )
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
