# Chapter 10 Study Guide: Build Safeguards for Models

**Book:** *Building Machine Learning Powered Applications*  
**Chapter focus:** Designing production ML systems that detect, prevent, and recover from model failures

---

## 1. Chapter Overview

A production machine learning system must be designed with the assumption that failures will occur.

Traditional software engineers use **fault tolerance** to keep systems functioning when individual components break. The same principle applies to ML systems:

> A model will eventually receive unfamiliar, malformed, misleading, or difficult examples, even if its average test performance is strong.

The goal is therefore not to build a model that never fails. The goal is to build a surrounding system that:

- Detects likely failures
- Prevents invalid predictions from reaching users
- Falls back to safer alternatives
- Maintains acceptable speed as traffic increases
- Supports reproducible model updates
- Collects evidence about real-world performance
- Allows users to correct mistakes
- Makes deployment and debugging manageable

The chapter develops safeguards in four major areas:

1. **Engineer around failures**
2. **Engineer for performance**
3. **Manage the model and data life cycle**
4. **Ask users for feedback**

It concludes with deployment lessons from Chris Moody and Stitch Fix.

---

# 2. Why Production ML Requires Safeguards

A model’s test score summarizes performance across a dataset. It does not guarantee that every individual prediction will be correct.

A model may fail because:

- Required features are missing
- A feature has the wrong type
- A value is outside the expected range
- Production data differs from training data
- The input is nonsensical or adversarial
- The model is uncertain
- The model is confidently wrong
- The prediction is technically valid but not useful
- A new model version introduces a regression
- A cache contains outdated results
- Data preprocessing changed unexpectedly
- Infrastructure cannot handle the request volume
- User behavior changes after deployment

Traditional code often throws an obvious error when input is invalid. ML models may behave differently: as long as the input has an acceptable shape and type, the model may return a prediction even when the input is meaningless.

For example, a text classifier might receive a string of random characters. The vectorizer may still transform the string into numbers, and the classifier may still assign a topic. The prediction looks structurally valid even though it is meaningless.

This makes ML failures especially dangerous:

> A model can fail silently by returning a plausible-looking answer.

---

# 3. Main Safeguard Locations

The chapter identifies three especially important places to verify an ML pipeline:

1. **Inputs**
2. **Model confidence or difficulty**
3. **Outputs**

A robust inference pipeline can be conceptualized as:

```text
Incoming request
      ↓
Input validation
      ↓
Difficulty or filtering check
      ↓
Primary model
      ↓
Confidence and output validation
      ↓
Fallback, error, or approved response
      ↓
User
```

Each stage protects the stages that follow.

---

# 4. Input Checks

A trained model learned from a dataset with particular properties:

- A fixed feature set
- Specific data types
- Particular value ranges
- Characteristic distributions
- Certain missing-value patterns
- Relationships among features

If production inputs differ substantially from those conditions, model performance may decline.

## 4.1 What input checks should verify

In order of importance, the chapter recommends checking:

1. **Feature presence**
2. **Feature types**
3. **Feature values**

### Check 1: Are all necessary features present?

Examples:

- A text model expects `question_text`
- A pricing model expects `location`, `distance`, and `time`
- A risk model expects demographic and historical fields
- An image model expects an image with defined dimensions

Missing a core feature can make the prediction invalid.

### Check 2: Are the features the correct type?

Examples:

- A numeric field should not contain arbitrary text
- A list should not arrive as a scalar
- A timestamp should be parseable as a date
- A Boolean field should not contain an unrelated category
- An image should be represented in the expected format

A model may not always crash when the type is wrong, especially after implicit conversions. It may instead produce a poor prediction.

### Check 3: Are the values reasonable?

Examples:

- Age should not be negative
- A probability should fall between 0 and 1
- Latitude should be between -90 and 90
- A text length should be nonnegative
- An image should not be empty
- A purchase amount should not be infinite

Full distribution validation can be difficult. A practical first safeguard is to define reasonable minimum and maximum values.

## 4.2 Checks versus tests

The chapter makes an important distinction.

### Tests

Tests verify that known code behavior remains correct.

They are usually:

- Run during development or continuous integration
- Based on predetermined inputs and expected outputs
- Triggered when code or models change
- Used to detect regressions

Example:

```text
Given this known feature vector,
the preprocessing function should return this expected output.
```

### Checks

Checks run inside the production pipeline.

They:

- Examine live inputs
- Influence control flow
- May prevent the model from running
- May trigger an error, fallback, or alternate model
- Operate for every relevant request

Example:

```text
If the request is missing a required feature,
do not call the model.
```

### Comparison

| Aspect | Test | Check |
|---|---|---|
| Purpose | Verify code behavior | Protect live inference |
| Timing | Development or deployment process | During production requests |
| Input | Known, predetermined | Real user or system input |
| Result | Pass/fail test report | Change pipeline control flow |
| Failure response | Fix code before release | Error, fallback, alternate path |

---

# 5. Input-Control Logic

When an input check fails, the system should not blindly run the model.

Possible responses include:

- Return a clear error
- Ask the user to correct the input
- Request missing information
- Use a heuristic
- Use an earlier or simpler model
- Decline to produce a prediction
- Log the event for analysis

The correct action depends on how essential the failed feature is.

## 5.1 Core information missing

If a required feature is central to the prediction, return an error that identifies the problem.

Example:

```text
Cannot generate a prediction because `location` is missing.
```

## 5.2 Partial information available

If enough information remains to provide a lower-quality but useful answer, use a fallback.

