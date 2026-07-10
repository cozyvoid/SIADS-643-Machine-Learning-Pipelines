# Chapter 9 Study Guide: Common Design Patterns

**Book:** *Clean Code in Python: Develop Maintainable and Efficient Code*  
**Author:** Mariano Anaya  
**Chapter:** 9 — Common Design Patterns

---

## 1. Chapter Overview

Chapter 9 examines common software design patterns from a Python-specific and clean-code perspective.

The chapter does **not** present design patterns as recipes that should be applied automatically. Instead, it asks a more important question:

> How can a pattern improve the clarity, flexibility, cohesion, and maintainability of a Python design?

The author emphasizes that design patterns are high-level arrangements of objects and responsibilities. Their underlying ideas are language-independent, but their implementation must respect the features and idioms of the language being used.

Python changes how many classic patterns should be implemented because it provides:

- first-class functions,
- first-class classes,
- dynamic typing,
- duck typing,
- descriptors,
- modules,
- magic methods,
- decorators,
- iterators,
- and multiple inheritance.

As a result:

- some patterns are already embedded in the language,
- some require much less code than in statically typed languages,
- and some become unnecessary or non-Pythonic when implemented in their classical form.

The chapter’s major themes are:

1. Patterns should **emerge from refactoring**, not be forced.
2. Python’s features often simplify classic object-oriented patterns.
3. Good patterns reduce coupling and preserve polymorphism.
4. Pattern names provide a shared vocabulary for discussing design.
5. A pattern is valuable only when it improves the current solution.
6. Clean code should express domain intent rather than advertise pattern names.

---

# 2. What a Design Pattern Is

A design pattern is a reusable, high-level solution structure for a recurring software design problem.

A pattern usually describes:

- the participating objects,
- their responsibilities,
- how they relate,
- how they communicate,
- and what tradeoffs the arrangement introduces.

A pattern is **not**:

- a complete implementation,
- a library,
- a single code snippet,
- or a rule that must always be followed.

It is a conceptual model that can be implemented differently depending on:

- the programming language,
- the domain,
- the current architecture,
- and the constraints of the project.

---

# 3. Why Design Patterns Matter

## 3.1 Proven solutions

Patterns capture approaches that have repeatedly worked for common design problems.

Using a known pattern can reduce the need to reinvent an entire solution from scratch.

## 3.2 Shared vocabulary

One of the chapter’s strongest points is that patterns provide a language for engineers.

When a developer says:

- “adapter,”
- “facade,”
- “state,”
- “command,”
- or “chain of responsibility,”

other engineers can quickly infer:

- the expected object relationships,
- where responsibilities should reside,
- and how control is likely to flow.

This speeds up design discussions.

## 3.3 Higher-level thinking

Patterns help developers “zoom out” from individual functions and think about:

- relationships among components,
- object collaboration,
- runtime behavior,
- system evolution,
- and architecture.

## 3.4 Cleaner abstractions

When applied appropriately, patterns often improve:

- cohesion,
- separation of concerns,
- polymorphism,
- extensibility,
- testability,
- and encapsulation.

---

# 4. Design Patterns Must Not Be Forced

The author repeatedly warns against choosing a pattern first and then bending the code to fit it.

A better process is:

1. Solve the current domain problem.
2. identify repeated structures or problems.
3. refactor toward clearer abstractions.
4. recognize when a known pattern has emerged.
5. apply only as much of the pattern as the problem requires.

This reflects the principle that patterns are generally **discovered**, not invented for every individual project.

## 4.1 Why forced patterns are harmful

Forcing a pattern can lead to:

- unnecessary classes,
- artificial interfaces,
- too much indirection,
- speculative flexibility,
- and over-engineering.

## 4.2 The rule of three

The chapter connects pattern extraction to the idea that an abstraction is more justified after the same problem has appeared several times.

Before generalizing, it is often better to wait until:

- the repetition is clear,
- the variation is understood,
- and the shared behavior can be named accurately.

---

# 5. Python-Specific Design Pattern Considerations

Python changes the implementation of classic patterns in several important ways.

## 5.1 Everything is an object

In Python:

- functions are objects,
- classes are objects,
- modules are objects,
- and custom instances are objects.

They can all be:

- assigned to variables,
- passed as arguments,
- returned from functions,
- stored in collections,
- or decorated.

This reduces the need for additional wrapper classes in some patterns.

## 5.2 First-class functions simplify behavioral patterns

A traditional object-oriented implementation may create a class with one method to represent a behavior.

In Python, the behavior can often be represented directly by a function.

This particularly simplifies patterns such as:

- strategy,
- command,
- and decorator.

## 5.3 Duck typing reduces interface boilerplate

Objects do not need to share a formal base class to be polymorphic.

If two objects provide the same required method, callers can treat them consistently.

For example, if both objects implement:

```python
render()
```

they can often be used interchangeably without a shared inheritance hierarchy.

## 5.4 Some patterns are built into Python

