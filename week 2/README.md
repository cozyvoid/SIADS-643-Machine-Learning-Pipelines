**TO: Dev team 3**

**From: Raj**

**Subject: data cleaning**

We've been hired by a survey research firm to help them build a pipeline to analyze their survey data. Your task is to build the import and cleaning step to handle the data about the survey respondents. (Later projects will build steps to associate this data with survey responses to enrich the data analysis.)

There are two files with data about each respondent:
  - respondent_contact.csv
  - respondent_other.csv

These need to be joined together based on the respondent_id field (which is the same for each respondent's data in both files). To do this, create a Python script called `respondent_data_clean.py`. This script must be runnable as a stand-alone script. It should take 3 required positional arguments:
  - contact_info_file (The path to the respondent_contact.csv file)
  - other_info_file (The path to the respondent_other.csv file)
  - output_file (The path to the output CSV file)

The script must join the data from the two input files, and then write the joined data to the file given in the output_file argument. The output_file must include these columns in this order:
  - respondent_id
  - name
  - address
  - phone
  - job
  - company
  - birthdate (A note about the "birthdate" field: its format used in the original file is "MMDDYYYY", but in the output file its format must be "YYYY-MM-DD".)

When your script is complete, this command...

```
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

... will create a file data/respondent_combined.csv, whose first entry will include data for respondent "Breanna Calderon".

A few notes:
  - The address field has a line break in it, so notice that the CSV format wraps that field in quotes.
  - You can use Pandas and the Python standard library
