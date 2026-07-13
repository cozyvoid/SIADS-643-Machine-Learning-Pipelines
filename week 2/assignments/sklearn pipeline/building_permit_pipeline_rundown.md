# Building-Permit Wait-Time Pipeline: Step-by-Step Rundown

## 1. Assignment objective

The goal was to build a machine-learning pipeline that predicts how many days a building permit will take to be issued. The assignment required two main pipeline stages:

1. A preprocessing stage named `preprocessor`
2. A modeling stage containing a random-forest model

Numeric and categorical variables had to be handled separately.

A strong oral-exam summary would be:

> “I created a scikit-learn pipeline that automatically preprocesses numeric and categorical permit features, then trains a random-forest regressor to predict permit wait time in days.”

---

## 2. Import the required libraries

```python
import argparse

import pandas as pd
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
```

Each import has a specific role:

- `argparse` reads the CSV filename from the command line.
- `pandas` loads and manipulates the data.
- `Pipeline` connects preprocessing and modeling steps.
- `ColumnTransformer` applies different transformations to different column types.
- `make_column_selector` automatically identifies numeric and categorical columns.
- `SimpleImputer` fills in missing values.
- `StandardScaler` standardizes numeric variables.
- `OneHotEncoder` converts categories into numeric indicator columns.
- `RandomForestRegressor` predicts a continuous value: wait time in days.
- `train_test_split` creates separate training and testing datasets.
- `mean_absolute_error` measures the average prediction error in days.

---

## 3. Build the numeric preprocessing pipeline

```python
num = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ]
)
```

This pipeline performs two operations.

### Median imputation

```python
SimpleImputer(strategy="median")
```

Missing numeric values are replaced with the median of their column.

The median is useful because it is less sensitive to extreme values than the mean. For example, a few unusually large permit values will not distort the median as much as they would distort the mean.

### Standard scaling

```python
StandardScaler()
```

Scaling transforms each numeric feature so that it has approximately:

- Mean equal to 0
- Standard deviation equal to 1

A random forest generally does not require scaling because it makes decisions using thresholds rather than distances. However, scaling was part of the assignment requirements and makes the preprocessing pipeline more reusable with other model types.

**Oral-exam point:**

> “Scaling is not essential for a random forest, but including it satisfies the assignment and creates a standardized preprocessing workflow.”

---

## 4. Build the categorical preprocessing pipeline

```python
cat = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="constant",
                fill_value="missing",
            ),
        ),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ]
)
```

### Categorical imputation

```python
SimpleImputer(
    strategy="constant",
    fill_value="missing",
)
```

Missing categorical values are replaced with the text `"missing"`.

This preserves the row instead of deleting it and treats missingness as its own category.

For example:

```text
permit_type = NaN
```

becomes:

```text
permit_type = "missing"
```

### One-hot encoding

```python
OneHotEncoder(handle_unknown="ignore")
```

Machine-learning models require numeric input, so one-hot encoding converts each category into its own binary column.

For example:

```text
permit_type
Residential
Commercial
```

might become:

```text
permit_type_Residential
permit_type_Commercial
```

### Why `handle_unknown="ignore"` matters

The test data may contain a category that was not present in the training data. Without this option, the pipeline could raise an error.

With unknown values ignored, the model can still make a prediction.

**Oral-exam point:**

> “Unknown categories are ignored so the model remains stable when new categorical values appear during testing or production use.”

---

## 5. Combine the numeric and categorical transformations

```python
preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            num,
            make_column_selector(dtype_include="number"),
        ),
        (
            "cat",
            cat,
            make_column_selector(
                dtype_include=["object", "category"]
            ),
        ),
    ]
)
```

`ColumnTransformer` allows different preprocessing procedures to be applied to different groups of columns.

The transformer has two named branches:

- `num` for numeric columns
- `cat` for categorical columns

The selectors identify columns based on their pandas data types.

```python
make_column_selector(dtype_include="number")
```

selects numeric columns.

```python
make_column_selector(dtype_include=["object", "category"])
```

selects text and categorical columns.

This is more flexible than manually listing column names. If the dataset gains another numeric or categorical feature, the pipeline can usually process it automatically.

**Oral-exam point:**

> “The `ColumnTransformer` runs the numeric and categorical preprocessing branches in parallel and combines their outputs into one feature matrix.”

---

## 6. Add the random-forest model

```python
return Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "modeling",
            RandomForestRegressor(
                n_estimators=100,
                random_state=1,
                n_jobs=-1,
            ),
        ),
    ]
)
```

The final pipeline has exactly two top-level steps:

1. `preprocessor`
2. `modeling`

This directly matches the assignment requirements.

### Random forest settings

