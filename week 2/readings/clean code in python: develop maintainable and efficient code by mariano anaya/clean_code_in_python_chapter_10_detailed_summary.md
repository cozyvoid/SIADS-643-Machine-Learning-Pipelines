# Chapter 10 Study Guide: Clean Architecture

**Book:** *Clean Code in Python: Develop Maintainable and Efficient Code*  
**Author:** Mariano Anaya  
**Chapter:** 10 — Clean Architecture

---

## 1. Chapter Overview

Chapter 10 moves from clean code at the level of functions, classes, and modules to clean architecture at the level of complete systems.

The chapter’s main argument is that the same principles used to write maintainable code also apply to larger software structures:

- separation of concerns,
- high cohesion,
- low coupling,
- dependency inversion,
- clear abstractions,
- testability,
- intention-revealing design,
- and pragmatic decision-making.

A clean architecture is one in which the system’s structure makes its purpose clear while technical details remain isolated behind boundaries.

The chapter focuses on three major goals:

1. Designing systems that remain maintainable over time.
2. Preserving important quality attributes as software grows.
3. Connecting clean-code principles with system-level architecture.

The chapter is more conceptual than earlier chapters because architecture concerns interactions among:

- applications,
- services,
- packages,
- teams,
- deployment units,
- infrastructure,
- and external dependencies.

---

# 2. From Clean Code to Clean Architecture

Clean architecture is not separate from clean code.

The chapter presents them as two levels of the same discipline.

At the code level, developers aim for:

- small functions,
- cohesive classes,
- explicit dependencies,
- and minimal coupling.

At the architecture level, the same goals become:

- focused components,
- stable interfaces,
- independently deployable units,
- controlled dependencies,
- and isolated infrastructure.

## 2.1 Code is the foundation of architecture

A well-designed architecture cannot compensate for poorly written code.

If implementation details are:

- tangled,
- duplicated,
- tightly coupled,
- or difficult to test,

the system will still become difficult to maintain.

Architecture provides the large-scale structure, but clean code determines whether each component can actually fulfill its role.

## 2.2 Design principles scale upward

Many concepts discussed earlier in the book are broader than individual functions or classes.

Examples include:

- design patterns,
- SOLID principles,
- dependency inversion,
- encapsulation,
- and separation of concerns.

These ideas can be applied to:

- packages,
- libraries,
- services,
- and distributed systems.

---

# 3. Quality Attributes

An architecture is useful only if it supports the qualities the system needs.

Common quality attributes include:

- maintainability,
- scalability,
- security,
- performance,
- reliability,
- availability,
- testability,
- operability,
- deployability,
- and extensibility.

The correct architecture depends on which attributes matter most for the product.

## 3.1 Operational quality also matters

Architecture quality is not limited to runtime performance.

It also includes how easily the system can be:

- built,
- tested,
- released,
- monitored,
- rolled back,
- and maintained.

A theoretically elegant system that is painful to deploy is not clean in practice.

## 3.2 Tradeoffs are unavoidable

Improving one quality attribute may weaken another.

Examples:

- microservices increase independent deployability but add network latency,
- abstraction improves replaceability but adds indirection,
- aggressive optimization may reduce readability,
- and strict isolation may increase duplication.

Architecture is therefore about managing tradeoffs, not maximizing every attribute simultaneously.

---

# 4. Separation of Concerns

Separation of concerns is one of the chapter’s central principles.

Different responsibilities should be placed in different components.

At the code level, this means:

- functions should do one thing,
- classes should have focused responsibilities,
- and modules should group related behavior.

At the architecture level, it means:

- services,
- packages,
- or subsystems should each own a clear capability.

## 4.1 Why small units help

Smaller components are easier to:

- understand,
- test,
- modify,
- deploy,
- and replace.

When requirements change, there should be one obvious place to update.

## 4.2 Architectural component

The word **component** is intentionally broad.

A component may be:

- a Python package,
- a service,
- a library,
- a deployable process,
- or another independently managed unit.

A useful architectural component generally has:

- one coherent purpose,
- a defined interface,
- a clear owner,
- and a lifecycle that can be managed separately.

## 4.3 Independent deployment

A component is especially valuable when it can be:

- released,
- versioned,
- tested,
- and deployed

independently from the rest of the system.

However, independent deployment is not always required. A cohesive Python package inside one application can still be a meaningful component.

---

# 5. Avoiding the Architectural “God Object”

A large monolithic system can suffer from the same problems as an oversized class.

If one application owns:

- every responsibility,
- every integration,
- every business rule,
- and every deployment concern,

then changes become difficult to isolate.

Possible consequences include:

- slow testing,
- risky releases,
- broad regressions,
- unclear ownership,
- and difficult scaling.

