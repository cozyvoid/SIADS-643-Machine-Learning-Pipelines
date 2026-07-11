# Chapter 4 Study Guide: Acquire an Initial Dataset

**Book:** *Building Machine Learning Powered Applications*  
**Chapter focus:** Finding, evaluating, representing, exploring, labeling, and improving an initial dataset before training the first machine learning model.

---

## 1. Chapter Overview

Chapter 4 argues that **data work is not a preliminary chore that ends before modeling begins**. In an applied machine learning product, the dataset is part of the product and should be revised repeatedly as the team learns more.

The chapter presents an end-to-end workflow for moving from an initial collection of raw examples to a dataset that is useful for machine learning:

1. Gather a small, manageable dataset.
2. inspect its format, quality, quantity, and distributions.
3. preprocess and serialize the cleaned data.
4. calculate summary statistics.
5. transform raw data into numerical vectors.
6. use dimensionality reduction and clustering to inspect structure.
7. manually label representative examples.
8. identify useful patterns, biases, and weak spots.
9. turn reliable patterns into features or modeling decisions.
10. gather or relabel data as new problems are discovered.

The ML Editor case study continues from Chapter 3. The application attempts to judge whether a written question is likely to be useful and answerable. Stack Exchange posts are used as an initial dataset, and community signals such as question score or whether a question received an accepted answer serve as **weak labels** for writing quality.

---

# 2. Central Principle: Iterate on the Dataset

## 2.1 Data development is iterative

Machine learning products improve through repeated cycles of:

- gathering data,
- inspecting data,
- labeling data,
- training a model,
- evaluating failures,
- and updating the dataset.

A dataset should therefore not be viewed as a fixed input. It is an evolving component of the machine learning system.

### Research versus industry

The chapter distinguishes two common settings:

| Setting | Typical treatment of data |
|---|---|
| Machine learning research | Standard benchmark datasets are usually fixed so that models can be compared fairly. |
| Traditional software engineering | Data is commonly treated as information that deterministic software receives, processes, and stores. |
| Machine learning product development | The dataset is actively selected, cleaned, labeled, expanded, rebalanced, and revised to improve the product. |

In industry, changing the data may produce a larger improvement than changing the model.

## 2.2 Why this matters

A model can only learn patterns that are represented in its training data. Model performance will be limited when:

- the examples are incorrect,
- labels are inconsistent,
- important cases are missing,
- one group is overrepresented,
- a feature is unavailable at inference time,
- or the collected examples do not resemble production inputs.

The practical implication is:

> When a machine learning system performs poorly, inspect the data before assuming that the model architecture is the problem.

---

# 3. “Do Data Science,” Not Only Model Building

The chapter emphasizes that a data scientist’s job is broader than selecting algorithms.

A model is a mechanism for extracting patterns from data. Before choosing a model, the practitioner must determine:

- whether predictive patterns exist,
- whether the available features capture those patterns,
- whether the labels represent the desired outcome,
- whether the dataset contains systematic bias,
- and whether the patterns will persist in production.

Many educational exercises provide a prepared dataset and concentrate on model training. Real projects often reverse that balance: **dataset curation, labeling, and validation consume much of the work**.

## Key lesson

The quality of a machine learning product depends on the relationship among:

- the business problem,
- the data-generating process,
- the labels,
- the representation,
- the model,
- and the production environment.

Improving only the model cannot repair a dataset that does not represent the real task.

---

# 4. Explore the First Dataset

## 4.1 Start with an available dataset, not a perfect dataset

A common source of delay is searching indefinitely for the ideal dataset. The chapter recommends beginning with a dataset that is:

- available now,
- small enough to inspect,
- relevant enough to test initial assumptions,
- and easy enough to preprocess.

Its purpose is to generate information, not to become the final production dataset.

## 4.2 Be efficient and start small

Although additional data often improves performance, starting with the largest possible dataset can slow early experimentation.

A smaller initial sample makes it easier to:

- view individual examples,
- verify labels,
- understand feature distributions,
- test preprocessing code,
- identify edge cases,
- and rerun experiments quickly.

### Examples

- At a company with terabytes of records, extract a uniform sample that fits in local memory.
- For an image classifier that recognizes car brands, begin with a few dozen street images.
- For a text classifier, inspect hundreds or thousands of examples before processing millions.

Once the team knows where the model struggles, it can collect more targeted data.

## 4.3 Possible data sources

An initial dataset may come from:

- public repositories such as Kaggle,
- domain-specific forums or archives,
- open web datasets,
- web scraping,
- internal databases or logs,
- sensors,
- manually generated examples,
- templates,
- simulations,
- or user interactions.

The source should be judged based on how closely it matches the expected production environment.

---

# 5. Insights Versus Products

Exploratory data analysis can serve two different goals.

## 5.1 Analysis-oriented exploration

The goal is to discover and communicate an insight.

Example:

- Fraudulent logins occur more often on Thursdays and frequently originate from the Seattle area.

## 5.2 Product-oriented exploration

The goal is to convert the discovered pattern into an automated decision or feature.

Example:

- Use login time and IP-derived location as model inputs for a fraud-prevention service.

## 5.3 Why product-oriented analysis is harder

A product team must ask additional questions:

- Will the pattern continue in future data?
- Is the relationship causal or accidental?
- Can the feature be computed at prediction time?
- Will the production distribution differ from the training distribution?
- How frequently should the model be retrained?
- Is the feature stable, ethical, and legally appropriate?

A descriptive correlation is not automatically a safe production feature.

---

# 6. A Data Quality Rubric

The chapter recommends assessing four broad areas before training a model:

1. **format,**
2. **quality,**
3. **quantity,**
4. **distribution.**

---

## 6.1 Data format

Determine whether the dataset already contains clear inputs and outputs or whether it must be transformed.

Questions to ask:

- What constitutes one training example?
- What is the prediction target?
- Are labels already present?
- Is the dataset stored in a usable table?
- Are records nested in JSON, XML, HTML, images, logs, or another format?
- Does one real-world event span multiple rows?
- Must events be joined across tables?
- Can preprocessing be reproduced?
- Can the same preprocessing run during production inference?

### Example: ad-click prediction

A raw click log may contain only click events. To train a classifier, the data must be converted into examples representing:

- an ad shown to a user,
- the user and ad attributes available at that moment,
- and whether the user clicked.

Without records of non-clicked impressions, the raw click log is not sufficient.

### Validate preprocessed fields

When a dataset includes calculated fields such as an average conversion rate, verify how they were produced. Whenever possible, recompute them from source data.

