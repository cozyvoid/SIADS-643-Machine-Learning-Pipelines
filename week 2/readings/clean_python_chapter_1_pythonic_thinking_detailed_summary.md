# Chapter 1 Study Guide: Pythonic Thinking

**Book:** *Clean Python: Elegant Coding in Python*  
**Author:** Sunil Kapil  
**Chapter:** 1 — Pythonic Thinking  
**Primary focus:** Writing Python code that is readable, simple, idiomatic, well documented, and explicit about failure.

> **Code note:** The code examples below are adapted from the chapter and corrected where necessary for valid syntax, current Python behavior, or clearer intent.

---

## 1. Chapter Overview

Chapter 1 introduces **Pythonic thinking**: writing code that uses Python’s conventions and language features in a way that is clear, concise, and maintainable.

Python is intentionally simple at the surface, but that simplicity makes disciplined coding especially important. A project can become difficult to maintain when developers use:

- unclear names,
- clever one-liners,
- overly dense comprehensions,
- hidden return behavior,
- broad exception handlers,
- inconsistent documentation,
- or unnecessary memory-heavy operations.

The chapter presents four broad areas of practice:

1. **Writing Pythonic code**
   - naming variables, functions, classes, constants, and arguments,
   - favoring readable expressions,
   - using common Python idioms,
   - and applying linting tools.

2. **Using docstrings**
   - documenting modules, classes, and functions,
   - choosing a consistent style,
   - and generating external documentation.

3. **Writing Pythonic control structures**
   - using list comprehensions appropriately,
   - deciding between lists and generators,
   - understanding loop `else`,
   - and using `range`.

4. **Raising and handling exceptions**
   - failing clearly instead of returning ambiguous values,
   - cleaning up resources,
   - defining domain-specific exceptions,
   - catching only expected failures,
   - and keeping `try` blocks narrow.

The chapter’s overall message is:

> Pythonic code is not simply code that uses Python syntax. It is code whose intent is obvious, whose behavior is predictable, and whose design makes future changes safer.

---

# 2. What “Pythonic” Means

Pythonic code follows the language’s established philosophy and conventions.

The chapter connects Pythonic thinking with:

- the **Zen of Python**,
- PEP 8,
- readable naming,
- explicit behavior,
- and appropriate use of built-in features.

Some ideas from the Zen of Python that are especially relevant are:

- **Beautiful is better than ugly.**
- **Explicit is better than implicit.**
- **Simple is better than complex.**
- **Readability counts.**
- **There should be one—and preferably only one—obvious way to do it.**
- **Errors should never pass silently.**
- **Practicality beats purity.**

A piece of code can be short without being Pythonic. Pythonic code balances:

- brevity,
- readability,
- correctness,
- and maintainability.

---

# 3. PEP 8 and Style Conventions

PEP 8 is Python’s primary style guide. It standardizes many visual and naming conventions so that code written by different developers remains familiar.

Style consistency reduces the mental effort required to read a codebase. A developer should not need to relearn:

- naming conventions,
- indentation,
- spacing,
- import order,
- or file organization

for every module.

PEP 8 is not a substitute for good design, but it provides a reliable baseline.

---

# 4. Naming Variables and Functions

## 4.1 Use `snake_case`

Variables and functions should normally use lowercase words separated by underscores.

```python
language_name = "Python"
job_title = "Software Engineer"
populated_countries = []

def calculate_tax(amount, tax_rate):
    return amount * tax_rate
```

This is easier to scan than compressed or mixed-case alternatives.

Avoid:

```python
jobtitle = "Software Engineer"
PopulatedCountriesList = []
calculateTaxData()
```

## 4.2 Names should communicate meaning

A name should explain what the value represents.

Weak:

```python
x = 30
data = get_data()
result = process(data)
```

Stronger:

```python
retry_limit = 30
customer_records = load_customer_records()
validated_customers = validate_customers(customer_records)
```

The stronger version reduces the number of assumptions a reader must make.

## 4.3 Avoid ambiguous identifiers

The chapter uses a user lookup as an example.

Ambiguous:

```python
def get_user_info(id):
    return execute_query_for_user(id)
```

Clearer:

```python
def get_user_by_id(user_id):
    return execute_user_query(user_id)
```

Improvements include:

- the function states the lookup key,
- the parameter identifies what kind of ID is expected,
- and the helper name uses the same vocabulary.

This avoids questions such as:

- Is the value a database row ID?
- Is it an account ID?
- Is it a payment ID?
- Does the function return one field or a complete user?

## 4.4 Use domain vocabulary consistently

If the domain uses the term `delivery_id`, do not alternate among:

- `id`,
- `order_key`,
- `delivery_number`,
- and `identifier`

unless they truly represent different concepts.

Consistent language makes code easier to search and understand.

---

# 5. Internal Names and Name Mangling

## 5.1 Single leading underscore

A single leading underscore indicates that a name is intended for internal use.

```python
_cached_books = {}
```

```python
class Repository:
    def _load_from_disk(self):
        ...
```

This is a convention, not access control. Python does not prevent callers from accessing the name.

The underscore communicates:

> This is an implementation detail and is not part of the supported public API.

## 5.2 Double leading underscore

A double leading underscore triggers **name mangling** inside a class.

```python
class Account:
    def __init__(self):
        self.__token = "secret"
```

Python internally changes the attribute name to something similar to:

```python
_Account__token
```

This is mainly intended to prevent accidental name collisions in subclasses. It does **not** provide true privacy or security.

Use double underscores sparingly. A single underscore is usually sufficient for internal implementation details.

