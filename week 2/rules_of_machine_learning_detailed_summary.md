# Detailed Summary: *Rules of Machine Learning: Best Practices for ML Engineering*

**Author:** Martin Zinkevich  
**Document length:** 24 pages  
**Primary focus:** Practical engineering principles for developing, launching, monitoring, and improving production machine-learning systems.

> **Historical context:** The document was written in 2016 and uses Google products such as Google Plus, Google Play, and YouTube as examples. Some product references are historical, but the engineering principles remain broadly applicable to modern ML systems.

---

## 1. Executive Summary

The article’s central argument is that successful machine-learning products are usually built through **sound engineering, reliable data pipelines, sensible objectives, strong monitoring, and iterative feature development**, rather than through immediate use of sophisticated algorithms.

The recommended progression is:

1. **Determine whether machine learning is needed.**
2. **Instrument metrics before building the model.**
3. **Launch a simple heuristic or simple model first.**
4. **Build and test the full production pipeline.**
5. **Monitor freshness, feature coverage, and silent failures.**
6. **Choose a simple, observable training objective.**
7. **Iterate by adding understandable features.**
8. **Analyze how model changes affect the actual product.**
9. **Prevent and measure training-serving skew.**
10. **When improvement slows, revisit objectives or add fundamentally new information.**

A recurring theme is:

> The model is only one component of the system. Production performance depends on the entire pipeline and on how predictions are translated into product decisions.

---

# 2. Intended Audience and Purpose

The guide is written for readers who already understand basic machine-learning concepts or have worked with a model.

It is not primarily a mathematical treatment of algorithms. Instead, it functions as an **engineering style guide** for machine learning, similar to a programming style guide. Its goal is to help teams avoid recurring production failures and organize their ML development process.

The document is divided into the following broad stages:

| Stage | Main concern |
|---|---|
| Before machine learning | Decide whether ML is appropriate and begin measuring the system. |
| Phase I: First pipeline | Build a simple, trustworthy end-to-end system. |
| Phase II: Feature engineering | Add signals, iterate, and improve the product. |
| Human analysis | Evaluate what changed and identify systematic problems. |
| Training-serving skew | Make training behavior match production behavior. |
| Phase III: Mature systems | Address objective tradeoffs, plateaus, and added complexity. |

---

# 3. Terminology

The article establishes several terms used throughout the guide.

## Instance

The object about which the system makes a prediction.

**Example:** A web page that must be classified as “about cats” or “not about cats.”

## Label

The target answer for a prediction task. A label may be:

- the correct answer supplied in training data, or
- the prediction produced by a trained system.

**Example:** `about_cats = True`.

## Feature

A measurable property of an instance used to make a prediction.

**Example:** Whether a web page contains the word “cat.”

## Feature column

A group of related features.

**Example:** A feature column representing all possible countries in which a user may live.

A single example may activate one or more values within the feature column.

## Example

An instance together with:

- its features, and
- its label.

## Model

A statistical representation of the prediction task. The model is trained on examples and then used to make predictions.

## Metric

Any numerical measurement reported by the system.

A metric may be important even if the model does not directly optimize it.

Examples include:

- click-through rate,
- daily active users,
- revenue,
- average watch time,
- complaint rate.

## Objective

The quantity the learning algorithm directly attempts to optimize.

The objective is usually one metric or a mathematically transformed version of a metric.

## Pipeline

All infrastructure surrounding the learning algorithm, including:

- gathering data,
- creating examples,
- generating features,
- training models,
- validating models,
- exporting models,
- and serving predictions.

The article treats the pipeline as at least as important as the model itself.

---

# 4. Core Philosophy

The article’s high-level engineering approach is:

1. Build a reliable end-to-end pipeline.
2. Start with a reasonable objective.
3. Add common-sense features using simple transformations.
4. Keep the pipeline reliable as the system evolves.

Most early improvements are expected to come from:

- obtaining better data,
- adding useful features,
- fixing infrastructure problems,
- and aligning the objective with product needs.

Complex algorithms should be introduced only after simpler approaches stop producing meaningful gains.

## Why complexity is delayed

Complexity can:

- make debugging harder,
- slow future launches,
- introduce new dependencies,
- obscure the source of performance changes,
- increase training-serving skew,
- and add long-term technical debt.

The document does not reject advanced models. It recommends using them only when their additional cost is justified.

---

# 5. Before Machine Learning

## Rule 1: Do not be afraid to launch without machine learning

Machine learning requires relevant data. A new product may not yet possess enough data to train a useful model.

A simple heuristic can often provide substantial value while also generating the interaction data needed for later ML development.

### Examples

- Rank marketplace applications by installation count or installation rate.
- Block publishers already known to send spam.
- Rank contacts by recency of use.
- Use alphabetical ordering when no behavioral signal exists.
- Use human editorial judgment when the task is small enough.

### Main principle

A simple product that works is preferable to an ML system trained on inadequate or irrelevant data.

A heuristic also establishes:

- a baseline,
- a source of labels,
- initial product behavior,
- and historical data.

