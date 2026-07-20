import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def make_pipeline():
    # replace this and the line below with your pipeline
    # from the previous assignment
    numerical_pipeline = Pipeline(
        steps = [
            ("imputer", SimpleImputer())
        ]
    )

    # categorical columns must be converted to numeric indicator columns
    # handle_unknown="ignore" prevents prediction errors for new categories
    categorical_pipeline = Pipeline(
        steps = [
            ("encoder", OneHotEncoder(handle_unknown = "ignore"))
        ]
    )

    # apply each preprocessing pipeline to the appropriate column type
    preprocessor = ColumnTransformer(
        transformers = [
            (
                "num",
                numerical_pipeline,
                make_column_selector(dtype_include = "number"),
            ),
            (
                "cat",
                categorical_pipeline,
                make_column_selector(dtype_include = "object")
            )
        ]
    )

    # the required top-level step names are "preprocessor" and "regressor"
    return Pipeline(
        steps = [
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(random_state = 1))
        ]
    )


def tune_hyperparameters(pipe, x_train, y_train):
    """
    Tune the hyperparameters of your pipeline using GridSearchCV.

    :param pipe: sklearn pipeline
    :param x_train: training data
    :param y_train: training target
    :return: fitted GridSearchCV object
    """

    parameter_grid = {
        "preprocessor__num__imputer__strategy": ["mean", "median"],
        "regressor__n_estimators": [10, 100, 1000],
    }

    grid_search = GridSearchCV(
        estimator=pipe,
        param_grid=parameter_grid,
        cv=5,
        scoring="neg_mean_absolute_error",
    )

    grid_search.fit(x_train, y_train)

    return grid_search

def train(data_frame):
    # We are predicting the wait time
    y = (data_frame["issued_date"] - data_frame["submitted_date"]).dt.days

    # Drop columns in dataframe that shouldn't be used to predict wait time
    x = data_frame.drop(
        [
            "issued_date",
            "submitted_date",
        ],
        axis=1,
    )

    # Split data into train and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

    # Make the pipeline
    pipe = make_pipeline()

    # Hyperparameter tune the pipeline on your training set and get the best model
    best_model = tune_hyperparameters(pipe, x_train, y_train)

    # Get score on the test set
    y_pred = best_model.predict(x_test)
    best_model_mae = mean_absolute_error(y_test, y_pred)
    print(best_model_mae)
    return best_model


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="cleaned data file (CSV)")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display metrics",
    )
    args = parser.parse_args()

    input_data = pd.read_csv(
        args.input_file,
        parse_dates=["submitted_date", "issued_date"],
    )

    best_result = train(input_data)
