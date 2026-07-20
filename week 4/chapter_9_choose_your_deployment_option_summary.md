# Chapter 9 Study Guide: Choose Your Deployment Option

**Book:** *Building Machine Learning Powered Applications*  
**Chapter focus:** Selecting an appropriate deployment architecture for an ML-powered product

---

## 1. Chapter Overview

Once a machine learning model has been developed, evaluated, and improved, it must be made available to users or other software systems. **Deployment** is the process of placing the model within a usable system so that it can receive data, generate predictions, and return useful results.

This chapter compares several common deployment approaches:

1. **Server-side streaming**
2. **Server-side batch prediction**
3. **Hybrid batch and streaming**
4. **Client-side, on-device deployment**
5. **Client-side, browser-based deployment**
6. **Federated learning**

The correct choice depends on the product’s operational requirements—not only on the model itself.

### Main deployment considerations

When choosing a deployment method, evaluate:

- **Latency:** How quickly must the prediction be returned?
- **Feature availability:** Are the necessary inputs available in advance or only when the user makes a request?
- **Hardware:** Can the client device run the model efficiently?
- **Network access:** Must the application work offline or under poor connectivity?
- **Privacy:** Can sensitive data be sent to and stored on a server?
- **Cost:** Who provides the computing resources—the organization or the user’s device?
- **Scalability:** Can the system handle increased traffic?
- **Reliability:** What happens if the server or network becomes unavailable?
- **Model complexity:** Is the model small enough to run locally?
- **Engineering complexity:** How difficult will the system be to build, operate, update, and monitor?

> **Central lesson:** Start with the simplest deployment approach that satisfies the product’s requirements. Add complexity only when there is evidence that it is necessary.

---

# 2. Server-Side Deployment

In **server-side deployment**, the model and inference code run on infrastructure controlled by the organization. A client sends a request to a server, the server processes the request, and the result is returned to the client.

This design fits naturally into traditional web development because the ML model can be exposed as an application endpoint or API.

## Basic server-side flow

```text
Client request
      ↓
Web server / API
      ↓
Validation and data gathering
      ↓
Preprocessing
      ↓
Model inference
      ↓
Postprocessing
      ↓
Prediction returned to client
```

Server-side inference is commonly implemented through either:

- **Streaming inference**
- **Batch inference**

---

# 3. Streaming Applications and APIs

A **streaming application** processes requests as they arrive. Each request is handled immediately and usually results in a separate inference call.

The user of the endpoint may be:

- A person interacting with an application
- A web or mobile application
- Another internal service
- An automated system that depends on model predictions

For example, a website-traffic forecasting model might send predictions to an internal infrastructure service that increases or decreases server capacity.

## 3.1 Streaming inference pipeline

A typical streaming request passes through the following steps.

### Step 1: Validate the request

The application checks that the incoming request is usable.

Validation may include:

- Confirming that required fields are present
- Checking data types and valid ranges
- Rejecting malformed input
- Verifying authentication or authorization
- Confirming that the user has permission to access the model

Validation prevents invalid, dangerous, or unauthorized data from reaching the model.

### Step 2: Gather additional data

The original request may not contain every feature needed by the model.

The system may need to retrieve:

- User profile information
- Historical behavior
- Current inventory
- Geographic information
- Recent transactions
- External contextual data

This stage can create additional latency because it may require database queries or service calls.

### Step 3: Preprocess the data

The incoming data must be transformed into the same representation expected by the trained model.

Examples include:

- Cleaning text
- Normalizing numeric values
- Encoding categories
- Resizing images
- Creating features
- Ordering columns correctly
- Handling missing values

The production preprocessing pipeline should match the preprocessing used during model training.

### Step 4: Run the model

The processed features are passed to the model, which produces a prediction, probability, score, ranking, or recommendation.

### Step 5: Postprocess the result

Raw model output is often not directly suitable for users.

Postprocessing may include:

- Converting scores into human-readable labels
- Applying business rules
- Clipping values to acceptable ranges
- Ranking alternatives
- Adding confidence information
- Rejecting unsafe or implausible results
- Formatting the output

### Step 6: Return the result

The final response is sent to the client, usually as:

- HTML
- JSON
- A rendered application view
- A message to another internal service

## 3.2 Simplified Flask example

The chapter illustrates streaming deployment with a lightweight Flask application.

```python
from flask import Flask, render_template, request

@app.route("/v3", methods=["POST", "GET"])
def v3():
    return handle_text_request(request, "v3.html")

def handle_text_request(request, template_name):
    if request.method == "POST":
        question = request.form.get("question")
        suggestions = get_recommendations_from_input(question)
        payload = {"input": question, "suggestions": suggestions}
        return render_template("results.html", ml_result=payload)
    else:
        return render_template(template_name)
```

### What the code does

#### `@app.route("/v3", methods=["POST", "GET"])`

This decorator registers `/v3` as an application route.

The route accepts two HTTP methods:

- **GET:** Display the initial input page
- **POST:** Receive user input and run the model

#### `v3()`

The route handler passes the request and the appropriate HTML template to `handle_text_request()`.

#### GET request behavior

When a user first visits the page, the browser sends a GET request.

The application returns the input template:

```python
return render_template(template_name)
```

#### POST request behavior

When the user submits the form:

1. The application extracts the text from the form.
2. It passes the text to the recommendation function.
3. It builds a payload containing the input and model output.
4. It renders the results page.

```text
User enters text
      ↓
POST request
      ↓
Retrieve form value
      ↓
Run recommendation model
      ↓
Create output payload
      ↓
Render results page
```

## 3.3 Advantages of streaming deployment

- Predictions use the most current information.
- Results can be returned immediately.
- The model can use inputs that exist only at request time.
- APIs integrate naturally with web applications and internal services.
- A small prototype can be implemented quickly.
- The model and dependencies remain centrally controlled.

## 3.4 Limitations of streaming deployment

- Each request creates inference work.
- Traffic spikes can delay requests or cause failures.
- Server capacity must grow with demand.
- Autoscaling and load balancing may be necessary.
- Network communication adds latency.
- The organization pays the inference and infrastructure costs.
- The server becomes a potential central failure point.
- Sending data to the server may introduce privacy risk.

## 3.5 When streaming is necessary

Streaming is appropriate when both of the following are true:

1. The model requires information that becomes available only at prediction time.
2. The result is needed immediately.

### Example: Ride-hailing price prediction

A ride-hailing price estimate may depend on:

- The user’s current location
- The requested destination
- Current driver availability
- Current traffic or demand

These values are time-sensitive and cannot be fully computed in advance. The user also needs the price immediately before deciding whether to request the trip.

### Streaming decision rule

Use streaming when:

```text
Features are available only at request time
                    +
Prediction must be returned immediately
                    =
Streaming inference
```

---

# 4. Batch Predictions

A **batch prediction system** processes many examples together at a scheduled or predetermined time. The system stores the resulting predictions so they can be retrieved later.

Batch inference is most appropriate when the features required by the model are available **before** the prediction is needed.

## 4.1 Batch workflow

```text
Scheduled batch time
        ↓
Load many examples
        ↓
Preprocess examples
        ↓
Run model on all examples
        ↓
Store predictions
        ↓
Later: retrieve prediction when needed
```

The workflow has two distinct phases.

### Batch-computation phase

- Collect the relevant examples
- Create features
- Run the model
- Save the predictions

### Retrieval phase

- A user or service requests a result
- The system retrieves the precomputed prediction
- No model inference is required at that moment

## 4.2 Example: Lead scoring

A sales organization may want a ranked list of promising companies for each salesperson.

Possible features include:

- Historical email conversations
- Company characteristics
- Market trends
- Past sales outcomes
- Engagement data

These features are already available before the salesperson begins work. A nightly job can score all prospects and store the ranked results so they are ready the next morning.

## 4.3 Example: Morning message prioritization

An application that ranks unread messages for a user can process them as a morning batch.

The application does not necessarily need to classify every message the instant it arrives. Instead, it can:

1. Collect unread messages.
2. Score them in the morning.
3. Store a prioritized list.
4. Display the list when the user opens the application.

## 4.4 Advantages of batch prediction