### Iterator

Python’s iteration protocol and `for` loops already implement the core ideas of the iterator pattern.

Writing a classical GoF-style iterator hierarchy would usually be non-Pythonic.

### Factory-like behavior

Because classes and functions are callable objects, a factory is often just a regular function.

### Facade

Modules and packages often naturally act as facades.

## 5.5 Simpler does not mean nonexistent

A pattern may be “invisible” because the language already provides it.

The design concept still exists, but Python removes the need for explicit infrastructure.

---

# 6. Categories of Design Patterns

The traditional Gang of Four classification includes three categories.

| Category | Main concern |
|---|---|
| Creational | How objects are created |
| Structural | How objects are composed and exposed |
| Behavioral | How objects communicate and divide runtime responsibilities |

The chapter focuses on selected patterns that are especially useful or instructive in Python.

---

# 7. Creational Patterns

Creational patterns control or simplify object construction.

They are useful when object creation involves:

- multiple dependencies,
- complex configuration,
- several supporting objects,
- shared state,
- or safety constraints.

The chapter discusses:

- factories,
- singleton alternatives,
- shared state and monostate,
- the Borg pattern,
- and builder.

---

# 8. Factories in Python

## 8.1 Classical purpose

A factory hides the details of creating a particular object.

A caller requests an object without needing to know:

- which concrete class is used,
- how dependencies are assembled,
- or which initialization steps are required.

## 8.2 Why factories are often simpler in Python

Because classes are callable objects, a factory can frequently be a normal function:

```python
def build_service(service_class, dependency):
    return service_class(dependency)
```

The class itself can be passed as a parameter.

## 8.3 When a function is enough

Use a function when creation logic is:

- small,
- stateless,
- easy to understand,
- and unlikely to need its own lifecycle.

## 8.4 When a more formal factory is justified

A dedicated object or dependency-injection library may be useful when creation requires:

- many dependencies,
- environment-specific configuration,
- object graphs,
- caching,
- lifecycle management,
- or alternate implementations.

## 8.5 Clean-code lesson

Do not introduce factory classes merely because a traditional pattern description shows them.

Use the smallest abstraction that safely centralizes object construction.

---

# 9. Singleton: Why It Should Usually Be Avoided

The singleton pattern attempts to guarantee that only one instance of a class exists.

The chapter strongly discourages this pattern in most cases.

## 9.1 Problems with singletons

Singletons behave like global variables.

They can introduce:

- hidden shared state,
- difficult unit testing,
- unpredictable side effects,
- order-dependent behavior,
- tight coupling,
- and difficulty creating subclasses.

Because any component can modify the singleton, it becomes harder to reason about the system.

## 9.2 Python modules as single-instance containers

If a project truly needs one shared object, a module often provides the simplest solution.

Python caches imported modules in:

```python
sys.modules
```

No matter how many times the module is imported, the same module object is reused.

An object created once at module level can therefore be shared.

```python
# configuration.py
settings = Settings()
```

Clients can import the same well-known object.

## 9.3 Well-known object versus singleton class

The author distinguishes between:

- a class that always returns the same instance, and
- an object that is created once and reused.

The second is often simpler.

Examples of well-known objects include:

- `None`,
- `True`,
- and `False`.

The emphasis is not on restricting class construction but on sharing one meaningful object.

---

# 10. Shared State and Monostate

The monostate pattern allows multiple instances to exist while keeping selected state synchronized across them.

This can be safer and more flexible than forcing a single instance.

---

## 10.1 Shared class attribute

The simplest form uses a class variable.

```python
class GitFetcher:
    _current_tag = None

    def __init__(self, tag):
        self.current_tag = tag

    @property
    def current_tag(self):
        if self._current_tag is None:
            raise AttributeError("tag was never set")
        return self._current_tag

    @current_tag.setter
    def current_tag(self, new_tag):
        self.__class__._current_tag = new_tag
```

All instances read and update the same class-level value.

### Example behavior

```python
f1 = GitFetcher(0.1)
f2 = GitFetcher(0.2)

f1.current_tag = 0.3

assert f2.current_tag == 0.3
```

## 10.2 Advantages

- instances remain normal objects,
- the class can still be instantiated,
- the shared behavior is explicit,
- and testing can be simpler than with a singleton constructor.

## 10.3 Risk

Shared state can still cause side effects.

Use it only when synchronized state is a true domain requirement.

---

# 11. Reusable Shared State with a Descriptor

When several attributes need the same shared-state behavior, a descriptor can encapsulate the logic.

```python
class SharedAttribute:
    def __init__(self, initial_value=None):
        self.value = initial_value
        self._name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.value is None:
            raise AttributeError(f"{self._name} was never set")
        return self.value

    def __set__(self, instance, new_value):
        self.value = new_value

    def __set_name__(self, owner, name):
        self._name = name
```

Then:

```python
class GitFetcher:
    current_tag = SharedAttribute()
    current_branch = SharedAttribute()
```

