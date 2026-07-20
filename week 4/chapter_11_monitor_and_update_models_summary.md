# Chapter 11 Study Guide: Monitor and Update Models

**Book:** *Building Machine Learning Powered Applications*  
**Chapter focus:** Monitoring deployed ML systems, detecting degradation, and safely evaluating and releasing new model versions

---

## 1. Chapter Overview

Deploying a model is not the end of the machine learning life cycle. Once a model is in production, the team must continually observe whether it remains:

- Accurate
- Useful
- Fast
- Reliable
- Safe
- Current
- Aligned with product goals

A deployed model operates in a changing environment. User behavior, available content, input distributions, business conditions, and adversarial strategies may all change over time. As a result, performance measured before deployment may not accurately describe performance months—or even days—later.

Chapter 11 answers three central questions:

1. **Why should models be monitored?**
2. **What should be monitored?**
3. **What actions should monitoring trigger?**

The chapter also explains how to compare model versions through:

- Offline evaluation
- Shadow deployment
- Live production experiments
- A/B testing
- Multiarmed bandits

> **Central lesson:** Monitoring is valuable only when it is connected to a decision or action, such as investigating an anomaly, retraining a stale model, rolling back a bad release, or promoting a better model.

---

# 2. Why Monitoring Matters

The goal of monitoring is to track the health of a production system.

For a normal software service, health includes:

- Response time
- Error rate
- Availability
- CPU and memory use
- Request volume
- Resource capacity

For an ML system, these are still important, but they are not sufficient. A model can return responses quickly, produce no software errors, and still give poor predictions.

ML monitoring must also address:

- Prediction quality
- Data freshness
- Feature drift
- Output drift
- Business impact
- User response
- Abuse or attacks
- Model-version performance
- Differences across user segments

A healthy ML service is therefore not merely one that is “up.” It is one that continues to provide value.

---

# 3. Monitoring Can Trigger Model Refreshes

Many deployed models become stale.

A model may become stale because:

- User preferences change
- Language evolves
- New products are added
- Old products disappear
- Economic conditions change
- Fraud strategies change
- Seasonal behavior changes
- Data collection processes change
- Policy or business rules change

A retraining schedule can be fixed, such as weekly or monthly, but monitoring allows retraining to be driven by actual model health.

## 3.1 Threshold-based retraining

Suppose a recommendation model uses implicit user feedback—such as clicks—to estimate performance.

The team can:

1. Continuously calculate a performance metric.
2. Define a minimum acceptable threshold.
3. Trigger retraining when the metric drops below the threshold.
4. Evaluate the candidate model.
5. Deploy it only if it is better.

```text
Monitor performance
        ↓
Metric remains acceptable?
   ├── Yes → continue serving
   └── No  → investigate and retrain
                        ↓
              validate candidate model
                        ↓
              deploy or reject candidate
```

## 3.2 Refresh rate is a product decision

Retraining more often is not automatically better.

Frequent retraining can create:

- Higher compute cost
- Operational burden
- More deployment risk
- Increased model instability
- Greater chance of learning from noisy short-term behavior

Monitoring helps determine when a refresh is justified instead of relying only on the calendar.

---

# 4. Monitoring Can Detect Abuse

Some ML systems operate in adversarial environments.

Examples include:

- Fraud detection
- Spam filtering
- Account security
- Abuse prevention
- Content moderation
- Bot detection
- Payment-risk systems

In these systems, some users actively try to discover and exploit model weaknesses.

## 4.1 Threshold-based anomaly alerts

Consider a bank login service.

If login attempts suddenly increase tenfold, the change may indicate:

- A credential-stuffing attack
- A bot campaign
- A denial-of-service attempt
- A system bug
- A legitimate but unusual traffic event

A basic alert can be triggered when a count crosses a threshold.

## 4.2 Rate-of-change monitoring

Absolute thresholds may be insufficient.

A system may also monitor:

- Rate of increase
- Acceleration
- Change relative to the same hour last week
- Change relative to seasonal expectations
- Differences by region or user cohort
- Unusual failure patterns

## 4.3 Model-based anomaly detection

When attacks are complex, a separate anomaly-detection model may identify suspicious combinations of signals more effectively than one simple rule.

However, an anomaly model also needs monitoring. It can drift, produce false alarms, or miss new attack patterns.

---

# 5. What to Monitor

A complete monitoring strategy typically combines three categories:

1. **Software and infrastructure metrics**
2. **Model and data metrics**
3. **Business and product metrics**

No single category is sufficient.

---

# 6. Software and Infrastructure Metrics

These metrics apply to nearly all production services.