- Resource needs are known before the job begins.
- Work can be parallelized efficiently.
- Infrastructure can be allocated for a predictable period.
- Predictions can be generated during lower-cost or low-traffic periods.
- User-facing retrieval is fast because the result is already computed.
- The system can behave similarly to a cache.
- Processing many examples together may improve hardware utilization.
- Temporary scaling can be easier than continuously supporting peak traffic.

## 4.5 Limitations of batch prediction

- Predictions may become stale.
- It is unsuitable when required features arrive only at request time.
- It is unsuitable when every result must reflect the latest state.
- The system must store and manage predictions.
- Batch failures can affect many examples at once.
- A schedule must be selected and maintained.
- New or uncommon requests may not have a precomputed result.

## 4.6 Important clarification

Batch prediction does not necessarily reduce the total number of examples that must be scored. The model may still run once for every example.

Its efficiency comes from:

- Processing at a controlled time
- Grouping work
- Parallelizing computation
- Improving resource utilization
- Avoiding user-facing inference latency

---

# 5. Hybrid Batch and Streaming Systems

A **hybrid deployment** combines batch and streaming inference.

The system precomputes predictions whenever possible. At request time, it:

- Retrieves a stored prediction when one is available and current
- Runs streaming inference when the result is missing or outdated

## Hybrid workflow

```text
Request arrives
      ↓
Is a current prediction stored?
      ├── Yes → Return stored prediction
      └── No  → Run model now → Return result
```

## Advantages

- Common predictions can be returned quickly.
- Unusual or new requests can still be handled.
- Precomputation reduces some real-time inference work.
- Results can remain available even when not everything can be predicted in advance.

## Disadvantages

- Both batch and streaming pipelines must be maintained.
- The system needs rules for determining when a prediction is stale.
- Data consistency becomes harder.
- Monitoring and testing become more complex.
- Different code paths may produce inconsistent results.
- Operational costs and maintenance burden increase.

> **Key trade-off:** A hybrid system can improve responsiveness and coverage, but it creates significantly more engineering complexity.

---

# 6. Client-Side Deployment

In **client-side deployment**, model inference runs on the user’s device instead of on the organization’s server.

Possible client devices include:

- Laptops
- Desktop computers
- Smartphones
- Tablets
- Smart speakers
- Cameras
- Doorbells
- Other connected devices

The model is still usually trained centrally. After training, it is packaged or distributed to the client for inference.

## Client-side flow

```text
Model trained on central infrastructure
                 ↓
Model distributed to client device
                 ↓
User provides input
                 ↓
Device runs preprocessing and inference
                 ↓
Prediction displayed locally
```

## 6.1 Advantages of client-side inference

### Lower server infrastructure cost

The user’s device provides the inference compute. The organization does not need to run one server-side inference job for every request.

### Better scalability

If the user base grows, the users also bring additional computing resources through their devices. This can reduce the need for server capacity to grow directly with inference traffic.

### Reduced network latency

Input data does not need to travel to a remote server and back. For some applications, network transfer takes longer than the model calculation itself.

### Offline functionality

The model can continue to work when:

- The user has no internet access
- The connection is unreliable
- The application is used in a remote location
- The network is slow or expensive

### Improved privacy

Sensitive input can remain on the device.

This reduces the need to:

- Transmit personal data
- Temporarily store it on a server
- Protect it within centralized infrastructure

Keeping sensitive data off the server lowers exposure risk.

## 6.2 Limitations of client-side inference

- Client hardware is less powerful than many servers.
- Different devices may produce different performance.
- Mobile devices have battery and heat constraints.
- Models may need to be compressed.
- Accuracy may decline after optimization.
- Device-specific engineering may be required.
- Updating deployed models can be more complicated.
- The organization has less control over the execution environment.
- Debugging failures across many devices is difficult.

## Server-side versus client-side latency

A server may run the model faster, but the total response time also includes network transfer.

A client may run the model more slowly, but avoids most network delay.

```text
Server-side total time:
Upload input + network delay + server inference + download result

Client-side total time:
Local preprocessing + local inference
```

The correct comparison is therefore not simply “Which processor is faster?” It is:

> **Which complete path returns an acceptable result faster and more reliably?**

---

# 7. Native On-Device Deployment