## 5.3 Double-ended “dunder” names

Names such as:

```python
__init__
__iter__
__enter__
__exit__
```

are reserved for Python’s special protocols.

Do not invent unrelated custom dunder names because future Python versions may assign meaning to them.

---

# 6. Naming Classes and Constants

## 6.1 Classes use `PascalCase`

```python
class UserInformation:
    ...
```

```python
class WeatherApiClient:
    ...
```

Each word begins with a capital letter and underscores are normally omitted.

## 6.2 Constants use uppercase names

```python
DEFAULT_TIMEOUT = 6
MAX_OVERFLOW = 7
TOTAL_RETRY_COUNT = 5
```

Python does not enforce immutability. Uppercase naming signals that the value should be treated as constant.

## 6.3 Avoid unnecessary type words

Prefer:

```python
countries = []
```

over:

```python
countries_list = []
```

when the type is already obvious or likely to change.

A name should primarily describe the meaning, not the implementation type.

---

# 7. Function and Method Arguments

Arguments follow normal variable naming rules.

```python
def calculate_tax(amount, yearly_tax_rate):
    ...
```

Instance methods conventionally receive `self` first:

```python
class Player:
    def get_total_score(self, player_name):
        ...
```

Class methods conventionally receive `cls` first:

```python
class Player:
    @classmethod
    def from_record(cls, record):
        return cls(record["name"])
```

These names are conventions understood throughout the Python ecosystem.

---

# 8. Readability Over Cleverness

The chapter warns against code written mainly to appear clever or reduce line count.

A compact expression may be acceptable when it remains immediately understandable. The problem begins when brevity hides:

- validation,
- edge cases,
- domain meaning,
- or failure behavior.

## 8.1 Sorting a list of dictionaries

A concise version:

```python
users = [
    {"first_name": "Helen", "age": 39},
    {"first_name": "Buck", "age": 10},
    {"first_name": "Anni", "age": 9},
]

users_by_name = sorted(
    users,
    key=lambda user: user["first_name"].lower(),
)
```

This is reasonable when:

- all items are dictionaries,
- every item has `first_name`,
- and the operation is simple.

A named helper is better when the behavior needs validation, reuse, or explanation:

```python
def normalized_first_name(user):
    """Return a user's first name in lowercase."""
    try:
        return user["first_name"].lower()
    except KeyError as exc:
        raise ValueError("User is missing 'first_name'.") from exc
    except AttributeError as exc:
        raise TypeError("'first_name' must be a string.") from exc


users_by_name = sorted(users, key=normalized_first_name)
```

Advantages of the helper:

- it has a meaningful name,
- it can be tested independently,
- its failures can be explained,
- and tracebacks identify it clearly.

## 8.2 Do not validate the wrong abstraction

The chapter’s original sorting example checks whether `users` is a dictionary even though it is being used as a sequence of dictionaries. A more accurate check would validate the actual contract:

```python
from collections.abc import Iterable, Mapping


def sort_users_by_name(users):
    """Return user mappings sorted by first name."""
    if not isinstance(users, Iterable):
        raise TypeError("users must be an iterable of mappings")

    users = list(users)

    if not users:
        return []

    if not all(isinstance(user, Mapping) for user in users):
        raise TypeError("Every user must be a mapping")

    return sorted(users, key=normalized_first_name)
```

The general lesson is not “always add validation.” It is:

> Make the expected input contract clear and validate the conditions that matter.

---

# 9. Break Complex Work into Helper Functions

A block that performs file handling, parsing, formatting, counting, and printing is difficult to test and debug.

Instead, separate responsibilities.

```python
import csv
from collections.abc import Iterable, Mapping


def process_salary_rows(rows: Iterable[Mapping[str, str]]) -> int:
    """Print employee salary information and return the row count."""
    line_count = 0

    for row in rows:
        print(f'{row["name"]} salary: {row["salary"]}')
        line_count += 1

    return line_count


def read_employee_file(file_name: str) -> int:
    """Read employee data from a CSV file."""
    with open(file_name, mode="r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return process_salary_rows(csv_reader)
```

This design separates:

- resource acquisition,
- CSV parsing,
- and row processing.

Benefits:

- `process_salary_rows()` can be tested with an in-memory list,
- the file is reliably closed,
- failures are easier to locate,
- and future behavior can be added in the appropriate function.

This reflects the **single-responsibility principle**.

---

# 10. String Construction

## 10.1 Use `str.join()` for many pieces

Strings are immutable. Repeated concatenation in a loop can create many intermediate strings.

Avoid:

```python
result = ""

for word in words:
    result += word + " "
```

Prefer:

```python
result = " ".join(words)
```

`join()` communicates that a separator is being placed between a collection of strings.

## 10.2 Use f-strings for a few named values

For a small fixed number of values, an f-string is usually clearer:

```python
full_name = f"{first_name} {last_name}"
```

The practical rule is:

- **many iterable pieces:** use `join()`,
- **a few known values:** use an f-string,
- **avoid repeated `+=` string building in loops.**

---

# 11. Compare with `None` Using `is`

`None` is a singleton sentinel. Test identity, not equality.

```python
if value is None:
    ...
```

```python
if value is not None:
    ...
```

Avoid:

```python
if value == None:
    ...
```

and the less readable:

```python
if not value is None:
    ...
```

## 11.1 Truthiness is not the same as `None`

This check:

```python
if value:
    ...
```

is false for many values:

- `None`,
- `False`,
- `0`,
- `0.0`,
- `""`,
- `[]`,
- `{}`,
- `set()`.

