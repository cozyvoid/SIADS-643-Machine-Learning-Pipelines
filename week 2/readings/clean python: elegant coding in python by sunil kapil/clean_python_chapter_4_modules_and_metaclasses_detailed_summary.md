# Chapter 4 Study Guide: Working with Modules and Metaclasses

**Book:** *Clean Python: Elegant Coding in Python*  
**Author:** Sunil Kapil  
**Chapter:** 4 — Working with Modules and Metaclasses  
**Primary focus:** Organizing Python code into clear modules and packages, controlling public APIs, and using advanced class-construction tools such as metaclasses, `__new__`, `__slots__`, and descriptors.

> **Code note:** The examples below are adapted from the chapter and corrected where the source uses Python 2 syntax, contains naming errors, or describes behavior inaccurately.

---

# 1. Chapter Overview

Chapter 4 moves from individual functions and classes to two broader Python mechanisms:

- **modules and packages**, which organize code,
- **metaprogramming tools**, which customize how classes and attributes behave.

The chapter’s main argument is that large Python projects remain maintainable only when code is divided into logical units with clear public interfaces.

Modules help developers:

- separate responsibilities,
- avoid namespace collisions,
- reduce coupling,
- reuse behavior,
- and create stable package APIs.

Metaclasses and related mechanisms help library authors:

- modify classes as they are created,
- enforce structural rules,
- generate attributes,
- control instantiation,
- cache instances,
- and build declarative APIs.

The chapter also introduces:

- `__init__.py`,
- import styles,
- `__all__`,
- `__new__`,
- `__slots__`,
- metaclass `__call__`,
- and descriptors.

The overall lesson is:

> Use modules routinely to clarify structure. Use metaclasses and other metaprogramming tools only when they solve a real framework- or library-level problem more clearly than ordinary functions, decorators, or classes.

---

# 2. Modules in Python

A Python module is usually a `.py` file.

```text
payment.py
```

The file name becomes the module name:

```python
import payment
```

A module can contain:

- functions,
- classes,
- constants,
- exceptions,
- and module-level configuration.

Example:

```python
# payment.py

DEFAULT_CURRENCY = "USD"


class PaymentProcessor:
    def charge(self, amount):
        ...
```

Client code:

```python
import payment

processor = payment.PaymentProcessor()
```

---

# 3. Packages

A package groups related modules in a directory.

Example structure:

```text
users/
├── __init__.py
├── info.py
└── payment.py
```

The package separates user-related concerns:

- `info.py` manages user profile data,
- `payment.py` manages user payment behavior.

Import examples:

```python
from users.info import UserProfile
from users.payment import PaymentMethod
```

Packages provide a higher-level namespace and allow a project to grow beyond one large file.

---

# 4. Why Modules Improve Clean Code

The chapter highlights four main benefits.

## 4.1 Scoping

Each module has its own namespace.

```python
# products.py
status = "available"
```

```python
# orders.py
status = "pending"
```

The names do not collide when used with module-qualified access:

```python
import orders
import products

print(products.status)
print(orders.status)
```

## 4.2 Maintainability

Modules establish boundaries.

A developer working on payment logic should not need to modify unrelated cart or profile code.

Clear module boundaries make it easier to:

- locate behavior,
- assign ownership,
- review changes,
- and understand dependencies.

## 4.3 Simplicity

A large problem is divided into smaller components.

Instead of one enormous `ecommerce.py`, use:

```text
ecommerce/
├── cart.py
├── catalog.py
├── orders.py
├── payment.py
└── shipping.py
```

Each module has a focused purpose.

## 4.4 Reusability

A module can be imported from:

- another module,
- a command-line application,
- a web service,
- a test suite,
- or a separate project if packaged.

---

# 5. Module Boundaries and the Single Responsibility Principle

A module should group closely related behavior.

Good:

```text
payments/
├── gateway.py
├── models.py
├── exceptions.py
└── validation.py
```

Less cohesive:

```text
utils.py
```

containing:

- payment calculations,
- email formatting,
- file uploads,
- date parsing,
- and database connections.

A module that becomes a miscellaneous dumping ground is difficult to maintain.

Useful questions include:

- Can the module’s purpose be explained in one sentence?
- Do its functions and classes change for related reasons?
- Does it expose one coherent concept?
- Are unrelated dependencies accumulating?

---

# 6. Naming Modules

PEP 8 recommends short, lowercase module names.

Preferred:

```text
payment.py
cart.py
users.py
validation.py
```

Longer names may use underscores when needed:

```text
payment_gateway.py
user_profile.py
```

Avoid:

```text
Payment.py
credit.card.py
user-payment.py
```

Problems with these names include:

- invalid or confusing import syntax,
- inconsistent conventions,
- and reduced readability.

## 6.1 Do not avoid underscores at the cost of clarity

The source recommends minimizing underscores, but clarity should take priority.

Prefer:

```text
payment_gateway.py
```

over:

```text
paymentgateway.py
```

The Python convention is lowercase names with underscores when they improve readability.