## 11.1 Benefits

The descriptor:

- centralizes shared-state behavior,
- avoids duplicated properties,
- improves cohesion,
- supports DRY,
- and can be unit tested independently.

## 11.2 Tradeoff

The descriptor introduces additional abstraction and code.

It is most justified when the behavior is reused enough to offset that cost.

---

# 12. The Borg Pattern

The Borg pattern is a full monostate approach in which different instances share their entire attribute dictionary.

## 12.1 Core technique

Each instance’s `__dict__` points to the same class-level dictionary.

```python
class TagFetcher:
    _attributes = {}

    def __init__(self, source):
        self.__dict__ = self.__class__._attributes
        self.source = source
```

All instances remain distinct objects, but their attributes are shared.

## 12.2 Why this works

Dictionaries are mutable objects.

When all instances reference the same dictionary, updating an attribute through one instance affects the state observed by all others.

## 12.3 Separate dictionaries per subclass

The shared dictionary should not live on a common base class if different subclasses require separate states.

Otherwise, state from unrelated classes would mix.

## 12.4 Mixin implementation

A mixin can reduce repetition:

```python
class SharedAllMixin:
    def __init__(self, *args, **kwargs):
        try:
            self.__class__._attributes
        except AttributeError:
            self.__class__._attributes = {}

        self.__dict__ = self.__class__._attributes
        super().__init__(*args, **kwargs)
```

Classes can then combine the mixin with their normal base behavior.

## 12.5 Advantages over a singleton

- objects can still be instantiated normally,
- inheritance is more manageable,
- callers do not need a special constructor,
- and identity is separated from shared state.

## 12.6 Risks

The pattern shares **all** instance attributes.

This can create:

- surprising interactions,
- hidden coupling,
- difficult cleanup between tests,
- and broad side effects.

The chapter treats it as a last-resort alternative, not a default design.

---

# 13. Builder Pattern

The builder pattern separates construction of a complex object from its final representation.

## 13.1 Problem solved

A complex object may require:

- many auxiliary objects,
- multiple configuration steps,
- validation,
- dependency wiring,
- and ordered initialization.

Requiring every caller to perform this setup creates duplication and errors.

## 13.2 Builder responsibility

A builder knows how to:

- create each component,
- connect the parts,
- apply configuration,
- and return the finished object.

## 13.3 Typical interface

The caller provides high-level parameters rather than manually constructing every internal dependency.

## 13.4 When it is most useful

The chapter suggests reserving builder-style APIs for:

- frameworks,
- libraries,
- reusable APIs,
- or genuinely complex construction processes.

## 13.5 When it is excessive

If the object can be created clearly with:

- a constructor,
- a class method,
- or a small factory function,

a builder may be unnecessary.

---

# 14. Structural Patterns

Structural patterns organize relationships among objects to create:

- simpler interfaces,
- more capable objects,
- flexible composition,
- or better encapsulation.

The chapter discusses:

- adapter,
- composite,
- decorator,
- and facade.

---

# 15. Adapter Pattern

The adapter pattern makes an incompatible object conform to the interface expected by the application.

It is also commonly called a wrapper.

## 15.1 Problem

Existing code expects:

```python
fetch(user_id, username)
```

A new external dependency provides:

```python
search(namespace)
```

The dependency cannot or should not be modified.

## 15.2 Adapter responsibility

The adapter translates:

- method names,
- argument formats,
- return values,
- or protocols.

---

## 15.3 Adapter through inheritance

```python
class UserSource(UsernameLookup):
    def fetch(self, user_id, username):
        user_namespace = self._adapt_arguments(user_id, username)
        return self.search(user_namespace)
```

### Advantage

The inherited method is directly available.

### Problems

Inheritance introduces:

- tighter coupling,
- inherited methods that may not be needed,
- dependence on the external class hierarchy,
- and a questionable “is-a” relationship.

The adapted object is not necessarily conceptually a subtype of the external dependency.

---

## 15.4 Adapter through composition

```python
class UserSource:
    def __init__(self, username_lookup):
        self.username_lookup = username_lookup

    def fetch(self, user_id, username):
        namespace = f"{user_id}:{username}"
        return self.username_lookup.search(namespace)
```

### Advantages

- lower coupling,
- explicit dependency,
- easier testing,
- and greater flexibility.

Composition is generally preferred.

## 15.5 Generic adaptation with `__getattr__`

A generic adapter could redirect unknown attributes to the wrapped object.

This can reduce repeated forwarding methods, but it may also:

- obscure the interface,
- forward methods unintentionally,
- and make behavior harder to understand.

Use explicit adaptation when clarity matters.

## 15.6 Clean-code contribution

The adapter isolates external incompatibility in one place.

The rest of the application can keep using one stable interface.

---

# 16. Composite Pattern

The composite pattern allows individual objects and groups of objects to be treated through the same interface.

## 16.1 Tree structure

A composite structure contains:

- leaf objects,
- composite or container objects,
- and potentially nested composites.

Clients do not need to distinguish between a leaf and a group.

## 16.2 Store example

A simple product has a price:

```python
class Product:
    @property
    def price(self):
        return self._price
```

A product bundle also has a price:

```python
class ProductBundle:
    @property
    def price(self):
        total = sum(product.price for product in self._products)
        return total * (1 - self._perc_discount)
```

The bundle can contain:

- products,
- or other bundles.

## 16.3 Polymorphism

Both objects expose:

```python
price
```

The bundle recursively asks each contained object for its price.

## 16.4 Benefits

- clients use one interface,
- nested structures are natural,
- recursion is localized,
- and container logic is encapsulated.

## 16.5 Clean-code contribution

The pattern avoids conditionals such as:

```python
if isinstance(item, ProductBundle):
    ...
else:
    ...
```

Each object knows how to provide its own result.

---

# 17. Decorator Pattern

The decorator pattern adds behavior to an object dynamically without modifying the original class or relying on a large inheritance hierarchy.

Do not confuse this pattern with Python’s `@decorator` syntax.

They share the idea of wrapping behavior, but they are not identical concepts.

---

## 17.1 Base object

```python
class DictQuery:
    def __init__(self, **kwargs):
        self._raw_query = kwargs

    def render(self) -> dict:
        return self._raw_query
```

Clients expect a `render()` method.

## 17.2 Decorator object

```python
class QueryEnhancer:
    def __init__(self, query):
        self.decorated = query

    def render(self):
        return self.decorated.render()
```

The wrapper exposes the same interface.

## 17.3 Concrete decorators

```python
class RemoveEmpty(QueryEnhancer):
    def render(self):
        original = super().render()
        return {
            key: value
            for key, value in original.items()
            if value
        }
```

```python
class CaseInsensitive(QueryEnhancer):
    def render(self):
        original = super().render()
        return {
            key: value.lower()
            for key, value in original.items()
        }
```

## 17.4 Chaining

```python
query = CaseInsensitive(RemoveEmpty(original))
```

The operations occur in the order created by the chain.

## 17.5 Advantages

- behavior can be selected at runtime,
- decorators can be combined,
- the original object remains unchanged,
- and multiple inheritance is avoided.

---

# 18. Function-Based Decorator Pattern

Python’s first-class functions provide a simpler alternative when each decoration is just a transformation.

```python
class QueryEnhancer:
    def __init__(self, query, *decorators):
        self._decorated = query
        self._decorators = decorators

    def render(self):
        result = self._decorated.render()

        for decorator in self._decorators:
            result = decorator(result)

        return result
```

Usage:

```python
QueryEnhancer(
    query,
    remove_empty,
    case_insensitive,
).render()
```

## 18.1 When functions are preferable

Use functions when each step:

- is stateless,
- has one transformation,
- and does not need its own identity or lifecycle.

## 18.2 When classes are preferable

Use objects when each decorator:

- has configuration,
- stores state,
- requires multiple methods,
- or represents an important domain concept.

## 18.3 Clean-code lesson

Choose the simplest representation of the behavior.

A function is often more Pythonic than a one-method class.

---

# 19. Facade Pattern

The facade pattern provides one simplified interface in front of a more complex subsystem.

## 19.1 Problem

Without a facade, many objects may need direct knowledge of many other objects.

This creates:

- many-to-many coupling,
- numerous interfaces,
- and difficult coordination.

## 19.2 Facade responsibility

The facade acts as:

- a hub,
- a single entry point,
- and a translator or coordinator.

External clients interact with the facade rather than the internal subsystem.

## 19.3 Benefits

- reduced coupling,
- simpler public API,
- better encapsulation,
- and freedom to refactor internals.

## 19.4 Facades in package design

A package’s `__init__.py` can act as a facade.

Internal modules define implementation objects.

The package root imports and exposes the supported public API.

Clients use:

```python
from package import PublicObject
```

rather than importing internal files directly.

This allows internal modules to be reorganized without breaking users.

## 19.5 Standard-library example

The `os` module acts as a facade over platform-specific modules such as:

- `posix`,
- or `nt`.

Clients import `os`, and the module exposes the correct implementation for the platform.

## 19.6 Clean-code contribution

A facade establishes a stable boundary and protects users from internal complexity.

---

# 20. Behavioral Patterns

Behavioral patterns focus on:

- runtime collaboration,
- division of responsibilities,
- message flow,
- and dynamic behavior.

The chapter discusses:

- chain of responsibility,
- template method,
- command,
- and state.

---

# 21. Chain of Responsibility

The chain of responsibility pattern passes a request through a sequence of handlers until one can process it.

## 21.1 Handler structure

Each handler:

- determines whether it can process the request,
- processes it if possible,
- or forwards it to its successor.