This protects against:

- misunderstood definitions,
- incorrect aggregation windows,
- label leakage,
- stale values,
- and undocumented preprocessing.

---

## 6.2 Data quality

Data quality problems include:

- missing values,
- corrupted records,
- malformed text,
- inaccurate labels,
- imprecise measurements,
- duplicated examples,
- inconsistent units,
- ambiguous cases,
- and information that humans cannot reliably interpret.

### Questions by data type

#### Logs

- Are events missing?
- Are some clients failing to report?
- Are timestamps trustworthy?
- Are event sequences complete?
- Are fields populated consistently?

#### Text

- Is the text readable?
- Are encodings corrupted?
- Are spelling and language consistent?
- Does the text contain boilerplate, HTML, or duplicated templates?
- Are multiple languages mixed together?

#### Images

- Are images clear and properly oriented?
- Is the target object visible?
- Are labels or bounding boxes accurate?
- Could a human perform the task from the image?

#### Labeled data

- Do human reviewers agree with the labels?
- Are the label definitions precise?
- Are some cases inherently ambiguous?
- Are labels missing systematically for particular groups?

### Practical interpretation

If humans cannot reliably infer the correct outcome from an input, a model may also struggle. Poor labels also establish an upper limit on measurable model performance.

---

## 6.3 Data quantity

Count:

- total examples,
- labeled examples,
- examples in each class,
- examples for important subgroups,
- and examples after cleaning.

A dataset may be large overall but still insufficient in the rare cases that matter most.

### Example from the chapter

A customer-support routing project had nine categories but only one example per category. Instead of building a more sophisticated model, the team generated additional examples using category-specific templates. This provided thousands of training instances and created a much more learnable problem.

The example illustrates a general rule:

> When the dataset contains almost no signal, a more complex model is not a substitute for additional data.

---

## 6.4 Distribution

Examine whether feature values and labels are represented in realistic proportions.

Questions include:

- Are any classes absent?
- Is one class overwhelmingly common?
- Are some groups represented by only a handful of examples?
- Are ranges plausible?
- Are there extreme outliers?
- Is the sample drawn from the same population as future production data?
- Does the dataset cover different times, regions, devices, and user groups?

A model trained on an unrepresentative dataset may perform well on a random test split drawn from the same biased source but fail in production.

---

## 6.5 Condensed quality checklist

| Category | Questions |
|---|---|
| Format | What is one example? What are the inputs and target? How much preprocessing is required? Can it be reproduced in production? |
| Quality | Are values missing, corrupted, noisy, ambiguous, duplicated, or mislabeled? |
| Quantity | How many examples exist overall and per class or subgroup? |
| Distribution | Are classes balanced enough? Are important cases absent? Does the dataset resemble production data? |

---

# 7. ML Editor Dataset Inspection

## 7.1 Initial source

The case study uses the anonymized Stack Exchange Data Dump. Stack Exchange contains themed question-and-answer communities. The Writing community is chosen because its posts provide a broad collection of writing-related questions.

The dataset includes metadata such as:

- post ID,
- post type,
- body text,
- title,
- score,
- answer count,
- accepted answer ID,
- tags,
- comments,
- dates,
- and user identifiers.

## 7.2 Raw format

The archive stores posts as XML rows, while the question body contains HTML markup. The preprocessing pipeline must therefore:

1. parse XML,
2. extract row attributes,
3. decode HTML,
4. isolate readable text,
5. create a tabular representation,
6. and save the processed output.

## 7.3 Parsing XML into a DataFrame

The chapter’s workflow uses:

- `xml.etree.ElementTree` to parse XML,
- `BeautifulSoup` to convert HTML into text,
- `pandas.DataFrame.from_dict()` to create a DataFrame,
- and `DataFrame.to_csv()` to serialize the result.

Conceptually:

```python
def parse_xml_to_csv(path, save_path=None):
    document = parse_xml(path)
    rows = extract_row_attributes(document)

    for row in rows:
        row["body_text"] = decode_html(row["Body"])

    df = create_dataframe(rows)

    if save_path:
        df.to_csv(save_path)

    return df
```

## 7.4 Preprocess once and serialize

Parsing tens of thousands of XML records and cleaning HTML can take long enough to slow every experiment.

The chapter recommends separating:

- **expensive, deterministic preprocessing**, and
- **frequently repeated model experimentation**.

After raw data is cleaned, save the processed form to disk. This reduces iteration time and makes experiments more reproducible.

### General pipeline pattern

```text
Raw source
   ↓
Deterministic cleaning
   ↓
Serialized processed dataset
   ↓
Feature generation and model experiments
```

---

# 8. Inspecting the Stack Exchange Data

## 8.1 Use `df.info()`

`DataFrame.info()` provides a quick overview of:

- columns,
- data types,
- non-null counts,
- and approximate dataset size.

This immediately surfaces fields with extensive missingness.

## 8.2 Validate suspicious values

The chapter finds posts with unexpected missing body text. Rather than automatically imputing or ignoring them, the author investigates the records and discovers an undocumented post type. Those records are removed.

This demonstrates an important workflow:

1. detect an anomaly,
2. inspect representative records,
3. determine the cause,
4. document the decision,
5. then clean or remove them.

## 8.3 Understand post relationships

A Stack Exchange post can be:

- a question,
- or an answer.

Questions and answers must be joined correctly. The chapter matches questions with accepted answers and manually inspects several pairs.

The purpose is not merely to confirm that the code runs. It verifies the meaning of the join.

### Validation question

Does the text in the joined answer actually respond to the associated question?

This kind of semantic check can reveal incorrect keys, index mismatches, or misunderstood schemas that summary statistics would miss.

## 8.4 Check outcome counts

The chapter divides questions into:

- questions with no answers,
- questions with one or more answers but no accepted answer,
- and questions with an accepted answer.

The groups are reasonably populated, so the dataset appears usable for initial experimentation.

The broader lesson is to verify that the outcomes needed for modeling have enough examples.

---

# 9. Labels and Weak Labels

A **label** is the target value a supervised model learns to predict.

For the ML Editor, the true concept of interest is something like:

- question quality,
- clarity,
- usefulness,
- or answerability.

These concepts are not directly available in the Stack Exchange dump. Instead, the project uses observable community behavior as a proxy.

Possible weak labels include:

- question score,
- whether a question received an answer,
- whether it received an accepted answer.

These are called **weak labels** because they are correlated with the desired concept but are not identical to it.