---

# 7. Package Naming

Package names are also usually short and lowercase.

Preferred:

```text
users/
payments/
order_processing/
```

Avoid uppercase package names:

```text
USERS/
Payments/
```

A dot in an import path represents package nesting, not part of a file name.

```python
from users.cards import payment
```

means:

```text
users/
└── cards/
    └── payment.py
```

---

# 8. Import Styles

Python allows several import styles.

## 8.1 Import the module

```python
import user

user.add_to_cart(product)
```

Advantages:

- the origin is visible,
- name collisions are less likely,
- and dependencies are clear.

## 8.2 Import a specific name

```python
from user import add_to_cart

add_to_cart(product)
```

This is concise and can be clear when only a few names are imported.

## 8.3 Star import

```python
from user import *
```

Avoid this in normal application code.

It makes it difficult to know:

- which names were imported,
- where a name came from,
- whether names were overwritten,
- and what the module depends on.

---

# 9. Qualified Imports Improve Traceability

Compare:

```python
from user import add_to_cart

add_to_cart(product)
```

with:

```python
import user

user.add_to_cart(product)
```

The second form makes the dependency explicit at the call site.

This is especially helpful when:

- several modules expose similar names,
- a file is long,
- or a reader is unfamiliar with the project.

---

# 10. Handling Name Collisions

This is ambiguous or invalid because the second import replaces the first:

```python
from mypackage import foo
from yourpackage import foo

foo.get_result()
```

Use module qualification:

```python
import mypackage
import yourpackage

mypackage.foo.get_result()
yourpackage.foo.feed_data()
```

Or use explicit aliases:

```python
from mypackage import foo as my_foo
from yourpackage import foo as your_foo
```

Qualified module imports are often the clearest solution.

---

# 11. Absolute and Relative Imports

Inside a package, Python supports:

- absolute imports,
- explicit relative imports.

## 11.1 Absolute import

```python
from purchase.cart import Cart
```

This names the full package path.

## 11.2 Explicit relative import

Inside `purchase/payment.py`:

```python
from .cart import Cart
```

or:

```python
from . import cart
```

The leading dot means “from the current package.”

## 11.3 Tradeoff

Relative imports can make internal package moves easier.

Absolute imports often make the full dependency clearer.

PEP 8 generally favors absolute imports, while explicit relative imports are acceptable for complex package layouts.

A practical rule:

- use one consistent style,
- avoid implicit relative imports,
- and do not hard-code paths that make refactoring unnecessarily difficult.

---

# 12. `__init__.py`

Historically, `__init__.py` marked a directory as a Python package.

Python 3.3 introduced namespace packages, which can exist without `__init__.py`.

However, `__init__.py` remains useful for:

- defining a public API,
- re-exporting selected names,
- package-level metadata,
- and lightweight package initialization.

---

# 13. Splitting a Module into Submodules

Suppose one module contains both cart and payment behavior.

Initial version:

```python
# purchase.py

class Cart:
    ...


class Payment:
    ...
```

As the code grows, split it:

```text
purchase/
├── __init__.py
├── cart.py
└── payment.py
```

`cart.py`:

```python
class Cart:
    def add_product(self, product):
        ...
```

`payment.py`:

```python
class Payment:
    def charge(self, user, amount):
        ...
```

---

# 14. Re-Exporting a Public API

`purchase/__init__.py` can expose selected classes:

```python
from .cart import Cart
from .payment import Payment

__all__ = ["Cart", "Payment"]
```

Client code:

```python
from purchase import Cart, Payment
```

The client does not need to know the internal file layout.

This creates a stable package-level interface.

---

# 15. Why Re-Exports Are Useful

Without a package API:

```python
from purchase.cart import Cart
from purchase.payment import Payment
```

With a package API:

```python
from purchase import Cart, Payment
```

Benefits:

- simpler imports,
- less knowledge of internal structure,
- easier refactoring,
- and a clear list of supported public names.

The package can later move `Cart` to another module without breaking client code, as long as `purchase.Cart` remains available.

---

# 16. Keep `__init__.py` Lightweight

Avoid using `__init__.py` for:

- expensive database connections,
- large network calls,
- complex initialization,
- or broad side effects.

Importing a package should generally be predictable and inexpensive.

Good uses include:

```python
__version__ = "1.2.0"

from .cart import Cart
from .payment import Payment
```

Poor use:

```python
database = connect_to_production_database()
download_remote_configuration()
```

Import-time side effects make testing and startup behavior harder to control.

---

# 17. `__all__`

`__all__` is a module-level sequence of public names.

```python
__all__ = [
    "CalculatePayment",
    "CreditCardPayment",
]
```

It primarily controls what is imported by:

```python
from payment import *
```

It may also communicate the intended public API to tools and readers.

---

# 18. Correct Behavior of `__all__`

Given:

```python
class MonthlyPayment:
    ...


class CalculatePayment:
    ...


class CreditCardPayment:
    ...


__all__ = [
    "CalculatePayment",
    "CreditCardPayment",
]
```