This is one reason to begin an ML project with a heuristic. The heuristic may later serve as a reliable backup when the learned model cannot safely run.

## 5.3 Example control flow

```python
def validate_and_handle_request(question_data):
    missing = find_absent_features(question_data)

    if missing:
        raise ValueError(f"Missing feature(s): {missing}")

    wrong_types = check_feature_types(question_data)

    if wrong_types:
        if "text_len" in question_data:
            if isinstance(question_data["text_len"], float):
                return run_heuristic(question_data["text_len"])

        raise ValueError(f"Incorrect type(s): {wrong_types}")

    return run_model(question_data)
```

### Logic in plain language

1. Find missing features.
2. If any are missing, stop and raise an error.
3. Check feature types.
4. If some types are wrong, determine whether a heuristic can still run.
5. If the heuristic is possible, use it.
6. Otherwise, raise an error.
7. Run the main model only after all checks pass.

---

# 6. Output Checks

Even if the input is valid, the model’s output may be invalid, implausible, unsafe, or useless.

Output validation asks:

> Should this result actually be shown to the user?

## 6.1 Plausibility checks

For a model predicting a person’s age, a reasonable output range might be:

```text
0 ≤ predicted age ≤ slightly above 100
```

A prediction of -12 or 800 should not be displayed, even if the model returned it successfully.

Other examples:

- A percentage should usually remain between 0 and 100
- A probability should remain between 0 and 1
- A count should usually be a nonnegative integer
- A date should be within a meaningful time range
- A price should not be negative
- A dosage recommendation must obey strict safety constraints

## 6.2 Usefulness checks

A plausible prediction is not automatically useful.

For the ML Editor, a recommendation to delete everything the user wrote could be mathematically valid but unhelpful and insulting.

Therefore, acceptable output should satisfy both:

1. **Plausibility**
2. **Usefulness**

This means output rules may encode product expectations, not only physical or mathematical bounds.

## 6.3 Output fallback example

```python
def validate_and_correct_output(question_data, model_output):
    try:
        verify_output_type_and_range(model_output)
    except ValueError:
        return run_heuristic(question_data["text_len"])

    return model_output
```

### Important implementation detail

The fallback should normally be returned. Otherwise, the function could run the heuristic but still return the invalid model output.

## 6.4 Backup hierarchy

A robust system may use the following sequence:

```text
Primary model
      ↓ failure
Simpler backup model
      ↓ failure
Heuristic
      ↓ failure
Clear error or abstention
```

Each fallback should also have its own validation.

---

# 7. Why a Simpler Backup Model Can Help

A simpler model may have lower average accuracy than a complex model, but the two models may make different mistakes.

The complex model may use a flexible decision boundary, while the simple model may use a smoother or more restricted boundary.

Because their error patterns are not perfectly correlated:

- The complex model may fail on an example the simple model gets right.
- The simple model can act as a useful fallback.
- Diversity of failure modes can improve system robustness.

This does not mean the simpler model should replace the primary model. It means the simpler model may be valuable when the primary output fails validation.

> Backup quality depends not only on average accuracy, but also on whether the backup makes different errors.

---

# 8. Model Failure Fallbacks

Input and output checks catch many problems, but they do not solve every case.

A model can receive:

- A valid input
- With all expected features
- Using the correct types
- Within reasonable ranges

It can then produce:

- A plausible output
- Within the approved range

And still be wrong.

The system therefore needs ways to identify difficult examples.

The chapter presents two main approaches:

1. **Use the model’s confidence**
2. **Train a separate filtering model**

---

# 9. Confidence-Based Abstention

Many classification models output class probabilities or scores.

If those probabilities are **well calibrated**, they can estimate how likely the prediction is to be correct.

Example:

```text
Class A probability: 0.51
Class B probability: 0.49
```

The model is uncertain, so the system might:

- Avoid showing the result
- Ask for more information
- Route the example to a human
- Use a fallback
- Return a low-confidence warning

## 9.1 Calibration matters

A model is calibrated when predictions assigned a probability near 0.8 are correct approximately 80% of the time.

Without calibration, a score of 0.95 may not mean the model is genuinely reliable.

Confidence-based safeguards are therefore most useful when:

- Probabilities are available
- Probabilities have been evaluated for calibration
- A meaningful threshold can be selected
- Abstaining is acceptable within the product

## 9.2 Limitation: confident errors

Models can be confidently wrong.

Examples include:

- Out-of-distribution inputs
- Adversarial examples
- Spurious correlations
- Data leakage effects
- Distribution shifts

Confidence alone is therefore not a complete safeguard.

## 9.3 Limitation: full inference cost

To obtain the main model’s confidence, the complete inference pipeline must run.

This is inefficient when:

- The main model is expensive
- It requires a GPU
- Many inputs are unsuitable
- Most model outputs will be discarded

A filtering model can address this problem.

---

# 10. Filtering Models

A **filtering model** predicts whether the main model is likely to succeed on an input.

It is usually a fast binary classifier:

```text
0 = main model likely to succeed
1 = main model likely to fail
```

It runs before the expensive model.

## 10.1 Purpose

A filtering model can:

- Block difficult inputs
- Reduce poor user-facing predictions
- Avoid unnecessary expensive inference
- Detect inputs unlike the main model’s successful cases
- Detect known failure patterns
- Screen some adversarial inputs
- Improve infrastructure efficiency

## 10.2 Filtering pipeline

```text
Input checks
      ↓ pass
Filtering model
      ├── likely hard → fallback, error, or abstain
      └── likely easy → run main model
```