The chapter does not argue that every monolith is bad. It argues that responsibilities must be separated even when they remain in one deployable application.

A modular monolith may be cleaner than a poorly designed microservice system.

---

# 6. Monoliths and Microservices

The chapter compares two broad architectural choices:

- one application composed of internal packages,
- multiple independently deployed services.

The important question is not “Which style is universally better?” but:

> Which structure provides the right balance of separation, performance, ownership, and operational cost for this system?

---

## 6.1 Benefits of microservices

Microservices can provide:

- independent deployment,
- independent scaling,
- separate ownership,
- language and framework freedom,
- fault isolation,
- and clear service boundaries.

Each service may be tested and released separately.

## 6.2 Costs of microservices

Microservices also introduce:

- network latency,
- distributed failures,
- service discovery,
- deployment coordination,
- monitoring complexity,
- versioned contracts,
- retries and timeouts,
- and more operational overhead.

Calls that would be local function calls become:

- HTTP requests,
- gRPC calls,
- or asynchronous messages.

## 6.3 Service contracts

A service must expose a stable contract so clients know how to interact with it.

The contract may define:

- request formats,
- response formats,
- error behavior,
- versioning,
- availability,
- and performance expectations.

This leads to concepts such as:

- service-level agreements (SLAs),
- service-level indicators (SLIs),
- and service-level objectives (SLOs).

## 6.4 Reuse does not always require a service

A common mistake is creating a microservice only because several systems need the same logic.

If all consumers use Python, the shared logic might be better distributed as a Python package.

A package avoids:

- network calls,
- service deployment,
- and runtime availability concerns.

## 6.5 When a service may be necessary

A service is more appropriate when:

- consumers use different languages,
- the logic requires centralized state,
- updates must be deployed independently,
- resource use must be isolated,
- or one team must own the behavior operationally.

## 6.6 Architectural decision

The choice between a package and a service should consider:

| Question | Package | Service |
|---|---|---|
| Same language required? | Usually yes | No |
| Network latency | None | Present |
| Independent deployment | Limited | Strong |
| Runtime dependency | No separate process | Separate process required |
| Versioning | Package versions | API versions |
| Operational overhead | Lower | Higher |
| Centralized control | Lower | Higher |

---

# 7. Abstractions at the Architectural Level

At the architecture level, abstractions should express the domain while hiding technical implementation details.

A system should reveal:

- what business problem it solves,
- which concepts it manages,
- and how responsibilities are divided.

It should avoid exposing unnecessary details such as:

- the ORM,
- the web framework,
- the database vendor,
- the HTTP client,
- or the serialization library.

## 7.1 Screaming architecture

The chapter references the idea of **screaming architecture**.

A system’s structure should “scream” its domain purpose.

A delivery system should visibly contain concepts such as:

- orders,
- delivery status,
- dispatch,
- transit,
- and completion.

It should not primarily appear to be about:

- Sanic,
- PostgreSQL,
- SQLAlchemy,
- Docker,
- or REST.

Those are implementation details.

---

# 8. Dependency Inversion at System Scale

The Dependency Inversion Principle states that high-level business rules should not depend directly on low-level implementation details.

Instead:

- both depend on stable abstractions,
- and low-level details adapt to the needs of the core.

## 8.1 Code-level inversion

At the class level, this may involve:

- abstract base classes,
- protocols,
- duck typing,
- dependency injection,
- or adapters.

## 8.2 Architecture-level inversion

At the system level, the core application should not import concrete technical implementations directly.

Instead, the system introduces a layer that translates between:

- domain concepts,
- and external systems.

Examples include:

- repository interfaces,
- storage adapters,
- web adapters,
- messaging gateways,
- and API clients.

---

# 9. Why an ORM Is Not the Final Abstraction

An ORM hides some database details, but it is still an external dependency.

The chapter warns against letting ORM entities become the application’s domain objects.

If business logic depends directly on:

- ORM classes,
- query objects,
- session behavior,
- or framework-specific metadata,

the domain becomes coupled to the persistence library.

## 9.1 Better design

Create application-owned abstractions above the ORM.

For example:

```text
Database / ORM
      ↓
Storage adapter
      ↓
Domain objects
      ↓
Business logic
```

The application works with its own domain models.

The adapter converts between:

- database rows or ORM entities,
- and domain objects.

## 9.2 Benefits

The storage technology can later change without rewriting the domain layer.

Possible changes include:

- replacing the ORM,
- switching database vendors,
- using direct SQL,
- querying another service,
- or reading from files.

The business rules remain stable as long as the adapter continues returning the expected domain objects.

---

# 10. Hexagonal Architecture

The chapter connects this approach to **hexagonal architecture**, also known as ports and adapters.

## 10.1 Core idea