## Risks of weak labels

A question can receive a low score because:

- it was posted when few users were online,
- it concerned a niche topic,
- it came from a new user,
- it was poorly formatted,
- or it was genuinely unclear.

Therefore, a model trained on score may learn platform behavior rather than writing quality.

Manual labeling is needed to test whether the weak label is credible.

---

# 10. Summary Statistics

Before examining advanced representations, calculate basic descriptive statistics.

Useful summaries include:

- counts,
- class proportions,
- averages,
- medians,
- standard deviations,
- quantiles,
- missing-value rates,
- unique-value counts,
- and distributions.

## 10.1 Why compare distributions by class?

Differences between classes can identify predictive features or reveal shortcuts.

Example:

- If positive tweets are always shorter than negative tweets, length may become highly predictive.
- That may be useful if the pattern is genuine.
- It may also indicate sampling bias if the production population will not preserve that relationship.

## 10.2 ML Editor example: question length

The chapter compares text-length distributions for high- and low-score questions.

The distributions overlap substantially, but high-score questions are somewhat more likely to be longer around certain ranges. This suggests that question length could be a useful feature, although it is not sufficient by itself.

## 10.3 Avoid overinterpreting a histogram

A visible difference is a hypothesis, not proof. Follow-up questions include:

- Does the trend hold in a validation sample?
- Is it caused by another variable?
- Does it remain after removing outliers?
- Is text length available and stable in production?
- Does the trend apply to all subgroups?

---

# 11. Explore Individual Examples Efficiently

Aggregate statistics cannot fully explain the dataset. Practitioners should inspect individual examples, but random inspection is inefficient.

The chapter recommends using:

- vectorization,
- dimensionality reduction,
- and clustering

to organize similar examples and make manual review more systematic.

---

# 12. Clustering: Concept and Purpose

## 12.1 Definition

Clustering is an unsupervised learning task that groups examples so that:

- examples within a cluster are relatively similar,
- and examples in different clusters are relatively dissimilar.

There is rarely one uniquely correct clustering.

## 12.2 Why use clustering during data exploration?

Clustering helps identify:

- common types of examples,
- rare subpopulations,
- outliers,
- dense and sparse regions,
- difficult categories,
- label inconsistencies,
- and potential data gaps.

## 12.3 Questions to ask about clusters

- How many meaningful groups appear?
- What do examples within each cluster share?
- How do clusters differ?
- Is one cluster much denser than another?
- Are certain clusters underrepresented?
- Are labels mixed or separated within clusters?
- Does one cluster contain harder or more ambiguous examples?
- Does one cluster correspond to corrupted or irrelevant data?

Sparse clusters may require more data. Difficult clusters may require new features, separate models, or revised label definitions.

---

# 13. Vectorization

## 13.1 Definition

**Vectorization** transforms a raw example into a numerical vector that a machine learning algorithm can process.

A vector representation determines which examples appear similar. It therefore affects:

- clustering,
- visualization,
- model training,
- and nearest-neighbor searches.

Poor representations can hide meaningful structure or create artificial structure.

---

# 14. Vectorizing Tabular Data

Tabular data may contain:

- continuous variables,
- counts,
- categories,
- dates,
- identifiers,
- and text.

Each type should be transformed appropriately.

## 14.1 Continuous variables

Variables measured on very different scales can distort distance-based methods and some models.

Example:

- annual income may range into hundreds of thousands,
- while number of comments may range from 0 to 20.

Without scaling, the larger numerical range can dominate.

## 14.2 Standardization

A common starting transformation is the **standard score**, or z-score:

$$
z = \frac{x - \mu}{\sigma}
$$

where:

- $x$ is the original value,
- $\mu$ is the training-set mean,
- $\sigma$ is the training-set standard deviation.

After standardization, a feature has approximately:

- mean 0,
- standard deviation 1.

This does not make the distribution normal; it only rescales it.

## 14.3 Categorical variables

Nominal categories should generally not be assigned arbitrary ordered numbers.

For example:

```text
red = 1
green = 2
blue = 3
```

would falsely imply that blue is larger than green and that the distance from red to blue is twice the distance from red to green.

### One-hot encoding

Each category receives its own binary column.

```text
red   = [1, 0, 0]
green = [0, 1, 0]
blue  = [0, 0, 1]
```

This avoids imposing an artificial ordering.

## 14.4 Limitation of one-hot encoding

All different categories are equally distant. This can be inappropriate when some categories are naturally related.

Example:

- Saturday and Sunday are more similar to each other than either is to Wednesday.

Learned embeddings can capture these relationships.

## 14.5 Dates

Raw timestamps often hide important structure. Extract useful components such as:

- year,
- month,
- day of month,
- day of week,
- hour,
- weekend indicator,
- holiday indicator,
- time since previous event,
- or season.

The right components depend on the product hypothesis.

## 14.6 Tags in the ML Editor dataset

Questions can have multiple tags. The chapter:

1. parses the tag string into a list,
2. creates binary indicator columns,
3. counts tag frequencies,
4. retains only sufficiently common tags,
5. and concatenates them with the other numerical features.

Rare categories may add a very wide, sparse feature space without enough observations to estimate reliable effects.

---

# 15. Vectorization and Data Leakage

## 15.1 Definition

**Data leakage** occurs when information unavailable during real prediction is used during training.

Leakage can produce unrealistically high validation performance and disappointing production results.

## 15.2 Leakage during preprocessing

Preprocessing parameters must be learned from the training set only.

Examples:

- calculate the mean and standard deviation using only training data,
- choose retained categories using only training data,
- fit a TF-IDF vocabulary only on training data,
- fit missing-value imputers only on training data,
- fit dimensionality transformations only on training data when they become model features.

Then apply the stored transformation to validation, test, and production data.

## 15.3 Correct sequence

```text
Split raw data
   ↓
Fit preprocessing on training set
   ↓
Transform training set
   ↓
Apply the same fitted preprocessing to validation and test sets
```

## 15.4 Incorrect sequence

```text
Fit preprocessing on the full dataset
   ↓
Split into training, validation, and test sets
```

The incorrect sequence allows validation and test information to influence training features.

---

# 16. Vectorizing Text

## 16.1 Bag of words

The simplest text representation is a vocabulary-based count vector.

Steps:

1. create a vocabulary of unique terms,
2. assign each term an index,
3. represent each document with a vector,
4. store the number of occurrences of each term.

This is called **bag of words** because it records which words appear but generally ignores word order.

### Strengths