```python
class Event:
    def __init__(self, next_event=None):
        self.successor = next_event

    def process(self, logline):
        if self.can_process(logline):
            return self._process(logline)

        if self.successor is not None:
            return self.successor.process(logline)
```

## 21.2 Concrete handlers

```python
class LoginEvent(Event):
    pattern = re.compile(
        r"(?P<id>\d+):\s+login\s+(?P<value>\S+)"
    )
```

```python
class LogoutEvent(Event):
    pattern = re.compile(
        r"(?P<id>\d+):\s+logout\s+(?P<value>\S+)"
    )
```

## 21.3 Runtime assembly

```python
chain = LogoutEvent(LoginEvent())
```

If the first handler cannot process the input, it passes it to the next.

## 21.4 Dynamic precedence

Because the chain is assembled at runtime, the application can control priority.

```python
chain = SessionEvent(LoginEvent(LogoutEvent()))
```

The first matching handler wins.

## 21.5 Advantages

- handlers are decoupled,
- new handlers can be added,
- processing order is configurable,
- and conditional logic is distributed.

## 21.6 Risks

- order can change behavior,
- an unhandled request may produce no result,
- and long chains can be difficult to trace.

The null object pattern can improve the unhandled case.

---

# 22. Template Method

The template method pattern defines the overall algorithm in a parent class while allowing subclasses to override selected steps.

## 22.1 Structure

The base class defines the stable workflow.

Subclasses customize specific operations.

In the event example:

- `process()` defines the workflow,
- `can_process()` checks suitability,
- `_parse_data()` extracts information,
- and subclasses mainly provide a pattern.

## 22.2 Benefits

- reusable control flow,
- reduced duplication,
- preserved polymorphism,
- and easy extension.

## 22.3 Framework use

A library can expose a base class whose users customize only particular hook methods.

The public algorithm remains compatible.

## 22.4 Design principles

A correct template method supports:

- open/closed principle,
- Liskov substitution,
- and code reuse.

## 22.5 Risk

Inheritance should be used only when subclasses truly share the template.

If variation is highly dynamic, composition may be more flexible.

---

# 23. Command Pattern

The command pattern represents an action as an object.

It separates:

- creation of a request,
- configuration of the request,
- and execution of the request.

## 23.1 Delayed execution

A command can be created now and run later.

In Python, a command can be:

- an object with `__call__()`,
- an object with a method such as `do()`,
- or a closure.

## 23.2 Mutable command configuration

A command object may support:

- adding filters,
- changing parameters,
- recording operations,
- or preparing execution.

## 23.3 Database examples

A database query object may be assembled through several method calls.

The query is not executed until a terminal operation such as:

```python
fetchall()
```

or iteration requests the results.

## 23.4 SQLAlchemy-style behavior

Methods often modify or return the command object, allowing fluent composition:

```python
query.filter(...).order_by(...)
```

## 23.5 Asynchronous use

The command pattern can separate:

- synchronous request preparation,
- from asynchronous execution.

This makes async syntax easier to isolate.

## 23.6 Additional advantages

Commands can support:

- logging,
- auditing,
- queuing,
- scheduling,
- retries,
- and undo behavior.

---

# 24. State Pattern

The state pattern represents each state of an object as a separate object with behavior.

This is useful when behavior changes significantly according to state.

## 24.1 Reification

Reification means turning an implicit concept into an explicit object.

Instead of representing state only with:

- a string,
- an integer,
- or an enumeration,

the design creates state classes.

## 24.2 Problem with one large stateful class

A merge request might have states such as:

- open,
- closed,
- and merged.

If one class handles every transition with `if` statements, it may accumulate:

- many responsibilities,
- complex conditionals,
- duplicated rules,
- and invalid transition checks.

## 24.3 State objects

```python
class MergeRequestState(abc.ABC):
    def __init__(self, merge_request):
        self._merge_request = merge_request

    @abc.abstractmethod
    def open(self):
        ...

    @abc.abstractmethod
    def close(self):
        ...

    @abc.abstractmethod
    def merge(self):
        ...
```

Each concrete state implements the same interface.

## 24.4 Open state

```python
class Open(MergeRequestState):
    def close(self):
        self._merge_request.approvals = 0
        self._merge_request.state = Closed

    def merge(self):
        ...
        self._merge_request.state = Merged
```

## 24.5 Closed state

```python
class Closed(MergeRequestState):
    def merge(self):
        raise InvalidTransitionError(
            "can't merge a closed request"
        )
```

## 24.6 Merged state

Invalid operations raise domain-specific exceptions.

## 24.7 Context object

The main `MergeRequest` delegates operations to its current state.

```python
def merge(self):
    return self.state.merge()
```

The state setter creates the appropriate state object.

## 24.8 Benefits

- each state has focused responsibilities,
- invalid transitions are explicit,
- state-specific rules are localized,
- large conditional blocks disappear,
- and new states can be added more cleanly.

---

# 25. Mutual References in the State Pattern

The state object knows the merge request, and the merge request knows the state object.