The application core contains:

- business rules,
- domain models,
- and use cases.

External technologies connect through adapters.

## 10.2 Ports

A port is an interface representing what the application needs or provides.

Examples:

- retrieve a delivery order,
- save an order,
- publish a notification,
- or handle a web request.

## 10.3 Adapters

Adapters translate a concrete technology into the port expected by the application.

Examples:

- a SQL repository,
- an HTTP controller,
- a queue publisher,
- or a filesystem reader.

## 10.4 Direction of dependency

Dependencies should point inward toward the business rules.

```text
Web framework ─┐
Database ORM ──┼──> Adapters ──> Application core
Message queue ─┘
```

The core does not know which technologies are used outside.

---

# 11. Software Components and Team Structure

Architecture is also organizational.

A large system is often divided among teams, and each team may own:

- one service,
- one package,
- one domain capability,
- or one set of integrations.

Clear boundaries reduce coordination overhead.

## 11.1 Component ownership

A component should have:

- responsible maintainers,
- documentation,
- a release process,
- and an explicit public interface.

## 11.2 Interface discipline

Teams can collaborate at scale only when components agree on contracts.

Without stable interfaces, internal changes propagate unpredictably across the system.

---

# 12. Python Packages as Architectural Components

A Python package is a convenient mechanism for:

- reusing code,
- centralizing shared logic,
- enforcing consistent behavior,
- and distributing tested functionality.

Packages are especially useful when the same logic is needed across several Python projects.

## 12.1 Conceptual integrity

A shared package can establish one approved way to perform a task.

Examples include:

- secure archive extraction,
- configuration parsing,
- API client behavior,
- validation,
- and domain-specific utilities.

This contributes to **conceptual integrity** because the organization uses one consistent implementation instead of many slightly different versions.

## 12.2 When to create a package

A package is appropriate when:

- behavior is reused,
- the abstraction is stable,
- ownership is clear,
- and the package has a coherent purpose.

A package should not become a miscellaneous collection of unrelated helpers.

---

# 13. Suggested Package Structure

The chapter presents a structure similar to:

```text
project/
├── Makefile
├── README.rst
├── setup.py
├── src/
│   └── apptool/
│       ├── __init__.py
│       ├── common.py
│       └── parse.py
└── tests/
    ├── unit/
    └── integration/
```

## 13.1 Why use `src/`

Placing the package under `src/` helps ensure tests use the installed package rather than accidentally importing code directly from the repository root.

It also reduces the chance of shipping unrelated files.

## 13.2 Public API

The package’s `__init__.py` can expose the intended public interface.

Internal modules can then be reorganized without breaking clients.

---

# 14. `setup.py` Package Definition

The chapter uses `setuptools`:

```python
from setuptools import find_packages, setup

setup(
    name="apptool",
    description="Description of the package",
    author="Dev team",
    version="0.1.0",
    packages=find_packages(where="src/"),
    package_dir={"": "src"},
)
```

Important fields include:

- package name,
- description,
- version,
- author,
- packages,
- package directory,
- and dependencies.

## 14.1 Distribution name versus import name

The distribution installed with:

```bash
pip install apptool
```

should ideally match the package imported with:

```python
from apptool import ...
```

They can differ, but matching names reduce confusion.

## 14.2 Package version

Versioning allows:

- multiple releases,
- upgrades,
- compatibility control,
- and rollback.

---

# 15. Building a Package

The chapter demonstrates creating a virtual environment and building source and wheel distributions.

```bash
python -m venv env
source env/bin/activate
pip install -U pip wheel
python setup.py sdist bdist_wheel
```

Artifacts are written to:

```text
dist/
```

They can then be published to:

- PyPI,
- or an internal package repository.

## 15.1 Current tooling note

The chapter uses `setup.py` directly because that was common in the book’s context.

Modern Python projects often use:

- `pyproject.toml`,
- PEP 517 build tools,
- and commands such as `python -m build`.

The architectural principles remain the same:

- reproducible builds,
- explicit metadata,
- stable versions,
- and controlled dependencies.

---

# 16. Packaging Best Practices

The chapter emphasizes several important rules.

## 16.1 Ensure platform independence

The package should not depend on:

- files available only on the developer’s computer,
- an accidental directory layout,
- or local environment assumptions.

## 16.2 Avoid shipping unnecessary test artifacts

Production packages do not normally need:

- large fixtures,
- local test data,
- or development-only files.

Tests should remain available in source control, but only required runtime files should be installed in production.

## 16.3 Separate runtime and development dependencies

Runtime dependencies are required to execute the package.

Development dependencies may include:

- test frameworks,
- linters,
- formatters,
- type checkers,
- build tools,
- and documentation generators.

## 16.4 Add command entry points