The filtering model should run only after deterministic input checks pass. There is no reason to use ML to evaluate an input that is already known to be malformed.

---

# 11. Training a Filtering Model

A filtering model can be trained using the main model’s successes and failures.

## 11.1 Create the labels

Suppose the main classifier predicts labels for a dataset.

For each example:

- Label it `0` if the prediction was correct.
- Label it `1` if the prediction was wrong.

These become the target labels for the filtering model.

## 11.2 Example

```python
from sklearn.ensemble import RandomForestClassifier

def get_filtering_model(classifier, features, labels):
    """
    Train a binary classifier that predicts whether
    the main classifier will make an error.
    """
    predictions = classifier.predict(features)

    # True means the main classifier was wrong.
    is_error = [
        predicted != actual
        for predicted, actual in zip(predictions, labels)
    ]

    filtering_model = RandomForestClassifier()
    filtering_model.fit(features, is_error)

    return filtering_model
```

## 11.3 Data requirement

This approach may not require new data collection.

The team can use:

- Held-out validation data
- Test data
- Historical production examples with known outcomes
- User-corrected predictions

However, care is needed to avoid training and evaluating the filtering model on the same examples.

A stronger workflow is:

1. Train the main model.
2. Run it on held-out examples.
3. Label each example as success or failure.
4. Split those examples again for filtering-model training and evaluation.
5. Evaluate filtering precision, recall, and operational benefit.

---

# 12. What a Filtering Model Should Detect

The chapter identifies several useful categories.

## 12.1 Qualitatively different inputs

Inputs may differ from the data on which the main model performs well.

Examples:

- Unusual language
- Very dark images
- New document formats
- Extreme transaction sizes
- Unexpected device signals

## 12.2 Known hard examples

Some inputs may resemble examples the main model repeatedly misclassified during validation.

## 12.3 Adversarial inputs

Some users or systems may deliberately construct inputs intended to fool the model.

A filtering model can sometimes detect patterns associated with such attempts.

---

# 13. Filtering-Model Requirements

A useful filtering model should satisfy two major criteria.

## 13.1 It should be fast

Its purpose is partly to reduce computation. A filtering model that is nearly as expensive as the main model provides little operational benefit.

## 13.2 It should block enough difficult cases

It need not catch every failure. It must catch enough to justify running it on every request.

## 13.3 Efficiency formula

Let:

- \(m\) = average execution time of the main model
- \(f\) = execution time of the filtering model
- \(b\) = proportion of inputs blocked by the filtering model

Without filtering:

\[
T_{\text{main only}} = m
\]

With filtering:

\[
T_{\text{filtered}} = f + (1-b)m
\]

Filtering is faster when:

\[
f + (1-b)m < m
\]

Rearranging:

\[
b > \frac{f}{m}
\]

### Interpretation

The blocked proportion must exceed the filter-to-main execution-time ratio.

### Example

If the filtering model is 20 times faster than the main model:

\[
\frac{f}{m} = \frac{1}{20} = 0.05
\]

It must block more than 5% of inputs to reduce average inference time.

## 13.4 Precision also matters

A filter could improve speed by blocking many inputs, but that would be harmful if it blocks inputs the main model would have handled correctly.

Therefore, monitor:

- **Filtering precision:** Of blocked inputs, how many were genuinely hard?
- **Filtering recall:** Of genuinely hard inputs, how many were blocked?
- **False-block rate:** How often are valid inputs unnecessarily denied?
- **Compute savings**
- **User impact**

The correct operating threshold depends on the cost of:

- Running the main model
- Showing a bad prediction
- Blocking a good prediction
- Asking the user to try again

---

# 14. Auditing the Filtering Model

A filtering model can hide its own mistakes because blocked examples never reach the main model.

To evaluate it, allow a small random sample of blocked inputs to continue through the main model.

This is sometimes called an exploration sample or holdout stream.

The team can then determine:

- Whether the blocked examples were truly difficult
- Whether the filter has become overly aggressive
- Whether production data has changed
- Whether the main model has improved on previously hard cases

This provides an unbiased window into what the filter is preventing.

---

# 15. Smart Reply Example

Google’s Smart Reply system uses a preliminary model—described as a **triggering model**—to decide whether the main response-suggestion model should run.

Only a minority of emails are suitable for automatic reply suggestions. Filtering unsuitable emails:

- Prevents irrelevant suggestions
- Reduces unnecessary main-model inference
- Lowers infrastructure requirements substantially

This illustrates that a filtering model can improve both:

1. **Prediction quality**
2. **Operational efficiency**

---

# 16. Engineer for Performance

Robustness also requires maintaining acceptable speed and reliability as usage increases.

A production system must support:

- More users
- More requests
- Larger datasets
- Frequent model updates
- More complicated pipelines
- Expensive models
- Multiple model versions

The chapter discusses:

1. Horizontal scaling
2. Separating application and inference infrastructure
3. Caching
4. Model and data life-cycle management
5. Reproducible training pipelines

---

# 17. Scaling to Multiple Users

Many software systems are **horizontally scalable**.

Horizontal scaling means adding more machines or service instances to handle more requests.

```text
More traffic
     ↓
Launch more serving instances
     ↓
Distribute requests across them
```

ML services can often scale similarly.

## 17.1 Challenges

The team may need:

- Load balancing
- Autoscaling
- Request queues
- Timeouts
- Rate limiting
- Health checks
- Replicated model artifacts
- Consistent preprocessing code
- Centralized logging
- Failure recovery