## 6.1 Latency

Latency measures how long the system takes to process a request.

Useful summaries include:

- Mean latency
- Median latency
- 95th percentile latency
- 99th percentile latency
- Latency by endpoint
- Latency by model version
- Latency by input size

High-percentile latency matters because a good average can hide very slow experiences for some users.

## 6.2 Error rate

Track the proportion of requests that:

- Fail validation
- Time out
- Return server errors
- Produce exceptions
- Trigger fallbacks
- Fail to load the model
- Fail during preprocessing or postprocessing

## 6.3 Availability

Availability measures whether the service can be reached and used.

Possible indicators:

- Successful health checks
- Uptime
- Request success rate
- Dependency availability
- Queue backlog

## 6.4 Resource use

Monitor:

- CPU
- GPU
- Memory
- Disk
- Network
- Cache use
- Queue length
- GPU utilization
- Number of serving instances

Resource metrics can reveal problems before users experience failures.

## 6.5 Request volume

Track total requests and changes over time.

Breakdowns may include:

- User segment
- Geography
- Application version
- Input type
- Time of day
- Model version

A traffic increase can indicate success, abuse, seasonality, or a system problem.

---

# 7. Model Performance Metrics

Model monitoring should detect whether predictive quality is declining.

The ideal metric depends on the model type and product.

Examples include:

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Mean absolute error
- Root mean squared error
- Ranking metrics
- Calibration
- Coverage
- Abstention rate
- False-positive rate
- False-negative rate

The major production challenge is that ground truth may be delayed, incomplete, or unavailable.

---

# 8. Feature Drift

**Feature drift** occurs when the production input distribution changes relative to the training distribution.

Examples:

- Average user age changes
- Message length increases
- New vocabulary appears
- Transaction amounts shift
- More traffic comes from mobile devices
- New geographic regions enter the product
- Sensor characteristics change

## 8.1 Simple monitoring

A first approach is to compare summary statistics for key features.

Monitor:

- Mean
- Variance
- Median
- Quantiles
- Missing-value rate
- Minimum and maximum
- Category frequencies
- Proportion of unseen categories
- Text length
- Image dimensions

An alert can be raised when a statistic differs from the training value by more than a selected threshold.

## 8.2 Why summary statistics are incomplete

Two distributions can have similar means and variances but different shapes.

More advanced comparisons may use:

- Histograms
- Population Stability Index
- Kolmogorov–Smirnov tests
- Jensen–Shannon divergence
- Wasserstein distance
- Classifier-based drift detection

The chapter’s main principle remains:

> Monitor whether production inputs still resemble the data used to develop the model.

## 8.3 Drift does not automatically mean failure

A changed input distribution may not reduce model quality.

Drift is a warning signal, not proof of degraded performance.

The correct response is to:

1. Investigate the change.
2. Identify affected cohorts.
3. Compare available performance or business metrics.
4. Retrain or revise the pipeline only when justified.

---

# 9. Output Drift

A model’s prediction distribution can also change.

Examples:

- A fraud model flags more transactions
- A classifier predicts one class more frequently
- A recommendation model promotes a narrower set of items
- A pricing model produces higher prices
- A risk score shifts upward

Output drift may indicate:

- Input drift
- Model degradation
- A broken feature
- A changed catalog
- Changed user behavior
- A legitimate environmental change

## 9.1 Why output monitoring matters

Ground truth may arrive slowly, but predictions are available immediately.

Output distribution monitoring can therefore provide early warnings.

## 9.2 Example: movie recommendations

A movie recommendation model should change its outputs when the available catalog changes.

The same viewing history may appropriately lead to a different recommendation after new films are released.

Therefore, output drift is not always bad. It must be interpreted in context.

---

# 10. The Ground-Truth Problem

To directly evaluate model quality, the team needs the correct outcome.

In production, ground truth may be:

- Delayed
- Expensive
- Unobservable
- Influenced by the model
- Available only for a biased subset
- Defined through noisy user behavior

This makes online model evaluation difficult.

---

# 11. Model Actions Can Bias Observed Data

A prediction may cause the application to take an action, changing what can later be observed.

## 11.1 Fraud example

Suppose a credit-card fraud model blocks transactions predicted as fraudulent.

For blocked transactions, the team cannot observe what would have happened had the transaction been approved.

The observed data then contains:

- Outcomes for transactions that were allowed
- Little or no direct outcome for transactions that were blocked

This creates a selection problem.

The model has changed the data-generating process.

## 11.2 Consequence

The observed set is not a random sample of all transactions.

If the team evaluates only allowed transactions, its estimate of precision and recall may be biased.