Frequently used commands should be exposed as package entry points rather than requiring users to know internal module paths.

## 16.5 Fail early

If installation requires operating-system libraries or compiled extensions, the build should fail with a useful message as early as possible.

---

# 17. Managing Dependencies

External dependencies are part of the delivered software.

A project must know exactly which versions are used.

## 17.1 Baseline

A **baseline** is the complete set of versions included in a build.

It allows a team to answer:

- Which libraries were deployed?
- Which transitive dependencies were included?
- Which version introduced a regression?
- Can the same artifact be rebuilt?

## 17.2 Repeatable builds

Given the same source code and configuration, the build should produce the same dependency set.

Without pinned dependency versions, the same Git commit may produce different artifacts on different days.

---

# 18. Version Ranges and Locked Requirements

A package may specify a supported dependency range:

```python
install_requires = ["sanic>=20,<21"]
```

This expresses compatibility while allowing upgrades within a major version.

However, the deployment should use a fully resolved set of exact versions.

## 18.1 `pip-tools`

The chapter recommends generating a locked `requirements.txt` with `pip-tools`.

```bash
pip-compile setup.py
```

The resulting file contains exact versions, including transitive dependencies.

## 18.2 Deployment rule

Install dependencies inside the production image from the locked requirements file.

```bash
pip install -r requirements.txt
```

## 18.3 Version control

The lock file should be committed to source control.

When upgrading:

```bash
pip-compile -U setup.py
```

The changed dependency versions become visible in the pull request.

---

# 19. Transitive Dependencies

A project may directly depend on one package, which depends on several others.

These indirect packages can still:

- break compatibility,
- introduce vulnerabilities,
- or alter runtime behavior.

A reproducible build therefore tracks the entire dependency tree, not only direct requirements.

---

# 20. Internal Dependency Repositories

Relying directly on a public registry introduces risks.

Potential concerns include:

- registry outages,
- removed packages,
- compromised artifacts,
- inconsistent availability,
- and inability to host private intellectual property.

The chapter recommends an internal artifact repository.

## 20.1 Internal repository role

The repository stores:

- approved third-party packages,
- internal packages,
- versioned artifacts,
- and controlled dependency mirrors.

## 20.2 Benefits

- improved availability,
- better governance,
- private package hosting,
- security review,
- and reproducible builds.

All production builds should resolve dependencies through the controlled internal repository.

---

# 21. Dependency Updates as Technical Debt Management

Outdated dependencies are a form of technical debt.

They may cause the organization to miss:

- security patches,
- performance improvements,
- new features,
- and compatibility updates.

## 21.1 Update continuously

Frequent small updates are easier than infrequent large upgrades.

This follows the continuous integration principle:

- integrate changes early,
- run automated tests,
- and correct incompatibilities incrementally.

## 21.2 Automation

Tools such as Dependabot can:

- detect new releases,
- update lock files,
- open pull requests,
- and trigger continuous integration.

If the build passes and the change is understood, the update can often be merged with minimal manual effort.

## 21.3 Security checks

Dependency workflows should include automated vulnerability scanning.

---

# 22. Artifact Versioning

Changing dependencies changes the delivered artifact, even if application code remains unchanged.

A new artifact version should therefore be published.

## 22.1 Semantic meaning

Versioning communicates compatibility.

The chapter references PEP 440 for Python version identifiers.

A typical version may look like:

```text
MAJOR.MINOR.PATCH
```

General interpretation:

- major: incompatible change,
- minor: backward-compatible functionality,
- patch: backward-compatible fix.

## 22.2 Stability versus currency

There is a tradeoff between:

- using the newest available software,
- and protecting system stability.

Supported ranges and continuous testing allow teams to balance these goals.

---

# 23. Docker Containers as Delivery Components

Packages distribute reusable code.

Containers distribute runnable applications and services.

A Docker container packages:

- the application,
- Python,
- system libraries,
- runtime dependencies,
- and startup configuration.

## 23.1 Why containers help Python deployment

Historically, Python deployment could be difficult because of differences in:

- interpreter versions,
- Linux distributions,
- C libraries,
- compiled extensions,
- and local environments.

A container image creates one canonical runtime.

## 23.2 Portability

The same image can be used for:

- development,
- testing,
- staging,
- and production.

This reduces “works on my machine” problems.

## 23.3 Reproducibility

A Dockerfile documents how the application environment is built.

Combined with locked dependencies, it supports repeatable delivery.

---

# 24. Containers and Separation of Concerns

A container should represent a focused service or process.

The same principles used for classes apply:

- one clear responsibility,
- explicit dependencies,
- minimal unnecessary contents,
- and controlled interfaces.

A container image should not become a giant environment containing unrelated applications.

---

