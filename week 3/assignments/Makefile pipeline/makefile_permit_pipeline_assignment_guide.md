# Machine Learning Pipelines Assignment Guide
## Building a Reproducible Permit-Model Workflow with `make`

## 1. Assignment Objective

The goal was to write a `Makefile` that connects three existing Python scripts into one reproducible workflow.

The final command must be:

```bash
make artifacts/model.pkl
```

That command must create all three required artifacts:

```text
artifacts/combined.csv
artifacts/clean.csv
artifacts/model.pkl
```

The fourth script, `permits_predict.py`, is not part of the build pipeline because it consumes an already-trained model rather than producing one.

---

## 2. Overall Pipeline

```text
JSON files in input_data/
          |
          v
permits_combine.py
          |
          v
artifacts/combined.csv
          |
          v
permits_clean.py
          |
          v
artifacts/clean.csv
          |
          v
permits_train.py
          |
          v
artifacts/model.pkl
```

Each file is the output of one stage and the input to the next stage. This ordering determines the dependency graph in the `Makefile`.

---

## 3. Repository Structure

The relevant files are organized approximately as follows:

```text
/home/labsuser/
├── input_data/
│   └── one or more JSON files
├── artifacts/
├── HELP.md
├── Makefile
├── permits_clean.py
├── permits_combine.py
├── permits_predict.py
├── permits_train.py
└── README.md
```

The important directory name is `input_data`, not `data`.

---

## 4. Step 1 — Activate the Course Environment

The course uses the `643_venv` Python environment. Confirm that the terminal prompt begins with:

```text
(643_venv)
```

When it does not, activate it with:

```bash
source /643_venv/bin/activate
```

This ensures that Python can find the required packages, including pandas and scikit-learn.

---

## 5. Step 2 — Inspect Each Script

Before writing the `Makefile`, inspect the scripts and their command-line interfaces:

```bash
python permits_combine.py -h
python permits_clean.py -h
python permits_train.py -h
python permits_predict.py -h
```

The help output reveals each script's required arguments and therefore its inputs and outputs.

### 5.1 `permits_combine.py`

Expected command pattern:

```bash
python permits_combine.py INPUT_DIRECTORY OUTPUT_FILE
```

For this assignment:

```bash
python permits_combine.py input_data artifacts/combined.csv
```

What it does:

1. Lists files in the input directory.
2. Sorts the filenames for a consistent order.
3. Reads each file as JSON with pandas.
4. Concatenates all records into one DataFrame.
5. Writes the result as a CSV file.

Its output is:

```text
artifacts/combined.csv
```

That output becomes the input to the cleaning stage.

### 5.2 `permits_clean.py`

Expected command pattern:

```bash
python permits_clean.py INPUT_FILE OUTPUT_FILE
```

For this assignment:

```bash
python permits_clean.py artifacts/combined.csv artifacts/clean.csv
```

What it does:

1. Reads the combined CSV.
2. Processes `submitted_date` and `issued_date` as dates.
3. Drops columns that are not needed by the model:
   - `permit_street_address`
   - `contractor`
   - `contractor_address`
   - `inspector`
4. Converts `permit_lot_size` from a text value into a floating-point number.
5. Writes the cleaned data to a new CSV.

Its output is:

```text
artifacts/clean.csv
```

That output becomes the input to model training.

### 5.3 `permits_train.py`

Expected command pattern:

```bash
python permits_train.py INPUT_FILE OUTPUT_FILE
```

For this assignment:

```bash
python permits_train.py artifacts/clean.csv artifacts/model.pkl
```

What it does:

1. Creates the target variable:

   ```text
   permit wait time = issued date - submitted date
   ```

2. Removes the date columns from the predictors.
3. Defines numerical preprocessing for `permit_lot_size`:
   - median imputation
   - standardization
4. Defines categorical preprocessing for:
   - `permit_type`
   - `permit_subtype`
5. Replaces missing categorical values with `"missing"`.
6. One-hot encodes categorical values.
7. Fits a `LinearRegression` model.
8. Uses a 70% training and 30% testing split with `random_state=1`.
9. Computes training and testing score and mean absolute error.
10. Serializes the fitted pipeline into a pickle file.