---

## Rule 2: Design and implement metrics first

Before defining the ML objective, instrument the current product as broadly as practical.

### Reasons to collect metrics early

1. Historical data cannot be recovered retroactively.
2. Early instrumentation may be easier to approve than later changes.
3. Designing the system around metrics prevents fragile log parsing.
4. Multiple metrics reveal which parts of the product are sensitive to changes.
5. Metrics support experiments and launch decisions.
6. Monitoring future problems becomes easier when baseline behavior is known.

### Experiment infrastructure

The article emphasizes having an experimentation framework that can:

- assign users to treatment and control groups,
- aggregate metrics by experiment,
- and compare versions of the product.

### Important distinction

Collecting many metrics does not mean optimizing all of them directly. Metrics provide situational awareness; the learning algorithm may still optimize one primary objective.

---

## Rule 3: Prefer machine learning over an increasingly complex heuristic

A simple heuristic can be an excellent starting point. A large network of special-case rules becomes difficult to maintain.

Once a team has:

- relevant data,
- a defined task,
- and a working baseline,

a trained model may be easier to update than continually expanding rule-based logic.

### Why complex heuristics become problematic

- Rules interact in unexpected ways.
- Priorities become difficult to reason about.
- Adding one exception may break another.
- Rules are rarely calibrated against one another.
- The system becomes dependent on undocumented historical decisions.

Machine learning can combine many signals within a consistent optimization framework.

---

# 6. ML Phase I: Build the First Pipeline

The first phase prioritizes **infrastructure reliability over model sophistication**.

The team must be able to trust:

- the examples,
- the features,
- the labels,
- the trained artifact,
- and the serving implementation.

---

## Rule 4: Keep the first model simple and get the infrastructure right

The first model often produces a large improvement simply because it replaces a weak or manual baseline.

The initial system must answer three questions:

1. How will examples reach the training algorithm?
2. What counts as a good or bad outcome?
3. How will predictions be integrated into the application?

Predictions may be:

- computed live for every request, or
- generated offline and stored for later retrieval.

### Why simple features help

Simple features make it easier to verify that:

- training receives the intended values,
- the model learns reasonable weights,
- serving receives the same values,
- and the model behaves consistently in both environments.

### Neutral launch

Some teams intentionally launch a first model with little or no expected ML improvement. The goal is to validate the pipeline without confusing infrastructure validation with product optimization.

### Primary output of the first model

The first model creates:

- baseline behavior,
- baseline metrics,
- operational experience,
- and a trustworthy foundation for later experiments.

---

## Rule 5: Test the infrastructure independently of the learning algorithm

Because trained models can behave unpredictably, the deterministic portions of the pipeline should be tested separately.

### Test data entering the learner

Verify:

- expected feature columns are populated,
- values have reasonable distributions,
- labels are present,
- missingness is understood,
- examples can be inspected manually where privacy permits,
- and statistics match trusted upstream sources.

### Test the trained model leaving the learner

The same fixed model and the same example should produce the same result in:

- the training environment, and
- the serving environment.

### Useful test strategy

Temporarily replace the learned model with a fixed model. This isolates:

- serialization,
- feature generation,
- loading,
- scoring,
- and serving logic

from the variability introduced by training.

---

## Rule 6: Be careful about dropped data when copying pipelines

Reusing an existing pipeline can silently preserve assumptions that do not apply to the new task.

### Examples of dangerous inherited behavior

- A feed-ranking pipeline drops old posts because freshness is important, but the copied pipeline needs historical posts.
- Logging records only content shown to users, eliminating all unshown negative examples.
- Data from several product surfaces is combined without a feature identifying its source.

### Main lesson

Whenever a pipeline is copied, audit:

- filters,
- joins,
- sampling,
- deduplication,
- logging,
- time windows,
- missing-value handling,
- and source identifiers.

Code reuse is valuable only when inherited assumptions are made explicit.

---

## Rule 7: Turn heuristics into features or handle them outside the model

Existing heuristics often contain valuable domain knowledge. They should not automatically be discarded when moving to ML.

The article proposes four ways to preserve that information.

### 1. Apply the heuristic before the model

Use this when the rule is authoritative.

**Example:** Immediately block a sender on a trusted blacklist rather than asking the model to relearn the blacklist.

### 2. Use the heuristic’s output as a feature

If a rule generates a relevance score, include the score as a model input.

The model can learn:

- how strongly to use it,
- where it fails,
- and how it interacts with other features.

### 3. Use the heuristic’s raw inputs as separate features

If a rule combines:

- installation count,
- text length,
- and day of week,

provide these values separately to the model.

This allows the learner to determine its own combination.

### 4. Modify the label or objective

If a heuristic captures product quality not represented in the current label, incorporate it into the label.

**Example:** Weight a download outcome by the item’s average rating.

### Caution

Every retained heuristic adds complexity. Use the simplest mechanism that preserves the needed behavior.

---

# 7. Monitoring

A production ML system requires monitoring not only of service availability but also of:

- data freshness,
- feature coverage,
- model quality,
- and distribution changes.

Alerts should be actionable and connected to a dashboard.

---

## Rule 8: Know the freshness requirements

Different models degrade at different rates.

A model may need retraining:

- hourly,
- daily,
- weekly,
- monthly,
- or only after significant product changes.

### Factors affecting freshness

- New items enter the system.
- User interests change.
- advertisers or spammers adapt.
- identifiers appear as features.
- feature definitions change.
- historical signals become stale.

### Operational implication

Monitoring urgency should match the business impact of an outdated model.

A stale model that quickly affects revenue or safety requires stronger alerting than a model whose performance changes slowly.

---

## Rule 9: Detect problems before exporting a model

A failed training job is an internal problem. A bad exported model becomes a user-facing problem.

Before deployment, run automated quality gates such as:

- held-out performance checks,
- AUC thresholds,
- calibration checks,
- feature-coverage checks,
- comparison with the current production model,
- and data-integrity validation.

If the data or model appears suspicious, do not export it.

### Alert severity

- A model that fails validation before deployment may justify an email or ticket.
- A production model causing user-visible harm may require paging and immediate rollback.

Preventing deployment is cheaper than repairing production damage.

---

## Rule 10: Watch for silent failures

ML systems may continue producing plausible output after a feature or data source fails.

This makes failures difficult to detect.

### Examples

- A joined table stops updating.
- Feature coverage falls from 90% to 60%.
- A data feed becomes several months stale.
- A feature’s default value begins appearing more frequently.
- A schema change silently alters a field.

The model may adapt to the broken input, causing gradual performance decay rather than a clear outage.

### Monitoring recommendations

Track:

- last update time,
- feature coverage,
- missing rates,
- value distributions,
- cardinality,
- label rates,
- and manual samples.

The article describes a stale table whose refresh improved installation rate by approximately 2%, illustrating that infrastructure maintenance can outperform model tuning.

---

## Rule 11: Assign owners and documentation to feature columns

Every important feature should have:

- a clear owner,
- a definition,
- a source,
- an expected update schedule,
- a description of why it is useful,
- and known limitations.

This reduces institutional knowledge loss when staff change roles or leave.

### Recommended feature documentation

- feature name,
- data type,
- producing system,
- transformation logic,
- default behavior,
- valid range,
- refresh cadence,
- coverage,
- owner,
- and intended semantic meaning.

---

# 8. Choosing the First Objective

A system may report many metrics, but a learning algorithm often needs one direct optimization target.

The article distinguishes:

- **metrics:** numbers the team observes,
- **objective:** the quantity the model directly optimizes.

---

## Rule 12: Do not overthink the first objective

During the early stages, many product metrics may improve together.

For example, optimizing clicks may also increase:

- session duration,
- engagement,
- or daily activity.

When broad gains are still available, the team does not need a perfect multi-objective formulation.

### Warning sign

If the optimized metric improves but the team repeatedly refuses to launch the model, the objective may not represent the product’s real priorities.

---

## Rule 13: Choose an observable and attributable objective

The best initial objective is connected directly to an action taken by the system.

### Good early objectives

- Was the ranked link clicked?
- Was the recommended item downloaded?
- Was the message forwarded or replied to?
- Was the item rated?
- Was the item marked as spam or offensive?

These outcomes are:

- measurable,
- attributable to an exposure,
- and available at the example level.

### Harder indirect outcomes

- Did the user return the following day?
- How long was the total session?
- Did daily active usage increase?
- Is the user satisfied?
- Is the product improving well-being?
- Is the company healthier?

These may be important launch metrics, but they are difficult to assign to one prediction.

### Use proxies thoughtfully

Observable actions can serve as proxies for harder goals. Human judgment is still required to determine whether the proxy supports the product’s long-term purpose.

---

## Rule 14: Start with an interpretable model

The article recommends models such as:

- linear regression,
- logistic regression,
- Poisson regression.

Their predictions can be interpreted as:

- expected values,
- rates,
- or probabilities.

### Benefits

- easier debugging,
- easier feature-weight inspection,
- simpler calibration analysis,
- and clearer identification of inconsistencies.

### Calibration

A calibrated model’s average prediction should align with the average observed label within relevant groups.

For example, among items assigned an average click probability of 0.20, approximately 20% should be clicked.

Calibration can reveal:

- implementation errors,
- distribution shifts,
- and serving inconsistencies.

### Important qualification

Interpretability is useful during development, but the final decision should be based on product utility rather than the elegance of the statistical model.

---

## Rule 15: Separate quality ranking from spam filtering

Quality ranking and adversarial filtering are different tasks.

### Quality ranking

Assumes content is created in good faith and attempts to order it by usefulness or predicted engagement.

### Spam filtering

Assumes adversaries will deliberately manipulate the system.

Spam signals:

- change quickly,
- may need daily updates,
- rely on reputation and abuse reports,
- and often include hard rules.

### Policy layer

The outputs of quality and spam systems should be combined through a policy layer that can enforce:

- blocking,
- safety rules,
- product-specific thresholds,
- and different levels of aggressiveness by context.

Spam should normally be removed from the quality model’s training data so the quality model learns distinctions among legitimate content.

---

# 9. ML Phase II: Feature Engineering and Iteration

Phase II begins after the team has:

- a functioning end-to-end pipeline,
- unit and system tests,
- reliable metrics,
- and serving infrastructure.

This phase focuses on collecting and combining obvious useful signals. Multiple launches are expected.

---

## Rule 16: Plan to launch and iterate repeatedly

The current model will not be the final model.

New versions commonly result from:

1. adding features,
2. changing regularization,
3. recombining existing signals,
4. or modifying the objective.

### Design for iteration

The pipeline should make it easy to:

- add and remove features,
- run parallel versions,
- rebuild from a clean copy,
- compare model versions,
- and validate correctness.

Do not delay a useful launch because every planned feature is not yet included.

---

## Rule 17: Begin with directly observed features

Directly observed features are usually easier to understand and maintain than learned features produced by:

- clustering systems,
- embeddings,
- factorization,
- deep networks,
- or external models.

### Risks of externally learned features

- The external model optimizes a different objective.
- The feature can become stale.
- Its semantic meaning may change after retraining.
- Failures are harder to trace.
- Dependency ownership may be unclear.

### Risks of complex learned representations

The article emphasizes that non-convex optimization can produce run-to-run variation, complicating the interpretation of experiments.

The recommendation is to establish a strong simple baseline before introducing learned features.

---

## Rule 18: Use content features that generalize across contexts

A new item may have little history within the current product surface but substantial history elsewhere.

Useful cross-context signals include:

- total watches,
- reshares,
- comments,
- ratings,
- co-watches,
- or previous user actions in another context.

### Benefit

These features help solve cold-start problems by providing evidence before an item accumulates local interactions.

### Sequence of development

First determine whether content is broadly useful within the context. Personalization—who likes it more or less—can follow.

---

## Rule 19: Use highly specific features when enough data exists

Large datasets can support millions of simple sparse features.

Examples include:

- document identifiers,
- canonical query identifiers,
- exact query-document combinations,
- and item-specific indicators.

These features may generalize poorly but perform well on frequent queries or common items.

### Conditions

- Overall feature-group coverage should be substantial.
- Regularization should suppress extremely rare or unreliable values.
- The number of learned weights should match the amount of data.

---

## Rule 20: Combine and transform features in understandable ways

The article highlights two common transformations.

## Discretization

Convert a continuous feature into ranges or buckets.

**Example:**

- age below 18,
- age from 18 to 35,
- age above 35.

Quantile-based boundaries are often sufficient. Excessive tuning of cut points is usually unnecessary.

## Feature crosses

Combine values from multiple feature columns.

**Example:**

```text
gender × country
```

This creates interaction features such as:

```text
male_and_Canada
```

### Benefits

Feature crosses allow a linear model to represent nonlinear interactions.

### Risks

Large crosses can:

- create enormous feature spaces,
- require massive datasets,
- and overfit.

Crosses involving three or more high-cardinality fields require especially large amounts of data.

### Text alternatives

Instead of crossing every query token with every document token, consider:

- a dot product or overlap count,
- discretized similarity,
- or intersection features for words present in both.

---

## Rule 21: Match feature complexity to data volume

The article offers a practical relationship:

> The number of reliable feature weights a linear model can learn grows with the number of training examples.

### Small dataset

With approximately 1,000 examples:

- use a small number of engineered features,
- aggregate text similarity,
- and use approaches such as TF-IDF.

### Medium or large dataset

With millions of examples:

- use sparse token intersections,
- feature selection,
- and regularization.

### Very large dataset

With billions of examples:

- use large feature crosses,
- query-token and document-token interactions,
- and millions of parameters.

### Main lesson

A model is not inherently too simple or too complex. Complexity must be judged relative to:

- data quantity,
- data diversity,
- noise,
- and regularization.

---

## Rule 22: Remove unused features

Unused or unsuccessful features create technical debt.

Costs include:

- extra computation,
- additional monitoring,
- unclear dependencies,
- harder debugging,
- and slower experimentation.

### Coverage matters

A feature used by only 8% of users may have limited overall effect.

However, low coverage does not automatically make a feature useless. A feature covering 1% of examples may still be valuable if it identifies a highly important subgroup.

Evaluate both:

- coverage, and
- conditional predictive value.

---

# 10. Human Analysis of the System

Before moving to more sophisticated methods, teams should analyze how models differ and where they fail.

This part is less algorithmic and more diagnostic.

---

## Rule 23: Remember that the development team is not the typical user

Internal evaluation is useful but biased.

Engineers may:

- know how the model works,
- focus on intended changes,
- prefer technically interesting behavior,
- or be emotionally invested in the result.

### Better feedback sources

- live A/B tests,
- external raters,
- usability studies,
- crowdsourced labels,
- representative user personas,
- and observation of real users.

