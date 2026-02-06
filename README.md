# Automation Pipeline

A configurable data scraping and automation pipeline designed to collect, parse, normalize, and export data.

## Features

- **Configurable Sources**: Define sources in `config/sources.yaml`.
- **Multiple Inputs**: Supports local HTML files, remote URLs, and JSON feeds (e.g., RemoteOK).
- **Multi-Source Scraping**: Scrape all configured sources simultaneously with `--all`.
- **Flexible Parsing**: Uses CSS selectors for HTML, key-value mapping for JSON, and RSS feed support.
- **Custom Headers**: Configure User-Agent and other headers directly in YAML.
- **Deduplication**: Automatically removes duplicate entries based on content hash.
- **Multiple Outputs**: Export data to CSV or directly to Google Sheets.

<img width="1060" height="604" alt="Ekran Resmi 2026-02-06 00 12 29" src="https://github.com/user-attachments/assets/72ed7045-11f6-4f37-a8c3-49c3b7abe148" />


## Installation

1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the pipeline using `runner.py`:

```bash
# Run the default source (index 0)
# Note: Indices correspond to the order in config/sources.yaml (starting at 0)
python runner.py

# Run all sources simultaneously
python runner.py --all

# Run a specific source by index
python runner.py --source 1

# Export to Google Sheets
python runner.py --all --gsheet "Target Sheet Name"
```

## Configuration

### Sources (`config/sources.yaml`)

Define your scraping targets here. Supported types: `local_html`, `remote_html`, `remote_json`.

#### Example: HTML Scraping (Hacker News)
```yaml
- name: hacker_news_jobs
  type: remote_html
  url: https://news.ycombinator.com/jobs
  container: "tr.athing"
  fields:
    title: ".titleline > a"
    url: ".titleline > a::attr(href)"
```

#### Example: RSS Feed (WeWorkRemotely)
```yaml
- name: weworkremotely
  type: remote_html
  url: https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss
  container: "item"
  fields:
    title: "title"
    url: "link"
    company: "title"
```

#### Example: JSON Feed (RemoteOK)
```yaml
- name: remoteok
  type: remote_json
  url: https://remoteok.com/remote-jobs.json
  headers:
    User-Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
  container: "none"
  fields:
    title: "position"
    url: "url"
    company: "company"
```

#### Example: JSON Dict (Remotive)
```yaml
- name: remotive
  type: remote_json
  url: https://remotive.com/api/remote-jobs
  container: "jobs"
  fields:
    title: "title"
    url: "url"
    company: "company_name"
```

### Google Sheets Setup

1.  Place your `credentials.json` in `credentials/` directory.
2.  Enable Google Sheets and Drive APIs.
3.  Share the sheet with the service account email.