Its output is:

```text
artifacts/model.pkl
```

The pickle contains both preprocessing and the trained regression model, so the same transformations can be applied to future prediction data.

### 5.4 Why `permits_predict.py` Is Excluded

`permits_predict.py` loads an existing model and uses it to make a prediction. It does not create any of the three required build artifacts.

This distinction is useful:

```text
Build pipeline: creates the trained model
Prediction script: consumes the trained model
```

---

## 6. Step 3 — Write the Makefile

The completed `Makefile` is:

```makefile
PYTHON := python
INPUT_DIR := input_data
ARTIFACT_DIR := artifacts
INPUT_FILES := $(wildcard $(INPUT_DIR)/*.json)

.PHONY: all clean

all: $(ARTIFACT_DIR)/model.pkl

$(ARTIFACT_DIR):
	mkdir -p $(ARTIFACT_DIR)

$(ARTIFACT_DIR)/combined.csv: permits_combine.py $(INPUT_FILES) | $(ARTIFACT_DIR)
	$(PYTHON) permits_combine.py $(INPUT_DIR) $@

$(ARTIFACT_DIR)/clean.csv: permits_clean.py $(ARTIFACT_DIR)/combined.csv | $(ARTIFACT_DIR)
	$(PYTHON) permits_clean.py $(ARTIFACT_DIR)/combined.csv $@

$(ARTIFACT_DIR)/model.pkl: permits_train.py $(ARTIFACT_DIR)/clean.csv | $(ARTIFACT_DIR)
	$(PYTHON) permits_train.py $(ARTIFACT_DIR)/clean.csv $@

clean:
	rm -rf $(ARTIFACT_DIR)
```

**Important:** Every recipe command underneath a target must start with an actual Tab character, not spaces.

---

## 7. Step 4 — Understand the Makefile Line by Line

### Variables

```makefile
PYTHON := python
INPUT_DIR := input_data
ARTIFACT_DIR := artifacts
```

Variables prevent repeated hard-coded values. If the Python command or directory name changes, it only needs to be changed once.

### Discovering the raw inputs

```makefile
INPUT_FILES := $(wildcard $(INPUT_DIR)/*.json)
```

`wildcard` expands to the JSON files in `input_data`.

These files are listed as prerequisites for `combined.csv`. Therefore, changing or adding a JSON file can cause the combine stage and all downstream stages to rebuild.

### Phony targets

```makefile
.PHONY: all clean
```

`all` and `clean` are command labels rather than files that the workflow intends to create. Declaring them phony prevents a real file named `all` or `clean` from interfering with those commands.

### Default target

```makefile
all: $(ARTIFACT_DIR)/model.pkl
```

The first target is the default target. Therefore:

```bash
make
```

is equivalent to:

```bash
make artifacts/model.pkl
```

### Artifact-directory target

```makefile
$(ARTIFACT_DIR):
	mkdir -p $(ARTIFACT_DIR)
```

This creates the output directory when needed.

The `-p` option avoids an error when the directory already exists.

### Combine target

```makefile
$(ARTIFACT_DIR)/combined.csv: permits_combine.py $(INPUT_FILES) | $(ARTIFACT_DIR)
	$(PYTHON) permits_combine.py $(INPUT_DIR) $@
```

Interpretation:

- **Target:** `artifacts/combined.csv`
- **Normal prerequisites:** `permits_combine.py` and the JSON input files
- **Order-only prerequisite:** the `artifacts` directory
- **Recipe:** run the combine script

`$@` is an automatic variable that means “the current target.” Here it expands to:

```text
artifacts/combined.csv
```

### Clean target

```makefile
$(ARTIFACT_DIR)/clean.csv: permits_clean.py $(ARTIFACT_DIR)/combined.csv | $(ARTIFACT_DIR)
	$(PYTHON) permits_clean.py $(ARTIFACT_DIR)/combined.csv $@
```

Interpretation:

- `clean.csv` depends on the cleaning script and `combined.csv`.
- If either prerequisite is newer than `clean.csv`, this recipe reruns.
- `$@` expands to `artifacts/clean.csv`.

### Model target