This star import:

```python
from payment import *
```

imports:

- `CalculatePayment`,
- `CreditCardPayment`.

It does **not** import `MonthlyPayment`.

The source reverses this behavior in its example.

A direct import still works:

```python
from payment import MonthlyPayment
```

`__all__` is not access control.

---

# 19. `__all__` Is Not a Metaclass

The chapter calls `__all__` a “special metaclass class,” which is incorrect.

`__all__` is simply a module-level variable containing names.

It does not:

- create classes,
- modify classes,
- enforce privacy,
- or prevent explicit imports.

Its main role is controlling star-import behavior and documenting public exports.

---

# 20. What a Metaclass Is

An ordinary class creates instances.

```text
Class → instance
```

A metaclass creates classes.

```text
Metaclass → class → instance
```

By default, most Python classes are instances of `type`.

```python
class User:
    pass
```

```python
type(User)
# <class 'type'>
```

The class object `User` was created by the metaclass `type`.

---

# 21. Classes Are Objects

A class is itself an object.

It has:

- a name,
- base classes,
- a namespace,
- attributes,
- methods,
- and a metaclass.

A class can be created dynamically with `type`:

```python
User = type(
    "User",
    (),
    {"role": "member"},
)
```

This is roughly equivalent to:

```python
class User:
    role = "member"
```

The three arguments are:

1. class name,
2. base classes,
3. class namespace.

---

# 22. Python 3 Metaclass Syntax

The source uses:

```python
__metaclass__ = awesome_attr
```

at module or class level.

That syntax is associated with Python 2 and does not define metaclasses in normal Python 3 class declarations.

Python 3 uses:

```python
class Example(
    metaclass=AwesomeMeta,
):
    ...
```

or a metaclass function:

```python
class Example(
    metaclass=awesome_meta,
):
    ...
```

---

# 23. Function-Based Metaclass

A metaclass can be a callable that returns a class.

Corrected example:

```python
def awesome_meta(
    class_name,
    bases,
    namespace,
):
    """Prefix public class attributes with 'awesome_'."""
    transformed = {}

    for name, value in namespace.items():
        if name.startswith("__"):
            transformed[name] = value
        else:
            transformed[
                f"awesome_{name}"
            ] = value

    return type(
        class_name,
        bases,
        transformed,
    )
```

Usage:

```python
class Example(
    metaclass=awesome_meta,
):
    value = "yes"
```

The resulting class has:

```python
Example.awesome_value
# "yes"
```

and not:

```python
Example.value
```

---

# 24. Correcting the Source Metaclass Example

The source contains several issues:

- it creates `awesome_prefix` but writes to `uppercase_attr`,
- `"_".join("awesome", name)` is invalid,
- module-level `__metaclass__` is Python 2 behavior,
- and the discussion mixes metaclasses with special methods.

Correct construction:

```python
f"awesome_{name}"
```

Correct Python 3 declaration:

```python
class Example(
    metaclass=awesome_meta,
):
    ...
```

---

# 25. When to Use Metaclasses

Most application code does not need a custom metaclass.

Metaclasses are appropriate when class creation itself must be customized consistently.

Possible use cases include:

- validating class definitions,
- registering subclasses,
- collecting declared fields,
- generating methods,
- enforcing naming conventions,
- wrapping methods,
- or building declarative frameworks.

Metaclasses are common in:

- ORMs,
- serialization frameworks,
- plugin systems,
- validation libraries,
- and web frameworks.

---

# 26. Why Frameworks Use Metaclasses

Framework users often write simple declarative code:

```python
class User(Model):
    name = CharField(max_length=30)
    age = IntegerField()
```

A metaclass may inspect the class namespace and transform field declarations into:

- descriptors,
- database metadata,
- validation rules,
- queries,
- or schema definitions.

The complexity is handled once inside the framework instead of repeated by every application class.

---

# 27. Metaclass Tradeoffs

Advantages:

- central enforcement,
- reduced application boilerplate,
- declarative APIs,
- automatic registration,
- and consistent class transformation.

Costs:

- harder debugging,
- less obvious control flow,
- unfamiliar syntax,
- complex inheritance interactions,
- and increased cognitive load.

Before creating a metaclass, consider simpler alternatives:

1. a normal function,
2. a class decorator,
3. `__init_subclass__`,
4. a descriptor,
5. a factory,
6. or explicit registration.

---

# 28. `__init_subclass__` as a Simpler Alternative

Modern Python allows a base class to react when a subclass is defined.

```python
class Plugin:
    registry = {}

    def __init_subclass__(
        cls,
        *,
        name,
        **kwargs,
    ):
        super().__init_subclass__(
            **kwargs
        )
        Plugin.registry[name] = cls
```

Usage:

```python
class CsvPlugin(
    Plugin,
    name="csv",
):
    ...
```

This may replace a custom metaclass for straightforward subclass registration.

---

# 29. Class Decorators as a Simpler Alternative

A class decorator can transform a completed class.

```python
def register(cls):
    registry[cls.__name__] = cls
    return cls
```