Use truthiness when all false-like values should be treated alike.

Use an explicit `None` check when `None` has a distinct meaning.

```python
if value is not None:
    process(value)
```

This allows empty containers and zero to remain valid inputs.

---

# 12. Prefer `is not` to `not ... is`

These are logically equivalent:

```python
if value is not None:
    ...
```

```python
if not value is None:
    ...
```

The first form is the normal, readable Python style.

---

# 13. Lambda Expressions Versus Named Functions

A lambda is an anonymous, single-expression function.

It is useful when a short function is needed only inside a larger expression:

```python
users_by_age = sorted(users, key=lambda user: user["age"])
```

Do not bind a lambda directly to a descriptive name:

```python
square = lambda value: value * value
```

Prefer:

```python
def square(value):
    """Return the square of a value."""
    return value * value
```

Benefits of `def`:

- the function has a useful name in tracebacks,
- it can have a docstring,
- type hints are easier to read,
- and future expansion is simpler.

A good rule:

> Use a lambda as a small local expression, not as a replacement for a normal named function.

---

# 14. Consistent Return Statements

A function’s return behavior should be predictable across all paths.

Inconsistent:

```python
def calculate_interest(principal, time, rate):
    if principal > 0:
        return principal * time * rate / 100
```

For nonpositive input, Python implicitly returns `None`. That may be intentional, but the contract is unclear.

Explicit version:

```python
def calculate_interest(principal, time, rate):
    """Return simple interest, or None for a nonpositive principal."""
    if principal <= 0:
        return None

    return principal * time * rate / 100
```

A stricter alternative may be better:

```python
def calculate_interest(principal, time, rate):
    """Return simple interest for a valid principal."""
    if principal <= 0:
        raise ValueError("principal must be greater than zero")

    return principal * time * rate / 100
```

The correct choice depends on the domain. The important point is to make the behavior explicit.

---

# 15. Use `startswith()` and `endswith()`

When checking prefixes or suffixes, use the methods that express that intent.

Prefer:

```python
message = "Hello, how are you doing?"

if message.startswith("Hello"):
    ...
```

over:

```python
if message[:5] == "Hello":
    ...
```

Prefer:

```python
if file_name.endswith(".csv"):
    ...
```

over:

```python
if file_name[-4:] == ".csv":
    ...
```

Benefits:

- clearer intent,
- fewer index assumptions,
- tuple support for multiple options,
- and better handling of strings shorter than the target.

```python
if file_name.endswith((".csv", ".tsv")):
    ...
```

---

# 16. Use `isinstance()` for Type Compatibility

Avoid exact type equality when subclasses should be accepted.

Avoid:

```python
if type(user_ages) is dict:
    ...
```

Prefer:

```python
if isinstance(user_ages, dict):
    ...
```

`isinstance()` recognizes subclasses.

For broader behavior-oriented checks, abstract base classes may be even better:

```python
from collections.abc import Mapping

if isinstance(user_ages, Mapping):
    ...
```

This accepts dictionary-like objects that satisfy the intended interface.

## 16.1 Do not overuse type checks

Python often favors duck typing:

```python
try:
    value = record["name"]
except (KeyError, TypeError):
    ...
```

Use `isinstance()` when the type distinction is part of the contract, not as a substitute for good interfaces.

---

# 17. Boolean Expressions

Boolean variables usually do not need comparison with `True` or `False`.

Avoid:

```python
if is_ready == True:
    ...
```

Prefer:

```python
if is_ready:
    ...
```

For the negative condition:

```python
if not is_ready:
    ...
```

Use identity checks only when distinguishing the literal boolean from other truthy or falsey values is genuinely required:

```python
if result is False:
    ...
```

That requirement is less common.

---

# 18. Keep Context Managers Focused

A context manager’s `__enter__()` and `__exit__()` methods should normally manage resource acquisition and release.

They should not hide unrelated business operations.

Clear design:

```python
class ProtocolConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._client = None

    def __enter__(self):
        self._client = Socket()
        self._client.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.close()

    def transfer_data(self, payload):
        self._client.send(payload)

    def receive_data(self):
        return self._client.receive()
```

Usage:

```python
with ProtocolConnection(host, port) as connection:
    connection.transfer_data(payload)
    response = connection.receive_data()
```

Responsibilities remain visible:

- `__enter__()` opens the connection,
- `__exit__()` closes it,
- and the `with` block performs the actual work.

---

# 19. Linting Tools

Linters examine code without running the complete application.

They can identify:

- syntax problems,
- unused variables,
- undefined names,
- import issues,
- naming violations,
- style inconsistencies,
- circular imports,
- complexity,
- docstring problems,
- and possible bugs.

The chapter names tools such as:

- Flake8,
- Pylint,
- and mypy.

## 19.1 Different tools have different roles

| Tool category | Typical purpose |
|---|---|
| Style linter | PEP 8 violations, imports, unused names |
| Static analyzer | likely bugs and code smells |
| Type checker | type compatibility |
| Formatter | consistent layout |
| Docstring checker | documentation conventions |
| Complexity checker | overly complex functions and branches |

Modern projects may combine tools such as:

- Ruff,
- Black,
- mypy or Pyright,
- Pylint,
- and pydocstyle.

## 19.2 Run checks at multiple stages

### In the editor

Immediate feedback while typing.

### Before committing

A pre-commit hook prevents common issues from entering version control.

### In continuous integration

CI ensures every contributor passes the same quality gates.

A practical flow is:

```text
Write code
    ↓
Editor feedback
    ↓
Pre-commit checks
    ↓
Pull request
    ↓
CI linting, typing, and tests
```

## 19.3 Linters are assistants, not designers

Passing a linter does not prove that code is:

- correct,
- well designed,
- secure,
- or understandable.

Linters catch mechanical problems. Human judgment remains necessary.

---

# 20. Docstrings

A docstring documents a module, class, function, or method.

It is placed as the first statement inside the object:

```python
def get_prime_numbers():
    """Return prime numbers between 1 and 100."""
```

Python stores it in the object’s `__doc__` attribute.

```python
print(get_prime_numbers.__doc__)
```

Docstring conventions are primarily described by **PEP 257**, while PEP 8 covers general style.

---

# 21. Basic Docstring Rules

The chapter recommends:

- triple double quotes,
- a concise first line,
- a period at the end,
- and consistent style.

Single-line example:

```python
def normalize_name(name):
    """Return a normalized user name."""
```

Use triple quotes even when the docstring fits on one line so it can be expanded later.

---

# 22. Multiline Docstrings

A multiline docstring normally contains:

1. a short summary line,
2. a blank line,
3. a longer explanation,
4. and optional parameter, return, exception, or usage information.

```python
def call_weather_api(url: str, location: str) -> str:
    """Return weather information for a city.

    The location must be a supported city name. Country and county
    names are not accepted.

    Raises:
        LocationNotFoundError: If the city is not recognized.
    """
```

## 22.1 Do not repeat type hints unnecessarily

When type annotations already state parameter and return types, a docstring should focus on:

- meaning,
- constraints,
- units,
- side effects,
- and exceptional behavior.

Do not merely repeat:

```text
url is a str
location is a str
```

Explain what the values mean.

---

# 23. Major Docstring Styles

The chapter lists four common formats.

## 23.1 Google style

```python
def fetch(url: str) -> dict:
    """Call a URL and return its response.

    Args:
        url: Address to request.

    Returns:
        Parsed response data.
    """
```

## 23.2 reStructuredText style

```python
def fetch(url: str) -> dict:
    """Call a URL and return its response.

    :param url: Address to request.
    :return: Parsed response data.
    """
```

## 23.3 NumPy style

```python
def fetch(url: str) -> dict:
    """Call a URL and return its response.

    Parameters
    ----------
    url
        Address to request.

    Returns
    -------
    dict
        Parsed response data.
    """
```

## 23.4 Epytext style

```python
def fetch(url: str) -> dict:
    """Call a URL and return its response.

    @param url: Address to request.
    @return: Parsed response data.
    """
```

No style is universally best for every project.

The critical requirement is:

> Select one style and use it consistently.

---

# 24. Module-Level Docstrings

A module docstring appears before imports.

```python
"""Provide network request helpers.

The module translates low-level network failures into the public
NetworkError and NetworkNotFound exceptions.
"""

import json
import urllib3
```

A module docstring should explain:

- the purpose of the module,
- its public responsibilities,
- important usage expectations,
- and major public exceptions.

It should not duplicate the detailed documentation of every function.

---

# 25. Class Docstrings

A class docstring explains:

- what the class represents,
- its main responsibility,
- important invariants,
- and possibly a brief usage example.

```python
class Student:
    """Represent a student and expose student profile operations.

    Instances contain identifying and academic information such as
    a name, age, and roll number.
    """
```

Avoid vague descriptions such as:

```text
This class handles things.
```

The docstring should reveal the domain role.

---

# 26. Function Docstrings

A function docstring should focus on:

- what the function does,
- important input constraints,
- the meaning of the result,
- side effects,
- and exceptions.

```python
def is_prime(number: int) -> bool:
    """Return whether an integer is prime.

    Args:
        number: Integer greater than or equal to two.

    Returns:
        True when the number is prime; otherwise False.

    Raises:
        ValueError: If number is less than two.
    """
```

Do not describe every implementation step. Documentation should explain the contract, not narrate the source code.

---

# 27. Documentation Tools

The chapter mentions several tools.

## 27.1 Sphinx

A widely used documentation generator that can build several output formats.

Common uses:

- API documentation,
- guides,
- cross-references,
- and hosted project documentation.

## 27.2 Pycco

Displays source code and accompanying documentation side by side.

## 27.3 Read the Docs

Builds, versions, and hosts documentation, commonly for open-source projects.

## 27.4 Epydoc

Generates API documentation from Python docstrings.

## 27.5 Why automation matters

Generated documentation reduces manual duplication.

A good workflow is:

```text
Docstrings in code
       ↓
Documentation generator
       ↓
Versioned HTML or PDF documentation
       ↓
Published documentation site
```

Documentation should be part of the development process, not postponed until the project is large.

---

# 28. Pythonic Control Structures

Python offers concise tools for iteration and filtering.

These tools are useful only when their use keeps the logic understandable.

The chapter covers:

- list comprehensions,
- lambdas,
- generators,
- loop `else`,
- and `range`.

---

# 29. List Comprehensions

A list comprehension creates a new list from an iterable.

Loop version:

```python
squares = []

for number in numbers:
    squares.append(number**2)
```

Comprehension:

```python
squares = [number**2 for number in numbers]
```

The comprehension directly expresses:

> Build a list containing the square of every number.

## 29.1 Filtering

```python
truthy_items = [item for item in data if item]
```

## 29.2 Transformation and filtering

```python
vowels = {"a", "e", "i", "o", "u"}

selected_vowels = [
    character
    for character in characters
    if character in vowels
]
```

## 29.3 Why comprehensions are useful