## 17.2 GPU serving

Deep learning models may require GPUs to meet latency requirements.

GPU-enabled machines are often much more expensive than ordinary compute instances.

The chapter recommends separating:

- General application logic
- GPU-based model inference

### Architecture

```text
Client
   ↓
Application server
   ↓
GPU inference service
   ↓
Application server
   ↓
Client
```

### Benefits

- Cheap application servers can scale web logic.
- Expensive GPU machines perform only inference.
- GPU utilization may improve.
- The team avoids running ordinary application work on premium hardware.

### Cost

This design introduces communication overhead between services.

The team must measure whether the added network or serialization latency remains acceptable.

---

# 18. Caching for Machine Learning

**Caching** stores the result of an expensive operation so repeated calls can return the stored result rather than recomputing it.

Caching is useful when:

- The same inputs occur repeatedly
- Inference is expensive
- Stored results remain valid
- Cache lookup is faster than recomputation

---

# 19. Caching Inference Results

A **least recently used (LRU) cache** stores a limited number of recent input-output pairs.

When the cache reaches its capacity, it discards the least recently used entry.

## Workflow

```text
New request
      ↓
Is input in cache?
      ├── Yes → return cached output
      └── No  → run model → store output → return output
```

## Python example

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def run_model(question_data):
    # Expensive model inference
    pass
```

## 19.1 When direct inference caching works

It works well when identical requests are common.

Examples:

- Repeated lookups of the same product
- Frequently requested standard documents
- Shared image URLs
- Popular queries
- Repeated scoring of unchanged records

## 19.2 When it does not work

It is less useful when every input is unique.

Example:

- Users upload different photographs of animal paw prints

Even if two photos show the same animal, the raw images are unlikely to be byte-for-byte identical, so an exact-input cache will rarely hit.

---

# 20. Cache Only Side-Effect-Free Functions

A function has a **side effect** when it changes something outside its return value.

Examples:

- Writing to a database
- Sending a notification
- Updating a counter
- Creating an audit log
- Charging a customer

Suppose `run_model()` both predicts and saves every request to a database.

If it is cached, repeated inputs may return a stored result without executing the database write. That may violate the intended behavior.

Therefore:

> Cache pure or side-effect-free computations whenever possible.

A better architecture separates responsibilities:

```python
prediction = cached_model_inference(features)
store_audit_record(features, prediction)
```

Only the deterministic inference function is cached.

---

# 21. Cache Value Depends on Cost

Caching is beneficial only if cache retrieval is faster than recomputation.

Factors include:

- Model inference time
- Feature retrieval time
- Preprocessing time
- Cache location
- Serialization cost
- Network latency
- Cache hit rate
- Cache size
- Data freshness requirements

Types of cache storage include:

- In-memory cache
- Local disk cache
- Distributed cache
- Database-backed cache

An in-memory cache is fast but limited and local to one process. A distributed cache is shareable but introduces network overhead.

---

# 22. Caching by Indexing and Precomputation

Even when user inputs are unique, some parts of the pipeline may be known in advance.

Search and recommendation systems often have a fixed or slowly changing catalog:

- Products
- Documents
- Listings
- Videos
- Images
- Articles

The system can precompute representations for these items.

## 22.1 Embedding-based search workflow

### Offline phase

```text
Catalog items
      ↓
Embedding model
      ↓
Stored vector embeddings
```

### Online phase

```text
User query
      ↓
Query embedding
      ↓
Similarity search against stored item embeddings
      ↓
