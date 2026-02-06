import yaml
import argparse

from core.collector import collect
from core.parser import parse
from core.normalizer import normalize
from core.deduplicator import deduplicate
from outputs.csv_output import write_csv
from outputs.gsheet_output import write_gsheet
from logs.logger import log


def process_source(source):
    log(f"Running source: {source['name']}")
    try:
        html = collect(source)
        parsed = parse(html, source["fields"], source.get("container", "div.job"))
        normalized = normalize(parsed, source["name"])
        return normalized
    except Exception as e:
        log(f"Error processing source {source['name']}: {str(e)}", level="ERROR")
        return []


def run(source_index=0, run_all=False, dry_run=False, gsheet_name=None, keywords=None):
    log("Pipeline started")

    with open("config/sources.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    if not sources:
        raise ValueError("No sources defined in sources.yaml")

    all_items = []

    if run_all:
        for source in sources:
            items = process_source(source)
            all_items.extend(items)
    else:
        try:
            source = sources[source_index]
            items = process_source(source)
            all_items.extend(items)
        except IndexError:
            raise ValueError(f"Source index {source_index} out of range")

    # Keyword Filtering
    if keywords:
        log(f"Filtering by keywords: {keywords}")
        target_keywords = [k.strip().lower() for k in keywords.split(",")]
        filtered_items = []
        for item in all_items:
            # Check filtering against title and company (if available)
            # You can extend this to description if present
            text_to_check = (str(item.get("title", "")) + " " + str(item.get("company", ""))).lower()
            if any(k in text_to_check for k in target_keywords):
                filtered_items.append(item)
        
        log(f"Filtered {len(all_items)} items down to {len(filtered_items)}")
        all_items = filtered_items

    unique = deduplicate(all_items)

    log(f"{len(unique)} records processed")

    if dry_run:
        print(f"[DRY-RUN] {len(unique)} records processed")
        log("Dry-run completed")
        return unique

    # CSV Output
    output_path = "demo/sample_output.csv"
    write_csv(unique, output_path)
    log(f"Output written to {output_path}")
    print(f"[OK] {len(unique)} records written to CSV")

    # Google Sheets Output
    if gsheet_name:
        write_gsheet(unique, gsheet_name)
    
    return unique


def main():
    parser = argparse.ArgumentParser(
        description="Config-driven scraping & automation pipeline"
    )
    parser.add_argument(
        "--source",
        type=int,
        default=0,
        help="Index of the source defined in sources.yaml",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all configured sources",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run pipeline without writing output",
    )
    parser.add_argument(
        "--gsheet",
        type=str,
        help="Name of the Google Sheet to export data to",
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Filter items by comma-separated keywords (e.g. 'python, senior')",
    )

    args = parser.parse_args()

    try:
        run(
            source_index=args.source,
            run_all=args.all,
            dry_run=args.dry_run,
            gsheet_name=args.gsheet,
            keywords=args.keywords,
        )
    except Exception as e:
        log(str(e), level="ERROR")
        raise


if __name__ == "__main__":
    main()