They can be:

- concise,
- expressive,
- and faster than a manually appended loop in many cases.

The main benefit is readability, not saving lines at any cost.

---

# 30. Avoid Complex Comprehensions

A comprehension becomes harmful when it contains:

- several nested loops,
- several conditions,
- complex transformations,
- assignments,
- or side effects.

Readable matrix transpose:

```python
transposed = [
    [matrix[row][column] for row in range(height)]
    for column in range(width)
]
```

This has two short loops and a clear purpose.

A dense filtering rule may be clearer as a loop.

Dense:

```python
valid_ages = [
    age
    for age in ages
    if age is not None and 10 < age < 100
]
```

This version is still fairly readable. If more rules are added, use a helper:

```python
def is_valid_age(age):
    """Return whether an age is present and within the accepted range."""
    return age is not None and 10 < age < 100


valid_ages = [age for age in ages if is_valid_age(age)]
```

Or use a loop when several actions are required:

```python
valid_ages = []

for age in ages:
    if not is_valid_age(age):
        continue

    audit_age(age)
    valid_ages.append(age)
```

Rule of thumb:

> Start with a comprehension for one clear transformation or filter. Switch to a helper or loop when the expression stops being instantly readable.

---

# 31. `map()` and `filter()` Versus Comprehensions

The chapter generally favors comprehensions for straightforward transformations and filters.

Using `map()`:

```python
squares = map(lambda number: number**2, numbers)
```

Using a comprehension:

```python
squares = [number**2 for number in numbers]
```

Using `filter()`:

```python
truthy_items = filter(None, data)
```

Using a comprehension:

```python
truthy_items = [item for item in data if item]
```

## 31.1 Important distinction

In Python 3, `map()` and `filter()` return lazy iterators, while a list comprehension immediately builds a list.

If lazy evaluation is desired, a generator expression may be the closest comparison:

```python
squares = (number**2 for number in numbers)
```

Choose based on:

- readability,
- memory needs,
- and whether a materialized list is required.

---

# 32. Appropriate Use of Lambda

Lambda is useful for a small function embedded in another operation.

```python
shortest = min(data, key=lambda item: len(item))
```

This is acceptable because the behavior is:

- short,
- local,
- and used once.

If the logic needs explanation or reuse:

```python
def item_length(item):
    """Return the length used for ordering items."""
    return len(item)


shortest = min(data, key=item_length)
```

The chapter’s recommendation is consistent with PEP 8:

- do not assign a lambda to a name,
- use `def` for named functions,
- keep lambdas inside expressions where their brevity adds clarity.

---

# 33. List Comprehensions Versus Generators

## 33.1 List comprehension

```python
matching_lines = [
    line
    for line in file_object
    if line.startswith(">>")
]
```

This creates the entire list in memory.

Use a list when:

- data is reasonably small,
- the result must be reused,
- indexing or list methods are needed,
- or all results are required immediately.

## 33.2 Generator expression

```python
matching_lines = (
    line
    for line in file_object
    if line.startswith(">>")
)
```

Values are produced as requested.

## 33.3 Generator function

```python
def matching_file_lines(file_name):
    """Yield matching lines from a text file."""
    with open(file_name, encoding="utf-8") as file_object:
        for line in file_object:
            if line.startswith(">>"):
                yield line
```

Usage:

```python
for line in matching_file_lines("logfile.txt"):
    print(line)
```

## 33.4 Benefits of generators

- low memory consumption,
- natural streaming,
- ability to stop early,
- and support for very large or unbounded inputs.

## 33.5 Limitations

A generator is normally consumed once.

After iteration, it is exhausted:

```python
lines = matching_file_lines("logfile.txt")

list(lines)
list(lines)  # Empty because the generator was consumed.
```

To iterate again, create a new generator or materialize the data.

---

# 34. `for`/`while` with `else`

Python allows an `else` clause after a loop.

The `else` block runs when the loop finishes **without executing `break`**.

```python
for number in numbers:
    if number == target:
        print("Found")
        break
else:
    print("Not found")
```

This is best understood as:

> Run `else` if no `break` occurred.

## 34.1 Why it can be confusing

Developers often associate `else` only with `if`, so the meaning may not be obvious.

The chapter recommends avoiding loop `else` when the team finds it difficult to read.

## 34.2 Flag-based alternative

```python
found = False

for number in numbers:
    if number == target:
        found = True
        break

if not found:
    print("Not found")
```

## 34.3 Pythonic clarification

Loop `else` is a legitimate Python feature and can be very clear for searches once the team understands it.

Avoid it when:

- the loop is complex,
- there are several `break` statements,
- or the audience is likely to misread it.

Use it when it cleanly expresses “no break occurred.”

---

# 35. `range()` in Python 3

`range()` represents an immutable arithmetic sequence.

```python
numbers = range(4)
```

This represents:

```text
0, 1, 2, 3
```

```python
list(range(4))
# [0, 1, 2, 3]
```

It stores:

- start,
- stop,
- and step

rather than materializing every integer.

## 35.1 Memory efficiency

```python
range(1_000_000_000)
```

does not allocate a billion integer objects.

## 35.2 Slicing

```python
range(10)[2:7]
# range(2, 7)
```

Reverse step:

```python
range(10)[7:2:-1]
# range(7, 2, -1)
```

## 35.3 Equality

Ranges compare by the sequences they represent:

```python
range(4) == range(0, 4)
# True
```

## 35.4 Use range when the numbers are the purpose

```python
for index in range(10):
    print(index)
```

