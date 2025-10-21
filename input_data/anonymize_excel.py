"""Anonymize Table_Genomic_Samplesv2.xlsx using existing mappings.

This script expects pandas and openpyxl to be available in the Python environment
you run it in (for example your `jfmr` environment). It loads
`.anon_mappings.json` from the same directory (if present), applies the mappings
to the target columns, creating new labels for unseen identifiers, and writes
an anonymized Excel file with suffix `_anon.xlsx`.

Usage (run in your jfmr env):
    python input_data/anonymize_excel.py

It will read `Table_Genomic_Samplesv2.xlsx` and write `Table_Genomic_Samplesv2_anon.xlsx`.
"""

from pathlib import Path
import json
import sys

try:
    import pandas as pd
except ImportError:
    print("pandas is required. Run this script in an environment with pandas installed (e.g. jfmr).")
    sys.exit(2)

TARGET_COLUMNS = ["population", "grower", "farm", "field", "bamid", "sampleid", "group"]
PREFIXES = {
    "population": "POP",
    "grower": "GROWER",
    "farm": "FARM",
    "field": "FIELD",
    "bamid": "BAM",
    "sampleid": "SAMPLE",
    "group": "GROUP",
}
MAPPING_FILE = Path(__file__).parent / ".anon_mappings.json"
INPUT_XLSX = Path(__file__).parent / "Table_Genomic_Samplesv2.xlsx"
OUTPUT_XLSX = Path(__file__).parent / "Table_Genomic_Samplesv2_anon.xlsx"


def load_mappings():
    if MAPPING_FILE.exists():
        with MAPPING_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # ensure keys for target columns
            for col in TARGET_COLUMNS:
                data.setdefault(col, {})
            return data
    else:
        return {col: {} for col in TARGET_COLUMNS}


def save_mappings(mappings):
    with MAPPING_FILE.open("w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)


def next_label(existing_map, prefix):
    if not existing_map:
        return f"{prefix}_1"
    nums = []
    for v in existing_map.values():
        parts = str(v).rsplit("_", 1)
        if len(parts) == 2 and parts[1].isdigit():
            nums.append(int(parts[1]))
    n = max(nums) + 1 if nums else 1
    return f"{prefix}_{n}"


def anonymize(df, mappings):
    # handle column names case-insensitively
    cols_present = {col: col.lower() for col in df.columns}
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


def main():
    if not INPUT_XLSX.exists():
        print(f"Input file not found: {INPUT_XLSX}")
        sys.exit(1)

    mappings = load_mappings()

    # read Excel (first sheet)
    try:
        df = pd.read_excel(INPUT_XLSX, dtype=str)
    except Exception as e:
        print(f"Failed to read {INPUT_XLSX}: {e}")
        sys.exit(1)

    df2 = anonymize(df, mappings)

    try:
        df2.to_excel(OUTPUT_XLSX, index=False)
    except Exception as e:
        print(f"Failed to write {OUTPUT_XLSX}: {e}")
        sys.exit(1)

    save_mappings(mappings)
    print(f"Wrote anonymized Excel: {OUTPUT_XLSX.name}")


if __name__ == "__main__":
    main()