- simple,
- fast,
- interpretable,
- and effective for many classification problems.

### Limitations

- loses word order,
- treats related words as unrelated,
- creates high-dimensional sparse vectors,
- and may be sensitive to vocabulary differences.

## 16.2 TF-IDF

**Term Frequency–Inverse Document Frequency** adjusts word counts so that:

- terms frequent in one document receive weight,
- but terms appearing in nearly every document receive less weight.

This emphasizes words that help distinguish one document from the collection.

In scikit-learn:

```python
vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_text)
validation_vectors = vectorizer.transform(validation_text)
```

The validation set must use `transform`, not `fit_transform`.

## 16.3 Word embeddings

Methods such as Word2Vec and fastText learn dense vectors in which words used in similar contexts receive similar representations.

This is motivated by the **distributional hypothesis**:

> Words occurring in similar linguistic contexts often have related meanings.

### Window size

When learning a word representation, the **window size** controls how many surrounding words are considered context.

## 16.4 Pretrained embeddings

Pretrained vectors can transfer semantic knowledge from a large external corpus.

Advantages:

- useful when the project dataset is small,
- semantically related words may be close in vector space,
- and downstream models may generalize better.

Risks:

- the source corpus may differ from the product domain,
- uncommon domain terms may be missing,
- and social biases in the original corpus may be transferred.

## 16.5 Sentence vectors

A simple sentence vector can be formed by averaging the vectors of its words.

This is easy but loses:

- word order,
- syntax,
- negation structure,
- and contextual meaning.

## 16.6 Large language model representations

Contextual language models can produce richer text representations because a word’s vector depends on the surrounding sentence.

They are often more accurate but may be:

- slower,
- more memory-intensive,
- harder to deploy,
- more difficult to interpret,
- and unnecessary for a first baseline.

The chapter repeatedly favors beginning with the simplest representation that can answer the product question.

---

# 17. Vectorizing Images

## 17.1 Raw representation

A digital image is already numerical.

An RGB image is typically represented as a tensor with shape:

```text
height × width × 3 channels
```

Each value records color intensity.

## 17.2 Why raw pixels may be insufficient

Pixel-level distance may not correspond to semantic similarity.

Two images of the same object can differ because of:

- lighting,
- position,
- scale,
- rotation,
- background,
- or camera quality.

## 17.3 Pretrained convolutional networks

Networks trained on large image datasets learn increasingly abstract representations across their layers.

Earlier layers often encode:

- edges,
- colors,
- and textures.

Later layers encode:

- shapes,
- object parts,
- and object-level structure.

The representation immediately before the final classification layer often serves as a useful general-purpose image embedding.

## 17.4 Feature extraction

The chapter demonstrates loading a pretrained VGG16 model and returning activations from the penultimate fully connected layer.

Conceptually:

```text
Image
   ↓
Pretrained image network
   ↓
Penultimate-layer activation
   ↓
Feature vector for clustering or downstream modeling
```

This allows a new project to benefit from representations learned on a much larger dataset.

---

# 18. Transfer Learning

## 18.1 Definition

**Transfer learning** reuses weights learned on one task as the starting point for another task.

This is more than copying the same architecture. The learned parameters are transferred.

## 18.2 Why transfer learning helps

It is especially useful when the new project has a limited labeled dataset.

Common examples:

- ImageNet-pretrained image models,
- language models pretrained on Wikipedia, books, or web text.

## 18.3 Risks

Pretrained models can carry biases, blind spots, and domain assumptions from their original training data.

A clean current dataset does not remove bias already encoded in a pretrained model.

Therefore, evaluate performance across:

- demographic groups,
- domains,
- languages,
- rare classes,
- and production-relevant slices.

---

# 19. Dimensionality Reduction

## 19.1 Problem

Vectors may contain hundreds or thousands of dimensions, making direct visualization impossible.

## 19.2 Definition

Dimensionality reduction maps high-dimensional vectors into fewer dimensions while trying to preserve important structure.

Common techniques discussed:

- PCA,
- t-SNE,
- UMAP.

## 19.3 Purpose in this chapter

Dimensionality reduction is used primarily as an exploratory tool.

A two-dimensional plot can help reveal:

- dense regions,
- isolated outliers,
- apparent clusters,
- label separation,
- overlap between classes,
- and regions requiring manual inspection.

## 19.4 Color by an informative attribute

For classification:

- color points by label.

For unsupervised analysis:

- color points by a feature, source, date, subgroup, or other property.

This can expose whether a feature or label is concentrated in a particular area of the representation space.

## 19.5 Caution

A dimensionality-reduction plot is an approximation. Apparent distances and clusters can be artifacts of the projection.

Any hypothesis from a UMAP or t-SNE plot should be validated with:

- original high-dimensional distances,
- cluster statistics,
- manual inspection,
- or model-based tests.

Do not treat the two-dimensional picture as literal ground truth.

---

# 20. Clustering in Practice

## 20.1 K-means baseline

K-means assigns each example to one of \(k\) clusters based on proximity to a cluster centroid.

Basic workflow:

```python
clusterer = KMeans(n_clusters=3, random_state=10)
cluster_ids = clusterer.fit_predict(vectorized_features)
```

## 20.2 Choosing the number of clusters

There is no universally correct value of \(k\).

Possible aids include:

- the elbow method,
- silhouette analysis,
- cluster size inspection,
- visualization,
- and interpretability.

For exploratory work, the goal is not perfect clustering. The goal is to find useful regions for inspection.

## 20.3 Cluster in the original representation space

The chapter clusters the higher-dimensional vectors and uses UMAP only to display the results.

This distinction matters:

- the clustering algorithm sees the full vector representation,
- while the chart shows an approximate two-dimensional projection.

Cluster boundaries may therefore not match what a viewer would draw by eye on the UMAP plot.

## 20.4 Cluster membership as a feature

Sometimes the data has a complex structure that is useful for prediction. Adding cluster membership as a feature may help a model use that structure.

This should be validated carefully and fitted without leakage.

---

# 21. “Be the Algorithm”

The chapter strongly recommends attempting the prediction task manually.

## 21.1 Why label examples yourself?

Manual labeling helps the practitioner understand:

- how difficult the task is,
- which information is needed,
- whether the labels are meaningful,
- which cases are ambiguous,
- what rules humans use,
- and what features might help a model.

## 21.2 Label even when labels already exist

Existing labels may be:

- noisy,
- weak,
- incomplete,
- inconsistent,
- or based on a different concept than the product target.