Return nearest items
```

Only the user query is embedded at inference time. Catalog embeddings are reused.

## 22.2 Benefits

- Most expensive computation happens in advance.
- Online latency decreases.
- Large catalogs can be searched efficiently.
- The approach scales well with vector indexes.
- The same stored embeddings can support many requests.

This is a form of caching even though the exact user request is not cached.

---

# 23. Cache Management Risks

Caching improves performance but introduces complexity.

## 23.1 Cache size

The cache size becomes an operational tuning parameter.

A larger cache may:

- Increase hit rate
- Consume more memory
- Increase management cost

A smaller cache may:

- Use less memory
- Evict useful results too soon

## 23.2 Staleness

When any relevant component changes, old cached results may become invalid.

Possible invalidation triggers:

- New model version
- New preprocessing logic
- Updated feature data
- Changed business rules
- Updated catalog
- Changed user state

## 23.3 Cache invalidation strategy

Possible methods:

- Clear the entire cache
- Version cache keys
- Apply expiration times
- Invalidate affected entries
- Maintain separate caches per model version

A robust cache key might include:

```text
model_version + pipeline_version + data_version + normalized_input
```

This prevents one model version from accidentally serving another model’s results.

---

# 24. Model and Data Life-Cycle Management

Production models often require regular updates.

A trained model is commonly saved as a binary artifact containing:

- Model type or architecture
- Learned parameters
- Configuration
- Possibly preprocessing metadata

A production application loads the model into memory and uses it for predictions.

Replacing one model file with another sounds simple, but real production updates involve:

- Version tracking
- Data dependencies
- Pipeline changes
- Deployment safety
- Rollback
- Cache invalidation
- Reproducibility

---

# 25. Reproducibility

When an error occurs, the team must be able to determine exactly what produced the prediction.

This requires preserving:

- The model artifact
- The training dataset or dataset version
- Model hyperparameters
- Preprocessing version
- Postprocessing version
- Application version
- Relevant feature definitions
- Random seeds and environment details

## 25.1 Unique identifiers

Each model-dataset pair should have a unique identifier.

Example:

```text
model_id: editor_classifier_v17
training_data_id: editor_data_2026_07_01
pipeline_version: preprocessing_v5
application_version: api_v12
```

## 25.2 Log every inference

Each prediction log should record enough metadata to reproduce the result.

Possible fields:

- Timestamp
- Request identifier
- Model identifier
- Training-data identifier
- Application version
- Pipeline version
- Input schema version
- Output
- Confidence score
- Fallback path used
- Filter decision
- Latency
- Error status

## 25.3 Why this matters

Without version metadata, a team may know that a bad prediction occurred but be unable to determine:

- Which model produced it
- Which preprocessing steps ran
- Which data created that model
- Whether a deployment was partially complete
- Whether a cache returned an older result

---

# 26. Resilient Model Updates

A new model should ideally be deployed without significant downtime.

A common strategy is to:

1. Launch a new serving instance with the updated model.
2. Send a small amount of traffic to it.
3. Compare performance with the previous version.
4. Increase traffic gradually.
5. Stop or roll back if quality declines.
6. Retire the old version after successful validation.

This resembles **canary deployment**.

## 26.1 Rollback

A deployment system should make it easy to restore the previous model when:

- Error rates increase
- Latency increases
- User feedback declines
- Predictions fail checks
- Resource usage becomes unacceptable
- Business metrics deteriorate

Rollback requires preserving older model and pipeline versions.

## 26.2 Deployment metrics

Monitor during rollout:

- Prediction latency
- Error rate
- Resource use
- Output distributions
- Confidence distributions
- Fallback frequency
- User behavior
- Business outcomes
- Version-specific traffic

---

# 27. Pipeline Flexibility

A model update is often not only a new binary file.

Performance improvements frequently come from:

- New features
- Revised preprocessing
- Different categorical encodings
- New normalization
- Updated postprocessing
- Changed thresholds
- Different output formats
- Revised business rules

This means the application and data pipeline may need to change together with the model.

## 27.1 Version the whole inference path

To reproduce a prediction, track:

```text
Input
  + preprocessing version
  + feature version
  + model version
  + postprocessing version
  + application version
  = reproducible inference
```

A model artifact alone is insufficient.

---

# 28. Reproducible Training Pipelines

The training process should be deterministic and repeatable.

For a fixed combination of:

- Dataset
- Preprocessing
- Features
- Model configuration
- Random seeds
- Environment

the pipeline should produce the same or meaningfully equivalent result.

Challenges include:

- Steps run in the wrong order
- Missing intermediate files
- Partial failures
- Hidden manual operations
- Inconsistent environments
- Different code versions
- Non-deterministic algorithms
- Data changing during the run

---

# 29. Directed Acyclic Graphs

A **directed acyclic graph (DAG)** represents a workflow as nodes and directed dependencies.

- A **node** represents a task or artifact.
- An **edge** represents a dependency.
- **Directed** means the workflow has an order.
- **Acyclic** means the graph does not loop back to an earlier step.

## Example

```text
Raw data
   ↓
Validation
   ↓
Cleaning
   ↓
Feature generation
   ↓
Train/validation split
   ↓
Model training
   ↓
Evaluation
   ↓
Model artifact
```

A more complex pipeline may branch:

```text
                ┌→ Text features ─┐
Raw data → Clean                  ├→ Merge → Train
                └→ Numeric features┘