### Cost perspective

A meeting involving many engineers can cost more than a large quantity of external human evaluation.

Use expert engineering time where it adds unique value.

---

## Rule 24: Measure how much the new model changes results

Before running a live experiment, quantify the difference between the candidate and production systems.

For ranking systems, compare:

- result-set overlap,
- symmetric difference,
- position-weighted changes,
- and queries with the largest ranking changes.

### Interpretation

- Very small changes are unlikely to produce major product effects.
- Very large changes deserve careful inspection.
- The system should be deterministic enough that a model compared with itself produces nearly zero difference.

This “delta analysis” helps determine what the model is actually changing.

---

## Rule 25: Product utility matters more than predictive score

A model may improve a statistical metric such as:

- log loss,
- likelihood,
- or pointwise prediction error

while making the actual product worse.

### Examples

- A click-probability model is used to rank results; ranking quality matters more than raw probability accuracy.
- A spam-probability model is thresholded; precision and recall around the threshold matter more than average log loss.

### Main principle

Evaluate the decision made with the prediction, not only the prediction itself.

Repeated disagreement between model loss and product performance indicates that the objective should be reconsidered.

---

## Rule 26: Look for patterns in errors and create features

A model error identifies a case where the current representation cannot produce the desired decision.

### Error-analysis workflow

1. Collect false positives, false negatives, or ranking reversals.
2. Group them by common traits.
3. Identify missing signals.
4. create general features that capture those traits.
5. retrain and verify that the errors improve.

### Example

If long posts are systematically demoted, add post-length features.

Instead of choosing one arbitrary definition of “long,” create several length buckets and let the model learn the appropriate relationship.

### Important limitation

A new feature will not correct behavior that the objective does not classify as an error.

If users click a low-quality joke application, a click-optimized model does not view its high rank as a mistake. The objective or label must change.

---

## Rule 27: Quantify undesirable behavior

Complaints such as “too many joke applications appear” are not actionable until converted into measurements.

Possible steps:

- have raters label joke applications,
- calculate their frequency in top results,
- define a quality metric,
- add a feature,
- create a constraint,
- or modify the objective.

### Guiding principle

> Measure first, optimize second.

Once a concern is numerical, the team can evaluate whether a change actually improves it.

---

## Rule 28: Similar short-term behavior may hide different long-term behavior

Two systems can appear equivalent in:

- offline evaluation,
- side-by-side comparison,
- and short A/B tests

while producing very different data over time.

### Example

A ranking model that memorizes each exact query-document pair may match current behavior but cannot promote new documents because they have no historical interactions.

### Long-term issue

The deployed model changes:

- what users see,
- what users click,
- and therefore what future training data contains.

This makes long-term evaluation difficult. The most accurate evaluation may require training only on data collected while the candidate policy was active.

---

# 11. Training-Serving Skew

Training-serving skew is a mismatch between model behavior during development and production.

The article identifies three main causes:

1. Training and serving transform data differently.
2. Data changes between training and serving.
3. The model affects the data it later learns from.

Because skew may not produce an obvious system failure, it must be measured directly.

---

## Rule 29: Log serving-time features for future training

The strongest way to ensure consistency is to store the exact features used when the model made a production prediction.

These logged features can later be joined with outcomes and used for training.

### Benefits

- training sees what serving actually used,
- online feature generation is audited,
- joins and defaults are preserved,
- and training-serving differences are easier to diagnose.

Even logging a sample of traffic can provide valuable consistency checks.

---

## Rule 30: Importance-weight sampled data

When the full dataset is too large, do not arbitrarily discard large groups of files or records.

Instead, sample examples probabilistically and assign a weight equal to the inverse sampling probability.

### Example

If an example is kept with probability 0.30:

\[
\text{importance weight} = \frac{1}{0.30} = \frac{10}{3}
\]

This allows the sampled dataset to approximate the original distribution.

### Why arbitrary dropping is dangerous

It can distort:

- label prevalence,
- calibration,
- user distribution,
- time periods,
- and rare outcomes.

---

## Rule 31: Joined feature tables can change between training and serving

Suppose a model joins a document ID to a table containing:

- comment counts,
- click counts,
- or other aggregate values.

If the table changes after training, the same document may produce different features during serving.

### Mitigations

- log serving-time features,
- use timestamped snapshots,
- version feature tables,
- or reconstruct features “as of” the prediction time.

A slowly changing table reduces but does not eliminate this risk.

---

## Rule 32: Reuse code between training and serving

Training is commonly batch-oriented, while serving is request-oriented. The systems cannot always be identical, but shared transformations reduce divergence.

### Recommended pattern

1. Gather raw data using environment-specific methods.
2. store it in a common intermediate object.
3. apply one shared transformation from that object into model features.

### Avoid

Using different programming languages for training and serving when it prevents sharing feature-generation logic.

Duplicated implementations inevitably drift.

---

## Rule 33: Evaluate on later data

A model trained through January 5 should be evaluated on January 6 and later.

A random split from the same time window may underestimate production degradation.