# 25. Delivery-Status Service Use Case

The chapter illustrates clean architecture with a food-delivery status service.

The service exposes a REST API that returns the current state of an order as JSON.

Its main concerns are:

1. retrieve order status,
2. present the result to a client.

The architecture separates these concerns into components.

```text
Client
  ↓
Web application
  ↓
Domain objects
  ↓
Storage abstraction
  ↓
Database or another data source
```

The web and storage concerns are represented as separate packages.

---

# 26. Figure 10.1

Figure 10.1 shows:

- a web service,
- one package responsible for web behavior,
- one package responsible for storage,
- and the storage package connecting to a database.

The diagram reinforces the chapter’s core point:

> The application uses focused components that hide technical details behind stable interfaces.

A screenshot of Figure 10.1 is optional. The structure is simple enough to reproduce textually, so the guide does not require the image to remain understandable.

---

# 27. Why Separate `web` and `storage`

The main application should not be concerned with:

- the database type,
- the ORM,
- SQL syntax,
- the web framework,
- routing internals,
- or JSON serialization details.

The packages serve as technical boundaries.

## 27.1 `storage`

Responsible for:

- retrieving raw data,
- translating it into domain objects,
- and exposing an application-friendly API.

## 27.2 `web`

Responsible for:

- integrating with the web framework,
- registering routes,
- translating framework errors,
- and exposing a stable application interface.

## 27.3 Main application

Responsible for:

- coordinating the use case,
- applying business behavior,
- and returning domain results.

---

# 28. Domain Models

The chapter defines pure domain objects for delivery states.

Examples include:

- `DispatchedOrder`,
- `OrderInTransit`,
- `OrderDelivered`,
- and `DeliveryOrder`.

These objects are not:

- ORM models,
- framework request objects,
- database rows,
- or serialization classes.

They represent business concepts.

---

## 28.1 Dispatched order

Stores when the order was dispatched and produces a domain message.

```python
class DispatchedOrder:
    status = "dispatched"

    def message(self) -> dict:
        return {
            "status": self.status,
            "msg": "...",
        }
```

## 28.2 Order in transit

Stores the current location.

## 28.3 Delivered order

Stores the delivery time.

## 28.4 Delivery order

Combines:

- a delivery identifier,
- and one status object.

```python
class DeliveryOrder:
    def message(self) -> dict:
        return {
            "id": self._delivery_id,
            **self._status.message(),
        }
```

## 28.5 Architectural significance

The application communicates through domain objects rather than technical persistence objects.

This keeps business language central.

---

# 29. State Collaboration in the Domain Model

`DeliveryOrder` delegates status-specific messaging to the current status object.

This resembles the state pattern discussed in Chapter 9.

Benefits include:

- focused status classes,
- polymorphic behavior,
- and elimination of large conditional blocks.

The architecture chapter shows how earlier design-pattern principles become building blocks in a larger system.

---

# 30. Application Layer Example

The application uses abstractions imported from `storage` and `web`.

```python
from storage import (
    DBClient,
    DeliveryStatusQuery,
    OrderNotFoundError,
)

from web import (
    NotFound,
    View,
    app,
    register_route,
)
```

A view retrieves the domain object and returns its message.

```python
class DeliveryView(View):
    async def _get(self, request, delivery_id: int):
        query = DeliveryStatusQuery(
            int(delivery_id),
            await DBClient(),
        )

        try:
            result = await query.get()
        except OrderNotFoundError as error:
            raise NotFound(str(error)) from error

        return result.message()
```

---

# 31. What the Application Code Hides

From the application code alone, the reader cannot determine:

- which database is used,
- whether an ORM exists,
- which web framework is used,
- whether storage uses SQL,
- or how JSON responses are created.

This is considered a good sign.

Those details are not relevant to the use case.

The application expresses:

> Retrieve the delivery status for this identifier and return its message.

---

# 32. Declarative Versus Imperative Style

The chapter describes the application as more declarative.

## 32.1 Declarative

The code states what result is required.

```text
Get delivery status.
Return its message.
```

## 32.2 Imperative

The code would manually describe every technical step:

```text
Open a database connection.
Construct SQL.
Execute the query.
Read the row.
Convert columns.
Build a response.
Serialize JSON.
```

By moving implementation steps behind abstractions, the core application becomes easier to read.

---

# 33. Replaceable Storage

The application relies on a contract:

```python
await query.get()
```

The method must return a `DeliveryOrder`.

The implementation may change to use:

- another database,
- another ORM,
- direct SQL,
- a file,
- a cache,
- or a remote service.

As long as the contract remains intact, the application does not need to change.

This is dependency inversion in practice.

---

# 34. Adapters in the Example

The `web` and `storage` packages likely contain adapters.

## 34.1 Web adapter