This is closely related to **counterfactual reasoning**:

> What would have happened if the model had made a different decision or if no action had been taken?

---

# 12. Counterfactual Evaluation

Counterfactual evaluation attempts to estimate performance under actions that were not actually taken.

A practical approach is to withhold the model’s action for a small random subset.

## 12.1 Random holdout approach

For a small, randomly selected group:

- Record the model prediction.
- Do not apply the usual automated action.
- Observe the actual outcome.
- Compare the prediction with ground truth.

This sample can provide a less biased estimate of performance.

## 12.2 Fraud trade-off

In a fraud system, allowing some randomly selected flagged transactions through may provide valuable labels.

However, it also permits some fraud.

The organization must balance:

- Evaluation quality
- Financial loss
- User safety
- Legal obligations
- Ethical constraints

## 12.3 When random withholding is inappropriate

In high-stakes settings, random nonintervention may be unacceptable.

Examples:

- Medical diagnosis
- Emergency response
- Safety systems
- Severe abuse prevention

Counterfactual evaluation methods must respect domain-specific risk.

---

# 13. Business and Product Metrics

The most important metrics are those connected to the product’s goal.

A model can have excellent offline accuracy while producing little product value.

Examples of business metrics include:

- Click-through rate
- Conversion rate
- Revenue
- Retention
- Engagement
- Time saved
- Human override rate
- Task completion
- Customer satisfaction
- Number of useful recommendations
- Reduction in fraud loss
- Reduced manual workload

## 13.1 Click-through rate

For search or recommendation systems:

\[
CTR = \frac{\text{number of clicks}}{\text{number of displayed results}}
\]

A declining CTR may indicate that recommendations are less useful.

However, CTR should not be interpreted alone. A design change may increase clicks without improving satisfaction.

## 13.2 Product failure despite technical health

Suppose:

- Latency is low
- Error rate is low
- Feature distributions appear stable
- The model returns valid outputs

But users ignore the recommendations.

The product is still failing.

Technical metrics describe system operation. Business metrics describe whether the system creates value.

---

# 14. Design the Product to Collect Better Feedback

The product interface can be designed to create more informative signals.

## 14.1 Aggregate feedback

A general action such as “share this result” provides one signal for the full output.

## 14.2 Granular feedback

Word-level or item-level suggestions allow the product to observe:

- Which suggestion was accepted
- Which suggestion was ignored
- Which suggestion was edited
- Which suggestion was rejected

Granular feedback provides richer labels for future model improvement.

## 14.3 ML Editor example

If users can apply individual writing recommendations, the system can track which recommendations were useful.

This can create training data for a later model version.

## 14.4 Volume requirement

Feedback-driven learning requires enough usage.

For a lightly used prototype, the resulting dataset may be too small.

---

# 15. Monitoring Must Drive Action

Dashboards alone do not improve a model.

Every monitored metric should have:

- A purpose
- An owner
- An expected range
- An alert threshold
- An investigation procedure
- A possible remediation

## Example response table

| Signal | Possible meaning | Possible action |
|---|---|---|
| Latency rises | Infrastructure overload or slower model | Scale service, profile pipeline, roll back |
| Input mean shifts | Feature drift | Investigate data source and cohort |
| Missing values rise | Broken upstream pipeline | Stop inference or fix ingestion |
| Output distribution changes | Drift or feature failure | Compare versions and business metrics |
| CTR drops | Recommendations less useful | Investigate, retrain, run experiment |
| Abuse attempts spike | Attack | Rate-limit, block traffic, update detection |
| Fallback use rises | More hard or invalid inputs | Inspect requests, revise checks or model |
| Segment performance falls | Unequal degradation | Pause rollout, retrain, redesign |
| New model underperforms | Bad release | Roll back |

---

# 16. CI/CD for Machine Learning

**CI/CD** means:

- **Continuous Integration:** Developers regularly merge changes into a shared codebase.
- **Continuous Delivery or Deployment:** New versions can be tested and released efficiently.

For ML, CI/CD must cover more than code.

A release may include:

- New training data
- New preprocessing
- New features
- New model parameters
- New thresholds
- New postprocessing
- New serving requirements

## 16.1 Main challenge

It is easy to automate deployment.

It is much harder to guarantee that the newly deployed model is better.

A passing software test suite confirms that the pipeline runs correctly. It does not prove that the new model improves user outcomes.

---

# 17. Offline Test-Set Evaluation

The safest first comparison uses held-out data.

The team can compare:

- Accuracy
- Precision and recall
- Regression error
- Calibration
- Fairness metrics
- Inference speed
- Memory use
- Performance by segment

