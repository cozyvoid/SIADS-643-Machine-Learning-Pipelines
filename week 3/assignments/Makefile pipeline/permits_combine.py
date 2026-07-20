import os

import pandas as pd


def combine(_files_to_combine):
    return pd.concat([pd.read_json(input_file) for input_file in input_files], ignore_index=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="directory of data files (JSON)")
    parser.add_argument("output_file", help="combined data file (CSV)")
    args = parser.parse_args()

    input_files = [os.path.join(args.input_dir, f) for f in sorted(os.listdir(args.input_dir))]

    combined = combine(input_files)
    combined.to_csv(args.output_file, index=False)
