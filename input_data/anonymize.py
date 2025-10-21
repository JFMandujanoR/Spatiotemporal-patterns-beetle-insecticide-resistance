"""Anonymize specified identifier columns across all CSV files in this folder.

Behavior
...
"""

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("pandas is required. Install it with: pip install pandas")
    raise

# canonical (lowercase) target column names
TARGET_COLUMNS = ["population", "grower", "farm", "field", "bamid", "sampleid", "group"]
MAPPING_FILE = ".anon_mappings.json"
PREFIXES = {
    "population": "POP",
    "grower": "GROWER",
    "farm": "FARM",
    "field": "FIELD",
    "bamid": "BAM",
    "sampleid": "SAMPLE",
    "group": "GROUP",
}


def load_mappings(mapping_path: Path):
    if mapping_path.exists():
        with mapping_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # ensure defaultdict-like behavior
            return {k: dict(v) for k, v in data.items()}
    else:
        return {col: {} for col in TARGET_COLUMNS}


def save_mappings(mapping_path: Path, mappings):
    with mapping_path.open("w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)


def next_label(existing_map: dict, prefix: str):
    # find max numeric suffix used so far
    if not existing_map:
        return f"{prefix}_1"
    nums = []
    for v in existing_map.values():
        parts = v.rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            nums.append(int(parts[1]))
    n = max(nums) + 1 if nums else 1
    return f"{prefix}_{n}"


def anonymize_dataframe(df: pd.DataFrame, mappings: dict):
    # Treat column matching case-insensitively: map dataframe columns to canonical keys
    cols_present = {col: col.lower() for col in df.columns}
    # for each dataframe column whose lowercase is a target, apply mapping under the canonical key
    for orig_col, lc in cols_present.items():
        if lc in TARGET_COLUMNS:
            col_map = mappings.get(lc, {})
            prefix = PREFIXES.get(lc, lc.upper())

            def map_value(x):
                if pd.isna(x):
                    return x
                s = str(x)
                if s in col_map:
                    return col_map[s]
                new_label = next_label(col_map, prefix)
                col_map[s] = new_label
                mappings[lc] = col_map
                return new_label

            df[orig_col] = df[orig_col].apply(map_value)
    return df


def process_file(path: Path, mappings: dict, inplace: bool):
    try:
        df = pd.read_csv(path, dtype=str)
    except Exception as e:
        print(f"Skipping {path.name}: could not read as CSV ({e})")
        return False

    df = anonymize_dataframe(df, mappings)

    if inplace:
        out_path = path
    else:
        out_path = path.with_name(path.stem + "_anon" + path.suffix)

    df.to_csv(out_path, index=False)
    print(f"Wrote anonymized file: {out_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Anonymize identifier columns in CSV files in the current folder")
    parser.add_argument("--inplace", action="store_true", help="Overwrite original files instead of writing *_anon.csv copies")
    args = parser.parse_args()

    cwd = Path(__file__).parent
    mapping_path = cwd / MAPPING_FILE

    mappings = load_mappings(mapping_path)

    csv_files = [p for p in cwd.iterdir() if p.is_file() and p.suffix.lower() == ".csv"]
    if not csv_files:
        print("No CSV files found in input_data/")
        return

    changed = False
    for f in csv_files:
        ok = process_file(f, mappings, args.inplace)
        changed = changed or ok

    if changed:
        save_mappings(mapping_path, mappings)
        print(f"Saved mappings to {mapping_path.name}")


if __name__ == "__main__":
    main()