## Advantages

- Low risk
- Reproducible
- Fast
- No user exposure
- Easy to compare candidates

## Limitations

- Test data may not match production
- User behavior cannot be observed
- Current drift may be absent
- Infrastructure performance is not fully tested
- The test set may be stale

Offline evaluation is necessary, but not sufficient.

---

# 18. Shadow Mode

In **shadow mode**, a candidate model is deployed alongside the current production model.

Both models receive the same live inputs.

- The current model’s output is shown to the user.
- The candidate model’s output is logged but not used.

## Workflow

```text
Production request
       ↓
 ┌───────────────┐
 │ Current model │ → result shown to user
 └───────────────┘
       +
 ┌────────────────┐
 │ Candidate model│ → result stored only
 └────────────────┘
```

## 18.1 Benefits

Shadow mode allows the team to evaluate:

- Candidate predictions on live inputs
- Differences between old and new models
- Production latency
- Resource use
- Infrastructure compatibility
- Candidate failures
- Output distribution changes

When ground truth becomes available, the candidate can be compared with the current model.

## 18.2 Major limitation

Because users do not see the candidate model’s output, the team cannot observe how users would react to it.

Shadow mode cannot directly measure:

- Candidate CTR
- Candidate conversion
- Candidate satisfaction
- Behavioral changes caused by the candidate

## 18.3 Cost

Running two models may:

- Double inference work
- Increase GPU use
- Increase storage
- Increase latency if not isolated
- Require additional logging infrastructure

---

# 19. Evaluation Spectrum

The chapter describes three broad stages.

| Method | User risk | Production realism | User-response information |
|---|---:|---:|---:|
| Offline test set | Lowest | Lowest | None |
| Shadow mode | Low | High | None |
| Live deployment or experiment | Highest | Highest | Available |

A safe release process often moves through these stages in order.

```text
Offline evaluation
        ↓ pass
Shadow deployment
        ↓ pass
Limited live experiment
        ↓ success
Broader rollout
```

---

# 20. A/B Testing

A/B testing compares two variants with different user groups.

- **Control group:** receives the current model
- **Treatment group:** receives the candidate model

After sufficient exposure, the team compares outcomes.

## 20.1 Basic structure

```text
Eligible users
      ↓ random assignment
 ┌─────────────┬─────────────┐
 │ Control A   │ Treatment B │
 │ old model   │ new model   │
 └─────────────┴─────────────┘
      ↓                ↓
Measure outcomes for each group
      ↓
Estimate treatment effect
```

## 20.2 Goal

The goal is to maximize the chance of selecting the better model while minimizing exposure to a worse model.

---

# 21. Choosing Experiment Groups

The groups should be comparable.

Random assignment helps ensure that observed outcome differences are caused by the model rather than by systematic cohort differences.

## Bad assignment example

- Control group contains expert users
- Treatment group contains new users

A difference in outcomes could be caused by experience rather than the model.

## 21.1 Stable assignment

A user should usually remain in the same group throughout the experiment.

Otherwise:

- The user may see both versions
- Treatment effects may contaminate one another
- The comparison may become invalid

---

# 22. Choosing Treatment Size

The treatment group should be:

- Large enough to support statistical inference
- Small enough to limit risk from a poor model

This is a direct trade-off between:

- Information gained
- User exposure
- Experiment duration
- Business risk

A common strategy is staged exposure:

1. Very small treatment group
2. Check safety and infrastructure
3. Increase treatment share
4. Continue only if metrics remain acceptable

---

# 23. Choosing Experiment Duration

An experiment must run long enough to collect sufficient data and capture normal variation.

Too short:

- Low statistical power
- Sensitive to daily noise
- May miss weekly seasonality
- May produce unstable conclusions

Too long:

- More users may experience a bad variant
- Product improvement is delayed
- Other changes may interfere
- Experiment opportunity cost increases

The planned duration should consider:

- Baseline metric rate
- Expected effect size
- Traffic volume
- Statistical significance level
- Required statistical power
- Day-of-week effects
- Seasonality

---

# 24. Statistical Significance

The treatment group may have a higher observed metric simply due to random variation.

A/B testing therefore commonly uses a two-sample hypothesis test.

## 24.1 Typical hypotheses

\[
H_0: \text{No true difference between model A and model B}
\]

\[
H_1: \text{A true difference exists}
\]

For directional improvement:

\[
H_1: \text{Model B performs better than model A}
\]

## 24.2 Practical significance

Statistical significance does not guarantee meaningful product value.

A tiny improvement may be statistically significant with a very large sample but not worth:

- Increased compute cost
- Added complexity
- Fairness risk
- Maintenance burden
- Higher latency

Teams should define a **minimum detectable effect** or minimum meaningful improvement.

---

# 25. Determine Sample Size in Advance

The required sample depends on:

- Baseline metric
- Expected improvement
- Desired power
- Significance level
- Variance
- Group allocation

A small expected improvement requires more data.

## 25.1 Why planning matters

The team should decide before the experiment:

- Primary metric
- Group sizes
- Test duration
- Significance threshold
- Stopping rule
- Segments to inspect

This reduces the risk of selectively interpreting results.

---

# 26. Repeated Significance Testing Error

A common mistake is to repeatedly check the p-value and stop as soon as it becomes significant.

This increases the false-positive rate.

Why?

Each additional check creates another opportunity for random fluctuation to look significant.

This practice is sometimes called:

- Peeking
- Optional stopping
- Repeated significance testing

## Better approaches

- Fix the sample size in advance
- Fix the duration in advance
- Use a valid sequential-testing method
- Adjust for multiple looks

---

# 27. Do Not Optimize Only One Metric

An experiment may improve the primary metric while damaging the product elsewhere.

Example:

- CTR rises
- User abandonment doubles

The new model should probably not be considered better.

## 27.1 Guardrail metrics

In addition to the primary metric, monitor guardrails such as:

- Retention
- Complaints
- Latency
- Error rate
- Revenue
- Diversity
- Safety
- Fairness
- User churn
- Resource cost

A release should satisfy both:

1. Improvement in the target metric
2. No unacceptable harm to guardrail metrics

---

# 28. Segment-Level Evaluation

Average performance can hide harm to a subgroup.

Example:

- Overall CTR increases
- CTR for one user segment falls sharply

The treatment may not be appropriate for full deployment.

Analyze performance by relevant segment, such as:

- New versus experienced users
- Device type
- Region
- Language
- Product category
- Traffic source
- Accessibility need
- Demographic group, when appropriate and legally permissible

Segment analysis should be preplanned when possible to avoid opportunistic conclusions.

---

# 29. Experiment Infrastructure

A/B testing requires systems that can:

- Assign users to groups
- Store assignments
- Route requests
- Serve different model versions
- Log exposure
- Record outcomes
- Join outcomes to exposures
- Analyze results
- Prevent conflicting experiments

## 29.1 Logged-in users

For authenticated users, group assignment can be stored with the user profile.

## 29.2 Logged-out users

Logged-out users are harder to track consistently.

Possible identifiers include:

- Cookies
- Device identifiers
- Anonymous session identifiers
- IP-based methods

Each has limitations involving:

- Privacy
- Reliability
- Shared devices
- Deleted cookies
- Changing networks
- Legal compliance

If the same person frequently sees both variants, the experiment may be contaminated.

---

# 30. Parallel Experiments

Large organizations may run many experiments simultaneously.

Potential problems include:

- Two tests modify the same interface
- One treatment changes the population seen by another
- Interaction effects
- Competing group assignments
- Overlapping metrics
- Increased multiple-testing risk

At scale, organizations may build experimentation platforms that manage:

- Assignment
- Isolation
- Traffic allocation
- Metrics
- Statistical analysis
- Experiment conflicts
- Dashboards

The chapter references examples from Airbnb, Uber, and Intuit.

---

# 31. Multiarmed Bandits

A/B testing typically uses fixed group allocations during a defined experiment.

A **multiarmed bandit** dynamically changes allocation based on observed performance.

The name comes from choosing among multiple slot machines, or “arms,” with unknown rewards.

## 31.1 Exploration versus exploitation

A bandit balances:

- **Exploitation:** Choose the currently best-performing model
- **Exploration:** Try other models to learn whether one is better

## 31.2 Basic behavior

```text
Most requests
      ↓
Current best-performing model

Small share of requests
      ↓
Alternative model chosen for exploration
```

Performance estimates are updated continuously.

## 31.3 Advantages

- Supports more than two alternatives
- Adapts allocation over time
- Sends more traffic to stronger variants
- Reduces exposure to weak options
- Can continue learning

## 31.4 Limitations

- Statistical analysis is more complex
- Delayed rewards are difficult
- Changing environments complicate learning
- Guardrail constraints are still needed
- Early noise may favor the wrong model
- Implementation is more complex than standard A/B testing

---

# 32. Contextual Bandits

A **contextual bandit** uses user or request features to decide which model or action is best for that specific context.

Instead of asking:

> Which model is best overall?

it asks:

> Which model is best for this user or situation?

Possible context:

- User history
- Device
- Location
- Time
- Language
- Product category
- Previous interactions

