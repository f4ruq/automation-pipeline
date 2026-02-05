# Automation Pipeline

A configurable data scraping and automation pipeline designed to collect, parse, normalize, and export data.

## Features

- **Configurable Sources**: Define sources in `config/sources.yaml`.
- **Multiple Inputs**: Supports local HTML files and remote URLs (e.g., Hacker News Jobs).
- **Flexible Parsing**: Uses CSS selectors to extract data.
- **Deduplication**: Automatically removes duplicate entries based on content hash.
- **Multiple Outputs**: Export data to CSV or directly to Google Sheets.

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
    *(Note: You may need to generate requirements.txt first: `pip freeze > requirements.txt`)*

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

Define your scraping targets here.

```yaml
- name: hacker_news_jobs
  type: remote_html
  url: https://news.ycombinator.com/jobs
  container: "tr.athing"
  fields:
    title: ".titleline > a"
    url: ".titleline > a::attr(href)"
```

### Google Sheets Setup

1.  Place your `credentials.json` in `credentials/` directory.
2.  Enable Google Sheets and Drive APIs.
3.  Share the sheet with the service account email.