```makefile
$(ARTIFACT_DIR)/model.pkl: permits_train.py $(ARTIFACT_DIR)/clean.csv | $(ARTIFACT_DIR)
	$(PYTHON) permits_train.py $(ARTIFACT_DIR)/clean.csv $@
```

Interpretation:

- `model.pkl` depends on the training script and `clean.csv`.
- If either changes, the model is retrained.
- `$@` expands to `artifacts/model.pkl`.

### Clean target

```makefile
clean:
	rm -rf $(ARTIFACT_DIR)
```

This removes generated outputs so the entire pipeline can be rebuilt from scratch.

---

## 8. Why the Vertical Bar Is Used

This syntax appears in the file rules:

```makefile
normal prerequisites | order-only prerequisites
```

The `artifacts` directory is an **order-only prerequisite**. It must exist before the recipe runs, but a timestamp change to the directory itself should not force every artifact to rebuild.

Without the vertical bar, adding or removing a file inside `artifacts` could update the directory timestamp and trigger unnecessary work.

---

## 9. Step 5 — Run the Pipeline

Move to the repository root:

```bash
cd /home/labsuser
```

Activate the environment if necessary:

```bash
source /643_venv/bin/activate
```

Save the `Makefile`, then remove old generated files:

```bash
make clean
```

Run the required assignment command:

```bash
make artifacts/model.pkl
```

The terminal should execute commands in this order:

```text
mkdir -p artifacts
python permits_combine.py input_data artifacts/combined.csv
python permits_clean.py artifacts/combined.csv artifacts/clean.csv
python permits_train.py artifacts/clean.csv artifacts/model.pkl
```

---

## 10. Step 6 — Verify the Outputs

List the generated files:

```bash
ls -l artifacts
```

The folder should contain:

```text
combined.csv
clean.csv
model.pkl
```

This verifies that the requested final target also caused the two intermediate targets to be generated.

---

## 11. Step 7 — Verify Incremental Build Behavior

Run the same command again:

```bash
make artifacts/model.pkl
```

Because the outputs already exist and none of their prerequisites changed, Make should report that the target is up to date.

This is a key benefit of `make`: it uses file dependencies and modification timestamps to avoid repeating unnecessary work.

### Examples of selective rebuilding

- If a raw JSON file changes, Make should rerun combine, clean, and train.
- If `permits_clean.py` changes, Make should rerun clean and train, but not combine.
- If `permits_train.py` changes, Make should rerun only training.
- If nothing changes, no stage should rerun.

---

## 12. Understanding the Terminal Warnings

The successful run displayed pandas `UserWarning` and `FutureWarning` messages from the provided date-conversion logic in `permits_clean.py`.

These were warnings rather than exceptions:

- The command continued to the training stage.
- `artifacts/model.pkl` was created.
- All three required files appeared in `artifacts`.

Therefore, the Makefile completed successfully. The assignment was to connect the existing scripts, not rewrite their internal date-processing implementation.

---

## 13. Common Errors and Fixes

### Error: wrong input-directory name

Incorrect:

```makefile
DATA_DIR := data
```

Correct for this repository:

```makefile
INPUT_DIR := input_data
```

### Error: “missing separator”

Cause: recipe lines were indented with spaces instead of a Tab.

Fix: replace the leading spaces before each shell command with one Tab.

### Error: `make: command not found`

Cause: `make` is not installed or the wrong environment/container is being used.

In the course lab, `make` should normally be available.

### Error: Python import failure

Cause: the course environment is not active.

Fix:

```bash
source /643_venv/bin/activate
```

### Error: “No rule to make target”

Possible causes:

- The target name was misspelled.
- The command was run outside the repository root.
- A prerequisite filename in the `Makefile` does not match the real file.

Use:

```bash
pwd
ls
```

to confirm the current directory and filenames.

### Error: running `bash make ...`

Incorrect:

```bash
bash make artifacts/model.pkl
```

Correct:

```bash
make artifacts/model.pkl
```

`make` is its own program; it is not a Bash script.

---

## 14. Makefile Pipeline vs. Scikit-Learn Pipeline

This assignment contains two different meanings of “pipeline.”

### Makefile pipeline

Coordinates files and programs across the whole project:

```text
raw files -> combined file -> cleaned file -> model file
```

### Scikit-learn pipeline

Coordinates preprocessing and modeling inside `permits_train.py`:

```text
imputation/encoding/scaling -> linear regression
```

The Makefile manages the project-level workflow. The scikit-learn `Pipeline` manages the model-level transformations.

---

## 15. Oral-Exam Explanation

### Polished 60–90 Second Answer

> The purpose of this assignment was to turn three separate Python scripts into one reproducible, dependency-aware workflow using a Makefile. I first inspected each script's command-line arguments to identify its inputs and outputs. The combine script reads the JSON files in `input_data` and creates `artifacts/combined.csv`. The cleaning script uses that file to create `artifacts/clean.csv`. The training script uses the cleaned data to fit a preprocessing and linear-regression pipeline and saves it as `artifacts/model.pkl`. In the Makefile, each output is a target and its required script and input files are prerequisites. This lets Make determine the correct execution order automatically. I also listed the raw JSON files as prerequisites, so changing the source data causes the necessary downstream stages to rebuild. The `artifacts` directory is an order-only prerequisite because it must exist, but its timestamp should not trigger unnecessary rebuilding. Finally, I verified that `make artifacts/model.pkl` generated all three artifacts and that rerunning the command did not repeat work when nothing had changed.

---

## 16. Likely Oral-Exam Questions

### What is a target?

A target is the file or action that a Makefile rule is responsible for producing. Example:

```text
artifacts/model.pkl
```

### What is a prerequisite?

A prerequisite is a file or target required before another target can be built. Example:

```text
artifacts/clean.csv
```

is a prerequisite of `artifacts/model.pkl`.

### What is a recipe?

A recipe is the shell command that Make runs to build a target.

### Why use a Makefile instead of manually running three commands?

A Makefile:

- records the workflow in code;
- enforces the correct execution order;
- avoids repeated manual commands;
- rebuilds only the stages affected by changes;
- makes the process reproducible for another developer.

### How does Make know whether to rerun a rule?

It compares modification timestamps. A target is rebuilt when it is missing or when one of its normal prerequisites is newer.

### Why are the JSON files prerequisites of `combined.csv`?

The combined CSV is derived from those files. If a source JSON file changes, the combined data is stale and must be regenerated.

### Why does `clean.csv` depend on `combined.csv`?

The cleaning script cannot create clean data until the raw files have been combined into one CSV.

### Why does `model.pkl` depend on `clean.csv`?

The model must be trained from the cleaned data rather than directly from the original JSON files.

### What does `$@` mean?

`$@` expands to the current target's filename. It allows one rule to refer to its own output without repeating the full path.

### What does `.PHONY` mean?

It tells Make that targets such as `all` and `clean` are command labels, not files whose timestamps should be checked.

### Why is the artifact directory an order-only prerequisite?

The directory must exist before output files are written, but a timestamp change to the directory should not cause the files to rebuild.

### Why is `permits_predict.py` not included?

It uses a trained model to make a prediction. It is an application or inference step, not one of the required model-building stages.

### What happens when a cleaning script changes?

`clean.csv` becomes older than `permits_clean.py`, so Make rebuilds `clean.csv`. Since `model.pkl` depends on `clean.csv`, the model is then retrained. The combine stage does not rerun because none of its prerequisites changed.

### Why save the model as a pickle file?

Pickling serializes the fitted preprocessing and regression pipeline so it can be loaded later without retraining.

---

## 17. Quick Review Sheet

```text
Final command:
make artifacts/model.pkl

Pipeline:
input_data/*.json
    -> artifacts/combined.csv
    -> artifacts/clean.csv
    -> artifacts/model.pkl

Scripts:
combine = JSON files to one CSV
clean   = transform and remove unwanted columns
train   = preprocess, fit regression model, save pickle
predict = not part of build pipeline

Core Make concepts:
target       = output to build
prerequisite = required input
recipe       = command that creates the output
$@           = current target
.PHONY       = action target, not a file
|            = starts order-only prerequisites
wildcard     = finds matching input files

Validation:
make clean
make artifacts/model.pkl
ls -l artifacts
make artifacts/model.pkl  # should be up to date
```