Contextual bandits can personalize model selection, but introduce additional complexity, bias, and monitoring requirements.

---

# 33. A/B Testing Versus Bandits

| Feature | A/B test | Multiarmed bandit |
|---|---|---|
| Allocation | Usually fixed | Changes dynamically |
| Goal | Estimate causal difference | Maximize reward while learning |
| Duration | Defined experiment | May run continuously |
| Analysis | Standard hypothesis testing | Sequential decision framework |
| Exposure to weak variant | Fixed by design | Usually decreases over time |
| Number of variants | Commonly two | Can support many |
| Simplicity | More familiar | More complex |
| Best use | Clear comparison and inference | Adaptive optimization |

---

# 34. Actions Monitoring Should Trigger

Monitoring should lead to one or more defined actions.

## 34.1 Investigate

Use when:

- Drift appears
- Output distribution changes
- A metric crosses a warning threshold
- A segment deteriorates

## 34.2 Retrain

Use when:

- Model performance declines
- Training data is stale
- New labeled data is available
- The population has changed

## 34.3 Recalibrate

Use when:

- Ranking remains useful
- Probability estimates no longer match observed rates

## 34.4 Update thresholds

Use when:

- Business costs change
- Class balance changes
- Desired precision-recall trade-off changes

## 34.5 Roll back

Use when:

- A new version harms users
- Error rate rises
- Latency becomes unacceptable
- Guardrail metrics decline

## 34.6 Scale infrastructure

Use when:

- Request volume grows
- Queue length rises
- Latency increases under load
- Resource saturation occurs

## 34.7 Fix upstream data

Use when:

- Missingness increases
- Schema changes
- Feature computation fails
- Data freshness declines

## 34.8 Redesign the product

Use when:

- Users cannot provide useful feedback
- Business metrics remain poor despite acceptable model metrics
- The interface prevents users from correcting results
- The model solves the wrong product problem

---

# 35. Suggested Monitoring Dashboard

A practical dashboard may contain several layers.

## Layer 1: Service health

- Requests per minute
- Error rate
- Latency percentiles
- Instance count
- CPU/GPU/memory
- Queue length

## Layer 2: Data health

- Missing-value rates
- Feature means and variances
- Category frequencies
- Unseen-category rate
- Input size
- Drift scores

## Layer 3: Model behavior

- Prediction distribution
- Confidence distribution
- Fallback rate
- Filter rejection rate
- Calibration
- Accuracy when labels arrive
- Performance by segment
- Model-version comparison

## Layer 4: Product impact

- CTR
- Conversion
- Retention
- Acceptance rate
- Correction rate
- User complaints
- Revenue or cost
- Human workload

## Layer 5: Release status

- Traffic by model version
- Shadow model metrics
- A/B experiment group sizes
- Experiment confidence intervals
- Rollout stage
- Alert status

---

# 36. Alert Design

Poor alerting can create alert fatigue.

## 36.1 Good alerts should be

- Actionable
- Specific
- Prioritized
- Owned
- Connected to a runbook
- Resistant to normal noise

## 36.2 Warning versus critical alerts

### Warning

- Small drift
- Elevated latency
- Mild performance decline

Action: investigate during normal operations.

### Critical

- Severe error spike
- Model unavailable
- Dangerous output distribution
- Large business-metric decline
- Abuse attack

Action: immediate response, failover, or rollback.

## 36.3 Threshold design

Thresholds can be:

- Absolute
- Relative to baseline
- Rate-of-change based
- Segment-specific
- Statistically derived
- Seasonally adjusted

---

# 37. Common Monitoring Mistakes

## Mistake 1: Monitoring only infrastructure

The service may be fast but wrong.

**Correction:** Include model and business metrics.

## Mistake 2: Monitoring only offline model accuracy

Offline data may not match production.

**Correction:** Add drift, feedback, and live performance signals.

## Mistake 3: Treating drift as proof of failure

Inputs can change without harming performance.

**Correction:** Use drift as an investigation trigger.

## Mistake 4: Ignoring model-induced selection bias

Actions based on predictions change which outcomes are observed.

**Correction:** Consider counterfactual evaluation or randomized holdouts when safe.

## Mistake 5: Optimizing one business metric

CTR may rise while retention or safety declines.

**Correction:** Add guardrail metrics.

## Mistake 6: Looking only at averages

A subgroup may be harmed.

**Correction:** Evaluate relevant segments.

## Mistake 7: Peeking at experiments

Stopping when significance first appears inflates false positives.

**Correction:** Predefine sample size or use valid sequential methods.

## Mistake 8: Changing assignment during an A/B test

