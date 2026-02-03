import yaml
import argparse

from core.collector import collect
from core.parser import parse
from core.normalizer import normalize
from core.deduplicator import deduplicate
from outputs.csv_output import write_csv
from logs.logger import log


def run(source_index=0, dry_run=False):
    log("Pipeline started")

    with open("config/sources.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])
    if not sources:
        raise ValueError("No sources defined in sources.yaml")

    try:
        source = sources[source_index]
    except IndexError:
        raise ValueError(f"Source index {source_index} out of range")

    log(f"Running source: {source['name']}")

    html = collect(source)
    parsed = parse(html, source["fields"])
    normalized = normalize(parsed, source["name"])
    unique = deduplicate(normalized)

    log(f"{len(unique)} records processed")

    if dry_run:
        print(f"[DRY-RUN] {len(unique)} records processed")
        log("Dry-run completed")
        return

    output_path = "demo/sample_output.csv"
    write_csv(unique, output_path)

    log(f"Output written to {output_path}")
    print(f"[OK] {len(unique)} records written")


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
        "--dry-run",
        action="store_true",
        help="Run pipeline without writing output",
    )

    args = parser.parse_args()

    try:
        run(source_index=args.source, dry_run=args.dry_run)
    except Exception as e:
        log(str(e), level="ERROR")
        raise


if __name__ == "__main__":
    main()