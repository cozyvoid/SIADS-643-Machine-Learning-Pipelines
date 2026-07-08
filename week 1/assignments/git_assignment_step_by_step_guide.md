# Git Assignment: Clean Step-by-Step Guide

## Assignment Requirements

Your repository must:

1. Use a branch named `main`.
2. Contain exactly 4 tracked files.
3. Have at least 6 commits.
4. Include at least one commit message containing the exact phrase:

   `Machine Learning Pipelines`

5. Include at least one revert commit.
6. Keep Git's default revert commit message unchanged.
7. Be pushed to GitHub.

---

## Step 1: Configure Git

Run these commands in the terminal:

```bash
git config --global user.name "Your Name"
git config --global user.email "youruniqname@umich.edu"
```

Example:

```bash
git config --global user.name "Sam Salazar"
git config --global user.email "youruniqname@umich.edu"
```

Verify the settings:

```bash
git config --global user.name
git config --global user.email
```

---

## Step 2: Clone the GitHub Repository

Copy the HTTPS repository link from GitHub, then run:

```bash
git clone https://github.com/ORGANIZATION/REPOSITORY-NAME.git
```

Example:

```bash
git clone https://github.com/mads643v2/git-demo-cozyvoid.git
```

Move into the repository folder:

```bash
cd git-demo-cozyvoid
```

Confirm that you are inside the repository:

```bash
git status
```

---

## Step 3: Create the `main` Branch

Check the current branch:

```bash
git branch --show-current
```

If Git reports `master` and there are no commits yet, create `main` directly:

```bash
git checkout -b main
```

Verify:

```bash
git branch --show-current
```

Expected output:

```text
main
```

> Important: If the repository has no commits yet, `git branch -M main` may fail because the `master` branch reference does not exist yet. In that case, use `git checkout -b main`.

---

## Step 4: Create the First File and Commit

Create a README file:

```bash
echo "# Machine Learning Pipeline Demo" > README.md
```

Stage and commit it:

```bash
git add README.md
git commit -m "Create project README"
```

This is commit 1.

---

## Step 5: Create the Second File and Commit

Create a requirements file:

```bash
echo "pandas" > requirements.txt
```

Stage and commit it:

```bash
git add requirements.txt
git commit -m "Add project requirements"
```

This is commit 2.

---

## Step 6: Create the Third File with the Required Commit Phrase

Create a simple Python file:

```bash
echo "print('Running the pipeline')" > pipeline.py
```

Stage and commit it using the required phrase:

```bash
git add pipeline.py
git commit -m "Set up Machine Learning Pipelines"
```

This is commit 3.

The commit message contains the exact required phrase:

```text
Machine Learning Pipelines
```

---

## Step 7: Create the Fourth File and Commit

Create a configuration file:

```bash
echo "model_name: logistic_regression" > config.txt
```

Stage and commit it:

```bash
git add config.txt
git commit -m "Add pipeline configuration"
```

This is commit 4.

At this point, the repository contains exactly four files:

```text
README.md
requirements.txt
pipeline.py
config.txt
```

---

## Step 8: Make Another Normal Commit

Update the README without creating a fifth file:

```bash
echo "This repository demonstrates basic Git operations." >> README.md
```

Stage and commit the change:

```bash
git add README.md
git commit -m "Expand project documentation"
```

This is commit 5.

---

## Step 9: Make a Commit That Will Be Reverted

Add a temporary line to `config.txt`:

```bash
echo "temporary_setting: true" >> config.txt
```

Stage and commit it:

```bash
git add config.txt
git commit -m "Add temporary configuration"
```

This is commit 6.

---

## Step 10: Revert the Previous Commit

Revert the most recent commit:

```bash
git revert --no-edit HEAD
```

This creates commit 7.

The `--no-edit` option keeps Git's default revert commit message unchanged.

Expected revert commit message:

```text
Revert "Add temporary configuration"
```

---

## Step 11: Verify the Assignment Requirements

### Confirm the branch

```bash
git branch --show-current
```

Expected:

```text
main
```

### Confirm exactly four tracked files

```bash
git ls-files
```

Expected:

```text
README.md
config.txt
pipeline.py
requirements.txt
```

The order may vary, but there should be exactly four files.

### Count the commits

```bash
git rev-list --count HEAD
```

Expected:

```text
7
```

The assignment requires at least 6 commits, so 7 is acceptable.

### Review the commit history

```bash
git log --oneline
```

You should see entries similar to:

```text
Revert "Add temporary configuration"
Add temporary configuration
Expand project documentation
Add pipeline configuration
Set up Machine Learning Pipelines
Add project requirements
Create project README
```

### Confirm the working tree is clean

```bash
git status
```

Expected:

```text
nothing to commit, working tree clean
```

---

## Step 12: Push the Repository to GitHub

Push the `main` branch:

```bash
git push -u origin main
```

If additional commits are made later, push them with:

```bash
git push origin main
```

---

## Step 13: Verify the Repository on GitHub

Open the repository in your web browser and refresh the page with:

```text
Ctrl + R
```

Confirm that GitHub shows:

- Branch: `main`
- Exactly 4 files
- At least 6 commits
- A commit containing `Machine Learning Pipelines`
- A revert commit named `Revert "Add temporary configuration"`

Once all of these appear on GitHub, the assignment is complete.

---

## Common Errors and Fixes

### Error: `fatal: not in a git directory`

Cause: You are running repository-specific commands outside the repository folder.

Fix:

```bash
cd git-demo-cozyvoid
git status
```

---

### Error: `cd: git-demo-cozyvoid: No such file or directory`

Cause: You are already inside the repository, or the folder has a different name.

Check the terminal prompt or run:

```bash
pwd
ls
```

If the prompt already shows something like:

```text
~/git-demo-cozyvoid
```

you are already inside the repository.

---

### Error: `git: 'pushs' is not a git command`

Cause: Typo.

Correct command:

```bash
git push -u origin main
```

---

### Error: `remote ref does not exist` when deleting `master`

Cause: No remote `master` branch exists.

This is not a problem. Do not delete anything. Continue using `main`.

---

### Error: `refname refs/heads/master not found`

Cause: The repository has no commits yet, so the `master` branch reference has not been created.

Fix:

```bash
git checkout -b main
```

---

## Final Submission Checklist

- [ ] Git name and email configured
- [ ] Repository cloned
- [ ] Current branch is `main`
- [ ] Exactly 4 tracked files
- [ ] At least 6 commits
- [ ] One commit contains `Machine Learning Pipelines`
- [ ] One commit reverts a previous commit
- [ ] Default revert message was preserved
- [ ] Working tree is clean
- [ ] Changes were pushed to GitHub
- [ ] GitHub displays the correct files and commits