But do not use `range(len(items))` when direct iteration is clearer:

```python
for item in items:
    process(item)
```

When both index and value are needed:

```python
for index, item in enumerate(items):
    process(index, item)
```

---

# 36. Exception Handling as Part of the API

Exceptions communicate that a function could not fulfill its contract.

Good exception handling improves:

- debugging,
- logging,
- caller behavior,
- production diagnosis,
- and API clarity.

A silent or ambiguous failure can travel through the program and cause a less understandable error later.

---

# 37. EAFP: Ask Forgiveness, Not Permission

Python often favors **EAFP**:

> Easier to ask forgiveness than permission.

Instead of checking every condition before an operation, attempt the operation and handle the expected exception.

Permission-first style:

```python
if key in record:
    value = record[key]
else:
    value = default
```

EAFP:

```python
try:
    value = record[key]
except KeyError:
    value = default
```

EAFP is especially useful when:

- the operation is normally successful,
- the exception is specific,
- and the pre-check could become stale or duplicate work.

It does not mean catching every exception indiscriminately.

---

# 38. Raise an Exception Instead of Returning Ambiguous `None`

Consider division.

Ambiguous:

```python
def divide(dividend, divisor):
    try:
        return dividend / divisor
    except ZeroDivisionError:
        return None
```

A caller may forget to check `None` and fail later.

Clearer options include allowing the original exception:

```python
def divide(dividend, divisor):
    """Return dividend divided by divisor."""
    return dividend / divisor
```

or translating it into a domain-level exception:

```python
class InvalidDivisorError(ValueError):
    """Raised when division is attempted with a zero divisor."""


def divide(dividend, divisor):
    """Return dividend divided by a nonzero divisor."""
    if divisor == 0:
        raise InvalidDivisorError("divisor must not be zero")

    return dividend / divisor
```

The exception tells the caller:

- the operation failed,
- why it failed,
- and where handling is required.

---

# 39. Use `finally` for Required Cleanup

The `finally` block executes whether or not an exception occurs.

```python
resource = acquire_resource()

try:
    use_resource(resource)
finally:
    release_resource(resource)
```

It is useful for ensuring cleanup.

## 39.1 Prefer context managers for common resources

File handling:

```python
with open(file_name, "w", encoding="utf-8") as file_object:
    file_object.write("Python is awesome")
```

The file closes automatically even if writing fails.

## 39.2 Safe SMTP cleanup

A direct `finally` block must account for acquisition failure:

```python
server = None

try:
    server = smtplib.SMTP(host=host, port=port)
    server.login(user, password)
    server.send_message(message)
finally:
    if server is not None:
        server.quit()
```

A library-provided context manager is preferable when available.

---

# 40. Define Custom Exception Classes

Custom exceptions give domain failures meaningful names.

```python
class UserNotFoundError(Exception):
    """Raised when a requested user cannot be found."""
```

Usage:

```python
def get_user_by_id(user_id):
    user = get_user_from_db(user_id)

    if user is None:
        raise UserNotFoundError(
            f"No user found for ID {user_id}."
        )

    return user
```

A caller can handle this exact condition:

```python
try:
    user = get_user_by_id(user_id)
except UserNotFoundError as exc:
    logger.info("User lookup failed: %s", exc)
```

## 40.1 Specific versus broader exceptions

Specific:

```python
class UserNotFoundError(Exception):
    ...
```

Broader category:

```python
class ValidationError(Exception):
    ...
```

Use a broad exception when several failures belong to one meaningful category.

Do not create so many exception classes that the hierarchy becomes harder to understand than the failures themselves.

## 40.2 Store structured context when useful

```python
class ValidationError(Exception):
    """Raised when one or more validation rules fail."""

    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors or {}
```

Structured data can help an API build a useful error response.

---

# 41. Catch Only Expected Exceptions

Avoid bare handlers:

```python
try:
    process_data(data)
except:
    print("Something is wrong")
```

A bare `except` catches nearly every exception derived from `BaseException`, including system-exiting exceptions.

Also avoid overly broad handling:

```python
except Exception:
    ...
```

unless the boundary genuinely requires it and the failure is logged or re-raised appropriately.

Prefer specific exceptions:

```python
try:
    even_numbers = get_even_numbers(numbers)
except TypeError as exc:
    raise ValidationError(
        "numbers must be an iterable of numeric values"
    ) from exc
```

## 41.1 Correct exception for `None`

Iterating over `None` raises `TypeError`; there is no built-in `NoneType` exception class to catch.

```python
try:
    get_even_numbers(None)
except TypeError:
    ...
```

## 41.2 Why specificity matters

Specific handlers:

- document expected failures,
- avoid hiding programming defects,
- make debugging easier,
- and force callers to make deliberate decisions.

---

# 42. When Broad Exception Handling Is Acceptable

A broad handler may be appropriate at a high-level application boundary, such as:

- a worker loop,
- a command-line entry point,
- an HTTP request boundary,
- or a process supervisor.

Even there, it should generally:

- log the traceback,
- translate the failure into a stable external response,
- perform required cleanup,
- or re-raise after logging.

```python
try:
    run_job()
except Exception:
    logger.exception("Unhandled job failure")
    raise
```

The broad handler must not silently turn unknown defects into apparent success.

---

# 43. Translate Third-Party Exceptions

External libraries expose exceptions based on their own terminology.

The application may translate them into domain-specific exceptions.