In native on-device deployment, a trained model is packaged directly inside a mobile, desktop, or embedded application.

Because client hardware is constrained, models should generally be made as small and efficient as possible.

## 7.1 Model optimization methods

### Use a simpler model

A smaller model class may require less memory and compute.

### Reduce the number of parameters

Neural networks with fewer layers, units, or weights are often easier to deploy.

### Pruning

**Pruning** removes model weights that contribute little to the result, often weights whose values are near zero.

Potential benefit:

- Smaller model
- Fewer operations
- Lower memory use

### Quantization

**Quantization** lowers the numeric precision used to store weights or perform calculations.

For example, a model may move from high-precision floating-point values to lower-precision representations.

Potential benefit:

- Smaller model files
- Faster computation
- Lower memory requirements
- Lower energy usage

Possible cost:

- Slight loss in predictive performance

### Reduce the feature set

Using fewer input features can reduce:

- Preprocessing time
- Memory use
- Sensor or data requirements
- Inference time

### Use mobile deployment libraries

Frameworks such as **TensorFlow Lite** provide tools for:

- Converting trained models
- Compressing models
- Quantizing weights
- Running models efficiently on mobile hardware

## 7.2 Accuracy versus operational value

Most models experience some performance loss when compressed or simplified for on-device use.

That loss may be acceptable when local execution provides greater product value.

### Example: Predictive keyboard

A predictive keyboard should respond quickly and work consistently. The advantages of local inference may outweigh a small loss in next-word prediction accuracy.

### Example: Plant-identification application

A hiker may need to identify a plant where internet service is unavailable. Offline functionality is therefore more important than using the largest and most accurate cloud model.

### Example: Translation application

A traveler may use a translation tool abroad without reliable network access. A smaller local model may be more useful than a more accurate model that cannot be reached.

### Example: Photo-filter application

Users may not want personal photos uploaded and stored remotely. Keeping the entire process on the device can become an important privacy feature.

## 7.3 When a server may still be preferable

Server deployment is often more appropriate when:

- The model is too large for typical client devices.
- The product depends on state-of-the-art model quality.
- Accuracy degradation is unacceptable.
- Inference is faster through the cloud even after network delay.
- The model requires frequently updated centralized information.
- Client-device compatibility would require excessive engineering effort.

## 7.4 Engineering cost

Compression and hardware optimization are not free.

Teams may need to:

- Quantize and prune the model
- Benchmark across devices
- Handle different operating systems
- Support different processors
- Manage model updates
- Test battery and memory usage

On-device deployment is worthwhile only when the benefits in privacy, latency, offline availability, reliability, or infrastructure cost justify the additional work.

---

# 8. Browser-Side Deployment

A browser-side model runs on the client device through a web browser, usually using JavaScript.

This approach combines parts of web deployment and local deployment:

- Users open a web page.
- The page downloads the model and its weights.
- The browser runs inference locally.
- The user does not need to install a separate native application.

## 8.1 TensorFlow.js

The chapter highlights **TensorFlow.js**, a framework that can:

- Run differentiable models in JavaScript
- Perform inference in the browser
- Train some models in the browser
- Load models originally trained in languages such as Python
- Use browser-supported acceleration

## 8.2 WebGL acceleration

TensorFlow.js can use **WebGL**, allowing the browser to perform computation through the client device’s GPU when available.

This may improve inference speed compared with ordinary JavaScript execution.

## 8.3 Advantages of browser-side deployment

- No native application installation is required.
- Inference uses the client’s computing resources.
- Input data can remain on the device.
- Server inference costs are reduced.
- A single web implementation may work across multiple devices.
- Less device-specific engineering may be required than native deployment.
- The organization may only need to serve the web page and model files.

## 8.4 Limitations of browser-side deployment

- The model must be downloaded to the client.
- Download time increases with model size.
- Bandwidth use may increase.
- The model may be downloaded again when the page is reopened, depending on caching behavior.
- Browser and device capabilities vary.
- Large models may create an unacceptable startup delay.
- The model and weights are more exposed to the client environment.

## 8.5 Appropriate model size

Browser-side deployment is most practical when the model is small enough to download quickly—often a few megabytes or less.

