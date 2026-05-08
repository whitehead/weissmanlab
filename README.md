## Weissman Lab Website

### Local testing

```
bundle exec jekyll serve
```

---

## Adding or updating a person

People and images are managed through two external sources that are synced into the repo automatically each Monday. You can also trigger a sync manually at any time.

- **People spreadsheet**: https://docs.google.com/spreadsheets/d/1-Eju9h1XovEBoBv0DGpxh92GYsZ8bzGkxRdRgUb7hvg
- **Portrait images folder**: https://drive.google.com/drive/folders/1Je52Gv36cGsAH1q1Xsj7hfnwu5gegTLh

---

### Step 1 — Add a row to the spreadsheet

Open the people spreadsheet and add a row with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `name` | Full name as it should appear on the site | `John Doe` |
| `pos` | Position — must match exactly one of the values below | `Post-doc` |
| `email` | Whitehead/MIT email | `jdoe@wi.mit.edu` |
| `id` | CamelCase identifier — used to match portrait images | `JohnDoe` |
| `alum` | `false` for current members, `true` for alumni | `false` |
| `now` | Current role (alumni only) — format: `Title \| Institution` | `Assistant Professor \| Harvard University` |

**Valid `pos` values** (spelling and capitalization must match exactly):

| `pos` value | Displayed as |
|-------------|--------------|
| `Principal Investigator` | Principal Investigator |
| `Lab Manager` | Lab Manager |
| `Administrative Lab Manager` | Administrative Lab Manager |
| `Administrative Assistant` | Administrative Assistant |
| `Lab Assistant` | Lab Assistant |
| `Visiting Scientist` | Visiting Scientist |
| `Post-doc` | Postdoctoral Fellow |
| `Grad student` | Graduate Student |
| `PhD Student` | PhD Student |
| `Masters Student` | Masters Student |
| `Technician` | Research Technician |
| `Software Engineer` | Software Engineer |
| `Undergrad` | Undergraduate Student |

The `id` field is how the site links a person to their portrait. It must be unique. The convention is `FirstLast` in CamelCase (e.g., `JohnDoe`, `JaneDoe`).

---

### Step 2 — Upload a portrait image

Upload the portrait to the [images folder](https://drive.google.com/drive/folders/1Je52Gv36cGsAH1q1Xsj7hfnwu5gegTLh) on Google Drive.

- **Filename must match the person's `id` exactly**, e.g. `JohnDoe.jpg`
- `.jpg` or `.png` are both fine — the script converts everything to JPEG
- Any resolution is fine — images are automatically resized to a max of 1200px on the longest side and kept under 3MB

Members without a portrait still appear on the site, but as a text-only list beneath the photo grid rather than as a photo card.

---

### Step 3 — Sync to the website

The site re-syncs from the spreadsheet and Drive folder every Monday at 6am UTC via GitHub Actions. To sync immediately:

1. Go to the [Actions tab](../../actions/workflows/update-data.yml) on GitHub
2. Click **Run workflow**

Or run locally (requires the `website` conda environment):

```bash
# Sync everything
conda run -n website python scripts/update_data.py

# Sync only people data
conda run -n website python scripts/update_data.py --people

# Sync only portrait images
conda run -n website python scripts/update_data.py --images

# Sync only publications
conda run -n website python scripts/update_data.py --publications
```

The script commits changes to `_data/people.yml`, `_data/publications.yml`, and `assets/img/people/` automatically when run via GitHub Actions.

---

## Marking someone as an alumnus

In the spreadsheet, change their `alum` column from `false` to `true` and fill in the `now` column with their current position in the format `Title | Institution`. They will move from the current members section to the alumni list on the next sync.

---

## Developer setup

### Prerequisites

- Ruby + Bundler (for Jekyll local preview)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda (for the data sync script)

### Create the conda environment

```bash
conda env create -f environment.yml
```

This creates the `website` environment with all dependencies needed to run `scripts/update_data.py`.

---

### Google Drive authentication (one-time setup)

The image sync uses the Google Drive API with OAuth. This requires a credentials file and a one-time browser login. The credentials file is not in the repo — ask a maintainer for it or follow the steps below to create your own.

#### Option A — Get credentials from a maintainer

1. Ask a current maintainer for `scripts/drive_credentials.json`
2. Place it at `scripts/drive_credentials.json` in the repo root (it is gitignored)
3. Run the script once to authenticate:
   ```bash
   conda run -n website python scripts/update_data.py --images
   ```
4. A browser window will open. Log in with a Google account that has access to the [Drive folder](https://drive.google.com/drive/folders/1Je52Gv36cGsAH1q1Xsj7hfnwu5gegTLh) and click **Allow**
5. The script will create `scripts/drive_token.json` — this caches your login for all future runs

#### Option B — Create your own credentials from scratch

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and create a new project (or select an existing one)
2. In the left sidebar, go to **APIs & Services → Library**, search for **Google Drive API**, and click **Enable**
3. Go to **APIs & Services → OAuth consent screen**
   - User type: **External**
   - Fill in the app name (e.g. `Weissman Lab Site`) and your email, then save
   - Under **Test users**, click **Add users** and add the Google account you will authenticate with
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**
   - Application type: **Desktop app**
   - Click **Create**, then **Download JSON**
5. Save the downloaded file as `scripts/drive_credentials.json`
6. Run the script to authenticate:
   ```bash
   conda run -n website python scripts/update_data.py --images
   ```
7. A browser window will open. Log in with the Google account you added as a test user and click **Allow**
8. `scripts/drive_token.json` is created — your login is now cached

Neither `scripts/drive_credentials.json` nor `scripts/drive_token.json` should ever be committed. Both are listed in `.gitignore`.

---

### Updating the GitHub Actions secret

GitHub Actions needs the Drive token to sync images in CI. After generating `scripts/drive_token.json` locally:

1. Copy the full contents of `scripts/drive_token.json`
2. Go to the repo on GitHub → **Settings → Secrets and variables → Actions**
3. Find the secret named `GOOGLE_DRIVE_TOKEN` and click **Update**
4. Paste the contents and save

The token contains a refresh token that keeps it valid indefinitely, but if it ever stops working (e.g. after revoking access in your Google account), repeat the local auth steps above and update the secret again.
