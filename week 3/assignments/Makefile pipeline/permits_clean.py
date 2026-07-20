import pandas as pd


def clean(input_file):
    df = pd.read_csv(
        input_file,
        parse_dates=["submitted_date", "issued_date"],
    )

    df["submitted_date"] = pd.to_datetime(df["submitted_date"], unit="s")
    df["issued_date"] = pd.to_datetime(df["issued_date"], unit="s")

    df = df.drop(
        [
            "permit_street_address",
            "contractor",
            "contractor_address",
            "inspector",
        ],
        axis=1,
    )

    df["permit_lot_size"] = df["permit_lot_size"].apply(lambda x: float(x[:-6]))

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="combined data file (CSV)")
    parser.add_argument("output_file", help="cleaned data file (CSV)")
    args = parser.parse_args()

    clean = clean(args.input_file)
    clean.to_csv(args.output_file, index=False)