```

## 29.1 Benefits of DAGs

DAGs make dependencies explicit.

They help teams:

- Run tasks in the correct order
- Retry failed steps
- Reuse completed steps
- Monitor pipeline progress
- Inspect logs
- Version workflow definitions
- Identify where failures occurred
- Schedule retraining
- Improve reproducibility

## 29.2 Tools

The chapter mentions:

- **Apache Airflow**
- **Luigi**

These tools allow teams to define DAGs and monitor execution through dashboards and logs.

## 29.3 When DAGs are worthwhile

For an early prototype, a workflow engine may be unnecessary overhead.

DAGs become more valuable when:

- Models are retrained regularly
- Pipelines contain many steps
- Multiple people contribute
- Failures are expensive
- Data dependencies are complex
- Production reproducibility is required
- Deployment happens frequently

> The more central a model becomes to the product, the more valuable structured workflow orchestration becomes.

---

# 30. Ask Users for Feedback

Automated checks cannot perfectly measure prediction quality.

Users interact directly with model outputs and can provide evidence about whether the outputs are correct or useful.

Feedback can be:

1. **Explicit**
2. **Implicit**

---

# 31. Explicit Feedback

Explicit feedback directly asks users to judge or correct a prediction.

Examples:

- “Was this prediction useful?”
- Thumbs up or thumbs down
- Star ratings
- Correcting a predicted category
- Choosing the right answer
- Editing a generated label
- Reporting an incorrect recommendation

## 31.1 Editable predictions

The Mint budgeting example displays automatically assigned transaction categories as editable fields.

This design:

- Gives users control
- Makes correction easy
- Produces labeled examples
- Reveals where the model fails
- Feels less intrusive than a separate survey

## 31.2 Good explicit-feedback design

Feedback should be:

- Easy to provide
- Integrated into the normal workflow
- Specific enough to be useful
- Optional when possible
- Clear about what is being evaluated
- Stored with the relevant model and pipeline version

---

# 32. Implicit Feedback

Implicit feedback is inferred from user behavior rather than directly requested.

Examples:

- Clicking a recommendation
- Ignoring a recommendation
- Purchasing a recommended item
- Rewriting generated text
- Repeating a search
- Abandoning a workflow
- Accepting an autocomplete suggestion
- Dismissing an alert
- Spending time on a selected result

## 32.1 Weak signals

Implicit behavior is noisy.

A click does not always mean a recommendation was good. A user may click accidentally or out of curiosity.

However, across many users, clicks may still correlate with relevance.

The goal is not to find a perfect signal. It is to find a signal that is useful **in aggregate**.

## 32.2 Weak labels

An action can provide a **weak label**.

For example, adding an “Ask on Stack Overflow” button to the ML Editor would allow the system to observe which suggestions users considered suitable enough to post.

The user is not directly rating the model, but the action provides evidence about output quality.

---

# 33. Risks of Feedback Collection

Feedback systems create additional responsibilities.

## 33.1 Privacy and data collection

The team must decide:

- What behavior to collect
- Whether consent is needed
- How long to retain it
- Who can access it
- How to protect it
- Whether it contains sensitive information

## 33.2 Feedback loops

Model recommendations influence user behavior, and user behavior is then used to retrain the model.

This can reinforce existing patterns.

Example:

1. A recommender shows popular items more often.
2. Users click those items because they are shown more often.
3. The clicks are treated as proof that the items are better.
4. The model promotes them even more.

This can reduce diversity and amplify bias.

## 33.3 Selection bias

Feedback is observed only for outputs users see.

If a filtering model blocks an example, the system may never learn whether the main model could have handled it.

Random exploration and careful experiment design are needed.

---

# 34. Feedback as Monitoring

User feedback can reveal model degradation before formal labels become available.

Signals may include:

- More corrections
- Lower click-through rate
- Increased abandonment
- More complaints
- Higher fallback use
- More repeated attempts
- Lower acceptance rate
- Increased human overrides

These signals do not replace evaluation, but they can serve as early warnings.

Feedback should be tied to:

- Model version
- Application version
- Input cohort
- Time period
- Experiment group
- User context, when ethically and legally appropriate

---

# 35. Stitch Fix Case Study

The chapter includes an interview with Chris Moody, who describes Stitch Fix’s approach to ML deployment.

The central philosophy is:

> Data scientists should be empowered to own the complete model life cycle, supported by reusable platform tooling.

---

# 36. End-to-End Data Scientist Ownership

At Stitch Fix, data scientists may own:

- Ideation
- Prototyping
- Model design
- Debugging
- ETL
- Training
- Sanity checks
- Metric definition
- A/B tests
- Error monitoring
- Log inspection
- Model updates
- Redeployment

This ownership helps align model choices with operational impact.

A data scientist who must support the deployed system has an incentive to choose models that are:

- Understandable
- Reliable
- Testable
- Easy to operate
- Worth their complexity

---

# 37. Role of the Platform Team

The platform team does not build a custom pipeline for every project.

Instead, it creates reusable abstractions and tools that allow data scientists to build and deploy their own systems.

This changes the engineering role from:

```text
Build each individual solution
```

to:

```text
Build a platform that enables many solutions
```

## Benefits

- Engineers spend less time on one-off requests.
- Data scientists move faster.
- Deployment becomes more standardized.
- Monitoring and debugging become more consistent.
- Teams can reuse proven components.
- Ownership boundaries become clearer.

---

# 38. Human-Algorithm Feedback Loops

Stitch Fix emphasizes collaboration between people and algorithms.

A weak interface simply displays the model result.

A stronger interface allows the user to:

- Correct it
- Adjust it
- Add context
- Override it
- Explain why it is wrong
- Improve future predictions

This approach avoids making users feel controlled by the algorithm.

It also produces high-value labels because the human expert is correcting the model as part of normal work.

## Design question

Data scientists should ask:

> How can the model make the user’s job easier while also allowing the user to make the model better?

---

# 39. Internal Deployment Tooling

The interview describes an internal platform that can:

- Accept a modeling pipeline
- Create a Docker container
- Validate function arguments
- Validate return types
- Expose inference as an API
- Deploy it
- Build a monitoring dashboard

This standardization allows data scientists to troubleshoot deployed models directly.

It also encourages robust design because the model owner experiences the consequences of operational complexity.

---

# 40. A/B Testing and Canary Deployment

Stitch Fix data scientists use an internal experimentation service to define and run A/B tests.

After analyzing results:

- The team decides whether evidence is conclusive.
- The data scientist can deploy the new version.

The deployment resembles canary rollout:

1. Deploy the new version to one instance.
2. Observe its performance.
3. Gradually update more instances.
4. Track how many instances run each version.
5. Monitor metrics continuously.
6. Stop or reverse the rollout if problems appear.

This reduces the risk of exposing all users to a faulty model at once.

---

# 41. Integrated Production Pipeline

The chapter’s ideas can be combined into one robust architecture.

```text
Incoming request
      ↓
Schema and type checks
      ↓
Range and distribution checks
      ↓
Filtering model
      ├── blocked → heuristic / alternate model / error
      └── accepted
              ↓
         Cache lookup
          ├── hit → retrieve result
          └── miss
                  ↓
             Primary model
                  ↓
         Confidence assessment
                  ↓
          Output validation
            ├── fail → backup model
            │             ↓
            │       output validation
            │          ├── fail → heuristic/error
            │          └── pass
            └── pass
                  ↓
          Postprocessing
                  ↓
          Return prediction
                  ↓
       Collect feedback and logs