### Why temporal testing matters

- user behavior changes,
- inventory changes,
- trends change,
- feature values drift,
- and labels mature over time.

The model may perform somewhat worse on future data, but a major drop suggests unstable or time-sensitive features.

---

## Rule 34: Accept a small short-term cost to obtain clean filtering data

Filtering systems hide negative examples from users. This causes selection bias because user feedback is observed only on examples the model allowed through.

### Proposed solution

Randomly exempt a small fraction of traffic from filtering.

For example:

- mark 1% of examples as held out,
- show all held-out examples,
- gather unbiased user feedback,
- and use those examples for training and evaluation.

### Tradeoff

The system temporarily allows a small amount of undesirable content, but it gains cleaner data.

Even tiny samples may be enough to estimate performance accurately at large scale.

---

## Rule 35: Ranking systems have inherent feedback skew

Changing the ranking changes which items receive exposure, which changes future interaction data.

A popular item may appear strong simply because the current system repeatedly shows it.

### Suggested strategies

- regularize broad features differently from query-specific features,
- favor positive evidence over negative assumptions,
- and limit document-only popularity features when they cause irrelevant items to appear everywhere.

### Example

A highly downloaded game may receive clicks for a “bird watching app” query, but it does not satisfy the user’s intent.

Optimizing immediate downloads may damage relevance and long-term satisfaction.

---

## Rule 36: Avoid feedback loops from position features

Items in higher positions receive more interactions because of their position.

If the model learns from this without correction, it may conclude that top-ranked items are intrinsically superior.

### Problem

During training, position is known. During candidate scoring, the final position has not yet been assigned.

This creates an asymmetry.

### Recommended structure

Separate:

- a function of position, and
- a function of item and user features.

Do not create crosses between position and document features if those interactions cannot be reproduced consistently at serving time.

---

## Rule 37: Measure training-serving skew explicitly

The article divides skew into three comparisons.

### 1. Training versus held-out data

This reflects generalization and possible overfitting.

A difference is expected.

### 2. Held-out versus next-day data

This reflects temporal shift.

Large drops may indicate time-sensitive features or unstable behavior.

### 3. Next-day versus live serving

The same model and same example should produce the same score.

A difference here usually indicates an engineering error.

### Practical dashboard

Track performance and feature statistics across all three stages rather than reporting only one offline metric.

---

# 12. ML Phase III: Mature Systems and Slower Growth

Phase III begins when:

- monthly improvements shrink,
- metrics begin trading off,
- easy features have been exhausted,
- and launches become harder to justify.

At this stage, the main constraints may be:

- objective alignment,
- new information sources,
- or product policy,

rather than model tuning.

The author notes that this stage is less standardized and requires teams to find context-specific solutions.

---

## Rule 38: Do not add features when the objective is the problem

If the model successfully optimizes its objective but the product still behaves undesirably, adding features may not help.

### Example

The model optimizes clicks or downloads, but launch decisions also depend on human quality ratings.

If the undesirable behavior is not represented in the objective, the model has no reason to correct it.

### Required decision

Change:

- the objective,
- the label,
- the policy layer,
- or the product goal.

Feature engineering cannot resolve a fundamental misalignment.

---

## Rule 39: Launch decisions represent long-term product goals

A team may reject a model even when it improves the optimized metric.

### Example

A candidate model:

- reduces logistic loss,
- increases installation rate,
- but decreases daily active users by 5%.

The model may be statistically better while the overall product is worse.

### Multiple launch metrics

Teams may care about:

- daily active users,
- 30-day active users,
- engagement,
- revenue,
- advertiser return,
- complaints,
- retention,
- and long-term partner health.

These metrics are themselves proxies for deeper goals such as:

- satisfying users,
- maintaining a healthy ecosystem,
- growing the product,
- and sustaining the company.

### Status quo and risk

The article presents two hypothetical systems:

| Experiment | Daily active users | Revenue per day |
|---|---:|---:|
| A | 1 million | $4 million |
| B | 2 million | $2 million |

A team running A may hesitate to move to B, while a team running B may hesitate to move to A. This apparent inconsistency reflects uncertainty and risk. Each metric protects against a different failure mode.

### Multi-objective learning

Constraints and weighted combinations can help, but no mathematical objective fully captures a product’s five-year health.

Human launch judgment remains necessary.

---

## Rule 40: Keep ensembles simple

A unified model using raw features is usually easiest to debug.

Ensembles may improve performance, but their structure should remain clear.

### Recommended architecture

Separate models into:

- **base models**, which consume raw features, and
- **ensemble models**, which consume only outputs of base models.

A model should not simultaneously be a complicated base model and a complicated ensemble.

### Desired ensemble properties

- monotonicity,
- calibrated or interpretable base scores,
- predictable behavior when one component changes,
- and limited stacking depth.

For example, increasing a base model’s predicted probability should not decrease the ensemble probability unless there is a clearly justified reason.

---

## Rule 41: When performance plateaus, add fundamentally new information

