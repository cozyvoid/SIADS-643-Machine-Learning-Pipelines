TO: Dev team 3
From: Raj
Subject: Hyperparameter Tuning for Client
Hey Dev team 3,

Our client is back with another request. After seeing what you did with the pipeline your team wrote earlier, the client is ready for the company to provide some better models for the data they have. What we need from you is for you to perform hyperparameter tuning to find the best combination of hyperparameters.

Specifically, we want you to try the following combinations:

1. Numerical Data Preprocessing:

Impute missing values with either the mean or the median.
2. Random Forest Regressor:

Use 10, 100, or 1000 trees in the forest.
Since we're not quite sure what the best combination is, you should explore these hyperparameter combinations with 5-fold cross-validation on your training data.

You might want to reference the documentation for the Pipeline class as well as look into GridSearchCV documentation when you're building this out.

Note: The steps in your pipeline must be named `preprocessor` and `regressor`.

Additionally, please ensure to use the parameter `scoring='neg_mean_absolute_error'` in the GridSearchCV