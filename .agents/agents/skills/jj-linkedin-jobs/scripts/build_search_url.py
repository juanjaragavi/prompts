#!/usr/bin/env python3
"""Build a LinkedIn Jobs search URL from job titles, locations, work modes, and
employment types.

LinkedIn Jobs search filters are encoded as short, non-obvious query params
(f_WT, f_JT, etc.) that are easy to get wrong by hand. This script encodes them
correctly so the result can be opened directly with a browser automation tool.

Usage:
    python3 build_search_url.py \
        --titles "Prompt Engineer" "AI Engineer" \
        --locations "Bogota, D.C., Capital District, Colombia" "Mexico City, Mexico" \
        --work-mode remote onsite \
        --employment-type F C T

Notes:
    - LinkedIn only accepts a single `location` value per search URL. This
      script prints one URL per requested location so the full preference set
      (e.g. Juan Jaramillo's four target cities) can be covered with one run
      per city, or omit --locations for a remote-anywhere / keywords-only
      search.
    - Employment type codes follow LinkedIn's own scheme: F=Full-time,
      P=Part-time, C=Contract, T=Temporary, V=Volunteer, I=Internship,
      O=Other. There is no distinct "Hourly" code -- treat hourly-rate
      preference as Contract/Temporary and mention it in the application
      message instead.
"""
import argparse
import urllib.parse

WORK_MODE_CODES = {"onsite": "1", "remote": "2", "hybrid": "3"}
EMPLOYMENT_TYPE_LABELS = {
    "F": "Full-time",
    "P": "Part-time",
    "C": "Contract",
    "T": "Temporary",
    "V": "Volunteer",
    "I": "Internship",
    "O": "Other",
}

BASE_URL = "https://www.linkedin.com/jobs/search/"


def build_keywords(titles):
    """Join multiple job titles into a single OR'd keyword query."""
    parts = [f'"{t}"' if " " in t else t for t in titles]
    return " OR ".join(parts)


def build_url(titles, location, work_modes, employment_types):
    params = {}
    if titles:
        params["keywords"] = build_keywords(titles)
    if location:
        params["location"] = location
    if work_modes:
        codes = sorted({WORK_MODE_CODES[m] for m in work_modes})
        params["f_WT"] = ",".join(codes)
    if employment_types:
        params["f_JT"] = ",".join(employment_types)
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"{BASE_URL}?{query}"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--titles", nargs="+", required=True, help="Job titles/keywords to search for."
    )
    parser.add_argument(
        "--locations",
        nargs="*",
        default=[None],
        help="One or more locations. Omit for a location-agnostic (remote) search.",
    )
    parser.add_argument(
        "--work-mode",
        nargs="+",
        choices=WORK_MODE_CODES.keys(),
        default=["remote", "onsite"],
        help="Location types to include (default: remote onsite).",
    )
    parser.add_argument(
        "--employment-type",
        nargs="+",
        choices=EMPLOYMENT_TYPE_LABELS.keys(),
        default=["F", "C", "T"],
        help="Employment type codes to include (default: F C T).",
    )
    args = parser.parse_args()

    for location in args.locations:
        url = build_url(args.titles, location, args.work_mode, args.employment_type)
        label = location or "Remote / any location"
        print(f"{label}: {url}")


if __name__ == "__main__":
    main()