Usage:

```python
@register
class JsonExporter:
    ...
```

Use a class decorator when the transformation does not require deep control over class creation.

---

# 30. `__new__`

`__new__` creates an instance.

`__init__` initializes an already-created instance.

The order is:

```text
Class is called
    ↓
__new__ creates instance
    ↓
__init__ initializes instance
    ↓
instance returned
```

Basic example:

```python
class User:
    def __new__(
        cls,
        *args,
        **kwargs,
    ):
        print("Creating instance")
        instance = super().__new__(cls)
        return instance

    def __init__(
        self,
        first_name,
        last_name,
    ):
        self.first_name = first_name
        self.last_name = last_name
```

Usage:

```python
user = User(
    "Larry",
    "Page",
)
```

---

# 31. When to Override `__new__`

Override `__new__` when controlling instance creation is necessary.

Common cases include:

- immutable subclasses,
- instance caching,
- singleton-like behavior,
- object interning,
- returning a different subclass,
- or low-level construction rules.

Do not override it for ordinary input validation that belongs naturally in `__init__`.

---

# 32. Validation in `__init__` Is Usually Clearer

The source validates constructor input inside a base class `__new__`.

A simpler design:

```python
class User:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError(
                "name must be a string"
            )

        self.name = name
```

Use `__new__` only when validation must occur before instance creation or when dealing with immutable types.

---

# 33. Base-Class Initialization

If every subclass needs shared state, ordinary base-class initialization is clearer.

```python
class UserBase:
    def __init__(self):
        self.base_property = (
            "Shared property"
        )
```

```python
class User(UserBase):
    def __init__(self, name):
        super().__init__()
        self.name = name
```

This is more explicit than silently assigning state in `__new__`.

---

# 34. `__slots__`

Normally, many Python instances store attributes in `__dict__`.

```python
class User:
    pass
```

```python
user = User()
user.first_name = "Larry"
```

The instance dictionary contains:

```python
user.__dict__
# {"first_name": "Larry"}
```

`__slots__` declares a fixed set of instance attributes and may prevent creation of `__dict__`.

```python
class User:
    __slots__ = (
        "first_name",
        "last_name",
    )
```

---

# 35. Benefits of `__slots__`

Potential benefits include:

- lower memory use per instance,
- slightly faster attribute access in some cases,
- and prevention of accidental new attributes.

These benefits can matter when creating very large numbers of small objects.

Example:

```python
class Coordinate:
    __slots__ = (
        "x",
        "y",
    )

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

Millions of `Coordinate` objects may consume substantially less memory than equivalent objects with dictionaries.

---

# 36. Restrictions of `__slots__`

With:

```python
class User:
    __slots__ = ("first_name",)
```

this works:

```python
user.first_name = "Larry"
```

this fails:

```python
user.last_name = "Page"
# AttributeError
```

The instance does not allow undeclared attributes unless `__dict__` is included.

---

# 37. Adding `__dict__` to `__slots__`

```python
class User:
    __slots__ = (
        "first_name",
        "__dict__",
    )
```

Now dynamic attributes are possible:

```python
user.first_name = "Larry"
user.last_name = "Page"
```

However, including `__dict__` removes much of the memory benefit.

---

# 38. `__slots__` and Inheritance

Slots interact with inheritance.

```python
class Base:
    __slots__ = ()


class Child(Base):
    __slots__ = ("value",)
```

The child has only the declared slot unless a base class introduces `__dict__`.

If a parent class has a normal instance dictionary, a child’s `__slots__` may not provide the expected memory savings.

Use inheritance carefully and test actual object behavior.

---

# 39. When Not to Use `__slots__`

Avoid `__slots__` by default.

It may complicate:

- inheritance,
- pickling,
- weak references,
- dynamic attributes,
- debugging,
- multiple inheritance,
- and some libraries that expect `__dict__`.

Use it after measurement shows that memory usage or attribute access is a real bottleneck.

The chapter’s benchmark values are environment-specific and should not be treated as universal.

---

# 40. Measuring `__slots__` Correctly

`sys.getsizeof()` alone does not show total object memory.

For a normal object, the separate `__dict__` also consumes memory.

A more meaningful comparison includes:

```python
import sys

normal_size = (
    sys.getsizeof(normal_object)
    + sys.getsizeof(
        normal_object.__dict__
    )
)
```

Memory profilers provide better estimates for large collections.

The important lesson is:

> Measure real workloads before introducing `__slots__`.

---

# 41. Callable Objects

Any class can define instance-level `__call__`.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return value * self.factor
```

Usage:

```python
double = Multiplier(2)

double(5)
# 10
```

The instance behaves like a function.

This does not require a metaclass.

---

# 42. Strategy-Like Callable Object

Corrected calculation example:

```python
from collections.abc import Callable


class Calculation:
    def __init__(
        self,
        operation: Callable[
            [int, int],
            int,
        ],
    ):
        self.operation = operation

    def __call__(
        self,
        first_number,
        second_number,
    ):
        if not isinstance(
            first_number,
            int,
        ):
            raise TypeError(
                "first_number must be int"
            )

        if not isinstance(
            second_number,
            int,
        ):
            raise TypeError(
                "second_number must be int"
            )

        return self.operation(
            first_number,
            second_number,
        )
```

Operations:

```python
def add(first, second):
    return first + second


def multiply(first, second):
    return first * second
```

Usage:

```python
addition = Calculation(add)
multiplication = Calculation(
    multiply
)

addition(5, 4)
# 9

multiplication(5, 4)
# 20
```

The source incorrectly calls `self.operation()` without arguments and defines the functions with an unnecessary `self`.

---

# 43. Metaclass `__call__`

When a class is called:

```python
user = User(...)
```

the class’s metaclass `__call__` controls the process.

By default, `type.__call__` roughly performs:

1. `User.__new__`,
2. `User.__init__`,
3. returns the instance.

A custom metaclass can intercept this operation.

```python
class LoggingMeta(type):
    def __call__(
        cls,
        *args,
        **kwargs,
    ):
        print(
            f"Creating {cls.__name__}"
        )
        return super().__call__(
            *args,
            **kwargs,
        )
```

---

# 44. Preventing Instantiation

Correct metaclass example:

```python
class NoInstances(type):
    def __call__(
        cls,
        *args,
        **kwargs,
    ):
        raise TypeError(
            f"{cls.__name__} "
            "cannot be instantiated"
        )
```

Usage:

```python
class UserUtilities(
    metaclass=NoInstances,
):
    @staticmethod
    def print_name(name):
        print(f"Name: {name}")
```

```python
UserUtilities()
# TypeError
```

```python
UserUtilities.print_name(
    "Larry Page"
)
```

## 44.1 Simpler alternative

A module of functions is usually clearer than a non-instantiable utility class.

```python
# user_utils.py

def print_name(name):
    print(f"Name: {name}")
```

Use a metaclass only when the class object itself provides meaningful behavior.

---

# 45. Instance Caching with a Metaclass

A metaclass can return an existing instance when called with the same key.

```python
class CachedById(type):
    def __init__(
        cls,
        name,
        bases,
        namespace,
    ):
        super().__init__(
            name,
            bases,
            namespace,
        )
        cls._instance_cache = {}

    def __call__(
        cls,
        object_id,
        *args,
        **kwargs,
    ):
        if object_id not in (
            cls._instance_cache
        ):
            cls._instance_cache[
                object_id
            ] = super().__call__(
                object_id,
                *args,
                **kwargs,
            )

        return cls._instance_cache[
            object_id
        ]
```

Class using the metaclass:

```python
class Entity(
    metaclass=CachedById,
):
    def __init__(self, object_id):
        self.object_id = object_id
```

Usage:

```python
first = Entity("first")
second = Entity("first")

first is second
# True
```

---

# 46. Corrections to the Source Caching Example

The source contains several problems:

- `class Foo(Memo)` makes `Memo` a base class, not a metaclass,
- the cache is named `__cache` but accessed as `cache`,
- it returns `self.__cache[id]` instead of `_id`,
- the constructor call uses `id=` while `__call__` expects `_id`,
- and `id` shadows Python’s built-in `id()` function.

Correct form:

```python
class Foo(
    metaclass=Memo,
):
    ...
```

Use a name such as `object_id`.

---

# 47. Risks of Instance Caching

Caching instances changes normal object semantics.

Risks include:

- stale state,
- memory growth,
- hidden global state,
- surprising identity behavior,
- test interference,
- and difficult lifecycle management.

Use:

- weak references,
- explicit cache invalidation,
- or a dedicated repository/factory

when appropriate.

A metaclass cache should be justified by a clear identity or resource requirement.

---

# 48. Descriptors

A descriptor is an object that defines one or more of:

- `__get__`,
- `__set__`,
- `__delete__`.

Descriptors customize attribute access.

```text
obj.attribute
    ↓
descriptor.__get__
```

```text
obj.attribute = value
    ↓
descriptor.__set__
```

```text
del obj.attribute
    ↓
descriptor.__delete__
```

Properties, methods, class methods, and static methods all rely on the descriptor protocol.

---

# 49. Descriptor Method Signatures

Correct signatures:

```python
def __get__(
    self,
    instance,
    owner,
):
    ...
```

```python
def __set__(
    self,
    instance,
    value,
):
    ...
```

```python
def __delete__(
    self,
    instance,
):
    ...
```

The source incorrectly describes `__set__` as receiving `owner`.

---

# 50. Data and Non-Data Descriptors

## Data descriptor

Defines:

- `__set__`,
- or `__delete__`.

A data descriptor has high priority over an instance dictionary.

## Non-data descriptor

Defines only `__get__`.

Instance attributes may override it.

This distinction matters when understanding Python’s attribute lookup order.

---

# 51. Dice Descriptor Example

A corrected descriptor:

```python
import random


class Dice:
    """Return a random roll for a configurable number of sides."""

    def __init__(self, sides=6):
        if not isinstance(sides, int):
            raise TypeError(
                "sides must be an integer"
            )

        if sides < 2:
            raise ValueError(
                "sides must be at least 2"
            )

        self.sides = sides

    def __get__(
        self,
        instance,
        owner,
    ):
        if instance is None:
            return self

        return random.randint(
            1,
            self.sides,
        )

    def __set__(
        self,
        instance,
        value,
    ):
        raise AttributeError(
            "dice values are read-only"
        )
```

Usage:

```python
class Game:
    d6 = Dice()
    d10 = Dice(10)
    d20 = Dice(20)
```

```python
game = Game()

game.d6
# Random value from 1 to 6
```

---

# 52. Why `instance is None` Matters

When accessed through the class:

```python
Game.d6
```

Python calls:

```python
Dice.__get__(
    descriptor,
    None,
    Game,
)
```

Returning `self` allows class-level inspection:

```python
Game.d6.sides
# 6
```

Without this check, class access would produce a random roll.

---

# 53. Correcting the Source Dice Example

The source contains multiple errors:

- `self.slides` should be `self.sides`,
- an f-string is missing a closing quote,
- validation checks `instance.sides` instead of `value`,
- assignment changes the descriptor’s shared `sides`,
- indentation is invalid,
- and the printed message is inconsistent.

A descriptor instance stored on the class is shared by all instances.

Changing `self.sides` in `__set__` would change behavior for every `Play` instance.

That may not be the intended design.

---

# 54. Per-Instance Descriptor Storage

A descriptor that stores per-instance values usually needs a unique backing name.

```python
class PositiveInteger:
    def __set_name__(
        self,
        owner,
        name,
    ):
        self.storage_name = (
            f"_{name}"
        )

    def __get__(
        self,
        instance,
        owner,
    ):
        if instance is None:
            return self

        return getattr(
            instance,
            self.storage_name,
        )

    def __set__(
        self,
        instance,
        value,
    ):
        if not isinstance(value, int):
            raise TypeError(
                "value must be an integer"
            )

        if value <= 0:
            raise ValueError(
                "value must be positive"
            )

        setattr(
            instance,
            self.storage_name,
            value,
        )
```

Usage:

```python
class Product:
    quantity = PositiveInteger()

    def __init__(self, quantity):
        self.quantity = quantity
```

The validation is reused across classes and attributes.

---

# 55. Read-Only Descriptor

```python
class ReadOnly:
    def __init__(self, value):
        self.value = value

    def __get__(
        self,
        instance,
        owner,
    ):
        return self.value

    def __set__(
        self,
        instance,
        value,
    ):
        raise AttributeError(
            "attribute is read-only"
        )
```

Descriptors can enforce attribute policies without repeated setter methods.

---

# 56. Descriptors Versus Properties

Use a property when behavior belongs to one attribute in one class.

```python
class Temperature:
    @property
    def fahrenheit(self):
        ...
```

Use a descriptor when the same attribute-management behavior is reused across:

- multiple attributes,
- multiple classes,
- or framework-declared fields.

```python
class User:
    age = PositiveInteger()


class Product:
    quantity = PositiveInteger()
```

A descriptor is a reusable attribute abstraction.

---

# 57. Descriptors Versus `__getattribute__`

`__getattribute__` intercepts nearly every attribute lookup.

It is powerful but easy to misuse.

Descriptors are usually more focused because they control only selected attributes.

Prefer a descriptor when the rule is attached to a particular field.

---

# 58. Modules and Public APIs

A clean package has two layers:

## Internal structure

```text
purchase/
├── _validation.py
├── cart.py
├── payment.py
└── models.py
```

## Public interface

```python
# purchase/__init__.py

from .cart import Cart
from .payment import Payment
from .models import Product

__all__ = [
    "Cart",
    "Payment",
    "Product",
]
```

Users depend on the stable public API rather than internal files.

---

# 59. Internal Modules

A leading underscore can communicate that a module is internal.

```text
purchase/_validation.py
```

Client code should normally not import:

```python
from purchase._validation import ...
```

This remains a convention, not enforcement.

The package may reorganize internal modules without preserving backward compatibility.

---

# 60. Circular Imports

Poor module boundaries can produce circular imports.

Example:

```python
# cart.py
from payment import Payment
```

```python
# payment.py
from cart import Cart
```

Possible symptoms include:

- partially initialized modules,
- missing attributes,
- fragile import ordering,
- and confusing runtime errors.

Solutions include:

- moving shared concepts to a third module,
- depending on abstractions,
- delaying an import locally only when justified,
- or redesigning responsibilities.

Example:

```text
purchase/
├── cart.py
├── payment.py
└── models.py
```

Both modules import shared models without importing each other.

---

# 61. Import-Time Execution

Top-level module code executes once when imported.

```python
print("Module loaded")
```

This can surprise callers.

Avoid expensive or dangerous top-level behavior.

Prefer:

```python
def initialize_service():
    ...
```

and call initialization explicitly.

