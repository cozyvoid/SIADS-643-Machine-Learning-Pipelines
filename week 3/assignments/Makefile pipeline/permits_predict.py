import pickle

import pandas as pd

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("permit_type")
    parser.add_argument("permit_subtype")
    parser.add_argument("permit_lot_size")

    parser.add_argument(
        "-m",
        "--model",
        type=argparse.FileType("rb"),
        default="model.pkl",
        help="trained model file (PKL)",
    )

    args = parser.parse_args()

    model = pickle.load(args.model)

    prediction = model.predict(
        pd.DataFrame(
            [
                {
                    "permit_type": args.permit_type,
                    "permit_subtype": args.permit_subtype,
                    "permit_lot_size": args.permit_lot_size,
                }
            ]
        )
    ).round(1)[0]

    print(f"Prediction of time until permit is issued --> {prediction} days")