For the ML Editor, manually judging question quality tests whether Stack Exchange score is a defensible proxy.

## 21.3 Sample systematically

Do not label only random points.

Review examples from:

- every cluster,
- common feature values,
- rare categories,
- outliers,
- high- and low-label regions,
- and ambiguous boundaries.

This increases the information gained from a small labeling effort.

## 21.4 Record the reasoning process

As you label, note the cues you use.

Possible cues for a good question might include:

- a clear request,
- enough context,
- a specific objective,
- appropriate length,
- and answerable wording.

These observations may become features or labeling guidelines.

## 21.5 Iterative loop

```text
Vectorize data
   ↓
Cluster and visualize
   ↓
Label representative examples
   ↓
Identify useful cues and problems
   ↓
Revise features, labels, or data
   ↓
Repeat
```

---

# 22. Data Trends, Bias, and Spurious Correlations

Manual inspection often reveals patterns. Not all patterns should be used.

## 22.1 Informative patterns

Examples:

- very short questions are often incomplete,
- certain action verbs may signal a concrete request,
- some visual textures may identify an object class.

These may lead to useful features.

## 22.2 Spurious patterns

A pattern may result from how the data was gathered rather than from the true task.

Example:

- Every French tweet in a small sample happens to be labeled negative.

A model may learn language rather than sentiment.

## 22.3 Why spurious features are dangerous

They can produce:

- high training accuracy,
- high validation accuracy when the split shares the same bias,
- and poor production performance when the correlation disappears.

## 22.4 Remedies

Preferred approach:

- collect additional examples that break the false correlation.

Other options:

- rebalance the dataset,
- revise the sampling strategy,
- remove unreliable features,
- add subgroup-based evaluation,
- or redesign the task.

Simply deleting the obvious feature may not be enough because models can reconstruct it from correlated inputs.

---

# 23. Let Data Inform Features and Models

Patterns discovered during inspection should affect:

- preprocessing,
- feature generation,
- sampling,
- labeling,
- model family,
- and evaluation.

The chapter argues that a useful feature representation makes important patterns easier for a model to learn.

---

# 24. Feature Engineering

## 24.1 Definition

Feature engineering creates or transforms inputs so that relevant patterns are easier for a model to capture.

A model does not receive the human concept directly. It receives the numerical representation.

## 24.2 Why feature engineering helps

It is particularly valuable when:

- the dataset is small,
- the signal is subtle,
- the model is simple,
- the raw representation hides structure,
- or interpretability matters.

With enormous clean datasets and highly expressive models, manual feature engineering may be less necessary, but the underlying representation still matters.

---

# 25. Seasonality Example

The chapter uses online retail traffic to demonstrate how date representation changes task difficulty.

Suppose sales increase during the final two weekends of every month.

## 25.1 Raw Unix timestamp

A Unix timestamp is the number of seconds since a reference date.

Although numerical, it does not make “last two weekends” easy to recognize. Similar calendar situations in different months have very different timestamp values.

## 25.2 Extracted date features

Create features such as:

- day of week,
- day of month,
- month,
- weekend status.

This gives the model access to relevant calendar components.

## 25.3 Representation bias

Encoding day of week as integers may impose a false numerical relationship.

For example:

```text
Monday = 1
Friday = 5
```

does not mean Friday is five times Monday.

Depending on the model, alternatives include:

- one-hot encoding,
- cyclical sine/cosine encoding,
- or learned embeddings.

## 25.4 Feature crosses

A feature cross combines two or more variables, often through multiplication or joint categories.

For example:

```text
day_of_week × day_of_month
```

This helps capture interactions in which neither feature is sufficient alone.

The target pattern requires both:

- a weekend,
- and a late date in the month.

## 25.5 Explicit indicator

When domain knowledge strongly supports a pattern, create a direct feature:

```text
is_last_two_weekends
```

This is not cheating. It is encoding a known, production-available signal.

The model still decides how much weight to assign it.

## 25.6 Practical principle

> Make the relevant pattern easy for the model to represent, provided the feature is legitimate and available at prediction time.

---

# 26. ML Editor Features Generated from Data Inspection

The chapter identifies several initial features.

## 26.1 Action verbs

Words such as **can** and **should** correlate with answered questions.

Feature example:

```text
contains_action_verb = 1 or 0
```

These words may signal a specific, answerable request.

## 26.2 Question marks

The presence of a question mark becomes a binary feature.

```text
has_question_mark = 1 or 0
```

This can distinguish a direct question from a statement or incomplete post.

## 26.3 Language-use questions

Questions asking about correct English usage tended to receive fewer answers in this particular community.

A feature is added to identify this topic.

This is dataset-specific and should not be assumed to generalize to every writing platform.

## 26.4 Normalized question length

Very short questions often went unanswered. The project adds a scaled length feature.

Length is a helpful signal, but it should not be interpreted as a complete measure of quality.

## 26.5 Title information

Manual labeling revealed that the title contains important context. The title is therefore incorporated into text features.

This is a good example of manual inspection changing the representation itself.

---

# 27. Robert Munro Interview: Main Lessons

The chapter concludes with practical advice from Robert Munro about finding, labeling, and using data.

---

## 27.1 Begin with the business problem

The product setting determines technical constraints.

For an editor:

- batch editing after submission may tolerate a slower model,
- live suggestions during typing require low latency.

This can rule out otherwise attractive modeling approaches.

The initial model should be:

- easy to implement,
- easy to evaluate,
- and trustworthy enough to teach the team something.

A simple classifier using bag-of-words features may be more useful initially than a complicated sequence model.

---

## 27.2 How much labeled data is needed?

There is no universal threshold, but the interview offers practical guidance for classification:

- roughly 1,000 examples of a rare category may provide enough signal to judge whether an approach is promising,
- around 10,000 examples may support more confidence in model estimates.

These numbers are heuristics, not guarantees. Task complexity, label noise, diversity, and class overlap matter.

## 27.3 Learning curves

Track model performance as the labeled dataset grows.

A **learning curve** helps estimate the marginal value of additional labeled data.

Questions to ask:

- Is performance still improving rapidly?
- Has it plateaued?
- Does a rare class improve when more examples are added?
- Is the bottleneck now label quality rather than quantity?

In many projects, labeling more relevant data produces a larger improvement than tuning the model.

---

# 28. Strategies for Selecting New Data to Label

## 28.1 Uncertainty sampling

Select examples about which the current model is least certain.

For a binary classifier, these may be predictions close to 0.5.

These examples often lie near the current decision boundary and can be highly informative.