This supports transitions because the state must modify the context.

The relationship should generally remain one-to-one.

Potential considerations include:

- garbage collection,
- weak references,
- and lifecycle management.

In ordinary cases, the previous state becomes unreachable after a transition and can be collected.

---

# 26. Delegation with `__getattr__`

The main object may contain repetitive forwarding methods:

```python
def open(self):
    return self.state.open()
```

```python
def close(self):
    return self.state.close()
```

A generic alternative is:

```python
def __getattr__(self, method):
    return getattr(self.state, method)
```

## 26.1 Advantage

Removes repeated delegation code.

## 26.2 Risk

The interface becomes less explicit.

A reader cannot see supported operations directly on the context class.

## 26.3 Role of type annotations

Annotating the state as:

```python
MergeRequestState
```

helps users locate the supported interface.

## 26.4 Clean-code tradeoff

Small amounts of explicit boilerplate may be preferable to clever generic forwarding when readability would suffer.

---

# 27. Null Object Pattern

The null object pattern returns a domain-compatible object instead of `None`.

## 27.1 Problem

A chain may fail to find a handler and return:

```python
None
```

A caller expecting a dictionary may then call:

```python
result.keys()
```

and receive:

```text
AttributeError
```

## 27.2 Simple fix

If the contract says the method returns a dictionary, return:

```python
{}
```

instead of `None`.

## 27.3 Domain object alternative

If a function normally returns a `User`, it may return:

```python
UnknownUser
```

when no user is found.

The null object implements the same expected interface.

## 27.4 Advantages

- preserves polymorphism,
- eliminates repeated `None` checks,
- makes the outcome meaningful,
- and can support logging or debugging behavior.

## 27.5 Exception alternative

The other valid option is to raise a clear domain exception.

The choice depends on whether absence is:

- an expected state,
- or an exceptional condition.

## 27.6 Avoid generic do-nothing objects

A universal object that responds to every operation is dangerous.

It can:

- hide real bugs,
- violate the original interface,
- and lose domain meaning.

`UnknownUser` is clearer than a generic object that silently accepts anything.

---

# 28. Patterns That Often Disappear in Python

The chapter does not cover every traditional pattern in detail because some are naturally absorbed by Python.

## 28.1 Iterator

Use:

- `__iter__`,
- `__next__`,
- generators,
- and normal iteration.

Do not recreate a classical iterator hierarchy.

## 28.2 Strategy

A strategy can frequently be passed as a function.

```python
def process(items, strategy):
    return strategy(items)
```

No separate strategy class is required unless the strategy needs state or multiple operations.

## 28.3 Factory

A function or callable class is often enough.

## 28.4 Command

A function, closure, or callable object may represent the command.

## 28.5 Main lesson

Use the language’s built-in mechanisms before constructing a formal pattern hierarchy.

---

# 29. Composition Versus Inheritance

Many patterns can be implemented with either inheritance or composition.

The chapter frequently favors composition.

## 29.1 Inheritance is appropriate when

- there is a true “is-a” relationship,
- subclasses share a stable template,
- substitutability is preserved,
- and extension points are intentional.

The template method pattern is a reasonable example.

## 29.2 Composition is appropriate when

- one object uses another,
- behavior needs runtime flexibility,
- dependencies should be replaceable,
- or inheritance would expose unrelated methods.

The adapter and decorator patterns often benefit from composition.

## 29.3 Clean-code rule

Prefer composition when inheritance would create unnecessary coupling.

---

# 30. Design Patterns and Polymorphism

A recurring benefit of the patterns in this chapter is preserving a stable interface.

Examples:

- `Product` and `ProductBundle` both expose `price`.
- query decorators preserve `render()`.
- state classes implement `open()`, `close()`, and `merge()`.
- event handlers implement `process()`.
- null objects support the same operations as normal objects.

Python’s duck typing means formal inheritance is not always required.

The core requirement is behavioral compatibility.

---

# 31. Design Patterns and the SOLID Principles

## 31.1 Single Responsibility Principle

Patterns distribute responsibilities.

Examples:

- adapters translate interfaces,
- state objects manage transitions,
- decorators perform one enhancement,
- and builders construct complex objects.

## 31.2 Open/Closed Principle

New behavior can often be added without changing existing code.

Examples:

- new event handlers,
- new query decorators,
- new states,
- and new composite leaves.

## 31.3 Liskov Substitution Principle

Objects exposing the same interface should remain interchangeable.

Examples:

- a bundle should behave like a priced item,
- a null object should behave like its domain type,
- and a state subclass should honor the state interface.

## 31.4 Interface Segregation

Facades and focused objects can expose smaller, clearer interfaces.

## 31.5 Dependency Inversion

Adapters and composition allow high-level code to depend on stable interfaces rather than external implementations.

---

# 32. Patterns as Software Engineering Theory

The author compares design patterns to established theory in other fields.

## 32.1 Chess opening analogy

Experienced chess players do not derive every opening move from scratch.

