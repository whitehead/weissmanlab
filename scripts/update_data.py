"""
Update _data/publications.yml and _data/people.yml from PubMed and Google Sheets.

Usage:
    python scripts/update_data.py [--publications] [--people]

    With no flags, both are updated.
"""

import argparse
import yaml
import pandas as pd
from pymed import PubMed

PUBMED_EMAIL = "lenail@mit.edu"
PEOPLE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1-Eju9h1XovEBoBv0DGpxh92GYsZ8bzGkxRdRgUb7hvg"
    "/export?format=csv"
)

# PubMed IDs to exclude (e.g. author corrections)
REMOVE_PUBMED_IDS = ["37853259", "38740926"]

JOURNAL_REPLACEMENTS = {
    "bioRxiv : the preprint server for biology": "biorxiv",
    "Methods in molecular biology (Clifton, N.J.)": "Methods in molecular biology",
    "Current biology : CB": "Current biology",
    "Science (New York, N.Y.)": "Science",
    "Proceedings of the National Academy of Sciences of the United States of America": "PNAS",
    "Molecular & cellular proteomics : MCP": "Molecular & cellular proteomics",
}


def update_publications():
    print("Fetching publications from PubMed...")
    pubmed = PubMed(tool="WeissmanLabSite", email=PUBMED_EMAIL)
    results = list(pubmed.query("Jonathan Weissman", max_results=500))
    print(f"  Found {len(results)} results")

    new_pubs = []
    for result in results:
        try:
            new_pubs.append(dict(
                title=result.title,
                authors=[
                    f"{a['firstname']} {a['lastname']}"
                    for a in result.authors
                ],
                publication_date=result.publication_date.strftime("%d/%m/%y"),
                publication_year=result.publication_date.strftime("%Y"),
                pubmed_id=result.pubmed_id.split("\n")[0],
                abstract=result.abstract,
                doi=result.doi.split("\n")[0],
                journal=result.journal,
            ))
        except Exception:
            print(f"  Skipping: {getattr(result, 'title', '(unknown)')}")

    df_new = pd.DataFrame.from_records(new_pubs)
    df_new["journal"] = df_new["journal"].replace(JOURNAL_REPLACEMENTS)
    df_new = df_new[~df_new["pubmed_id"].isin(REMOVE_PUBMED_IDS)]

    with open("_data/publications.yml") as f:
        df_old = pd.json_normalize(yaml.safe_load(f))

    # Add publications whose DOI isn't already in the file; keep all old entries.
    df_added = df_new[~df_new["doi"].isin(df_old["doi"])]
    print(f"  {len(df_added)} new publication(s) to add")

    df_merged = pd.concat([df_added, df_old]).sort_values(
        ["publication_year", "pubmed_id"], ascending=False
    ).reset_index(drop=True)

    records = [
        {k: v for k, v in row.items() if str(v) != "nan"}
        for row in df_merged.to_dict(orient="records")
    ]

    with open("_data/publications.yml", "w") as f:
        yaml.dump(records, f, default_flow_style=False, sort_keys=False)

    print("  Written to _data/publications.yml")


def update_people():
    print("Fetching people from Google Sheets...")
    people = pd.read_csv(PEOPLE_SHEET_URL)
    df_obj = people.select_dtypes(["object"])
    people[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    print(f"  Found {len(people)} people")

    class _Dumper(yaml.SafeDumper):
        def write_line_break(self, data=None):
            super().write_line_break(data)
            if len(self.indents) == 1:
                super().write_line_break()

    records = [
        {k: v for k, v in row.items() if pd.notnull(v)}
        for row in people.to_dict(orient="records")
    ]

    with open("_data/people.yml", "w") as f:
        yaml.dump(records, f, Dumper=_Dumper, default_flow_style=False, sort_keys=False)

    print("  Written to _data/people.yml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publications", action="store_true")
    parser.add_argument("--people", action="store_true")
    args = parser.parse_args()

    run_all = not args.publications and not args.people
    if args.publications or run_all:
        update_publications()
    if args.people or run_all:
        update_people()