A common entry-point guard:

```python
def main():
    ...


if __name__ == "__main__":
    main()
```

This prevents command-line behavior from running when the file is imported as a module.

---

# 62. Import Caching

Python caches imported modules in `sys.modules`.

```python
import configuration
import configuration
```

The module is normally executed only once per interpreter process.

This means module-level mutable objects behave like shared state.

```python
# cache.py
items = {}
```

All importers reference the same dictionary.

Use module-level state cautiously.

---

# 63. Practical Module Design Checklist

Before creating or reviewing a module, ask:

- Does the module have one coherent purpose?
- Is the name short, lowercase, and meaningful?
- Are public names clearly defined?
- Is `__init__.py` lightweight?
- Are imports explicit?
- Are star imports avoided?
- Are internal modules marked or hidden behind the package API?
- Are circular dependencies absent?
- Does import execute side effects?
- Can the module be tested independently?
- Are related functions and classes grouped together?
- Would a package boundary be clearer than a larger module?

---

# 64. Practical Metaprogramming Checklist

Before using a metaclass, descriptor, or `__new__`, ask:

- Can a normal function solve the problem?
- Can a class decorator solve it?
- Can `__init_subclass__` solve it?
- Can ordinary inheritance solve it?
- Is the behavior repeated across many classes?
- Does class creation need validation or transformation?
- Will the API become simpler for users?
- Will future developers understand the mechanism?
- Can it be tested thoroughly?
- Is the additional indirection justified?

---

# 65. Common Mistakes from the Chapter

## Mistake 1: Using Python 2 metaclass syntax

Incorrect in normal Python 3:

```python
__metaclass__ = SomeMeta
```

Correct:

```python
class Example(
    metaclass=SomeMeta,
):
    ...
```

## Mistake 2: Treating `__all__` as privacy

`__all__` controls star imports, not direct imports.

## Mistake 3: Calling `__new__` a metaclass

`__new__` is a special method. It can exist on ordinary classes or metaclasses.

## Mistake 4: Using `__new__` for simple validation

Use `__init__` unless pre-construction control is necessary.

## Mistake 5: Introducing `__slots__` without measurement

Slots restrict objects and complicate inheritance.

## Mistake 6: Using a metaclass for a callable instance

Ordinary instance `__call__` is sufficient.

## Mistake 7: Storing per-instance data on the descriptor object

A descriptor placed on a class is shared. Store per-instance values on the instance.

## Mistake 8: Making imports hide dependencies

Prefer explicit module qualification when it improves clarity.

## Mistake 9: Overloading `__init__.py`

Keep package initialization predictable and inexpensive.

## Mistake 10: Using metaclasses in normal application code without a strong reason

Metaclasses should simplify a public abstraction, not merely demonstrate advanced syntax.

---

# 66. Corrected Metaclass Registration Example

A realistic metaclass use case is subclass registration.

```python
class Registered(type):
    registry = {}

    def __new__(
        metaclass,
        name,
        bases,
        namespace,
        **kwargs,
    ):
        cls = super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )

        if name != "Exporter":
            metaclass.registry[
                cls.format_name
            ] = cls

        return cls
```

```python
class Exporter(
    metaclass=Registered,
):
    format_name = None
```

```python
class JsonExporter(Exporter):
    format_name = "json"
```

```python
class CsvExporter(Exporter):
    format_name = "csv"
```

Lookup:

```python
exporter_class = (
    Registered.registry["json"]
)
```

This removes manual registration boilerplate.

---

# 67. Simpler Registration with `__init_subclass__`

The same behavior may not require a metaclass:

```python
class Exporter:
    registry = {}
    format_name = None

    def __init_subclass__(
        cls,
        **kwargs,
    ):
        super().__init_subclass__(
            **kwargs
        )

        if cls.format_name is not None:
            Exporter.registry[
                cls.format_name
            ] = cls
```

This is easier for many teams to understand.

Prefer the simpler mechanism unless the metaclass provides additional necessary behavior.

---

# 68. Relevant Code Summary

## Public package API

```python
# purchase/__init__.py

from .cart import Cart
from .payment import Payment

__all__ = ["Cart", "Payment"]
```

## Python 3 metaclass

```python
class Example(
    metaclass=AwesomeMeta,
):
    ...
```

## Custom metaclass

```python
class AwesomeMeta(type):
    def __new__(
        metaclass,
        name,
        bases,
        namespace,
    ):
        ...
        return super().__new__(
            metaclass,
            name,
            bases,
            namespace,
        )
```

## Instance creation

```python
class User:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        ...
```

## Slots

```python
class Coordinate:
    __slots__ = ("x", "y")
```

## Callable instance

```python
class Operation:
    def __call__(self, value):
        ...
```

## Metaclass call interception

```python
class Cached(type):
    def __call__(cls, key):
        ...
```

## Descriptor

```python
class Field:
    def __get__(
        self,
        instance,
        owner,
    ):
        ...

    def __set__(
        self,
        instance,
        value,
    ):
        ...
```

