**Subject: Task: Developing an ML Pipeline for Building Permit Data**

Hello Dev team,

We've got a new ticket for you! We've onboarded a new customer who has contracted our services to build a machine learning pipeline for analyzing building permit data. Specifically, they are interested in a model that can estimate the expected wait time for building permits in terms of days.

The dataset they've provided, 'clean.csv', contains both categorical and numerical information. Your task is to enhance the existing 'permits_train.py' file by completing the 'make_pipeline' function. The goal is to create and return a pipeline with two stages: preprocessing and modeling.

For the preprocessing stage, we need to establish substages num and cat to handle numerical and categorical feature preprocessing, respectively. Ensure that when processing categorical features, you impute missing values with the string 'missing' and perform one-hot encoding with unknown values ignored. Name this stage `preprocessor`.

When processing numerical features, impute missing data with the median and apply standard scaling.

The modeling stage should include your random forest model.

Import all necessary packages from sklearn to build the pipeline. The completed script should be capable of executing with the command:

```
python permits_train.py clean.csv
```

This command will read in the client-provided dataset, create a model for estimating the expected wait time for building permit approvals using a random forest, and print out the model metrics.

Thank you for your attention to this task. Let's deliver a robust solution for our client!
