# Machine Learning Pipelines Assignment Rundown
## Hyperparameter Tuning with `GridSearchCV`

## 1. Assignment Objective

The goal of this assignment was to improve an existing permit wait-time prediction pipeline by testing several combinations of preprocessing and random-forest settings.

The assignment required:

- Numerical missing values imputed with either the **mean** or **median**
- A `RandomForestRegressor` using **10, 100, or 1,000 trees**
- **5-fold cross-validation**
- `scoring="neg_mean_absolute_error"`
- Top-level pipeline steps named:
  - `preprocessor`
  - `regressor`

The overall workflow was:

```text
Load CSV
   ↓
Create permit wait-time target
   ↓
Split into training and testing sets
   ↓
Preprocess numerical and categorical variables
   ↓
Test six hyperparameter combinations
   ↓
Select and refit the best model
   ↓
Evaluate it on the held-out test set
```

---

## 2. Activate the Course Environment

The course uses a dedicated Python environment called `643_venv`.

The environment is active when the terminal prompt begins with:

```text
(643_venv)
```

When it is not active, run:

```bash
source /643_venv/bin/activate
```

This ensures the correct versions of pandas and scikit-learn are available.

---

## 3. Import the Required Tools

The completed script imports:

```python
import pandas as pd

from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
```

### Purpose of Each Tool

| Tool | Purpose |
|---|---|
| `pandas` | Loads and manipulates the permit data |
| `Pipeline` | Connects preprocessing and modeling steps |
| `ColumnTransformer` | Applies different transformations to different column types |
| `SimpleImputer` | Replaces missing numerical values |
| `OneHotEncoder` | Converts categorical data into numerical indicator columns |
| `RandomForestRegressor` | Predicts permit wait time |
| `GridSearchCV` | Tests multiple hyperparameter combinations |
| `train_test_split` | Separates training and testing data |
| `mean_absolute_error` | Measures prediction error |

---

## 4. Load the Dataset

The script accepts the CSV filename as a required command-line argument:

```python
parser.add_argument("input_file", help="cleaned data file (CSV)")
```

The CSV is loaded with:

```python
input_data = pd.read_csv(
    args.input_file,
    parse_dates=["submitted_date", "issued_date"],
)
```

The `parse_dates` argument converts the two date columns from text into pandas datetime values.

This conversion is necessary because the target is calculated by subtracting the two dates.

### Correct Execution Command

```bash
python /home/labsuser/permits_train.py /home/labsuser/clean.csv
```

The command contains three parts:

```text
python + script filename + input CSV filename
```

---

## 5. Create the Target Variable

The model predicts how many days a permit takes to be issued.

The target variable is created with:

```python
y = (
    data_frame["issued_date"]
    - data_frame["submitted_date"]
).dt.days
```

In plain language:

```text
permit wait time = issued date − submitted date
```

Example:

```text
Submitted: January 1
Issued: January 8
Wait time: 7 days
```

This is a **regression problem** because the model predicts a numerical quantity rather than a category.

---

## 6. Create the Predictor Variables

After creating the target, the two date columns are removed from the predictors:

```python
x = data_frame.drop(
    [
        "issued_date",
        "submitted_date",
    ],
    axis=1,
)
```

The remaining predictors include variables such as:

- Permit type
- Permit subtype
- Permit lot size

The date columns should not remain in `x` because they were already used to calculate the answer the model is trying to predict.

Leaving `issued_date` in the predictors would create **target leakage**.

### Target Leakage

Target leakage occurs when the predictors contain information that:

- Would not realistically be available when making a prediction, or
- Directly reveals the target

Because wait time is calculated from the issue date, using the issue date to predict wait time would give the model access to the answer.

---

## 7. Split the Data

The data is split into training and testing portions:

```python
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.3,
    random_state=1,
)
```

This creates:

- **70% training data**
- **30% testing data**

The training data is used for:

- Learning model patterns
- Performing cross-validation
- Selecting hyperparameters

The test data is reserved for the final evaluation.

### Why Keep a Separate Test Set?

Cross-validation helps choose the best model, but it repeatedly evaluates models on portions of the training data.

The test set remains untouched until the end and provides a more objective estimate of future performance.

### Why Use `random_state=1`?

A train-test split includes randomness. Setting `random_state=1` makes the split reproducible.

Another person running the same code should receive the same split and approximately the same result.

---

## 8. Build the Numerical Preprocessing Pipeline

The numerical pipeline contains a `SimpleImputer`:

```python
numerical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer()),
    ]
)
```

The imputer fills missing numerical values.

The strategy is not fixed here because `GridSearchCV` will test:

```python
"mean"
"median"
```

### Mean Imputation

The missing value is replaced with the arithmetic average:

```text
mean = sum of values ÷ number of values
```

Mean imputation can be affected by unusually large or small values.

### Median Imputation

The missing value is replaced with the middle value after sorting.

Median imputation is usually more resistant to outliers.

### Why Include an Imputer When the Current Data Is Clean?

Even when the current CSV contains no missing values, including an imputer:

- Satisfies the assignment requirements
- Makes the pipeline robust to future missing data
- Keeps preprocessing consistent during training and prediction

If the current numerical column has no missing values, mean and median imputation may produce identical transformed data. In that case, the grid search can produce a tie between the two strategies.

---

## 9. Build the Categorical Preprocessing Pipeline

Random forests require numerical input, but permit type and permit subtype contain text categories.

The categorical pipeline uses one-hot encoding:

```python
categorical_pipeline = Pipeline(
    steps=[
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ]
)
```

One-hot encoding converts categories into binary columns.

For example:

```text
permit_type
Building
Maintenance
Electrical
```

may become:

```text
permit_type_Building
permit_type_Maintenance
permit_type_Electrical
```

Each column contains either:

```text
1 = category is present
0 = category is absent
```

### Why Use `handle_unknown="ignore"`?

The model could later encounter a category that was not present during training.

Without this setting, the encoder could raise an error. With it, unseen categories are safely represented using zeros in the known category columns.

---

## 10. Combine Preprocessing with `ColumnTransformer`

Different column types require different processing:

- Numerical columns → imputation
- Categorical columns → one-hot encoding

The `ColumnTransformer` applies the correct pipeline to each type:

```python
preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numerical_pipeline,
            make_column_selector(dtype_include="number"),
        ),
        (
            "cat",
            categorical_pipeline,
            make_column_selector(dtype_include="object"),
        ),
    ]
)
```

The transformer names are:

```text
num
cat
```

These names become important when specifying nested hyperparameters.

### Column Selectors

This selector identifies numerical columns:

```python
make_column_selector(dtype_include="number")
```

This selector identifies text-based categorical columns:

```python
make_column_selector(dtype_include="object")
```

The advantage is that the code does not have to manually list every predictor column.

---

## 11. Create the Complete Model Pipeline

The preprocessor and random-forest model are joined into one pipeline:

```python
return Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(random_state=1),
        ),
    ]
)
```

The top-level names are exactly:

```text
preprocessor
regressor
```

These names were explicitly required by the assignment.

The completed implementation follows this sequence:

```text
Raw predictor data
       ↓
ColumnTransformer
       ↓
Numerical imputation + categorical encoding
       ↓
RandomForestRegressor
       ↓
Predicted wait time
```

Keeping preprocessing and modeling in one pipeline ensures that every training fold and every future prediction uses the same transformations.

---

## 12. Define the Hyperparameter Grid

The tested values are defined in a dictionary:

```python
parameter_grid = {
    "preprocessor__num__imputer__strategy": [
        "mean",
        "median",
    ],
    "regressor__n_estimators": [
        10,
        100,
        1000,
    ],
}
```

There are:

```text
2 imputation strategies
×
3 random-forest sizes
=
6 hyperparameter combinations
```

The six combinations are:

| Imputation | Number of Trees |
|---|---:|
| Mean | 10 |
| Mean | 100 |
| Mean | 1,000 |
| Median | 10 |
| Median | 100 |
| Median | 1,000 |

---

## 13. Understand the Double Underscores

Scikit-learn uses double underscores to access parameters inside nested pipelines.

For example:

```python
"regressor__n_estimators"
```

means:

```text
Go to the regressor step
→ change its n_estimators parameter
```

The numerical imputer is nested more deeply:

```python
"preprocessor__num__imputer__strategy"
```

This path means:

```text
preprocessor
    ↓
num transformer
    ↓
imputer step
    ↓
strategy parameter
```

A useful way to read it is:

```text
preprocessor → num → imputer → strategy
```

Every arrow is represented by:

```text
__
```

Using single underscores creates an invalid parameter name.

The incorrect version was:

```python
"preprocessor_num_imputer_strategy"
```

The correct version is:

```python
"preprocessor__num__imputer__strategy"
```

---

## 14. Configure `GridSearchCV`

The grid search is created with:

```python
grid_search = GridSearchCV(
    estimator=pipe,
    param_grid=parameter_grid,
    cv=5,
    scoring="neg_mean_absolute_error",
)
```

### `estimator=pipe`

The object being tuned is the complete pipeline, not just the random forest.