A lightweight model can make browser inference an attractive way to reduce server costs without requiring a fully native mobile application.

---

# 9. Federated Learning: A Hybrid Training Approach

The earlier approaches primarily address where a **trained model performs inference**. Federated learning also changes where and how the model learns.

In a federated learning system:

1. Each client has a local model.
2. The local model learns from the user’s local data.
3. The client sends aggregated model updates to a server.
4. The server combines updates from many clients.
5. An improved shared model is distributed back to clients.

## Federated learning flow

```text
Central model sent to clients
             ↓
Clients train locally on private data
             ↓
Clients send aggregated model updates
             ↓
Server combines updates
             ↓
Improved model returned to clients
```

## 9.1 Personalization

A single global model may not perform equally well for every user.

This is especially relevant in applications involving:

- Content recommendation
- Writing assistance
- Healthcare
- Keyboard prediction
- User-specific behavior

Federated learning can allow clients to share a general model architecture while learning parameter values influenced by individual usage patterns.

## 9.2 Privacy benefit

The raw user data stays on the client.

Instead of uploading the complete local dataset, the client sends model updates that may be aggregated and anonymized.

This can reduce centralized collection of sensitive information.

However, the chapter emphasizes that privacy still requires careful engineering. The updates must be properly protected and anonymized.

## 9.3 Shared learning benefit

Users receive personalized models while still benefiting from patterns learned across the broader population.

Conceptually:

```text
Local personalization
         +
Knowledge aggregated across users
         =
Federated learning
```

## 9.4 Complexity and risks

Federated learning is more difficult than training one centralized model.

Challenges include:

- Monitoring many local models
- Handling inconsistent client hardware
- Handling clients that disconnect
- Combining updates from non-identical user data
- Confirming that local models perform well
- Preventing model updates from revealing sensitive information
- Managing model versions
- Protecting the aggregation system
- Testing fairness across users

## 9.5 Example: Gboard

Google’s Gboard keyboard is used as an example of federated learning.

Writing style varies substantially across users, making it difficult for one universal model to perform equally well for everyone. Training at the user level helps the system learn local language patterns while still benefiting from aggregate improvements.

---

# 10. Deployment Options Comparison

| Deployment option | Prediction timing | Where inference runs | Best when | Main advantages | Main disadvantages |
|---|---|---|---|---|---|
| Streaming API | Per request | Server | Current inputs are needed and predictions must be immediate | Fresh predictions, centralized control, easy API integration | Network latency, server cost, scaling burden |
| Batch prediction | Scheduled | Server | Inputs are known in advance and predictions can be precomputed | Efficient resource use, fast retrieval, predictable workload | Stale results, storage needs, unsuitable for real-time features |
| Hybrid batch + streaming | Precomputed when possible; live otherwise | Server | Most requests are predictable but some require live inference | Fast common cases plus full coverage | Highest operational complexity |
| Native on-device | Per request | Client device | Offline use, privacy, or low network latency is essential | Offline, private, lower server costs | Model compression, device limitations, maintenance burden |
| Browser-side | Per request after page/model load | Browser/client | A small model should run locally without app installation | Cross-device web access, local inference, lower server cost | Model download time, bandwidth, browser variability |
| Federated learning | Local inference and local training | Clients plus aggregation server | Personalization and privacy are central | Personalized models, raw data stays local | Complex training, monitoring, aggregation, and privacy protection |

---

# 11. Decision Framework

A deployment decision can be organized as a series of questions.

## Question 1: When are the features available?

### Only at request time

Favor **streaming inference**.

Examples:

- Current location
- Live inventory
- Current traffic
- Current market state
- Recent sensor readings

### Available in advance

Consider **batch prediction**.

Examples:

- Nightly lead scoring
- Daily message ranking
- Weekly customer-risk scoring
- Precomputed recommendations

---

## Question 2: How quickly is the result needed?

### Immediately

Use:

- Streaming server inference
- Native on-device inference
- Browser-side inference

### Later or on a schedule

Use batch inference.

---

## Question 3: Must the application work offline?

### Yes

Use:

- Native on-device deployment
- Browser deployment with appropriate offline caching, when feasible

### No

Server-side deployment remains an option.

---

