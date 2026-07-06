# Module 1 Assignment Part 2: Rodeo Column Renaming

## Goal

Complete the `rename_rodeo_columns()` function in `rodeo.py`.

The function must:

1. Convert column names to lowercase.
2. Replace spaces with underscores.
3. Remove the trailing word `Data` when it appears at the end of a column name.

Example:

```text
Participant Count Data  ->  participant_count
Rodeo Clown Count       ->  rodeo_clown_count
Hats Visible            ->  hats_visible
Cost Data               ->  cost
```

---

## Step 1: Open the Assignment Workspace

Launch the Part 2 assignment in VS Code.

The workspace should contain:

```text
README.md
HELP.md
rodeo.py
```

For this part, the work is completed directly in the assignment workspace. No separate Git repository is needed unless the assignment instructions explicitly provide a GitHub Classroom link.

---

## Step 2: Activate the Course Python Environment

Open a terminal using:

```text
Terminal → New Terminal
```

If the terminal prompt does not already begin with `(643_venv)`, run:

```bash
source /643_venv/bin/activate
```

A correctly activated terminal should look similar to:

```text
(643_venv) labsuser@vscode:~$
```

---

## Step 3: Open `rodeo.py`

The starter code contains an empty function:

```python
def rename_rodeo_columns(columns):
    # Replace this and the line below with your code...
    raise NotImplementedError
```

Leave the provided test code under this line unchanged:

```python
if __name__ == "__main__":
```

Only replace the placeholder code inside the function.

---

## Step 4: Add the Function Code

Use this implementation:

```python
def rename_rodeo_columns(columns):
    # Create an empty list to store the cleaned column names.
    corrected_columns = []

    # Process each original column name one at a time.
    for column in columns:
        # Remove unnecessary spaces from the beginning and end.
        column = column.strip()

        # Remove the trailing word "Data" when it appears at the end.
        if column.lower().endswith(" data"):
            column = column[:-5]

        # Convert the name to lowercase and replace spaces with underscores.
        column = "_".join(column.lower().split())

        # Add the cleaned name to the results list.
        corrected_columns.append(column)

    # Return the completed list of corrected column names.
    return corrected_columns
```

---

## Step 5: Understand the Main Steps

### Create a results list

```python
corrected_columns = []
```

This list stores each cleaned column name.

### Loop through the original names

```python
for column in columns:
```

This processes one column name at a time.

### Remove outside whitespace

```python
column = column.strip()
```

This removes extra spaces at the beginning or end.

### Remove trailing `Data`

```python
if column.lower().endswith(" data"):
    column = column[:-5]
```

The condition checks whether the name ends with the word `Data`.

The slice `[:-5]` removes:

```text
 Data
```

including the preceding space.

### Convert to lowercase and underscores

```python
column = "_".join(column.lower().split())
```

This:

1. Converts the text to lowercase.
2. Splits the words at whitespace.
3. Rejoins the words using underscores.

Example:

```text
Rodeo Clown Count
```

becomes:

```text
rodeo_clown_count
```

### Save the cleaned name

```python
corrected_columns.append(column)
```

This adds the corrected name to the results list.

### Return the result

```python
return corrected_columns
```

This sends the completed list back to the provided test code.

---

## Step 6: Save the File

Save `rodeo.py` using:

```text
Ctrl + S
```

---

## Step 7: Run the Provided Test

In the terminal, run:

```bash
python rodeo.py
```

Expected output:

```text
Original                  Corrected
-----------------------------------
Participant Count Data    participant_count
Rodeo Clown Count         rodeo_clown_count
Hats Visible              hats_visible
Cost Data                 cost
```

If the output matches, the function is working correctly.

---

## Step 8: Remove Unneeded Backup Files

If you created a backup such as:

```text
rodeo_backup.py
```

delete it before submitting:

```bash
rm rodeo_backup.py
```

Confirm the remaining files:

```bash
ls
```

The assignment workspace should contain only the expected files, such as:

```text
README.md
HELP.md
rodeo.py
```

---

## Step 9: Submit the Assignment

Use the assignment's submission panel or grader.

Before submitting, confirm:

- `rodeo.py` is saved.
- The course environment is active.
- `python rodeo.py` runs without errors.
- The output matches the expected cleaned column names.
- No unnecessary backup files remain.

---

## Common Errors

### `NotImplementedError`

Cause: The placeholder line is still present.

Remove:

```python
raise NotImplementedError
```

and replace it with the completed function code.

### `python: can't open file 'rodeo.py'`

Cause: The terminal is not in the folder containing `rodeo.py`.

Check the current files:

```bash
ls
```

Then move to the correct folder if needed.

### Git reports `not a git repository`

This Part 2 workspace may not require Git. Complete and submit the assignment directly through the provided course environment unless the instructions explicitly require a GitHub repository.

### Extra `rodeo_backup.py` file appears

Delete it before submission:

```bash
rm rodeo_backup.py
```

---

## Final Checklist

- [ ] Opened the Part 2 VS Code workspace
- [ ] Activated `(643_venv)`
- [ ] Edited only the function in `rodeo.py`
- [ ] Converted names to lowercase
- [ ] Replaced spaces with underscores
- [ ] Removed trailing `Data`
- [ ] Saved `rodeo.py`
- [ ] Ran `python rodeo.py`
- [ ] Confirmed the expected output
- [ ] Removed unnecessary backup files
- [ ] Submitted through the assignment grader