The custom `View` may adapt a framework-specific view class to an application-owned API.

## 34.2 Storage adapter

`DeliveryStatusQuery` may translate:

- database records,
- ORM objects,
- or external responses

into `DeliveryOrder`.

## 34.3 Why adapters matter

They isolate third-party interfaces so the rest of the system depends on project-owned abstractions.

---

# 35. Creating the Service Package

The application is packaged with a structure similar to:

```text
project/
├── Dockerfile
├── libs/
│   ├── storage/
│   └── web/
├── Makefile
├── README.rst
├── setup.py
└── statusweb/
    ├── __init__.py
    └── service.py
```

The `libs/` directory contains local package dependencies in the example.

In a real organization, these could be installed from an internal artifact repository.

---

# 36. Application Dependencies

The service declares dependencies on:

```python
install_requires = [
    "web==0.1.0",
    "storage==0.1.0",
]
```

Those packages may have their own dependencies.

The complete container build must include the entire resolved dependency tree.

---

# 37. Console Entry Points

The chapter defines:

```python
entry_points={
    "console_scripts": [
        "status-service = statusweb.service:main",
    ],
}
```

This creates an executable command:

```bash
status-service
```

The command calls:

```python
statusweb.service.main
```

## 37.1 Benefits

- users do not need to know module paths,
- the virtual environment is handled correctly,
- startup becomes consistent,
- and Docker can invoke one stable command.

---

# 38. Virtual Environment Structure

A virtual environment typically contains:

```text
<venv>/lib/<python-version>/site-packages
<venv>/bin
```

## 38.1 `site-packages`

Contains installed packages.

## 38.2 `bin`

Contains:

- Python,
- pip,
- and console entry points.

The generated command uses the correct environment and dependencies.

---

# 39. Dockerfile Example

The chapter provides a Dockerfile similar to:

```dockerfile
FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python-dev \
        gcc \
        musl-dev \
        make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD . /app

RUN pip install /app/libs/web /app/libs/storage
RUN pip install /app

EXPOSE 8080

CMD ["/usr/local/bin/status-service"]
```

---

# 40. Dockerfile Responsibilities

## 40.1 Base image

Provides:

- Linux,
- Python,
- and basic runtime tooling.

## 40.2 System dependencies

Installs libraries required to build or run Python packages.

## 40.3 Working directory

Creates a predictable application location.

## 40.4 Source copy

Adds the project files.

## 40.5 Package installation

Installs internal libraries and the application.

## 40.6 Port declaration

Documents the service port.

## 40.7 Command

Starts the application through the package entry point.

---

# 41. Build-Time Versus Runtime System Dependencies

Some operating-system libraries are needed only to compile Python extensions.

Others are required while the application runs.

## 41.1 Build-only dependencies

Examples may include:

- compilers,
- headers,
- and build tools.

These can sometimes be removed from the final image through multi-stage builds.

## 41.2 Runtime dependencies

Libraries needed by the application at execution time must remain in the final image.

## 41.3 Prebuilt wheels

If a compatible wheel is available, compilation may not be necessary.

This can reduce:

- image size,
- build time,
- and attack surface.

---

# 42. Local Development with Containers

The same Dockerfile can be used locally.

A `docker-compose.yml` file may define:

- the service,
- a database,
- queues,
- caches,
- and network relationships.

This improves onboarding and makes development environments more consistent.

---

# 43. Example Service Response

The running service can be tested with:

```bash
curl http://localhost:5000/status/1
```

A response may look like:

```json
{
  "id": 1,
  "status": "dispatched",
  "msg": "Order was dispatched on 2018-08-01T22:25:12+00:00"
}
```

The output reflects the domain model rather than exposing storage details.

---

# 44. Dependency Flow

The chapter emphasizes that dependencies should flow inward.

The application imports from `storage` and `web`.

Those technical packages should not import and depend on the application’s use-case implementation.

```text
External technology
        ↓
Adapters
        ↓
Application use case
        ↓
Domain rules
```

## 44.1 Why direction matters

If storage depends on the application, both become tightly coupled.

Instead, storage implements the interface required by the application.

This makes the low-level component conform to the high-level policy.

---

# 45. Weak Coupling Through Contracts

The application requires:

- an object with `get()`,
- asynchronous behavior,
- and a `DeliveryOrder` result.

Any storage implementation satisfying this contract can be substituted.

This is a weak dependency compared with direct reliance on:

- a concrete ORM session,
- a database table,
- or a framework-specific query API.

---

# 46. Architectural Limitations and Leaky Abstractions

No abstraction is perfect.

Technical details eventually influence the application.

## 46.1 Asynchronous interface

The example’s storage and web interactions are asynchronous.

That requirement is visible in:

```python
await query.get()
```

Any replacement must preserve this behavior.

The technical choice has become part of the contract.

## 46.2 Web-framework influence

A sufficiently complex application may need framework-specific features that cannot be hidden completely.

## 46.3 Changing protocols

Moving from REST to:

- GraphQL,
- gRPC,
- or messaging

would require changes in the application boundary and startup configuration.

The goal is not zero change. The goal is to localize change.

## 46.4 Abstraction leaks

An abstraction leaks when underlying implementation details become visible through the interface.

Clean architecture reduces leaks but cannot eliminate every one.

---

# 47. Testability

Separating components makes testing easier.

## 47.1 Domain tests

Pure domain objects can be tested without:

- databases,
- web servers,
- Docker,
- or external services.

## 47.2 Application tests

Storage and web dependencies can be replaced with:

- mocks,
- fakes,
- or in-memory adapters.

## 47.3 Component tests

Each package or service can be tested in isolation.

## 47.4 Integration tests

The complete application must still be tested with real components working together.

---

# 48. Testing Pyramid

The chapter revisits the testing pyramid from Chapter 8.

A healthy system generally has:

1. many fast unit tests,
2. fewer component or integration tests,
3. very few full end-to-end tests.

```text
          End-to-end
        Integration
      Component tests
    Unit tests
```

The broader tests are necessary but slower and more expensive.

Clean boundaries allow the majority of business behavior to be tested at lower levels.

---

# 49. Intention-Revealing Architecture

A clean architecture communicates the system’s purpose.

Names should describe domain concepts.

Good examples:

- `DeliveryOrder`,
- `OrderInTransit`,
- `DeliveryStatusQuery`,
- `OrderNotFoundError`.

Less useful architectural names would emphasize technologies:

- `SQLAlchemyDeliveryRow`,
- `SanicDeliveryController`,
- or `PostgresStatusService`.

Technology names may be appropriate inside adapters, but they should not dominate the core.

---

# 50. Architecture Should Tell a Story

Just as a clean function should tell a clear story, a clean architecture should allow a reader to understand:

- what the system does,
- which components own each responsibility,
- how information flows,
- and where technical details live.

A reader should not need to inspect every implementation file to understand the high-level use case.

---

# 51. Practicality Beats Purity

The chapter ends with a pragmatic warning.

Architectural principles are guides, not laws.

Perfect isolation may be:

- impossible,
- too expensive,
- or not worth the complexity.

Examples include:

- accepting an asynchronous contract,
- using some framework-specific behavior,
- keeping a modular monolith,
- or avoiding a service split.

The correct design is the one that best supports the real project.

---

# 52. Main Architectural Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| Split into packages | Reuse and modularity | Versioning and dependency management |
| Split into services | Independent deployment | Network and operational complexity |
| Add abstraction layer | Replaceability | More code and indirection |
| Use ORM directly | Faster initial development | Domain coupling |
| Use domain models | Clear business logic | Mapping code required |
| Lock dependencies | Reproducibility | Upgrade maintenance |
| Use internal registry | Control and availability | Infrastructure ownership |
| Use containers | Portability | Build and image management |
| Hide framework | Cleaner core | Some abstraction leakage remains |
| Async interfaces | Concurrency benefits | Contract becomes technology-sensitive |

---

# 53. Common Mistakes

## 53.1 Treating microservices as the default

A service boundary should solve a real ownership, scaling, or interoperability problem.

## 53.2 Turning every shared function into a service

Use a package when local reuse is sufficient.

## 53.3 Allowing ORM entities into the domain

Translate persistence models into application-owned objects.

## 53.4 Naming architecture after frameworks

Expose business purpose first.

## 53.5 Ignoring transitive dependencies

Lock and track the full dependency tree.

## 53.6 Installing floating versions in production

Use deterministic requirement files.

## 53.7 Never upgrading dependencies

Continuous small upgrades are safer than large delayed migrations.

## 53.8 Assuming containers alone guarantee reproducibility

The Docker image must also use locked dependencies and controlled sources.

## 53.9 Shipping unnecessary files

Keep production artifacts minimal.

## 53.10 Trying to abstract every technical detail

Accept unavoidable constraints when further abstraction adds no practical value.

---

# 54. Practical Architecture Checklist

## Domain

- Are business concepts represented explicitly?
- Are domain objects independent of frameworks?
- Does the architecture reveal its purpose?

## Components

- Does each component have one coherent responsibility?
- Are interfaces documented?
- Can components be tested independently?
- Is ownership clear?

## Dependencies

- Do dependencies point toward the domain?
- Are external systems behind adapters?
- Are concrete frameworks isolated?
- Are transitive dependencies locked?

## Packaging