## Question 4: Is the input sensitive?

### Highly sensitive

Prefer keeping data on the client when possible.

Possible approaches:

- On-device inference
- Browser-side inference
- Federated learning

### Data may safely be transmitted

Server-side deployment may be simpler.

---

## Question 5: Can the client device run the model?

### Yes, after reasonable optimization

Consider client-side deployment.

### No

Use a server or redesign the model.

---

## Question 6: Is centralized control important?

A server makes it easier to:

- Update the model
- Enforce a single version
- Monitor behavior
- Patch problems
- Control dependencies
- Prevent direct distribution of model files

Client deployment reduces that control.

---

## Question 7: Is added complexity justified?

Use the least complex architecture that satisfies the product requirements.

A reasonable progression is:

```text
Prototype
   ↓
Simple streaming endpoint or batch job
   ↓
Measure real bottlenecks
   ↓
Add scaling, caching, hybrid inference, or client deployment only if needed
```

---

# 12. Practical Selection Examples

## Scenario A: Fraud score during checkout

Requirements:

- Current transaction data is necessary.
- The decision must be made immediately.
- The organization needs centralized control.

**Likely choice:** Streaming server-side inference

---

## Scenario B: Daily customer-churn list

Requirements:

- Customer history is already stored.
- Managers need a list each morning.
- Minute-by-minute updates are unnecessary.

**Likely choice:** Batch prediction

---

## Scenario C: Product recommendation catalog

Requirements:

- Most recommendations can be generated overnight.
- New products or unusual users still need a result.

**Likely choice:** Hybrid batch and streaming

---

## Scenario D: Offline plant identification

Requirements:

- The application may be used without a network.
- Image data may be private.
- Some accuracy loss is acceptable.

**Likely choice:** Native on-device inference

---

## Scenario E: Small interactive model on a website

Requirements:

- The model is only a few megabytes.
- Users should not install an application.
- Server inference cost should remain low.

**Likely choice:** Browser-side inference

---

## Scenario F: Personalized mobile keyboard

Requirements:

- Writing patterns differ by user.
- Raw typed text should remain private.
- The model should benefit from learning across users.

**Likely choice:** Federated learning

---

# 13. Key Trade-Offs to Remember

## Freshness versus efficiency

- Streaming gives fresher predictions.
- Batch gives more predictable and efficient processing.

## Accuracy versus portability

- Large server models may be more accurate.
- Smaller client models are easier to run locally.

## Central control versus privacy

- Server deployment gives the organization more control.
- Client deployment keeps more data with the user.

## Infrastructure cost versus engineering cost

- Server deployment can create ongoing compute costs.
- Client deployment can lower inference costs but require more optimization and compatibility work.

## Simplicity versus coverage

- A single batch or streaming pipeline is simpler.
- A hybrid pipeline covers more cases but is harder to maintain.

## Compute speed versus network speed

- Servers usually compute faster.
- Clients avoid network delay.
- The relevant metric is end-to-end response time.

---

# 14. Common Misunderstandings

## “Batch means fewer predictions”

Not necessarily. Batch processing may still score every example. Its advantage is coordinated, predictable, and parallel execution.

## “Client-side is always faster”

Not necessarily. Client hardware may be slower. It is faster only when avoiding network transfer outweighs the slower local computation.

## “Client-side deployment requires training on the device”

No. A model can be trained centrally and distributed to the device only for inference.

## “Federated learning means no privacy risk”

No. Raw data may remain local, but model updates still require careful aggregation, anonymization, and security controls.

## “The most accurate model is automatically the best deployment choice”

No. A slightly less accurate model may produce a better product if it is faster, private, reliable, inexpensive, or usable offline.

## “Hybrid systems are always better”

No. They increase complexity and should be used only when the benefits justify maintaining two inference paths.

---

# 15. Oral-Exam Ready Explanation

A strong concise explanation of the chapter is:

> Chapter 9 explains that model deployment is a systems-design decision. A streaming API is appropriate when inputs arrive at request time and a result is needed immediately. Batch inference is appropriate when inputs are known in advance and predictions can be precomputed. A hybrid system uses stored predictions when possible and live inference otherwise, but it is more complex. Client-side deployment can reduce server costs, network latency, and privacy risk, while enabling offline use, but it requires smaller models and more device-specific engineering. Browser deployment provides local inference through JavaScript, while federated learning allows local models to learn from private user data and share aggregated updates. The correct option depends on latency, privacy, network, hardware, cost, model complexity, and maintenance requirements.

---

# 16. Possible Oral-Exam Questions

## 1. What is the main difference between streaming and batch inference?

**Answer:** Streaming processes each request as it arrives, while batch inference processes many examples together ahead of the time when the predictions are needed.

## 2. When is streaming inference required?

**Answer:** It is required when the model needs information available only at request time and the result must be returned immediately.

## 3. Why can batch inference be more resource efficient?

**Answer:** The workload size and timing are known in advance, so computing resources can be allocated, parallelized, and used more efficiently.

## 4. What is the main drawback of a hybrid system?

**Answer:** It requires maintaining both batch and streaming pipelines, which increases operational complexity, testing burden, and risk of inconsistent results.

## 5. Why deploy a model on the client?

**Answer:** Client deployment can reduce server cost and network latency, preserve privacy, improve scalability, and allow offline operation.

## 6. Why might an on-device model be less accurate?

**Answer:** It may need to be simplified, pruned, quantized, or reduced in size so it can run efficiently on limited hardware.

## 7. What is quantization?

**Answer:** Quantization reduces the numeric precision of model weights or calculations to decrease model size and computational cost.

## 8. What is pruning?

**Answer:** Pruning removes model parameters—often near-zero weights—that contribute little to predictions.

## 9. What is the benefit of TensorFlow.js?

**Answer:** It allows models to run in JavaScript inside a browser, using the client’s hardware and potentially WebGL acceleration, without requiring a native application.

## 10. What is federated learning?

**Answer:** Federated learning trains or updates models locally on client data and sends aggregated model updates to a server, rather than sending raw user data.

## 11. Why does the chapter recommend starting simple?

**Answer:** More complex architectures create additional development and maintenance costs. Complexity should be introduced only after real requirements or bottlenecks have been validated.

---

# 17. Key Terms

| Term | Meaning |
|---|---|
| Deployment | Making a trained ML model available within a usable application or system |
| Inference | Using a trained model to produce a prediction |
| Endpoint | A network-accessible route through which a client sends requests |
| Streaming inference | Processing individual requests as they arrive |
| Batch inference | Processing many examples together on a schedule |
| Precomputation | Generating results before they are requested |
| Latency | Time required to return a result |
| Scalability | Ability to support increasing demand |
| Client-side inference | Running the model on the user’s device |
| On-device model | A model packaged into and executed by an application on a device |
| Pruning | Removing low-value model parameters |
| Quantization | Reducing numerical precision to improve model efficiency |
| TensorFlow Lite | A framework for optimizing and running models on mobile or constrained devices |
| TensorFlow.js | A JavaScript framework for training or running models in a browser |
| WebGL | Browser technology that can use GPU acceleration for graphical and numerical computation |
| Federated learning | Training across decentralized devices while keeping raw data local |
| Model update | A change to model parameters learned during training |
| Hybrid inference | Combining precomputed batch predictions with live streaming inference |

---

# 18. Final Takeaways

1. Deployment should be chosen according to product and infrastructure requirements, not model preference alone.
2. Streaming is appropriate for immediate predictions that depend on real-time features.
3. Batch is appropriate when features are available in advance and results can be precomputed.
4. Hybrid systems improve flexibility but significantly increase complexity.
5. Client-side deployment reduces network dependence, centralized inference cost, and exposure of sensitive data.
6. On-device models usually require optimization such as pruning, quantization, simplification, or feature reduction.
7. Browser-side inference can provide local execution without requiring a native application.
8. Federated learning supports personalization and local data privacy but is operationally complex.
9. End-to-end latency matters more than model execution speed alone.
10. The recommended strategy is to deploy the simplest workable system, measure its limitations, and iterate only when justified.

---

## One-Sentence Memory Aid

> **Stream when the answer must be fresh, batch when it can be prepared, run locally when privacy or offline access matters, and add complexity only when the product truly needs it.**