They learn tested structures and apply that knowledge when appropriate.

## 32.2 Mathematical formula analogy

A developer should understand why a pattern works, but does not need to rediscover it every time the same problem appears.

## 32.3 Practical value

Patterns save:

- time,
- mental energy,
- and communication effort.

They become reusable conceptual building blocks.

---

# 33. Should Code Name the Pattern?

The chapter generally advises against naming production classes after patterns.

## 33.1 Poor naming

```text
EnhancedQueryDecorator
```

This emphasizes implementation technique rather than domain intent.

## 33.2 Better naming

```text
EnhancedQuery
QueryEnhancer
CaseInsensitiveQuery
```

These names describe what the object does.

## 33.3 Why pattern names can be harmful

- users do not need implementation details,
- the name may obscure domain meaning,
- and the design may later evolve away from the pattern.

## 33.4 Documentation exception

Mentioning the pattern in a docstring or design document may be useful for maintainers.

But the code should remain understandable without requiring knowledge of the pattern name.

---

# 34. Pattern Transparency

The best pattern implementations are often invisible to their users.

Examples:

- users of `os` do not need to know that it is acting as a facade,
- Python programmers use the iterator pattern through `for`,
- and callers of a composite do not need to know whether an item is a leaf or a bundle.

Transparency indicates that the abstraction is doing its job.

---

# 35. When Not to Use a Pattern

Do not apply a pattern simply because:

- it is familiar,
- it appears in a book,
- or the problem vaguely resembles the pattern diagram.

Avoid the pattern when:

- a function solves the problem,
- a direct composition is clearer,
- the anticipated variation does not yet exist,
- the abstraction has only one use,
- or the pattern adds more complexity than it removes.

## Questions to ask

1. What current problem does the pattern solve?
2. Which coupling or duplication does it reduce?
3. Does Python already provide the behavior?
4. Can a function or small class solve it more clearly?
5. Will the abstraction improve testing?
6. Is the runtime flexibility actually required?
7. Can future developers understand the result?

---

# 36. Pattern Comparison Table

| Pattern | Problem solved | Typical Python approach | Main caution |
|---|---|---|---|
| Factory | Complex or variable creation | Function, class method, or DI container | Do not build factory hierarchies unnecessarily |
| Singleton | One shared instance | Module-level well-known object | Hidden global state |
| Monostate | Shared state across instances | Class attributes or descriptors | Side effects across instances |
| Borg | Share all instance attributes | Shared `__dict__` | Very broad hidden coupling |
| Builder | Complex multi-step construction | Builder object or fluent API | Excessive for simple objects |
| Adapter | Incompatible interfaces | Composition and explicit translation | Generic forwarding can hide behavior |
| Composite | Treat leaves and groups uniformly | Duck-typed shared interface | Recursive structures can become opaque |
| Decorator | Add behavior dynamically | Wrapper objects or functions | Do not confuse with `@decorator` syntax |
| Facade | Simplify a subsystem | Public service object or package API | Facade can become a “god object” |
| Chain of Responsibility | Try handlers in sequence | Linked objects or handler list | Order affects results |
| Template Method | Reuse an algorithm skeleton | Base class with override hooks | Inheritance can become rigid |
| Command | Represent delayed action | Callable object, function, or closure | Avoid unnecessary command classes |
| State | State-dependent behavior | State objects with delegation | More classes and mutual references |
| Null Object | Avoid `None` checks | Domain-specific empty object | Generic no-op objects hide bugs |

---

# 37. Detailed Clean-Code Lessons by Pattern

## Factory

Centralize complex construction, but prefer simple functions when possible.

## Monostate

Separate object identity from shared state, but recognize that shared state still has risks.

## Adapter

Protect the application from external interfaces and isolate translation logic.

## Composite

Let objects answer the same message rather than writing external type checks.

## Decorator

Add orthogonal behavior through composition and preserve the original interface.

## Facade

Expose one stable entry point and hide internal organization.

## Chain of Responsibility

Replace large conditional dispatch with focused handlers and runtime ordering.

## Template Method

Reuse stable control flow while allowing limited customization.

## Command

Separate intention from execution and make operations easier to queue or delay.

## State

Move state-dependent rules into explicit objects rather than one large conditional class.

## Null Object

Preserve return-type consistency and domain meaning.

---

# 38. Common Mistakes

## 38.1 Treating patterns as mandatory templates

A pattern is a tool, not a requirement.

## 38.2 Recreating patterns Python already provides

Examples include manual iterator frameworks and one-method strategy classes.

## 38.3 Using inheritance for convenience

Inheritance should model substitutability, not merely code reuse.

## 38.4 Creating generic magic-method solutions

Overuse of:

- `__getattr__`,
- shared `__dict__`,
- or universal null objects

can reduce readability and hide errors.

## 38.5 Confusing design-pattern decorator with Python decorator syntax

They overlap conceptually but solve different implementation problems.