Small variations on existing features eventually produce diminishing returns.

At that point, consider new data sources such as:

- short- and long-term user history,
- cross-product activity,
- knowledge graphs,
- entities,
- richer content representations,
- or deep learning.

### Important qualification

New information often requires new infrastructure and may deliver smaller gains at higher cost.

Evaluate return on investment, latency, ownership, and technical debt.

---

## Rule 42: Popularity is not the same as diversity, personalization, or relevance

Metrics such as:

- clicks,
- watch time,
- reshares,
- ratings,
- and downloads

often measure popularity.

Popularity can dominate features intended to promote:

- diversity,
- personalization,
- and query relevance.

### Why this occurs

The most popular content is often a strong short-term predictor for many users.

Features representing individual preferences or result diversity may receive less weight than expected.

### Options

- use post-processing to enforce diversity,
- introduce explicit constraints,
- revise the objective,
- or evaluate longer-term metrics.

If diversity improves retention or satisfaction, that evidence can justify treating it as a separate product goal.

---

## Rule 43: Social connections transfer across products better than interests

A user’s close relationships may remain stable across applications.

Their content interests may vary by product context.

### Implication

A friendship or relationship-strength model may transfer successfully between products.

A personalization model based on content preferences may not.

### Possible alternatives

- use raw cross-product behavior rather than a transferred preference score,
- use the presence of activity on another product as a feature,
- and validate transfer assumptions rather than treating them as universal.

---

# 13. Related Work and Appendix

The document recommends additional resources on:

- introductory applied machine learning,
- probabilistic machine learning,
- analysis of large complex datasets,
- deep learning,
- technical debt in ML systems,
- and TensorFlow.

The appendix briefly explains the Google products used in the examples.

## YouTube

- **Watch Next:** ranks videos to show after the current video.
- **Home Page:** ranks recommendations for users browsing the home page.

## Google Play

Uses ML for:

- search,
- personalized home-page recommendations,
- and “Users Also Installed” recommendations.

## Google Plus

Used ML for:

- stream ranking,
- trending or “What’s Hot” ranking,
- and people recommendations.

---

# 14. Major Themes Across the 43 Rules

## 14.1 Infrastructure before sophistication

A model cannot compensate for:

- missing examples,
- broken joins,
- stale tables,
- inconsistent features,
- or deployment errors.

## 14.2 Metrics before optimization

Measure broadly before selecting one objective.

Metrics provide evidence for:

- experiments,
- alerts,
- debugging,
- and launch decisions.

## 14.3 Simple systems accelerate learning

A simple first model makes it easier to identify whether problems come from:

- the data,
- the objective,
- the features,
- the model,
- or the product.

## 14.4 Feature engineering is initially more valuable than model complexity

During early growth, understandable features often produce larger gains than sophisticated algorithms.

## 14.5 The objective is not the product

An optimized objective is only a proxy.

The final decision depends on:

- multiple metrics,
- human judgment,
- policy,
- safety,
- and long-term strategy.

## 14.6 Production data is affected by the model

Ranking and filtering systems change what users see. This changes future labels and creates feedback loops.

## 14.7 Training and serving must be treated as one system

Shared code, serving-time logs, temporal evaluation, and explicit skew measurements are essential.

## 14.8 Mature systems require new information or new goals

Once incremental features stop working, the team must either:

- find a fundamentally new signal,
- or revise what the system is trying to optimize.

---

# 15. Practical End-to-End Checklist

## Before building a model

- Confirm that ML is necessary.
- launch a basic heuristic when appropriate.
- instrument product and business metrics.
- establish an experimentation framework.
- begin collecting historical data.

## First pipeline

- define one example and one label.
- use a simple interpretable model.
- build training and serving infrastructure.
- test feature generation independently.
- validate a fixed model in both environments.
- audit copied pipelines for dropped data.
- preserve useful heuristics.

## Monitoring

- define freshness requirements.
- set model-export quality gates.
- monitor data age and feature coverage.
- alert on missingness and distribution changes.
- assign owners to feature sources.
- document feature semantics.

## Objective design

- start with a direct attributable behavior.
- use indirect outcomes as launch metrics.
- retain a policy layer for non-ML constraints.
- revise the objective if offline gains repeatedly fail launch review.

## Feature engineering

- design for repeated launches.
- begin with observed features.
- use cross-context content signals.
- match model complexity to data size.
- use discretization and feature crosses carefully.
- remove unsuccessful features.

## Evaluation

- compare the candidate with production.
- inspect the largest behavioral changes.
- evaluate the final product decision.
- analyze error patterns.
- quantify qualitative complaints.
- consider long-term feedback effects.

## Training-serving consistency

- log serving-time feature values.
- use importance weighting for sampled examples.
- version or snapshot joined tables.
- reuse feature code.
- evaluate on future time periods.
- gather unbiased held-out traffic for filters.
- correct for ranking and position effects.
- monitor each source of skew.

## Mature systems