This means preprocessing occurs separately within each cross-validation fold, helping prevent data leakage.

### `param_grid=parameter_grid`

This tells `GridSearchCV` which parameter combinations to test.

### `cv=5`

This performs five-fold cross-validation.

The training data is divided into five approximately equal folds.

For each hyperparameter combination:

1. Train on folds 1–4 and validate on fold 5
2. Train on folds 1–3 and 5, validate on fold 4
3. Continue until every fold has served as validation data once
4. Average the five validation scores

Because there are six combinations:

```text
6 combinations × 5 folds = 30 cross-validation fits
```

After identifying the winner, `GridSearchCV` refits the best pipeline on the entire training set by default.

### `scoring="neg_mean_absolute_error"`

`GridSearchCV` assumes that higher scores are better.

But with MAE:

```text
smaller error = better model
```

Scikit-learn therefore multiplies MAE by `-1` during tuning.

Example:

```text
Actual MAE: 1.8
GridSearchCV score: -1.8
```

A score of `-1.8` is better than `-2.5` because `-1.8` is numerically larger.

The negative sign is only a scoring convention. The model is not producing a negative number of error days.

---

## 15. Fit the Grid Search

The grid search is trained using only the training data:

```python
grid_search.fit(x_train, y_train)
```

This line performs the entire tuning process:

1. Tries every hyperparameter combination
2. Performs five-fold cross-validation
3. Calculates the average validation score
4. Selects the best combination
5. Refits the best pipeline on all training data

The fitted `GridSearchCV` object is returned:

```python
return grid_search
```

Although the variable is called `best_model`, it is technically a fitted `GridSearchCV` object.

Its best fitted pipeline is available through:

```python
best_model.best_estimator_
```

Its selected hyperparameters are available through:

```python
best_model.best_params_
```

---

## 16. Evaluate the Final Model

The best model predicts the held-out test data:

```python
y_pred = best_model.predict(x_test)
```

Because `GridSearchCV` refits the best pipeline automatically, calling `.predict()` uses the selected model.

The final test MAE is calculated with:

```python
best_model_mae = mean_absolute_error(
    y_test,
    y_pred,
)
```

It is then printed:

```python
print(best_model_mae)
```

The output was:

```text
1.8074920386817275
```

This means:

> On the held-out test data, the model’s predicted permit wait time was approximately **1.81 days away from the actual wait time, on average**.

MAE does not tell us whether predictions are generally too high or too low. It measures the average absolute size of the errors.

---

## 17. Final Tuning Results

Using the completed script and dataset, `GridSearchCV` selected:

```python
{
    "preprocessor__num__imputer__strategy": "mean",
    "regressor__n_estimators": 1000,
}
```

The approximate cross-validation MAE was:

```text
1.83 days
```

The final held-out test MAE was:

```text
1.81 days
```

The similar cross-validation and test errors suggest that the selected model generalized reasonably well to the held-out data.

Because the numerical data had no missing values, the choice between mean and median did not materially alter the data. The selected mean strategy may therefore have resulted from a tie or near-tie.

---

## 18. Why Use a Pipeline?

A pipeline provides several major benefits.

### Consistency

The same preprocessing steps are used during:

- Cross-validation
- Final training
- Testing
- Future predictions

### Leakage Prevention

The imputer and encoder are fitted only on the training portion of each cross-validation fold.

Without a pipeline, someone might preprocess the entire dataset before cross-validation, allowing information from validation observations to influence preprocessing.

### Simpler Deployment

The fitted pipeline accepts raw predictor data and automatically performs all required transformations before predicting.

### Hyperparameter Tuning

`GridSearchCV` can tune parameters from multiple pipeline components at the same time.

In this assignment, it tuned:

- A preprocessing choice
- A model choice

---

## 19. Why Use a Random Forest?

A random forest combines predictions from many decision trees.

Each tree is trained using a randomized version of the data and predictors. The final regression prediction is based on the average prediction across the trees.

### Advantages

Random forests:

- Capture nonlinear relationships
- Model interactions between variables
- Require little feature scaling
- Are usually more stable than one decision tree
- Work with mixed features after categorical encoding

### Meaning of `n_estimators`

`n_estimators` is the number of trees in the forest.

```text
10 trees:
Fast, but potentially less stable

100 trees:
More stable, moderate computation

1,000 trees:
Potentially more stable, but much slower
```

More trees usually reduce variance, but they also increase computation time. Improvement eventually levels off.

---

## 20. Common Errors from This Assignment

### Error 1: Missing CSV Argument

Incorrect:

```bash
python /home/labsuser/permits_train.py
```

Result:

```text
the following arguments are required: input_file
```

Correct:

```bash
python /home/labsuser/permits_train.py /home/labsuser/clean.csv
```

---

### Error 2: Running Python Code as a Shell Script

Incorrect:

```bash
/home/labsuser/permits_train.py
```

This caused errors such as:

```text
from: command not found
syntax error near unexpected token
```

The Bash shell was trying to interpret Python code.

Correct:

```bash
python /home/labsuser/permits_train.py /home/labsuser/clean.csv
```

---

### Error 3: Incorrect Parameter Path

Incorrect:

```python
"preprocessor_num_imputer_strategy"
```

Correct:

```python
"preprocessor__num__imputer__strategy"
```

Nested pipeline parameter names require double underscores.

---

### Error 4: Trailing Whitespace

Pylint initially found invisible spaces at the ends of two lines.

They were removed with:

```bash
sed -i 's/[[:space:]]\+$//' /home/labsuser/permits_train.py
```

After correcting the formatting, the assignment received:

```text
20/20
```

---

## 21. Oral-Exam Explanation

A polished one-minute explanation:

> In this assignment, I built a scikit-learn pipeline to predict permit wait time in days. I first created the target by subtracting the submitted date from the issued date, and then removed both date columns from the predictors to avoid leakage. I split the data into 70% training and 30% testing data. Inside the pipeline, a ColumnTransformer handled numerical and categorical columns separately. Numerical values were passed through a SimpleImputer, while categorical values were converted with one-hot encoding. The transformed data was then passed to a RandomForestRegressor. I used GridSearchCV to compare mean versus median imputation and random forests with 10, 100, or 1,000 trees. With six combinations and five-fold cross-validation, the search performed 30 validation fits. It selected the best configuration using negative mean absolute error and then refit that configuration on the full training set. Finally, I evaluated it on the untouched test set, where the MAE was about 1.81 days.

---

## 22. Likely Oral-Exam Questions

### What Is a Hyperparameter?

A hyperparameter is a model setting chosen before training.

Examples from this assignment:

```text
Imputation strategy
Number of trees
```

A learned model parameter, by contrast, is estimated during training.

---

### Why Did You Need Both a Train-Test Split and Cross-Validation?

Cross-validation was used within the training data to select hyperparameters.

The separate test set was used only once at the end to estimate how the selected model performs on unseen data.

---

### Why Was Preprocessing Placed Inside the Pipeline?

It ensures that preprocessing is learned only from the relevant training fold during cross-validation, which reduces leakage and keeps training and prediction behavior consistent.

---

### Why Use `ColumnTransformer`?

The dataset contains different data types. Numerical columns require imputation, while categorical columns require encoding. `ColumnTransformer` applies the correct transformation to each type.

---

### Why Is the Scoring Value Negative?

Scikit-learn’s tuning tools maximize scores. Since lower MAE is better, scikit-learn negates MAE so that the numerically largest score represents the smallest error.

---

### Why Use MAE?

MAE is easy to interpret because it is expressed in the same units as the target.

Here, an MAE of approximately 1.81 means the predictions were off by roughly 1.81 days on average.

---

### What Does Five-Fold Cross-Validation Do?

It divides the training data into five sections, trains on four, validates on one, and repeats until every section has served as validation data.

---

### What Does `random_state=1` Do?

It makes randomized procedures reproducible, including the train-test split and the random forest.

---

### Why Did 1,000 Trees Take Longer?

Each tree must be independently trained. A model with 1,000 trees requires substantially more computation than one with 10 or 100 trees.

---

### What Did `GridSearchCV` Return?

It returned a fitted `GridSearchCV` object containing:

- The best parameter combination
- The best fitted pipeline
- Cross-validation results
- A `.predict()` method that uses the best refitted model

---

## 23. Key Concepts to Remember

```text
Pipeline
Connects preprocessing and modeling steps.

ColumnTransformer
Applies different preprocessing to different column types.

OneHotEncoder
Converts categorical values into numerical indicators.

SimpleImputer
Replaces missing values.

Hyperparameter
A setting selected before model training.

GridSearchCV
Tests every requested hyperparameter combination.

Cross-validation
Evaluates models across multiple training-validation splits.

MAE
Average absolute distance between predictions and actual values.

Target leakage
Predictor data improperly contains information about the answer.
```

---

## 24. Final Takeaway

This assignment demonstrated how to combine:

- Data preparation
- Mixed-type preprocessing
- Model training
- Hyperparameter tuning
- Cross-validation
- Final test evaluation

into one reproducible scikit-learn workflow.

The completed solution passed the grader with a score of **20/20**.
