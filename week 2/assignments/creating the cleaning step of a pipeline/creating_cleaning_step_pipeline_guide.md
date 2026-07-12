# Creating the Cleaning Step of a Pipeline
## Revised Assignment Rundown and Oral-Exam Review

## 1. Assignment objective

The survey company stores respondent information in two separate CSV files:

- `data/respondent_contact.csv`
- `data/respondent_other.csv`

The goal is to create a standalone Python script named:

```text
respondent_data_clean.py
```

The script must:

1. Accept three required positional command-line arguments.
2. Read the two CSV files.
3. Join them using `respondent_id`.
4. Convert `birthdate` from `MMDDYYYY` to `YYYY-MM-DD`.
5. Keep the required output columns in the required order.
6. Write the cleaned data to a new CSV file.
7. Work with both the assignment data and the grader's hidden test data.
8. Pass `pylint` without errors.

---

## 2. Correct project structure

The grader expects the Python script in the project root, not inside the `data` folder.

```text
/home/labsuser/
├── HELP.md
├── README.md
├── respondent_data_clean.py
└── data/
    ├── respondent_contact.csv
    └── respondent_other.csv
```

The generated file will also be placed inside `data`:

```text
data/respondent_combined.csv
```

### Important correction

This is correct:

```text
/home/labsuser/respondent_data_clean.py
```

This is not the expected grader location:

```text
/home/labsuser/data/respondent_data_clean.py
```

---

## 3. What the pipeline does

```text
respondent_contact.csv
            \
             → Read both files
            /
respondent_other.csv
            ↓
Join on respondent_id
            ↓
Convert birthdate format
            ↓
Select required columns
            ↓
Write respondent_combined.csv
```

This is a pipeline because the same sequence of data-processing steps can be run repeatedly and consistently.

---

## 4. Required command-line arguments

The script takes three positional arguments:

```text
1. contact_info_file
2. other_info_file
3. output_file
```

The intended command is:

```bash
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

Python interprets the command as:

```text
contact_info_file = data/respondent_contact.csv
other_info_file   = data/respondent_other.csv
output_file       = data/respondent_combined.csv
```

The script automates the cleaning work after these three paths are supplied.

---

## 5. Final script

```python
"""Join and clean respondent data from two CSV files."""

import argparse

import pandas as pd


OUTPUT_COLUMNS = [
    "respondent_id",
    "name",
    "address",
    "phone",
    "job",
    "company",
    "birthdate",
]


def clean_respondent_data(
    contact_info_file,
    other_info_file,
    output_file,
):
    """Join the respondent files and write the cleaned output."""

    # Load the respondent contact information.
    contact_df = pd.read_csv(contact_info_file)

    # Read birthdate as text so leading zeros are preserved.
    other_df = pd.read_csv(
        other_info_file,
        dtype={"birthdate": "string"},
    )

    # Join the two files using the shared respondent ID.
    combined_df = contact_df.merge(
        other_df,
        on="respondent_id",
        how="inner",
        validate="one_to_one",
    )

    # Convert birthdates from MMDDYYYY to YYYY-MM-DD.
    combined_df["birthdate"] = pd.to_datetime(
        combined_df["birthdate"].str.zfill(8),
        format="%m%d%Y",
    ).dt.strftime("%Y-%m-%d")

    # Keep the required columns in the required order.
    combined_df = combined_df[OUTPUT_COLUMNS]

    # Write the cleaned data without an extra index column.
    combined_df.to_csv(
        output_file,
        index=False,
    )


def main():
    """Read command-line arguments and run the cleaning step."""

    parser = argparse.ArgumentParser(
        description="Join and clean respondent data."
    )

    parser.add_argument(
        "contact_info_file",
        help="Path to the respondent contact CSV file.",
    )

    parser.add_argument(
        "other_info_file",
        help="Path to the respondent other-information CSV file.",
    )

    parser.add_argument(
        "output_file",
        help="Path for the cleaned combined CSV file.",
    )

    args = parser.parse_args()

    clean_respondent_data(
        args.contact_info_file,
        args.other_info_file,
        args.output_file,
    )


if __name__ == "__main__":
    main()