- determine whether the objective is misaligned.
- use multiple metrics in launch decisions.
- keep ensembles shallow and interpretable.
- seek qualitatively new information.
- distinguish popularity from relevance and diversity.
- validate cross-product transfer assumptions.

---

# 16. Common Failure Modes Highlighted by the Article

| Failure mode | Why it happens | Recommended response |
|---|---|---|
| Building ML before data exists | The product has no relevant historical examples. | Launch a heuristic and collect data. |
| Optimizing an uninstrumented product | Important historical metrics are unavailable. | Add metrics before formalizing the objective. |
| Complex rule system | Heuristics accumulate conflicting exceptions. | Move to ML once a useful dataset exists. |
| Broken pipeline mistaken for model weakness | Feature or serving code is incorrect. | Test infrastructure independently. |
| Copied pipeline drops useful data | Old assumptions remain hidden. | Audit every filter and join. |
| Stale feature source | The model adapts gradually, hiding the failure. | Monitor freshness and coverage. |
| Statistical metric improves but product worsens | The objective does not match the decision. | Evaluate utility and revise the objective. |
| New feature has no effect | The objective does not treat the behavior as an error. | Change labels, policy, or objective. |
| Randomly sampled split looks strong | Future data differs from historical data. | Use temporal validation. |
| Training and serving scores disagree | Transformations or tables differ. | Share code and log serving features. |
| Ranking reinforces popularity | Exposure creates future labels. | Address feedback loops and relevance. |
| Personalization features underperform | Popularity dominates short-term objectives. | Use constraints or longer-term metrics. |
| Mature model stops improving | Existing signals are exhausted. | Add a new information source or rethink goals. |

---

# 17. Important Conceptual Distinctions

## Metric versus objective

- **Metric:** Any measured quantity.
- **Objective:** The quantity directly optimized by the model.

The product may use many metrics while the model uses one objective.

## Prediction quality versus decision quality

A model can predict probabilities more accurately but produce a worse ranking or filtering decision.

Evaluate the downstream action.

## Offline performance versus production performance

Offline results may not account for:

- changing inventory,
- selection bias,
- exposure effects,
- latency,
- policy,
- or future user behavior.

## Feature freshness versus model freshness

A recent model using stale feature tables may still behave poorly.

Both artifacts and input data require monitoring.

## Popularity versus relevance

A popular result may attract clicks without satisfying the user’s specific intent.

## Short-term versus long-term behavior

Two models may have the same immediate metrics but generate different future datasets and product trajectories.

---

# 18. Exam-Style Summary

*Rules of Machine Learning* argues that production ML should be approached primarily as an engineering discipline. Teams should not begin with advanced algorithms. They should first determine whether ML is needed, instrument metrics, establish a simple heuristic baseline, and build a reliable end-to-end pipeline.

The first model should be simple and interpretable so that engineers can verify data flow, feature generation, training, model export, and serving. Existing heuristics should either remain as policy rules or be converted into features. Production monitoring must include model freshness, feature coverage, data freshness, and silent failures.

The initial objective should be a directly observable user behavior, such as a click or download. Broader outcomes such as satisfaction and retention should be monitored as product metrics and used in launch decisions. The objective is only a proxy for product value.

Once the pipeline works, teams should iterate rapidly by adding understandable features. Feature complexity should grow with dataset size. Model comparison should focus on actual behavioral changes and downstream utility, not only predictive loss. Error analysis should guide feature development, while qualitative complaints should be converted into measurable quantities.

Training-serving skew is a central production risk. Teams should reuse feature code, log serving-time features, use temporal evaluation, importance-weight sampled data, version feature tables, and explicitly compare training, next-day, and live behavior. Ranking and filtering systems require special care because their predictions affect which future labels are observed.

When a mature system plateaus, the limiting factor may be objective alignment rather than missing features. Launch decisions depend on several metrics and human judgment. Further improvement may require qualitatively new information, carefully designed ensembles, explicit diversity or relevance policies, or a revised optimization target.

---

# 19. Condensed Takeaways

1. **Do not use ML merely because ML is available.**
2. **Instrument the product before choosing an objective.**
3. **Use a simple baseline to generate data and establish behavior.**
4. **Treat the pipeline as a first-class engineering system.**
5. **Test feature and serving infrastructure independently.**
6. **Monitor data, not only model metrics.**
7. **Choose an objective that is observable and attributable.**
8. **Use interpretable models to establish a trustworthy baseline.**
9. **Separate adversarial filtering from quality ranking.**
10. **Expect continuous iteration rather than one final model.**
11. **Match feature complexity to dataset size.**
12. **Analyze product changes, not only loss functions.**
13. **Turn subjective complaints into measurable quantities.**
14. **Account for feedback loops and long-term effects.**
15. **Log serving features and measure training-serving skew.**
16. **Use future data for realistic evaluation.**
17. **Recognize that popularity can overpower relevance and personalization.**
18. **When gains plateau, seek new information or rethink the objective.**
19. **Use multiple metrics and human judgment for launch decisions.**
20. **Prefer maintainable systems that can improve repeatedly.**