### Risk

Uncertainty sampling can overfocus on:

- noisy examples,
- ambiguous cases,
- or one narrow subpopulation.

It should be balanced with representative sampling.

## 28.2 Error model

Create labels indicating whether the current model predicts each example correctly.

Then train a second model to predict model failure.

Use this error model to locate unlabeled examples similar to known mistakes.

Workflow:

```text
Current model predictions
   ↓
Correct/incorrect labels
   ↓
Train error model
   ↓
Score unlabeled examples
   ↓
Label examples predicted to fail
```

## 28.3 Labeling model

Train a classifier to distinguish:

- examples already labeled,
- from examples not yet labeled.

Then select unlabeled examples that look most different from the existing labeled set.

This increases labeled-set coverage.

## 28.4 Preserve a representative test set

Targeted labeling strategies should not replace unbiased evaluation.

A system may improve dramatically on one difficult topic while degrading elsewhere.

Maintain a test set that reflects the real product population, often through random or carefully stratified sampling.

---

# 29. Monitoring and Dataset Updates After Deployment

A deployed model may become less accurate because the data distribution changes.

Signals of drift include:

- changing uncertainty,
- declining business metrics,
- lower user engagement,
- higher correction rates,
- worsening subgroup performance,
- and new types of input.

A drop in a business metric does not prove model drift, but it should trigger investigation.

The dataset should then be updated with:

- recent examples,
- newly important classes,
- common failure cases,
- and representative production inputs.

---

# 30. Complete Chapter Workflow

```text
1. Define the product prediction task
2. Gather a small initial dataset
3. Identify one example, inputs, and target
4. Parse and clean raw records
5. Save deterministic preprocessing outputs
6. Inspect missingness and suspicious records
7. Verify joins and labels manually
8. Count examples overall and per class
9. Compare feature distributions
10. Split data appropriately
11. Fit vectorization on training data only
12. Transform text, images, or tables into vectors
13. Project vectors for exploratory visualization
14. Cluster similar examples
15. Label representative examples manually
16. Validate weak labels
17. Identify bias, gaps, and ambiguous cases
18. Generate features from reliable patterns
19. Gather or relabel additional data
20. Repeat before and after model deployment
```

---

# 31. Common Mistakes to Avoid

## Mistake 1: Searching for a perfect dataset

**Better approach:** Start with a usable sample and refine it based on evidence.

## Mistake 2: Beginning with all available data

**Better approach:** Use a small, representative subset for early inspection and pipeline testing.

## Mistake 3: Treating preprocessing as a black box

**Better approach:** Reproduce and validate calculated fields whenever possible.

## Mistake 4: Assuming missingness is random

**Better approach:** Investigate which examples and groups are missing and why.

## Mistake 5: Trusting existing labels automatically

**Better approach:** Manually label representative examples and measure agreement.

## Mistake 6: Fitting transformations before splitting

**Better approach:** Fit all learned preprocessing on the training set only.

## Mistake 7: Treating UMAP or t-SNE as ground truth

**Better approach:** Use projections to generate hypotheses and validate them elsewhere.

## Mistake 8: Inspecting only random examples

**Better approach:** Sample across clusters, classes, outliers, and difficult regions.

## Mistake 9: Using a correlation without asking why it exists

**Better approach:** Determine whether the pattern is stable, legitimate, and available in production.

## Mistake 10: Responding to poor performance only with model tuning

**Better approach:** Inspect errors, labels, sampling, representation, and coverage first.

---

# 32. Important Terms

| Term | Meaning |
|---|---|
| Dataset iteration | Repeatedly improving data collection, cleaning, labeling, balance, and coverage. |
| Weak label | An imperfect proxy for the desired target. |
| Vectorization | Converting raw data into numerical vectors. |
| Standardization | Rescaling a variable using its mean and standard deviation. |
| One-hot encoding | Representing a category with a binary indicator vector. |
| Bag of words | Text representation based on word counts without preserving order. |
| TF-IDF | Text weighting that reduces the influence of words common across documents. |
| Embedding | A dense learned vector intended to preserve meaningful similarity. |
| Data leakage | Use of information during training that would not be available during real inference. |
| Dimensionality reduction | Mapping high-dimensional vectors into fewer dimensions while preserving some structure. |
| Clustering | Grouping similar examples without using target labels. |
| Feature engineering | Creating or transforming variables to expose useful patterns. |
| Feature cross | A feature representing an interaction between multiple features. |
| Transfer learning | Reusing weights learned on a previous task or dataset. |
| Uncertainty sampling | Labeling examples for which the model is least confident. |
| Learning curve | A plot or analysis of performance as training-set size grows. |
| Data drift | Change in the production data distribution over time. |
| Concept drift | Change in the relationship between inputs and the target. |

---

# 33. Code and Implementation Lessons

## 33.1 Use reproducible preprocessing

- Place cleaning logic in functions.
- save processed datasets with versioned names.
- retain raw data when possible.
- record package versions and parameters.
- avoid manual spreadsheet edits that cannot be reproduced.

## 33.2 Use pipelines for learned transformations

A scikit-learn pipeline can prevent leakage by fitting transformations only on the training folds during cross-validation.

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])
```

## 33.3 Preserve identifiers

Keep a stable identifier for each example so that:

- manual labels can be joined back,
- incorrect records can be traced,
- data revisions can be audited,
- and production errors can be investigated.

## 33.4 Separate raw, processed, and modeled data

A useful project structure is:

```text
data/
  raw/
  interim/
  processed/
  labels/
  splits/