```python
from botocore.exceptions import ClientError


class InstanceNotFoundError(Exception):
    """Raised when the requested cloud instance does not exist."""


def describe_instance(ec2_client, instance_id):
    try:
        return ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]

        if error_code == "InvalidInstanceID.NotFound":
            logger.info(
                "Cloud instance was not found: %s",
                instance_id,
            )
            raise InstanceNotFoundError(
                f"Instance {instance_id} was not found."
            ) from exc

        raise
```

Important practices:

- inspect documented third-party exception types,
- handle only known error codes,
- preserve the original exception with `raise ... from exc`,
- log useful context,
- and re-raise unknown failures.

Do not translate every third-party exception automatically. Translate when doing so improves the application contract.

---

# 44. Keep `try` Blocks Narrow

A `try` block should contain only the operation expected to fail with the handled exception.

Less clear:

```python
try:
    data = get_data_from_db(query)
    transformed = transform_data(data)
    return format_result(transformed)
except DatabaseConnectionError:
    raise
```

If the block grows, it becomes unclear which line is expected to raise the database exception.

Narrow:

```python
try:
    data = get_data_from_db(query)
except DatabaseConnectionError:
    raise

transformed = transform_data(data)
return format_result(transformed)
```

An `else` clause can make this relationship explicit:

```python
try:
    data = get_data_from_db(query)
except DatabaseConnectionError as exc:
    raise DataAccessError("Could not load data.") from exc
else:
    return transform_data(data)
```

Benefits of narrow `try` blocks:

- clearer intent,
- fewer accidentally caught defects,
- easier debugging,
- and more accurate error translation.

---

# 45. File-Writing Example with Better Exception Boundaries

Rather than wrapping unrelated lines in one broad block:

```python
def write_to_file(file_name, message):
    try:
        file_object = open(file_name, "w")
        file_object.write(message)
        file_object.close()
    except (FileNotFoundError, OSError):
        ...
```

Prefer a context manager and translate only the expected I/O boundary:

```python
class FileWriteError(OSError):
    """Raised when application data cannot be written to a file."""


def write_to_file(file_name, message):
    """Write a message to a UTF-8 text file."""
    try:
        with open(
            file_name,
            mode="w",
            encoding="utf-8",
        ) as file_object:
            file_object.write(message)
    except OSError as exc:
        raise FileWriteError(
            f"Unable to write to {file_name!r}."
        ) from exc
```

The context manager handles closing, and the custom exception expresses the application-level failure.

---

# 46. Important Clarifications to the Chapter’s Examples

Several examples in the source communicate useful principles but contain typographical or conceptual issues. These corrections are worth remembering.

## 46.1 Double underscores cause name mangling

They do not prevent it.

```python
self.__value
```

is transformed to a class-qualified name.

## 46.2 `startswith()` is the preferred form

The source’s “do” and “don’t” labels are reversed in one displayed example. The intended recommendation is:

```python
text.startswith("Hello")
```

rather than manual slicing.

## 46.3 `range(4)` stops before 4

```python
list(range(4))
# [0, 1, 2, 3]
```

The stop value is exclusive.

## 46.4 `NoneType` is not a catchable built-in exception

Operations on `None` commonly raise `TypeError` or `AttributeError`, depending on the operation.

## 46.5 Negative divisors are valid

The problem in arithmetic division is a divisor equal to zero, not a divisor that is less than zero.

## 46.6 Bare Boolean examples need intent

If `is_empty` is `False`, then:

```python
if is_empty:
```

does not run. To check that something is not empty:

```python
if not is_empty:
```

Use a Boolean expression that matches the variable’s meaning.

## 46.7 Context managers should return the managed object

A typical `__enter__()` implementation returns `self` so the object can be used after `as`.

## 46.8 A resource may not have been acquired

When using `finally`, do not call cleanup on a variable that may never have been initialized.

## 46.9 `map()` and `filter()` are lazy in Python 3

Comparisons with list comprehensions should account for the fact that the comprehension creates a list immediately, whereas `map()` and `filter()` return iterators.

---

# 47. Practical Pythonic Coding Checklist

## Naming

- Use `snake_case` for variables and functions.
- Use `PascalCase` for classes.
- Use uppercase names for constants.
- Choose specific domain names.
- Use one leading underscore for internal APIs.
- Use double underscores only when name-mangling behavior is needed.

## Expressions

- Prefer obvious code over clever code.
- Extract helpers when behavior needs a name.
- Use `join()` for many string pieces.
- Use f-strings for a few named values.
- Compare `None` with `is` and `is not`.
- Use `startswith()` and `endswith()`.
- Use `isinstance()` when type compatibility matters.
- Avoid `== True` and `== False`.

## Functions

- Keep functions focused.
- Make return behavior consistent.
- Use named functions instead of assigned lambdas.
- Keep input contracts clear.
- Separate resource management from business operations.

## Tooling

- Run linting in the editor.
- Use pre-commit hooks.
- Repeat checks in CI.
- Add static typing where it clarifies contracts.
- Treat tool warnings as prompts for investigation, not unquestionable rules.

## Documentation

- Add module, class, and function docstrings where they add value.
- Use one docstring style consistently.
- Document contracts rather than implementation details.
- State important exceptions and side effects.
- Generate documentation automatically.

## Control structures

- Use comprehensions for simple transformations and filters.
- Use helpers or loops when conditions become dense.
- Use generators for large or streamed data.
- Use lists when results must be reused or indexed.
- Understand loop `else` before using it.
- Use `range()` for arithmetic sequences and `enumerate()` for indexes plus values.

## Exceptions