- Is reusable Python logic packaged cleanly?
- Is runtime metadata explicit?
- Are package versions meaningful?
- Are dev dependencies separated?

## Delivery

- Is the runtime reproducible?
- Is the Docker image minimal?
- Is there one canonical startup command?
- Can the same artifact move through environments?

## Testing

- Can the domain run without infrastructure?
- Are component tests available?
- Are integration tests limited but sufficient?
- Can external adapters be replaced?

## Operations

- Can the system be released safely?
- Are dependencies scanned and updated?
- Can components be rolled back?
- Are service contracts and expectations clear?

---

# 55. End-to-End Architectural Flow

A clean system can be visualized as:

```text
User or client
      ↓
Delivery/web adapter
      ↓
Application use case
      ↓
Domain model
      ↓
Storage port
      ↓
Storage adapter
      ↓
Database or external system
```

Supporting delivery infrastructure:

```text
Source code
    ↓
Package metadata
    ↓
Locked dependencies
    ↓
Docker image
    ↓
Testing pipeline
    ↓
Staging
    ↓
Production
```

---

# 56. Connection to Previous Chapters

Chapter 10 acts as a synthesis of the book.

## Clean functions and classes

Become cohesive architectural components.

## SOLID principles

Become dependency direction and component boundaries.

## Decorators and descriptors

Support reusable implementation details inside components.

## Exceptions

Become part of stable component contracts.

## Unit testing

Becomes a layered system testing strategy.

## Refactoring

Becomes architectural evolution.

## Design patterns

Become reusable structures such as adapters, facades, and state objects.

## Dependency injection

Becomes replaceable infrastructure.

---

# 57. Concise Exam-Style Summary

Chapter 10 explains how clean-code principles scale into clean architecture. A maintainable system separates responsibilities into cohesive components, controls dependencies, and keeps business rules independent from frameworks, databases, and delivery technologies. Architecture should reveal the domain problem rather than the technical tools used to implement it.

Components may be Python packages, libraries, services, or deployable processes. Microservices provide independent deployment and language flexibility but introduce latency, network failures, and operational overhead. Shared logic does not always require a service; a package may be more efficient when all consumers use Python.

Dependency inversion is applied at system scale by placing adapters between the application core and external technologies. An ORM is not a sufficient domain abstraction because it remains an external dependency. The core should use application-owned domain objects while storage and web adapters translate technical representations.

Python packages provide reusable components and conceptual integrity. Good packaging includes explicit metadata, source layout, versioning, separate development dependencies, and stable entry points. Dependencies must be locked, including transitive dependencies, to create repeatable builds. Internal artifact repositories improve reliability, security, and private distribution. Dependencies should be upgraded continuously to avoid technical debt.

Docker containers provide a canonical runtime containing the interpreter, operating-system libraries, application, and dependencies. Containers improve portability across development, testing, and production, but reproducibility still requires locked dependency versions.

The chapter’s delivery-status example separates domain objects, storage, and web concerns. The application retrieves a `DeliveryOrder` through a storage abstraction and returns its domain message without exposing the database, ORM, or web framework. Dependencies flow inward toward the business rules, making implementations replaceable and tests simpler.

No abstraction is perfect. Async behavior, framework constraints, and protocol choices may leak into the application. The objective is not architectural purity but localized change, understandable boundaries, and practical maintainability.

---

# 58. Key Takeaways

1. **Clean architecture extends clean-code principles to complete systems.**
2. **Architecture quality depends on both runtime and operational attributes.**
3. **Separate responsibilities into cohesive components.**
4. **A component can be a package, library, service, or process.**
5. **Microservices are a tradeoff, not a universal goal.**
6. **Use packages when local Python reuse is sufficient.**
7. **Architecture should reveal domain intent, not frameworks.**
8. **Dependencies should point inward toward business rules.**
9. **Use adapters around databases, ORMs, web frameworks, and APIs.**
10. **Keep domain objects independent from technical libraries.**
11. **An ORM is an implementation detail, not the domain model.**
12. **Packages support reuse and conceptual integrity.**
13. **Use explicit versions and reproducible package builds.**
14. **Track direct and transitive dependencies.**
15. **Install production dependencies from a locked file.**
16. **Use an internal artifact repository for controlled builds.**
17. **Upgrade dependencies continuously to limit technical debt.**
18. **Version artifacts whenever their contents change.**
19. **Use containers to establish one canonical runtime.**
20. **A Dockerfile alone does not guarantee reproducibility.**
21. **Use package entry points for stable startup commands.**
22. **Test the domain without external infrastructure.**
23. **Use many unit tests and fewer integration tests.**
24. **Accept that some abstractions will leak.**
25. **Localize technical change rather than attempting impossible purity.**
26. **Practicality should guide architectural decisions.**