```

This reduces accidental overwriting and clarifies the provenance of each file.

---

# 34. Detailed Analysis of Figures 4-9, 4-10, 4-12, and 4-13

The supplied screenshots clarify how the chapter uses visualization to move from broad data exploration to specific modeling and feature-engineering decisions.

---

## Figure 4-9: UMAP Plot Colored by Whether a Question Was Answered

![UMAP projection colored by whether each question was answered.](<Screenshot 2026-07-08 153839.png>)

### What the figure displays

Each point represents one Stack Exchange question after the question text has been converted into a high-dimensional numerical vector and projected into two dimensions with UMAP.

The colors represent the outcome:

- **blue:** answered question,
- **orange:** unanswered question.

The horizontal and vertical coordinates do not correspond to named features. They are coordinates created by UMAP to preserve portions of the high-dimensional neighborhood structure.

### Main visual pattern

The projection contains:

- one large group in the upper-right,
- one smaller group in the lower-left,
- several tiny isolated groups,
- and at least one distant outlier near the bottom.

Within both major groups, answered and unanswered questions are heavily intermixed. There is no clean boundary that separates the two outcomes.

### Interpretation

The text representation appears to organize questions into different semantic or stylistic regions, but those regions do not correspond directly to whether a question received an answer.

In practical terms:

- questions that are close in the embedding space may discuss similar topics or use similar language,
- but similar wording alone does not determine whether a question is answered,
- and answer status is probably influenced by several factors that are not captured by the text embedding alone.

Possible missing factors include:

- specificity,
- timing,
- community activity,
- topic popularity,
- title quality,
- question length,
- formatting,
- and whether the request is objectively answerable.

### Modeling implication

Because the two labels overlap substantially, a simple classifier based only on this two-dimensional projection would likely perform poorly.

This does **not** mean that the full high-dimensional vectors are useless. UMAP deliberately compresses information, so some class-separating structure may be lost. However, the plot provides evidence that the task is not trivially separable.

The project should therefore consider:

- additional engineered features,
- cluster-specific analysis,
- better labels,
- title information,
- and possibly a more expressive model.

### Important caution

The apparent distance between two points on the chart should not be treated as an exact measurement. UMAP is an approximate visualization. The plot should be used to generate inspection questions, not as proof that particular examples are truly far apart or belong to objectively distinct classes.

### Questions prompted by the figure

- What kinds of questions make up the lower-left group?
- Why are the tiny islands separated from the major groups?
- Does the distant outlier represent corrupted text, an unusually long post, or a legitimate rare case?
- Are some local regions more heavily unanswered than the plot initially suggests?
- Would coloring by topic, question length, or language reveal what created the major groups?

---

## Figure 4-10: UMAP Projection Colored by K-Means Cluster

![Figure 4-10. UMAP projection of questions colored by cluster assignment.](<Screenshot 2026-07-08 153855.png>)

### What the figure displays

The same general question representation is shown in two dimensions, but the colors now represent clusters assigned by a clustering algorithm rather than answer status.

The visible cluster assignments include:

- a blue cluster concentrated in the lower-left and some isolated points,
- a green cluster occupying much of the upper portion of the large upper-right group,
- and a yellow cluster concentrated toward the lower portion of the upper-right group.

### Main visual pattern

The lower-left group is assigned almost entirely to one cluster, indicating that it is substantially different from the large upper-right group in the original vector space.

The upper-right group is divided into green and yellow clusters. These colors overlap on the two-dimensional plot instead of forming a perfectly clean visual split.

### Why the clusters do not perfectly match the visible two-dimensional shapes

K-means was fitted to the original higher-dimensional vectors, while UMAP was used only to display those vectors in two dimensions.

As a result:

- the clustering algorithm had access to information that the two-dimensional plot no longer shows,
- points that look close on the plot may differ in omitted dimensions,
- and points that look somewhat separated may still be similar in the original representation.

The overlap between green and yellow is therefore not automatically evidence that K-means failed. It may reflect information loss or distortion introduced by UMAP.

### Relationship to Figure 4-9

Figure 4-9 shows that answer labels are mixed within the large regions. Figure 4-10 shows that the text vectors nevertheless contain recognizable internal structure.

Together, the figures suggest:

1. the embedding can distinguish types of questions,
2. those types are not identical to answered versus unanswered status,
3. and each cluster should be manually inspected to discover what it represents.

A cluster might correspond to:

- a topic,
- a writing style,
- a post format,
- a vocabulary pattern,
- or a type of request.

### Modeling implication

Cluster membership may be useful for:

- selecting representative examples to label,
- performing error analysis,
- identifying sparse subgroups,
- or creating an additional model feature.

Cluster membership should not be assumed to be predictive without validation. It may summarize topic rather than quality.

### Outliers and small islands

The isolated points and tiny groups deserve manual inspection. They may represent:

- rare but valid question types,
- preprocessing errors,
- extremely short or long text,
- unusual characters,
- duplicate templates,
- or embedding failures.

Removing them automatically would be premature. First determine what they are and whether they are relevant to production.

---

## Figure 4-12: Using Bokeh to Inspect and Label Data

![Interactive Bokeh visualization used to inspect an individual unanswered question.](<Screenshot 2026-07-08 153910.png>)

### What the figure displays

The Bokeh visualization allows a user to select or hover over an individual point and inspect the underlying text and label.

The displayed example says, in substance, that the writer wants general feedback and welcomes any tips or suggestions. Its recorded outcome is:

```text
got_answer: False
```

### Why this example may have gone unanswered

The request is polite, but it is difficult to answer effectively because it is broad and underspecified.

The post does not clearly provide:

- the actual writing sample,
- a focused question,
- the type of feedback requested,
- a particular problem to solve,
- or objective criteria for a useful answer.

A potential responder would not know whether to comment on:

- grammar,
- structure,
- plot,
- voice,
- style,
- or general writing technique.

This makes the question difficult to answer in a concrete and reusable way.

### Why the example is useful for the ML Editor

The example supports the idea that answerability depends on more than readability.

The text is understandable, yet the request lacks specificity. This distinction is important:

- **readability** asks whether the text is easy to understand,
- **answerability** asks whether the reader can provide a focused response,
- **quality** may include both, along with relevance and sufficient context.

A model based only on Flesch readability could incorrectly consider this a good question.

### Possible features suggested by the example

Manual inspection might motivate features related to:

- presence of a direct question,
- presence of a question mark,
- specificity of the requested feedback,
- whether supporting content is included,
- action-oriented phrases such as “how can,” “should I,” or “what is,”
- vague phrases such as “any tips” or “any suggestions,”
- and the amount of contextual information.

Some of these features are difficult to express with simple word counts, which may justify richer language representations later.

### Label-validation lesson

This single example is consistent with the weak label `got_answer = False`, but one example does not prove that the label is always accurate.

The correct workflow is to inspect multiple examples from the same region and ask:

- Do most appear vague?
- Are any strong questions mislabeled as unanswered?
- Did some go unanswered for reasons unrelated to writing quality?
- Do multiple human reviewers agree?

The interactive plot makes this repeated inspection faster.

---

## Figure 4-13: Extracted Date Features and Feature Crosses

![Figure 4-13. Comparison of day-of-week, day-of-month, and crossed date features.](<Screenshot 2026-07-08 153927.png>)

### What the figure displays

The chart compares three numerical representations over time:

- **DoW:** day of week,
- **DoM:** day of month,
- **Cross:** a combination of the day-of-week and day-of-month values.

The red boxes highlight late-month weekend periods.

### Day-of-week feature

The day-of-week line repeatedly rises and resets each week.

This representation exposes weekly periodicity, which a raw Unix timestamp would hide. However, day of week alone cannot identify whether a weekend occurs near the beginning or end of a month.

### Day-of-month feature

The day-of-month line rises from the beginning toward the end of each month and then resets.

This exposes monthly position, but it cannot distinguish weekends from weekdays.

### Feature cross

The cross combines both values. Its largest peaks tend to occur when:

- the day-of-month value is high,
- and the day-of-week value is also high.

This makes some late-month weekend observations stand out more strongly than they would under either feature alone.

### Why the cross helps

Suppose high sales occur during the final weekends of a month.

Neither individual feature is sufficient:

- late weekdays have a high day-of-month value but are not weekends,
- early weekends have the correct day of week but are not late in the month.

The interaction feature gives the model a stronger signal for the joint condition.

### Important limitation visible in the chart

The numerical day-of-week coding introduces an arbitrary scale. In the chapter’s example, Saturday and Sunday may receive very different numeric values even though both are weekends.

Therefore, multiplying day of week by day of month may emphasize one weekend day more strongly than the other. The feature cross is helpful, but it is not a perfect semantic representation of “late-month weekend.”

This illustrates the broader warning that feature encodings introduce assumptions.

### Better alternatives

Depending on the model and business rule, clearer features could include:

```text
is_weekend
is_last_half_of_month
is_last_two_weekends
```

A combined binary indicator such as `is_last_two_weekends` directly represents the known pattern and avoids the arbitrary magnitude imposed by integer day-of-week encoding.

Other options include:

- one-hot encoding the day of week,
- crossing `is_weekend` with a late-month indicator,
- or using cyclical sine and cosine encodings for recurring calendar variables.

### Main lesson

The figure demonstrates a progression:

```text
Raw date
   ↓