```python
n_estimators=100
```

The model builds 100 decision trees.

Each tree produces a prediction, and the forest averages those predictions.

```python
random_state=1
```

This makes the results reproducible. Running the code again with the same data and settings should produce the same split and model behavior.

```python
n_jobs=-1
```

This tells scikit-learn to use all available CPU cores when training the forest.

### Why use a random forest?

A random forest is appropriate because:

- The target is numeric.
- It can model nonlinear relationships.
- It can capture interactions between features.
- It is relatively resistant to overfitting compared with a single decision tree.
- It works with many transformed input features.

---

## 7. Create the prediction target

```python
y = (
    data_frame["issued_date"]
    - data_frame["submitted_date"]
).dt.days
```

The model predicts permit wait time.

The target is calculated as:

```text
wait time = issued date − submitted date
```

The `.dt.days` component converts the time difference into an integer number of days.

Example:

```text
Submitted: January 1
Issued: January 11
Wait time: 10 days
```

This is a regression problem because the target is a continuous numeric quantity rather than a class label.

**Oral-exam point:**

> “The target variable was not stored directly in the dataset, so I engineered it by subtracting the submission date from the issue date.”

---

## 8. Remove the date columns from the predictors

```python
x = data_frame.drop(
    [
        "issued_date",
        "submitted_date",
    ],
    axis=1,
)
```

The original dates are removed from the feature matrix after the target is calculated.

This is important because the issued date directly determines the target. Including it would create target leakage.

Target leakage occurs when the model receives information that would not realistically be available when making a prediction.

In practice, the issued date is not known when a permit is first submitted. Therefore, it cannot be used to predict how long approval will take.

**Oral-exam point:**

> “I removed both date columns after constructing the target, especially the issued date, because using it would leak the answer into the model.”

---

## 9. Split the data into training and testing sets

```python
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.3,
    random_state=1,
)
```

The data is divided into:

- 70% training data
- 30% testing data

The training set is used to fit the preprocessing steps and the model.

The test set represents unseen data and is used to estimate how well the model generalizes.

Using `random_state=1` makes the split reproducible.

A key benefit of the pipeline is that preprocessing is learned only from the training data when this line runs:

```python
trained_model.fit(x_train, y_train)
```

For example, numeric medians and scaling parameters are calculated from `x_train`, not from the entire dataset. This helps prevent data leakage.

---

## 10. Train the complete pipeline

```python
trained_model = make_pipeline()
trained_model.fit(x_train, y_train)
```

The call to `.fit()` performs all of the following automatically:

1. Identifies numeric and categorical columns.
2. Calculates numeric medians.
3. Fills missing numeric values.
4. Learns scaling parameters.
5. Fills missing categorical values.
6. Learns one-hot-encoding categories.
7. Transforms the training data.
8. Fits the random-forest model.

This is one of the main advantages of using a pipeline: the entire workflow is treated as one model object.

When predictions are made, the same transformations are applied automatically:

```python
trained_model.predict(x_test)
```

---

## 11. Evaluate model performance

```python
model_metrics = {
    "train_data": {
        "score": trained_model.score(x_train, y_train),
        "mae": mean_absolute_error(
            y_train,
            trained_model.predict(x_train),
        ),
    },
    "test_data": {
        "score": trained_model.score(x_test, y_test),
        "mae": mean_absolute_error(
            y_test,
            trained_model.predict(x_test),
        ),
    },
}
```

Two metrics are calculated.

### R² score

For a regressor, `.score()` returns the coefficient of determination, or R².

R² measures how much of the variation in wait times is explained by the model.

General interpretation:

- `1.0`: perfect predictions
- `0.0`: no better than predicting the average
- Below `0.0`: worse than predicting the average

The observed results were approximately:

```text
Training R²: 0.959
Testing R²: 0.846
```

The model explains about 84.6% of the variation in the test data.

### Mean absolute error

MAE measures the average absolute difference between the predicted and actual wait times.

Observed results:

```text
Training MAE: 0.998 days
Testing MAE: 1.838 days
```

The test MAE means that predictions differ from actual wait times by about 1.84 days on average.

MAE is especially useful here because it is expressed in the same unit as the target: days.

---

## 12. Interpret the difference between training and test results

The training performance is better than the testing performance:

```text
Training R²: 0.959
Testing R²: 0.846
```

```text
Training MAE: 0.998 days
Testing MAE: 1.838 days
```

This is expected because the model was fitted on the training data.

The gap suggests some overfitting, but the test results remain strong. A random forest often performs extremely well on its training data because individual trees can model detailed patterns.

A good oral-exam interpretation is:

> “The model performs better on the training data than on the test data, which indicates some overfitting. However, the test R² remains high and the average error is under two days, so the model still generalizes reasonably well.”

---

## 13. Load the CSV from the command line

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file",
        help="cleaned data file (CSV)",
    )
```

The script expects the CSV file path as a positional command-line argument.

It is run with:

```bash
python permits_train.py clean.csv
```

The file is loaded with:

```python
input_data = pd.read_csv(
    args.input_file,
    parse_dates=["submitted_date", "issued_date"],
)
```

The `parse_dates` argument ensures that pandas treats the two date columns as datetime values. Without that conversion, subtracting the dates may fail or behave incorrectly.

The training function is then called:

```python
model = train(input_data)
```

---

## 14. Why a pipeline is important

Using a pipeline provides several benefits.

### Consistency

The same transformations are used during both training and prediction.

### Reduced leakage risk

Preprocessing parameters are learned from the training data during `.fit()`.

### Simpler code

The user only needs to call:

```python
model.fit(x_train, y_train)
model.predict(x_test)
```

### Easier deployment

The preprocessing steps and model can be saved together as one object.

### Easier cross-validation

The entire pipeline can be passed into tools such as `cross_val_score` or `GridSearchCV`.

---

# Likely oral-exam questions

## Why is this a regression problem?

Because the target is a numeric number of days, not a category.

## Why use median imputation for numeric data?

The median is robust to outliers and provides a valid numeric replacement for missing values.

## Why use `"missing"` for categorical data?

It keeps incomplete rows and allows missingness to be represented as its own category.

## Why is one-hot encoding necessary?

Most scikit-learn models require numeric input and cannot directly process text labels.

## Why use `handle_unknown="ignore"`?

It prevents errors when unseen categories appear in test or production data.

## Why use a `ColumnTransformer`?

Numeric and categorical variables require different preprocessing operations.

## Why remove the date columns?

The issued date determines the target and would cause target leakage. The target is created from the dates before they are removed.

## Why use a random forest?

It handles nonlinear relationships, feature interactions, and mixed transformed inputs effectively.

## Does a random forest require feature scaling?

No. Tree-based models are generally insensitive to feature scale. Scaling was included because the assignment required it and because it makes the preprocessing pipeline reusable.

## What does MAE tell us?

It gives the model’s average prediction error in days.

## What does R² tell us?

It measures the proportion of variation in permit wait time explained by the model.

## Why calculate both training and testing metrics?

Comparing them helps identify overfitting and shows how well the model generalizes to unseen data.

## What does `random_state=1` do?

It makes the train/test split and random-forest behavior reproducible.

## What does `n_jobs=-1` do?

It uses all available processor cores to train the random forest faster.

---

# Limitations and possible improvements

The completed assignment meets all requirements and received full credit, but several improvements could be considered in a production project.

### Cross-validation

A single train/test split depends on one random division of the data. Cross-validation would provide a more stable estimate of model performance.

### Hyperparameter tuning

Parameters such as tree depth, minimum samples per leaf, and number of trees could be optimized using `GridSearchCV` or `RandomizedSearchCV`.

### Temporal validation

Because permit data involves dates, a time-based split may be more realistic than a random split. A production model should ideally be trained on earlier permits and tested on later permits.

### Feature engineering

Potential features could include:

- Submission month
- Day of the week
- Permit workload at submission time
- Seasonal indicators
- Historical average wait time by permit type
- Location-based features

These features must be created only from information available at prediction time.

### Missing target values

Rows with a missing submitted date or issued date would produce a missing target. A production version should detect and remove or investigate those rows before training.

### Model persistence

The fitted pipeline could be saved with `joblib` so it can be reused without retraining.

---

# One-minute oral-exam explanation

> “The purpose of the assignment was to predict building-permit wait time in days. I first created the target by subtracting the submitted date from the issued date. I then removed those date columns from the predictors to avoid leakage, especially because the issued date would reveal the answer. I split the data into training and test sets using a 70/30 split.
>
> For preprocessing, I created separate numeric and categorical pipelines. Numeric missing values are replaced with the median and then standardized. Categorical missing values are replaced with the string ‘missing,’ and the variables are one-hot encoded. Unknown categories are ignored so new values do not cause prediction errors.
>
> A `ColumnTransformer` applies the correct preprocessing based on each column’s data type. That preprocessor is combined with a `RandomForestRegressor` in a two-stage pipeline. The pipeline ensures that preprocessing is learned from the training data and applied consistently to future data.
>
> The model achieved a test R² of approximately 0.846 and a test MAE of approximately 1.84 days. That means it explained about 84.6% of the variation in test wait times and was wrong by about 1.84 days on average.”