## 38.6 Using a singleton for convenient global access

Convenience does not justify hidden shared state.

## 38.7 Overgeneralizing before the pattern is clear

Wait until repeated behavior reveals the actual abstraction.

## 38.8 Naming classes after patterns

Prefer domain intent over implementation vocabulary.

---

# 39. Suggested Refactoring Process Toward a Pattern

When code begins to feel difficult to maintain:

1. Identify duplicated behavior or large conditional structures.
2. identify the responsibility that varies.
3. separate stable behavior from variable behavior.
4. define the smallest compatible interface.
5. move responsibilities into cohesive objects or functions.
6. use composition before inheritance where possible.
7. run tests after each change.
8. compare the new structure with known patterns.
9. keep only the parts of the pattern that improve the design.

Patterns should describe the result of the refactoring, not dictate every step.

---

# 40. Review Questions

1. Why should design patterns emerge rather than be forced?
2. How does Python’s dynamic nature simplify classic patterns?
3. Why is a function often sufficient as a factory?
4. Why does the chapter discourage singletons?
5. How does a module provide a shared object?
6. What is the difference between singleton and monostate?
7. How does a descriptor implement reusable shared state?
8. How does the Borg pattern share attributes?
9. What risks arise from sharing `__dict__`?
10. When is a builder justified?
11. Why is composition generally better for an adapter?
12. How does the composite pattern preserve polymorphism?
13. How does the decorator pattern differ from Python’s `@decorator` syntax?
14. When is a function-based decorator preferable?
15. How does a package’s `__init__.py` act as a facade?
16. Why does the order of a chain of responsibility matter?
17. How does template method reuse code?
18. How can a command support delayed execution?
19. Why does the state pattern reduce conditional complexity?
20. What are the tradeoffs of forwarding through `__getattr__`?
21. Why should a null object be domain-specific?
22. Which patterns are largely built into Python?
23. Why should classes not normally be named after patterns?
24. How do patterns support SOLID principles?
25. When is a simpler solution better than a pattern?

---

# 41. Concise Exam-Style Summary

Chapter 9 explains how common design patterns can support clean Python code when they arise naturally from a real design problem. Patterns are high-level arrangements of responsibilities and object collaboration, not rigid code templates. Python changes many classical implementations because functions, classes, and modules are first-class objects, duck typing reduces the need for formal interfaces, and language features such as iteration and magic methods already embody some patterns.

Creational patterns address object construction. Factories are often regular functions in Python. Singletons should generally be avoided because they create global mutable state; module-level well-known objects or monostate approaches may be simpler. Shared class attributes and descriptors can synchronize selected state, while the Borg pattern shares the full `__dict__` across instances. Builder is useful for genuinely complex object construction, particularly in reusable APIs.

Structural patterns organize object relationships. Adapter translates an incompatible external interface, preferably through composition. Composite lets individual objects and nested groups expose the same interface. Decorator adds behavior dynamically through wrapper objects or functions. Facade exposes one stable entry point to a complex subsystem or package and protects clients from internal changes.

Behavioral patterns organize runtime cooperation. Chain of responsibility sends a request through ordered handlers. Template method places stable control flow in a base class while subclasses customize selected steps. Command represents an action separately from its execution, supporting deferred or asynchronous work. State turns each state into an object so that transitions and state-specific rules are distributed across focused classes rather than one large conditional block.

The null object pattern preserves type consistency by returning a domain-compatible empty object instead of `None`. The chapter concludes that patterns are most valuable as proven theory and a shared vocabulary, but they should remain transparent to users. Code should be named according to domain intent, and simpler Pythonic solutions should always be preferred over unnecessary pattern machinery.

---

# 42. Key Takeaways

1. **Design patterns should emerge from real repeated problems.**
2. **Patterns are conceptual structures, not mandatory code templates.**
3. **Python simplifies many classic object-oriented patterns.**
4. **Use first-class functions instead of unnecessary one-method classes.**
5. **Use duck typing instead of inheritance-only polymorphism.**
6. **Avoid singletons and hidden global state.**
7. **Use modules for shared well-known objects when appropriate.**
8. **Use shared attributes or descriptors for limited monostate behavior.**
9. **Treat the Borg pattern as a risky last resort.**
10. **Use builders only for genuinely complex construction.**
11. **Prefer composition for adapters and decorators.**
12. **Use composites to treat leaves and groups uniformly.**
13. **Use facades to create stable, simple APIs.**
14. **Use chains when runtime handler order matters.**
15. **Use template methods for stable workflows with limited variation.**
16. **Use commands to separate request preparation from execution.**
17. **Use state objects when behavior varies substantially by state.**
18. **Use domain-specific null objects to preserve polymorphism.**
19. **Do not hide complexity behind overly generic magic methods.**
20. **Name code after domain intent, not pattern terminology.**
21. **The best pattern implementations are often invisible to users.**
22. **Use patterns as theory and vocabulary, not as decoration.**