```

Every decision should be logged with version metadata.

---

# 42. Safeguard Checklist

## Input safeguards

- [ ] Confirm required features are present
- [ ] Validate feature types
- [ ] Validate ranges
- [ ] Detect malformed inputs
- [ ] Check schema version
- [ ] Monitor distribution shifts
- [ ] Reject or redirect invalid requests

## Model safeguards

- [ ] Evaluate probability calibration
- [ ] Set abstention thresholds
- [ ] Identify known hard cases
- [ ] Consider a filtering model
- [ ] Measure filter precision and recall
- [ ] Audit a sample of blocked inputs
- [ ] Maintain a backup model or heuristic

## Output safeguards

- [ ] Validate type
- [ ] Validate plausible range
- [ ] Apply business rules
- [ ] Check usefulness
- [ ] Prevent unsafe outputs
- [ ] Validate fallback outputs
- [ ] Return clear errors when necessary

## Performance safeguards

- [ ] Measure end-to-end latency
- [ ] Add horizontal scaling
- [ ] Separate GPU inference where appropriate
- [ ] Use caching when hit rates justify it
- [ ] Cache only side-effect-free functions
- [ ] Precompute catalog representations
- [ ] Version and invalidate caches

## Life-cycle safeguards

- [ ] Archive model artifacts
- [ ] Version datasets
- [ ] Version preprocessing and postprocessing
- [ ] Log model and application versions
- [ ] Support canary deployment
- [ ] Support rollback
- [ ] Use reproducible training workflows
- [ ] Consider DAG orchestration

## Feedback safeguards

- [ ] Make corrections easy
- [ ] Collect explicit feedback
- [ ] Identify useful implicit signals
- [ ] Monitor weak labels in aggregate
- [ ] Protect user privacy
- [ ] Watch for negative feedback loops
- [ ] Connect feedback to model versions

---

# 43. Common Mistakes

## Mistake 1: Trusting any structurally valid prediction

A model can produce an output for nonsense input.

**Correction:** Validate inputs before inference and outputs afterward.

## Mistake 2: Treating tests and production checks as the same

Tests validate expected code behavior. Checks control live inference.

**Correction:** Use both.

## Mistake 3: Relying only on confidence

Models can be confidently wrong, and confidence requires running the model.

**Correction:** Combine calibration, filtering, validation, and feedback.

## Mistake 4: Using a filter without auditing blocked examples

The filter may block useful requests.

**Correction:** Allow a random sample through for evaluation.

## Mistake 5: Caching a function with side effects

Cache hits may skip necessary writes or actions.

**Correction:** Separate pure inference from side-effect operations.

## Mistake 6: Failing to clear or version a cache

Old predictions may remain after a model update.

**Correction:** Use explicit cache invalidation and versioned keys.

## Mistake 7: Versioning only the model file

A prediction also depends on data processing and application logic.

**Correction:** Version the complete inference pipeline.

## Mistake 8: Deploying a new model to all users immediately

A faulty update can affect everyone.

**Correction:** Use staged or canary deployment with rollback.

## Mistake 9: Collecting behavior without considering feedback loops

The model can reinforce its own recommendations.

**Correction:** Use controlled experiments, exploration, and bias analysis.

## Mistake 10: Adding production complexity too early

DAGs, filters, distributed caches, and canary systems may overwhelm a prototype.

**Correction:** Add safeguards proportionate to the model’s importance and risk.

---

# 44. Oral-Exam Ready Summary

> Chapter 10 applies fault-tolerance principles to machine learning. Since every model will eventually fail on some examples, a production ML system should validate inputs, detect difficult cases, check outputs, and provide fallback behavior. Input checks confirm required features, types, and valid values, while output checks prevent implausible or useless predictions from reaching users. Confidence thresholds can support abstention, but a fast filtering model may identify hard examples before expensive inference. Production systems must also scale through horizontal replication, selective GPU services, caching, and precomputed representations. Reproducibility requires versioning the model, training data, preprocessing, postprocessing, and application. DAG tools such as Airflow or Luigi can make complex training workflows repeatable. Finally, explicit and implicit feedback help judge real-world performance, detect degradation, and create new training data. The Stitch Fix example shows the value of reusable platform tooling, end-to-end data scientist ownership, human feedback loops, A/B testing, and gradual canary deployments.

---

# 45. Possible Oral-Exam Questions

## 1. Why must production ML systems assume models will fail?

**Answer:** No model is correct on every example. Production data can be malformed, unfamiliar, shifted, adversarial, or simply difficult, so the surrounding system must detect and mitigate errors.

## 2. What is the difference between an input check and a test?

**Answer:** A test verifies expected code behavior using known inputs, usually during development. An input check runs inside the production pipeline and changes what the system does with a live request.

## 3. What should input checks validate?

**Answer:** Required feature presence, feature types, and reasonable feature values.

## 4. Why are range checks useful but insufficient?

**Answer:** They can reject impossible values, but a plausible value can still be incorrect for the specific case.

## 5. Why keep a heuristic after training an ML model?

**Answer:** It can serve as a fallback when inputs are incomplete, the main model fails, or output validation rejects a prediction.

## 6. Why might a simpler backup model help?

**Answer:** It may make different errors from the primary model, allowing it to correctly handle some examples the complex model misses.

## 7. What is confidence-based abstention?

**Answer:** The system avoids showing predictions when a calibrated confidence score falls below a selected threshold.

## 8. Why is confidence alone insufficient?

**Answer:** Models can be confidently wrong, especially under distribution shift or adversarial input, and confidence is available only after full inference.

## 9. What is a filtering model?

**Answer:** A fast binary classifier that predicts whether the main model is likely to fail on a given input.

## 10. How is a filtering model trained?

**Answer:** Run the main model on labeled data, mark each example according to whether the main model was correct, and train the filter to predict those error labels.

## 11. When does a filtering model reduce average inference time?

**Answer:** When the fraction of blocked examples exceeds the ratio of the filter’s inference time to the main model’s inference time: \(b > f/m\).

## 12. Why should blocked inputs occasionally be allowed through?

**Answer:** To estimate whether the filtering model is wrongly blocking examples and to observe changes in main-model performance.

## 13. What is horizontal scaling?

**Answer:** Adding more serving instances or machines to handle increased request volume.

## 14. Why separate application logic from GPU inference?

**Answer:** Ordinary servers are cheaper. They can handle web logic while expensive GPU instances focus only on model computation.

## 15. When is an LRU cache useful?

**Answer:** When identical inputs occur repeatedly and retrieving a stored result is faster than recomputing it.

## 16. Why should cached functions have no side effects?

**Answer:** A cache hit skips execution, so required actions such as database writes would not occur.

## 17. How can search systems use precomputation?

**Answer:** They can embed catalog items in advance, store the vectors, and embed only the user query during inference.

## 18. Why must caches be invalidated after model updates?

**Answer:** The cache may otherwise return outputs created by an older model or pipeline.

## 19. What must be versioned to reproduce a prediction?

**Answer:** The model, training data, preprocessing, postprocessing, feature definitions, and application version.

## 20. What is a DAG?

**Answer:** A directed acyclic graph that represents pipeline tasks and their dependencies in a fixed, non-circular workflow.

## 21. What is the difference between explicit and implicit feedback?

**Answer:** Explicit feedback directly asks users to evaluate or correct a prediction. Implicit feedback infers quality from user behavior.

## 22. Why is implicit feedback considered weak?

**Answer:** A behavior such as a click may correlate with quality but does not prove that the prediction was correct.

## 23. What is a canary deployment?

**Answer:** A gradual rollout in which a new version initially receives limited traffic while its performance is monitored before wider release.

## 24. What is the main lesson from Stitch Fix?

**Answer:** Reusable platform tools can empower data scientists to own the full model life cycle, while human feedback, experimentation, monitoring, and gradual deployment improve reliability.

---

# 46. Key Terms

| Term | Meaning |
|---|---|
| Fault tolerance | Ability of a system to continue operating when components fail |
| Input check | Live validation that influences inference control flow |
| Output check | Validation that determines whether a prediction should be shown |
| Heuristic | Rule-based method that can serve as a baseline or fallback |
| Abstention | Choosing not to produce or display a model prediction |
| Calibration | Agreement between predicted probabilities and observed correctness |
| Filtering model | Model that predicts whether another model will fail |
| Triggering model | Preliminary model that decides whether a main model should run |
| Horizontal scaling | Adding more machines or service instances |
| GPU inference service | Separate service dedicated to model computation on GPUs |
| Cache | Stored result reused to avoid repeated computation |
| LRU cache | Cache that removes the least recently used entries first |
| Side effect | State change beyond a function’s returned value |
| Embedding | Vector representation used to capture similarity |
| Cache invalidation | Removing or replacing results that are no longer current |
| Model artifact | Saved representation of a trained model |
| Reproducibility | Ability to recreate a model or prediction from recorded inputs and versions |
| Resilience | Ability to continue service and recover from faulty updates |
| Rollback | Restoring a previous model or application version |
| Pipeline version | Identifier for preprocessing, feature, and postprocessing logic |
| DAG | Directed acyclic graph representing task dependencies |
| Explicit feedback | Direct user evaluation or correction |
| Implicit feedback | Behavioral signal used to infer model usefulness |
| Weak label | Imperfect label inferred from indirect evidence |
| Feedback loop | Cycle in which model outputs influence data used to update the model |
| A/B test | Controlled comparison between system variants |
| Canary deployment | Gradual deployment to a small share of traffic before expansion |

---

# 47. Final Takeaways

1. A production ML model should be treated as a component that will sometimes fail.
2. Validate feature presence, types, and values before inference.
3. Distinguish development tests from live production checks.
4. Validate outputs for plausibility, safety, and usefulness.
5. Maintain a fallback hierarchy that can include simpler models, heuristics, or abstention.
6. Calibrated confidence can identify uncertainty but cannot detect every error.
7. Filtering models can block difficult examples before expensive inference.
8. A filter is operationally useful when its compute savings and quality benefits exceed its cost.
9. Horizontal scaling and separated GPU inference can support growing traffic efficiently.
10. Cache repeated work only when results remain valid and functions are side-effect-free.
11. Precompute catalog embeddings or other reusable representations whenever possible.
12. Version and invalidate caches when models, data, or pipelines change.
13. Reproducibility requires tracking far more than the model file.
14. Use staged deployment and rollback to reduce the risk of updates.
15. DAGs help organize, monitor, and reproduce complex training workflows.
16. Explicit and implicit feedback provide evidence about real-world quality.
17. Feedback systems must account for privacy, noise, selection bias, and reinforcing loops.
18. Good platform abstractions allow data scientists to own models from prototype through monitoring.
19. Human correction should be designed as part of the product, not as an afterthought.
20. Production complexity should grow only when the model’s scale, importance, and risk justify it.

---

## One-Sentence Memory Aid

> **Check the input, predict only when appropriate, validate the output, keep a safe fallback, version everything, and learn from how users respond.**