Users seeing both variants can contaminate results.

**Correction:** Use stable assignment.

## Mistake 9: Deploying directly after test-set improvement

Offline success may not translate to production.

**Correction:** Use shadow mode and limited experiments.

## Mistake 10: Collecting metrics without response plans

A dashboard does not fix the model.

**Correction:** Define owners, thresholds, and actions.

---

# 38. Recommended Model-Update Workflow

A disciplined release process may follow these steps.

## Step 1: Detect a need

Signals:

- Model metric decline
- Drift
- Business metric decline
- New data
- New product requirement
- Abuse pattern

## Step 2: Diagnose the cause

Determine whether the issue is:

- Model staleness
- Broken feature
- Pipeline bug
- Infrastructure problem
- Product-design issue
- Attack
- Seasonal change

## Step 3: Develop a candidate

Possible changes:

- Retrain
- Add data
- Revise features
- Recalibrate
- Adjust thresholds
- Change model architecture

## Step 4: Offline validation

Compare:

- Predictive metrics
- Segment performance
- Calibration
- Latency
- Resource use
- Safety checks

## Step 5: Shadow deployment

Observe:

- Live input behavior
- Infrastructure compatibility
- Prediction differences
- Candidate errors

## Step 6: Limited experiment

Use:

- Small treatment group
- Stable assignment
- Predefined metrics
- Guardrails
- Planned duration

## Step 7: Analyze

Evaluate:

- Statistical significance
- Practical significance
- Segment effects
- Business value
- Operational cost

## Step 8: Gradual rollout

Increase traffic while monitoring.

## Step 9: Roll back if necessary

Preserve the previous version and deployment path.

## Step 10: Continue monitoring

A successful release can still degrade later.

---

# 39. Oral-Exam Ready Summary

> Chapter 11 explains that deployed ML models must be monitored for both system health and continued product value. Standard software metrics such as latency, error rate, and resource use remain important, but ML systems also require monitoring of feature drift, output distributions, predictive performance, user feedback, and business metrics. Monitoring can reveal when a model is stale, when an attack is occurring, or when a new release is harming users. Ground truth is often difficult to observe because model actions change which outcomes occur, as in fraud systems that block transactions. Randomized holdouts can support counterfactual evaluation when the risk is acceptable. New models should move from offline evaluation to shadow mode and then to controlled live experiments. A/B tests require random and stable assignment, sufficient sample size, predefined stopping rules, statistical and practical significance, guardrail metrics, and segment analysis. Multiarmed bandits provide a more adaptive alternative. Ultimately, monitoring should drive concrete actions such as retraining, rollback, scaling, recalibration, or product redesign.

---

# 40. Possible Oral-Exam Questions

## 1. Why is ordinary software monitoring insufficient for ML?

**Answer:** A model can be fast and available while producing inaccurate or useless predictions, so teams must also monitor data, model behavior, and business impact.

## 2. How can monitoring determine retraining frequency?

**Answer:** The team can trigger retraining when a performance or freshness metric crosses a predefined threshold.

## 3. How can monitoring detect abuse?

**Answer:** It can alert on unusual traffic counts, rates of change, or anomaly scores that indicate attacks or attempts to defeat the model.

## 4. What is feature drift?

**Answer:** A change in the production input distribution relative to the model’s training data.

## 5. Does feature drift prove that the model is failing?

**Answer:** No. It is a warning signal that should trigger investigation and performance checks.

## 6. Why monitor prediction distributions?

**Answer:** Output drift may reveal changed inputs, broken features, model degradation, or legitimate environmental change before ground truth becomes available.

## 7. Why can ground truth be difficult to observe?

**Answer:** It may be delayed or unavailable, and actions based on model predictions can prevent the counterfactual outcome from being observed.

## 8. How does a fraud model create selection bias?

**Answer:** Blocked transactions do not reveal what would have happened if approved, so outcomes are observed mainly for transactions the model allowed.

## 9. What is counterfactual evaluation?

**Answer:** Estimating what outcomes would have occurred under actions that were not actually taken.

## 10. How can randomized holdouts support evaluation?

**Answer:** By withholding the model’s action for a small random subset, the team can observe less biased outcomes.

## 11. Why are business metrics essential?

**Answer:** They determine whether the model actually creates product value, even when technical metrics look good.

## 12. What is shadow mode?

**Answer:** Running a candidate model in parallel with the production model while logging its predictions but not showing them to users.

## 13. What can shadow mode test?

**Answer:** Live-input behavior, infrastructure compatibility, latency, resource use, and prediction differences.

## 14. What can shadow mode not test?