Extract meaningful components
   ↓
Represent interactions
   ↓
Create a direct domain feature when justified
```

Each step makes the relevant pattern easier for the model to learn.

---

## Combined Meaning of the Four Figures

The figures illustrate a connected workflow:

1. **Figure 4-9:** visualize the relationship between the current representation and the weak label.
2. **Figure 4-10:** organize the vector space into clusters for systematic inspection.
3. **Figure 4-12:** inspect individual examples inside those regions and identify human decision rules.
4. **Figure 4-13:** convert discovered or known patterns into representations that a model can learn more easily.

This is the chapter’s central data-development loop:

```text
Represent
   ↓
Visualize and cluster
   ↓
Inspect and label
   ↓
Identify patterns and problems
   ↓
Engineer better features or gather better data
   ↓
Repeat
```

The purpose of visualization is not merely to create an attractive chart. Each figure supports a concrete decision about labels, features, data coverage, or the next modeling experiment.

---

# 35. Review Questions

1. Why should a production dataset be treated as part of the product rather than as a fixed input?
2. Why can beginning with a small dataset accelerate an ML project?
3. What is the difference between discovering an insight and building a product feature from it?
4. What four areas should be checked in an initial data-quality review?
5. Why should preprocessing be serialized before repeated model experiments?
6. What is a weak label, and what weak labels are used for the ML Editor?
7. How can summary statistics reveal either a useful feature or a dataset shortcut?
8. Why does clustering require vectorized data?
9. Why should clustering be performed on the original vectors rather than only on a two-dimensional UMAP projection?
10. Why should practitioners manually label examples even when labels already exist?
11. What is data leakage during normalization?
12. Why is one-hot encoding usually safer than assigning arbitrary integers to nominal categories?
13. What information does a bag-of-words model discard?
14. How do pretrained embeddings differ from TF-IDF?
15. Why can transfer learning introduce bias?
16. What is the purpose of dimensionality reduction during data exploration?
17. Why are t-SNE and UMAP plots considered hypothesis-generating tools rather than proof?
18. How do feature crosses help a model?
19. Why is an explicit feature such as `is_last_two_weekends` legitimate?
20. What is uncertainty sampling, and what is its main risk?
21. How does an error model guide additional labeling?
22. Why should targeted labeling be accompanied by a representative test set?
23. What signals might indicate that a deployed dataset needs updating?
24. Why can additional high-quality data outperform model tuning?

---

# 36. Concise Exam-Style Summary

Chapter 4 explains how to acquire and inspect an initial dataset before training a machine learning model. The main principle is that data is an evolving part of an ML product, not a fixed prerequisite. Practitioners should start with a small, manageable dataset and evaluate its format, quality, quantity, and distribution. Raw records should be parsed, cleaned, validated, and serialized so preprocessing does not slow experimentation.

The chapter then introduces vectorization for tabular data, text, and images. Numerical features may be standardized, categorical features one-hot encoded, text represented with TF-IDF or embeddings, and images represented with features extracted from pretrained neural networks. All learned preprocessing must be fitted on the training set only to avoid data leakage.

Vectorized data can be explored using dimensionality reduction and clustering. These tools help organize individual examples, identify dense and sparse regions, reveal possible bias, and guide manual labeling. Practitioners should “be the algorithm” by labeling representative examples themselves, even when existing labels are available, because this reveals ambiguity, weak labels, and useful human decision rules.

Finally, the chapter shows how patterns discovered in the data should inform feature engineering and data collection. Features should make genuine, production-available patterns easier for a model to learn. Examples include date components, feature crosses, action-verb indicators, question marks, title information, and normalized text length. Robert Munro’s interview reinforces that teams should begin with the business problem, gather diverse data, use active-labeling strategies carefully, preserve a representative test set, and continue updating the dataset as production behavior changes.

---

# 37. Key Takeaways

1. **Start with a small dataset that can be inspected quickly.**
2. **Treat the dataset as an evolving part of the ML product.**
3. **Inspect format, quality, quantity, and distribution before modeling.**
4. **Validate joins, labels, and preprocessing through manual examples.**
5. **Save deterministic preprocessing results to speed iteration.**
6. **Fit vectorizers and scalers on training data only.**
7. **Use vectorization, dimensionality reduction, and clustering to inspect structure.**
8. **Manually label representative examples to understand the task.**
9. **Investigate whether patterns are genuine or artifacts of collection.**
10. **Use reliable patterns to improve features, models, and data-gathering plans.**
11. **Additional representative data often matters more than a more complex model.**
12. **Continue monitoring and revising the dataset after deployment.**
