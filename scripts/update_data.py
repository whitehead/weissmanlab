"""
Update _data/publications.yml and _data/people.yml from PubMed and Google Sheets,
and sync people portrait images from Google Drive.

Usage:
    python scripts/update_data.py [--publications] [--people] [--images]

    With no flags, all three are updated.

    For --images, first-time use will open a browser for Google OAuth.
    Requires scripts/drive_credentials.json (OAuth client secrets from Google Cloud Console).
    After the first auth, a token is cached in scripts/drive_token.json.
"""

import argparse
import io
import os
import tempfile
import yaml
import pandas as pd
from pathlib import Path
from PIL import Image
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from pymed import PubMed

PUBMED_EMAIL = "lenail@mit.edu"
PEOPLE_IMAGES_FOLDER_ID = "1Je52Gv36cGsAH1q1Xsj7hfnwu5gegTLh"
IMAGES_DIR = "assets/img/people"
MAX_IMAGE_DIMENSION = 1200  # pixels on longest side
MAX_IMAGE_BYTES = 3 * 1024 * 1024
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
DRIVE_CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "drive_credentials.json")
DRIVE_TOKEN_FILE = os.path.join(os.path.dirname(__file__), "drive_token.json")

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


def _get_drive_service():
    creds = None
    if os.path.exists(DRIVE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(DRIVE_TOKEN_FILE, DRIVE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(DRIVE_CREDENTIALS_FILE, DRIVE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(DRIVE_TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("drive", "v3", credentials=creds)


def update_images():
    print("Fetching people images from Google Drive...")
    service = _get_drive_service()

    results = service.files().list(
        q=f"'{PEOPLE_IMAGES_FOLDER_ID}' in parents and trashed=false",
        fields="files(id,name)",
        pageSize=1000,
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
    ).execute()

    all_files = results.get("files", [])
    print(f"  Found {len(all_files)} file(s) in folder")
    if all_files:
        print(f"  Files: {[f['name'] for f in all_files]}")

    files = [
        f for f in all_files
        if Path(f["name"]).suffix.lower() in (".jpg", ".jpeg", ".png")
    ]
    print(f"  Found {len(files)} image(s)")

    os.makedirs(IMAGES_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            p = Path(file["name"])
            tmp_path = os.path.join(tmpdir, file["name"])

            request = service.files().get_media(fileId=file["id"])
            with io.FileIO(tmp_path, "wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()

            dest = os.path.join(IMAGES_DIR, f"{p.stem}.jpg")
            img = Image.open(tmp_path)
            if img.mode != "RGB":
                img = img.convert("RGB")

            w, h = img.size
            if max(w, h) > MAX_IMAGE_DIMENSION:
                ratio = MAX_IMAGE_DIMENSION / max(w, h)
                img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

            quality = 85
            img.save(dest, "JPEG", quality=quality)
            while os.path.getsize(dest) > MAX_IMAGE_BYTES and quality > 50:
                quality -= 10
                img.save(dest, "JPEG", quality=quality)

            img.close()
            print(f"  Saved {p.stem}.jpg ({os.path.getsize(dest) // 1024}KB)")

    print(f"  Processed {len(files)} image(s)")


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
    parser.add_argument("--images", action="store_true")
    args = parser.parse_args()

    run_all = not args.publications and not args.people and not args.images
    if args.publications or run_all:
        update_publications()
    if args.people or run_all:
        update_people()
    if args.images or run_all:
        update_images()