**Answer:** How users would respond to the candidate model’s outputs.

## 15. What is the control group in an A/B test?

**Answer:** The group that receives the current model or existing experience.

## 16. Why must assignment be random?

**Answer:** To make groups comparable so outcome differences can be attributed to the model rather than cohort differences.

## 17. Why should user assignment remain stable?

**Answer:** Exposure to both variants can contaminate the experiment and invalidate the comparison.

## 18. Why determine experiment duration in advance?

**Answer:** To ensure sufficient data and avoid biased optional stopping or repeated significance testing.

## 19. What is practical significance?

**Answer:** Whether the improvement is large enough to matter operationally or commercially, not merely statistically detectable.

## 20. What are guardrail metrics?

**Answer:** Secondary metrics used to ensure that improving the primary metric does not create unacceptable harm elsewhere.

## 21. Why inspect segments?

**Answer:** Average improvement can hide severe degradation for a subgroup.

## 22. What infrastructure does A/B testing require?

**Answer:** Stable assignment, traffic routing, exposure logging, outcome collection, model-version serving, and analysis.

## 23. What is a multiarmed bandit?

**Answer:** An adaptive method that sends most traffic to the current best option while continuing to explore alternatives.

## 24. What is a contextual bandit?

**Answer:** A bandit that uses user or request features to choose the best model or action for a particular context.

## 25. What should monitoring ultimately do?

**Answer:** Trigger defined actions such as investigation, retraining, rollback, scaling, threshold updates, or product changes.

---

# 41. Key Terms

| Term | Meaning |
|---|---|
| Monitoring | Continuous observation of system, model, and product health |
| Model freshness | Degree to which a model still reflects the current environment |
| Feature drift | Change in the input-feature distribution |
| Output drift | Change in the distribution of model predictions |
| Ground truth | Correct outcome used to evaluate a prediction |
| Selection bias | Distortion caused by observing a nonrepresentative subset |
| Counterfactual | Outcome that would have occurred under a different action |
| Counterfactual evaluation | Estimating performance under unobserved alternative actions |
| Business metric | Measure tied to product or organizational value |
| Click-through rate | Clicks divided by displayed recommendations or results |
| CI/CD | Practices for integrating, validating, and releasing changes efficiently |
| Shadow mode | Candidate model runs on live inputs without affecting users |
| Control group | Group receiving the current model |
| Treatment group | Group receiving the candidate model |
| A/B test | Randomized comparison between two variants |
| Statistical significance | Evidence that an observed difference is unlikely under the null hypothesis |
| Practical significance | Whether the effect is large enough to matter |
| Statistical power | Probability of detecting a true effect |
| Repeated significance testing | Rechecking significance until a favorable result appears |
| Guardrail metric | Secondary metric that protects against unintended harm |
| Multiarmed bandit | Adaptive algorithm balancing exploration and exploitation |
| Contextual bandit | Bandit that personalizes decisions using contextual features |
| Experiment contamination | Mixing or interference that makes variant effects difficult to isolate |
| Canary rollout | Gradual increase in traffic to a new version |
| Rollback | Restoration of a previous production version |

---

# 42. Final Takeaways

1. Monitoring begins after deployment and continues throughout the model’s life.
2. ML monitoring must include system, data, model, and product metrics.
3. Monitoring can reveal model staleness and determine when retraining is needed.
4. Anomaly monitoring is essential in adversarial applications.
5. Feature drift is easier to observe than true performance degradation.
6. Output drift can provide an early warning when labels are delayed.
7. Model actions can bias the outcomes available for evaluation.
8. Counterfactual evaluation may require randomized nonintervention when ethically acceptable.
9. Business metrics are the ultimate measure of whether the model creates value.
10. Product interfaces can be designed to collect granular feedback.
11. Offline test performance is necessary but not enough for release decisions.
12. Shadow mode tests a candidate on live inputs without affecting user experience.
13. A/B testing is the main method for observing causal product impact.
14. A/B tests require comparable groups, stable assignment, sufficient sample size, and predefined stopping rules.
15. Statistical significance should be paired with practical significance.
16. Guardrails prevent optimization of one metric at the expense of the overall product.
17. Segment analysis prevents averages from hiding subgroup harm.
18. Experimentation requires dedicated assignment, routing, logging, and analysis infrastructure.
19. Multiarmed bandits adapt traffic allocation while continuing to learn.
20. Every dashboard and alert should be connected to a defined operational action.

---

## One-Sentence Memory Aid

> **Monitor whether the service works, whether the data changed, whether the model still helps users, and whether the evidence is strong enough to retrain, roll back, or release a better version.**