```

The file must end with a final newline after `main()`.

---

## 6. Code walkthrough

### Import `argparse`

```python
import argparse
```

`argparse` allows the user or grader to supply file paths through the terminal.

This makes the script reusable with different datasets.

### Import Pandas

```python
import pandas as pd
```

Pandas is used to:

- read CSV files;
- join DataFrames;
- convert dates;
- select columns;
- write the final CSV.

### Define the required output columns

```python
OUTPUT_COLUMNS = [
    "respondent_id",
    "name",
    "address",
    "phone",
    "job",
    "company",
    "birthdate",
]
```

This list guarantees the required order of the output columns.

### Read the contact file

```python
contact_df = pd.read_csv(contact_info_file)
```

This loads the contact data into a DataFrame.

### Read birthdate as text

```python
other_df = pd.read_csv(
    other_info_file,
    dtype={"birthdate": "string"},
)
```

Birthdates such as:

```text
04161957
```

begin with a zero. If the value were treated as an integer, it could become:

```text
4161957
```

Reading it as a string preserves all eight characters.

### Join on `respondent_id`

```python
combined_df = contact_df.merge(
    other_df,
    on="respondent_id",
    how="inner",
    validate="one_to_one",
)
```

- `on="respondent_id"` uses the shared key.
- `how="inner"` keeps only respondents present in both files.
- `validate="one_to_one"` checks that each ID appears at most once in each file.

### Convert the birthdate

```python
combined_df["birthdate"] = pd.to_datetime(
    combined_df["birthdate"].str.zfill(8),
    format="%m%d%Y",
).dt.strftime("%Y-%m-%d")
```

This performs three operations:

1. `.str.zfill(8)` restores leading zeros if needed.
2. `pd.to_datetime(..., format="%m%d%Y")` parses the original date.
3. `.dt.strftime("%Y-%m-%d")` produces the required output format.

Example:

```text
04161957 → 1957-04-16
```

### Select columns in the required order

```python
combined_df = combined_df[OUTPUT_COLUMNS]
```

This removes any unwanted columns and fixes the output order.

### Write the output CSV

```python
combined_df.to_csv(
    output_file,
    index=False,
)
```

`index=False` prevents Pandas from adding an unwanted numbered column.

### Parse the terminal arguments

```python
args = parser.parse_args()
```

This reads the three file paths supplied in the command.

### Use the main guard

```python
if __name__ == "__main__":
    main()
```

This runs `main()` when the file is executed directly.

It also allows the module to be imported elsewhere without automatically running the script.

---

## 7. Exact terminal workflow

### Step 1: Activate the course environment

```bash
source /643_venv/bin/activate
```

The prompt should begin with:

```text
(643_venv)
```

### Step 2: Move to the project root

```bash
cd ~
```

### Step 3: Confirm the project structure

```bash
ls
```

Expected:

```text
HELP.md
README.md
data
respondent_data_clean.py
```

Then inspect the data folder:

```bash
ls data
```

Expected:

```text
respondent_contact.csv
respondent_other.csv
```

### Step 4: Run the script

```bash
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

The script may complete without printing anything. That is normal.

### Step 5: Confirm the output file exists

```bash
ls data
```

Expected:

```text
respondent_contact.csv
respondent_other.csv
respondent_combined.csv
```

### Step 6: Preview the output

```bash
head -5 data/respondent_combined.csv
```

The first record should include Breanna Calderon, with the birthdate:

```text
1957-04-16
```

---

## 8. Run pylint

From the project root:

```bash
pylint respondent_data_clean.py
```

The target result is:

```text
Your code has been rated at 10.00/10
```

### Final-newline warning

The warning:

```text
C0304: Final newline missing
```

means the file ends immediately after the final character.

Fix it in VS Code by:

1. Clicking after the final `)` in `main()`.
2. Pressing Enter once.
3. Saving with `Ctrl+S`.

A reliable terminal fix is:

```bash
printf '\n' >> respondent_data_clean.py
```

Then rerun:

```bash
pylint respondent_data_clean.py
```

---

## 9. How the automatic grader works

The assignment is automatically graded.

The grader checks:

```text
Works with assignment data     4 points
Works with different data      5 points
Pylint finds no issues         1 point
```

The hidden-data test is important because it verifies that:

- filenames are not hard-coded;
- the script accepts command-line arguments;
- the logic works with a different dataset;
- the output format remains correct.

The grader runs the script from the project root, so the script must be located at:

```text
/home/labsuser/respondent_data_clean.py
```

---

## 10. Errors encountered and what they meant

### Missing positional arguments

Error:

```text
the following arguments are required:
contact_info_file, other_info_file, output_file
```

Cause:

```bash
python respondent_data_clean.py
```

was run without the three file paths.

Correct command:

```bash
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

### `FileNotFoundError`

Error:

```text
No such file or directory: 'respondent_contact.csv'
```

Cause:

- the terminal was in the wrong directory;
- the file path was incomplete;
- the file had been deleted;
- the filename did not match exactly.

Useful diagnostic commands:

```bash
pwd
ls
ls data
```

### Incorrect absolute path

Examples of incorrect paths included:

```text
/home/labuser/...
```

instead of:

```text
/home/labsuser/...
```

Linux paths must also use forward slashes:

```text
/home/labsuser
```

not:

```text
\home\labsuser
```

### `NameError: main is not defined`

Cause:

`main()` was accidentally nested inside another function because of indentation.

These lines must begin at the far-left margin:

```python
def clean_respondent_data(...):
```

```python
def main():
```

```python
if __name__ == "__main__":
```

### `SyntaxError` near `.dt.strftime(...)`

Cause:

A punctuation or parenthesis error occurred in the date-conversion expression.

Correct form:

```python
combined_df["birthdate"] = pd.to_datetime(
    combined_df["birthdate"].str.zfill(8),
    format="%m%d%Y",
).dt.strftime("%Y-%m-%d")
```

### Script passed locally but grader failed

Cause:

The script was inside the `data` directory instead of the project root.

Incorrect:

```text
/home/labsuser/data/respondent_data_clean.py
```

Correct:

```text
/home/labsuser/respondent_data_clean.py
```

### Address appears on two terminal lines

The address contains an embedded newline.

A valid CSV stores it inside quotes:

```csv
"00024 Emily Forge
West Kristenville, MO 06306"
```

It is still one field and one respondent record.

---

## 11. Useful validation commands

Check the output columns:

```bash
python -c "import pandas as pd; print(pd.read_csv('data/respondent_combined.csv').columns.tolist())"
```

Expected:

```text
['respondent_id', 'name', 'address', 'phone', 'job', 'company', 'birthdate']
```

Check the output shape and first record:

```bash
python -c "import pandas as pd; df = pd.read_csv('data/respondent_combined.csv'); print(df.shape); print(df.iloc[0])"
```

Check that the script is in the root:

```bash
ls ~/respondent_data_clean.py
```

Check that the input files exist:

```bash
ls ~/data/respondent_contact.csv
ls ~/data/respondent_other.csv
```

---

## 12. Strong oral-exam explanation

> I created a standalone Python command-line script that accepts the contact file, the other respondent-information file, and an output path as three positional arguments. I used Pandas to read both CSV files and explicitly loaded birthdate as a string so leading zeros would not be lost. I merged the DataFrames on `respondent_id` using an inner one-to-one merge, reformatted birthdate from `MMDDYYYY` to `YYYY-MM-DD`, selected the required columns in the required order, and wrote the result with `index=False`. The script uses a main guard so it runs directly but can also be imported. I also verified the project structure expected by the grader and confirmed the script passes pylint with a score of 10 out of 10.

---

## 13. Likely oral-exam questions

### Why use `respondent_id` as the join key?

It is the shared identifier that connects the same respondent across both files. Names, phone numbers, or addresses are less reliable because they may be duplicated or formatted differently.

### Why use an inner join?

The final record requires data from both files. An inner join keeps respondents with matching records in both sources.

### What would a left join do?

It would keep every respondent from the left DataFrame, even if no matching record existed in the right DataFrame. Unmatched fields would become missing values.

### Why read `birthdate` as a string?

Birthdates can begin with zero. Numeric types do not preserve leading zeros.

### Why use `zfill(8)`?

It guarantees that the original date string contains eight characters before parsing.

### Why specify `format="%m%d%Y"`?

It tells Pandas exactly how to interpret the original date format and avoids ambiguous parsing.

### Why use `strftime("%Y-%m-%d")`?

It converts the parsed date into the exact format required by the assignment.

### Why use `index=False`?

The DataFrame index is not one of the required output columns.

### Why use `argparse`?

It allows the script to process different files without changing the source code. This is why it can pass the hidden-data test.

### Why use `validate="one_to_one"`?

It checks the assumption that each respondent ID appears once in each source. If duplicate IDs exist, Pandas raises an error rather than silently producing duplicated combinations.

### What does the main guard do?

It calls `main()` only when the file is executed directly. It prevents the script from running automatically when imported.

### Why did the VS Code Run button fail?

The basic Run button executed only the script path and did not supply the three required positional arguments.

### Why did the grader initially fail?

The grader expected `respondent_data_clean.py` in the project root, but it was initially stored inside the `data` folder.

---

## 14. Final checklist

### Before running

```text
□ Course environment is active
□ Current directory is /home/labsuser
□ respondent_data_clean.py is in the project root
□ respondent_contact.csv is inside data
□ respondent_other.csv is inside data
□ Script accepts three positional arguments
□ File ends with a final newline
```

### Run

```bash
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

### Validate

```text
□ respondent_combined.csv was created
□ First respondent is Breanna Calderon
□ Birthdate is formatted as 1957-04-16
□ Required columns are in the correct order
□ Address line break is preserved
□ No extra index column exists
□ Pylint score is 10.00/10
```

### Submit

```text
□ Script is in the grader's expected location
□ Functional test passes
□ Pylint passes
□ Assignment is resubmitted
```