---

# 69. Review Questions

1. What is the difference between a module and a package?
2. How do modules improve scoping?
3. Why should module names normally be lowercase?
4. When does an underscore improve a module name?
5. Why are star imports discouraged?
6. What are the advantages of module-qualified access?
7. What is the difference between absolute and relative imports?
8. How can `__init__.py` define a public package API?
9. Why should `__init__.py` avoid expensive side effects?
10. What does `__all__` actually control?
11. Why is `__all__` not a security or privacy mechanism?
12. What creates a normal Python class?
13. What is the default metaclass?
14. How is Python 3 metaclass syntax written?
15. Why is the chapter’s module-level `__metaclass__` example outdated?
16. When is a metaclass justified?
17. What simpler alternatives should be considered first?
18. What is the difference between `__new__` and `__init__`?
19. When is overriding `__new__` appropriate?
20. Why is ordinary validation usually clearer in `__init__`?
21. What problem does `__slots__` solve?
22. What restrictions does `__slots__` introduce?
23. Why does adding `__dict__` reduce the value of slots?
24. How does instance `__call__` differ from metaclass `__call__`?
25. How can a metaclass cache instances?
26. What risks come with instance caching?
27. What methods define the descriptor protocol?
28. What is the difference between a data and non-data descriptor?
29. Why should `__get__` handle `instance is None`?
30. When is a property simpler than a descriptor?
31. How can circular imports reveal weak module boundaries?
32. Why should top-level import behavior remain lightweight?

---

# 70. Concise Exam-Style Summary

Chapter 4 explains how modules and packages organize Python projects and how metaprogramming tools customize class and attribute behavior. A module is usually one `.py` file, while a package groups modules under a shared namespace. Well-designed modules support scoping, maintainability, simplicity, and reuse. Module names should normally be short, lowercase, and descriptive.

Imports should make dependencies clear. Star imports are discouraged because they hide where names originate and create collision risks. Importing a module and using qualified names often improves readability. Inside packages, both absolute and explicit relative imports are valid; consistency and clarity are more important than blindly applying one form.

`__init__.py` can re-export selected classes and functions to create a stable package-level API. `__all__` specifies which names participate in star imports, but it does not enforce privacy or prevent direct imports.

A metaclass creates classes in the same way that a class creates instances. In Python 3, metaclasses are declared with `metaclass=...`. Metaclasses are useful for frameworks that need to validate or transform class definitions, register subclasses, gather declared fields, or create declarative APIs. They should be avoided when a function, decorator, descriptor, or `__init_subclass__` can solve the problem more simply.

`__new__` creates an instance before `__init__` initializes it. It is mainly useful for immutable subclasses, caching, or low-level instance control. Ordinary input validation usually belongs in `__init__`.

`__slots__` can reduce instance memory and sometimes improve attribute access by replacing the usual instance dictionary with declared storage slots. It also prevents undeclared attributes and complicates inheritance, dynamic behavior, and some libraries. It should be used only after profiling demonstrates a meaningful need.

An ordinary object can become callable by implementing instance `__call__`. A metaclass can implement its own `__call__` to control what happens when a class is instantiated. This can support behaviors such as instance caching, although such designs introduce hidden shared state and lifecycle risks.

Descriptors define `__get__`, `__set__`, or `__delete__` to customize selected attribute access. They are useful for reusable validation, computed fields, and managed attributes. Properties are built on the same protocol and are usually simpler when behavior belongs to only one class attribute.

---

# 71. Key Takeaways

1. **Use modules to divide a project into cohesive responsibilities.**
2. **Use lowercase, readable module and package names.**
3. **Prefer explicit imports over star imports.**
4. **Use qualified module access when it improves traceability.**
5. **Use `__init__.py` to define a stable public package API.**
6. **Keep package initialization lightweight.**
7. **Use `__all__` to document and control star-import exports.**
8. **Do not treat `__all__` as access control.**
9. **Remember that classes are objects created by metaclasses.**
10. **Use Python 3 `metaclass=...` syntax.**
11. **Consider functions, decorators, descriptors, and `__init_subclass__` before metaclasses.**
12. **Use metaclasses mainly for framework-level class transformation or enforcement.**
13. **Use `__new__` only when instance creation itself must change.**
14. **Use `__init__` for normal initialization and validation.**
15. **Adopt `__slots__` only after measuring a real memory or performance need.**
16. **Understand that slots restrict dynamic attributes and complicate inheritance.**
17. **Use instance `__call__` for callable objects.**
18. **Use metaclass `__call__` only when class instantiation must be controlled globally.**
19. **Treat instance caching as shared state with lifecycle risks.**
20. **Use descriptors for reusable attribute-management behavior.**
21. **Store per-instance descriptor values on the instance, not the shared descriptor.**
22. **Use properties when one class needs one managed attribute.**
23. **Avoid circular imports by improving module boundaries.**
24. **Avoid expensive or surprising code at import time.**
25. **Use advanced Python mechanisms to simplify an API—not to make ordinary code look clever.**