- Raise clear exceptions for failed contracts.
- Do not silently return `None` for unexpected failure.
- Catch only expected exception types.
- Translate third-party errors at system boundaries.
- Preserve causes with `raise ... from exc`.
- Keep `try` blocks narrow.
- Use context managers or `finally` for cleanup.
- Log enough context to diagnose production failures.

---

# 48. Chapter Structure by Page Range

| Pages | Main subjects |
|---:|---|
| 1–5 | Pythonic thinking, PEP 8, naming variables, functions, classes, and constants |
| 6–9 | Readability, avoiding clever expressions, helper functions, and single responsibilities |
| 10–17 | Python idioms, `None`, lambdas, returns, strings, types, Booleans, context managers, and linting |
| 18–25 | Docstring rules, styles, module/class/function documentation, and documentation tools |
| 26–37 | List comprehensions, lambdas, generators, loop `else`, and `range()` |
| 37–48 | Exceptions, `finally`, custom exceptions, specific handlers, third-party failures, and narrow `try` blocks |

---

# 49. Review Questions

1. What makes code Pythonic rather than merely valid Python?
2. Why does consistent naming matter in a large codebase?
3. What is the difference between `_name` and `__name` inside a class?
4. When should a lambda be replaced by a named function?
5. Why is `value is None` different from `if value`?
6. When is `str.join()` preferable to repeated concatenation?
7. Why is `startswith()` clearer than slicing?
8. How does `isinstance()` differ from exact `type()` comparison?
9. What should `__enter__()` and `__exit__()` normally do?
10. Which problems can a linter identify?
11. What belongs in a module-level docstring?
12. How do Google, reStructuredText, and NumPy docstring styles differ?
13. When is a list comprehension clearer than a loop?
14. When should a comprehension be converted into a loop or helper?
15. What is the memory difference between a list and a generator?
16. When does a loop’s `else` block execute?
17. Why does `range()` use little memory?
18. What does EAFP mean?
19. Why can returning `None` for an unexpected failure be dangerous?
20. When should a custom exception be introduced?
21. Why should broad exception handlers be avoided?
22. How should third-party exceptions be translated?
23. Why should a `try` block contain as little code as possible?
24. How do exceptions and logging support maintainability in production?

---

# 50. Concise Exam-Style Summary

Chapter 1 introduces Pythonic thinking as the practice of writing code that follows Python’s philosophy of simplicity, explicitness, and readability. PEP 8 provides common style conventions, including `snake_case` for functions and variables, `PascalCase` for classes, and uppercase names for constants. Names should describe domain meaning rather than rely on vague terms such as `data`, `result`, or `id`.

Readable code is preferred over clever one-line expressions. Named helper functions improve testing, debugging, and error reporting when logic requires validation or explanation. Common idioms include using `join()` for multiple string pieces, `is None` for sentinel comparison, `startswith()` and `endswith()` for prefix and suffix checks, `isinstance()` for subtype-compatible type checks, and direct Boolean expressions rather than comparisons with `True` or `False`.

Linters enforce consistent mechanical standards and can identify style violations, unused names, import problems, complexity, and possible errors. They are most effective when integrated into editors, pre-commit hooks, and continuous integration.

Docstrings document the public contract of modules, classes, and functions. They normally use triple double quotes, a concise summary, and optional detail about arguments, results, exceptions, and usage. Projects should choose a consistent style such as Google, reStructuredText, or NumPy format. Tools such as Sphinx and Read the Docs can generate and publish documentation.

List comprehensions are appropriate for simple transformations and filters, while normal loops or helper functions are clearer for complex logic. Generators produce values lazily and are better for large or streamed data, whereas lists are useful when results must be retained and reused. A loop’s `else` clause runs only when no `break` occurs, and `range()` efficiently represents numeric sequences without storing every number.

Exceptions are a core part of an API. Functions should raise meaningful failures rather than hide them by returning ambiguous values. Resource cleanup should use context managers or `finally`. Custom exception classes make domain failures explicit, and handlers should catch only expected exception types. Third-party exceptions may be translated into application-level exceptions while preserving the original cause. Keeping `try` blocks narrow makes failure boundaries easier to understand and prevents unrelated defects from being hidden.

---

# 51. Key Takeaways

1. **Pythonic code prioritizes readability over cleverness.**
2. **Use established naming conventions consistently.**
3. **Choose names that expose domain intent.**
4. **Use a single underscore for internal APIs and double underscores sparingly.**
5. **Break multi-responsibility blocks into focused helpers.**
6. **Use `join()` for collections of strings and f-strings for a few values.**
7. **Compare with `None` using `is` or `is not`.**
8. **Do not confuse falsey values with `None`.**
9. **Use `def` instead of assigning a lambda to a name.**
10. **Make return behavior explicit across all paths.**
11. **Use `startswith()` and `endswith()` for semantic clarity.**
12. **Use `isinstance()` when subclasses should be accepted.**
13. **Keep context managers focused on acquiring and releasing resources.**
14. **Automate linting and static checks throughout development.**
15. **Write consistent, contract-focused docstrings.**
16. **Use comprehensions only while they remain easy to read.**
17. **Use generators for large, streamed, or one-pass data.**
18. **Understand `for`/`while ... else` before using it.**
19. **Use `range()` as an efficient numeric iterable.**
20. **Raise exceptions when a function cannot fulfill its contract.**
21. **Catch specific failures rather than hiding unknown bugs.**
22. **Use custom exceptions to express domain meaning.**
23. **Translate third-party errors at application boundaries.**
24. **Keep `try` blocks as narrow as possible.**
25. **Treat exceptions, logging, and documentation as core maintainability features.**
