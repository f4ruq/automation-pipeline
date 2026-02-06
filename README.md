# Automation Pipeline

A configurable data scraping and automation pipeline designed to collect, parse, normalize, and export data.

## Features

- **Configurable Sources**: Define sources in `config/sources.yaml`.
- **Multiple Inputs**: Supports local HTML files, remote URLs, and JSON feeds (e.g., RemoteOK).
- **Flexible Parsing**: Uses CSS selectors for HTML and key-value mapping for JSON.
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
python runner.py

# Run a specific source by index
python runner.py --source 1

# Export to Google Sheets
python runner.py --source 1 --gsheet "Target Sheet Name"
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

### Google Sheets Setup

1.  Place your `credentials.json` in `credentials/` directory.
2.  Enable Google Sheets and Drive APIs.
3.  Share the sheet with the service account email.
