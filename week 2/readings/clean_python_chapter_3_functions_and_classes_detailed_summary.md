# Chapter 3 Study Guide: Writing Better Functions and Classes

**Book:** *Clean Python: Elegant Coding in Python*  
**Author:** Sunil Kapil  
**Chapter:** 3 — Writing Better Functions and Classes  
**Primary focus:** Designing focused functions and classes that are readable, predictable, testable, and aligned with Python conventions.

> **Code note:** The examples below are adapted from the chapter and corrected where the source contains syntax errors, naming inconsistencies, or behavior that does not match valid Python.

---

# 1. Chapter Overview

Chapter 3 focuses on two of Python’s central building blocks:

- functions,
- classes.

The chapter’s main idea is that good functions and classes have:

- clear responsibilities,
- understandable boundaries,
- predictable return behavior,
- useful failure behavior,
- readable interfaces,
- and internal structures that are easy to navigate.

The chapter repeatedly returns to the **single responsibility principle (SRP)**:

> A function or class should have one clear reason to change.

This does not mean every function must be only a few lines long or every class must fit on one screen. Size is less important than responsibility.

The chapter covers the following major topics:

## Functions

- create small, focused functions,
- use generators for large or unknown data volumes,
- raise exceptions instead of returning ambiguous `None`,
- use default and keyword arguments for readable interfaces,
- avoid unnecessary explicit `None` returns,
- write defensive code with logging and tests,
- and use lambdas only for trivial local expressions.

## Classes

- determine class size by responsibility rather than line count,
- organize class members consistently,
- use properties for computed values and validation,
- use static methods only when behavior belongs conceptually to the class,
- use abstract base classes when subclasses must implement a contract,
- use class methods as alternative constructors,
- and avoid unnecessary private-style getters and setters.

---

# 2. Functions Are Objects in Python

Python functions are first-class objects.

They can be:

- assigned to variables,
- passed into other functions,
- returned from functions,
- stored in collections,
- decorated,
- and inspected.

```python
def normalize_name(name):
    return name.strip().title()


normalizer = normalize_name

print(normalizer("  ada lovelace "))
# Ada Lovelace
```

Because functions are flexible, it is especially important to design them carefully.

A function should communicate:

- what it expects,
- what it does,
- what it returns,
- and how it fails.

---

# 3. Create Small, Focused Functions

The chapter recommends that a function perform one main task.

The goal is not to minimize line count mechanically. The goal is to avoid mixing unrelated responsibilities.

A function may contain several steps while still performing one cohesive job.

For example, a function that validates, transforms, and saves a user might actually contain three different responsibilities:

```python
def process_user(user):
    validate_user(user)
    normalized_user = normalize_user(user)
    save_user(normalized_user)
```

This orchestration function is still cohesive because its responsibility is coordinating the user-processing workflow.

The implementation details remain separated.

---

# 4. Measuring Function Size by Responsibility

The chapter argues that function size should be judged by task boundaries, not only by:

- number of lines,
- number of characters,
- or number of statements.

A useful diagnostic question is:

> Can I describe this function accurately with one short sentence?

If the description requires “and” several times, the function may contain multiple responsibilities.

For example:

> Read a file **and** parse email addresses **and** deduplicate them **and** print the results.

This suggests multiple units of behavior.

---

# 5. Email Extraction Example

The chapter begins with a function that both reads a file and extracts email addresses.

## 5.1 Combined version

```python
import re


def get_unique_emails(file_name):
    """Read a file and return the unique email addresses it contains."""
    emails = set()

    with open(file_name, encoding="utf-8") as file_object:
        for line in file_object:
            matches = re.findall(
                r"[\w.-]+@[\w.-]+",
                line,
            )

            for email in matches:
                emails.add(email)

    return emails
```

This function performs at least two concerns:

1. file iteration,
2. email extraction and deduplication.

## 5.2 Separated version

```python
import re
from collections.abc import Iterator


EMAIL_PATTERN = re.compile(
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"
)


def read_lines(file_name: str) -> Iterator[str]:
    """Yield lines from a UTF-8 text file."""
    with open(file_name, encoding="utf-8") as file_object:
        yield from file_object


def extract_emails(text: str) -> list[str]:
    """Return email-like values found in a string."""
    return EMAIL_PATTERN.findall(text)


def get_unique_emails(file_name: str) -> set[str]:
    """Return unique email addresses found in a text file."""
    emails: set[str] = set()

    for line in read_lines(file_name):
        emails.update(extract_emails(line))

    return emails
```

This version separates:

- file reading,
- regex extraction,
- and deduplication.

## 5.3 Why this is cleaner

Each function can be tested separately.

```python
def test_extract_emails():
    text = "Contact ada@example.com or grace@example.org."
    assert extract_emails(text) == [
        "ada@example.com",
        "grace@example.org",
    ]
```

The file-reading behavior can also be replaced or reused independently.

---

# 6. Refactor After the First Working Version

The chapter recommends a practical sequence:

1. make the feature work,
2. confirm the behavior,
3. inspect the code for duplication and mixed responsibilities,
4. refactor into cleaner functions,
5. keep tests passing throughout.

This avoids premature abstraction.

A developer often understands the correct boundaries only after seeing the first complete implementation.

This follows a common cycle:

```text
Make it work
    ↓
Make it clear
    ↓
Make it efficient, if necessary
```

---

# 7. Return Generators for Large or Unknown Data

A generator function uses `yield` to produce values one at a time.

```python
def read_lines(file_name):
    """Yield lines from a text file."""
    with open(file_name, encoding="utf-8") as file_object:
        for line in file_object:
            yield line
```

Calling this function does not immediately read the entire file.

```python
lines = read_lines("application.log")
```

`lines` is a generator object.

Values are produced as iteration requests them:

```python
for line in lines:
    process(line)
```

---

# 8. Why Generators Matter

Generators are useful for two major reasons.

## 8.1 Lazy execution

The function pauses at each `yield`.

Python resumes from that point when the next value is requested.

Conceptually:

```text
Call generator function
      ↓
Receive generator object
      ↓
Request next value
      ↓
Run until yield
      ↓
Pause and preserve state
      ↓
Request another value
      ↓
Resume after yield
```

## 8.2 Lower memory use

A list stores every result at once.

```python
def load_lines(file_name):
    with open(file_name, encoding="utf-8") as file_object:
        return list(file_object)
```

A generator streams values:

```python
def stream_lines(file_name):
    with open(file_name, encoding="utf-8") as file_object:
        yield from file_object
```

The generator is preferable when:

- the input can be very large,
- only one pass is required,
- processing can occur incrementally,
- or consumers may stop before reading everything.

---

# 9. Generator-Based Email Extraction

The chapter changes the email function to yield matches.

```python
def iter_emails(file_name):
    """Yield email addresses found in a text file."""
    for line in read_lines(file_name):
        for email in extract_emails(line):
            yield email
```

Usage:

```python
for email in iter_emails("messages.txt"):
    print(email)
```

## 9.1 Important distinction: this is not unique

The source names the generator `get_unique_emails`, but simply yielding every match does not remove duplicates.

For uniqueness, a set of previously seen values is still needed:

```python
def iter_unique_emails(file_name):
    """Yield each email address once, preserving discovery order."""
    seen = set()

    for email in iter_emails(file_name):
        if email in seen:
            continue

        seen.add(email)
        yield email
```

This uses memory proportional to the number of unique email addresses, but it avoids storing every duplicate occurrence.

---

# 10. When to Return a List, Set, or Generator

## Return a list when:

- consumers need indexing,
- consumers need repeated iteration,
- the result size is known and manageable,
- ordering matters,
- or the full result is naturally one value.

```python
def get_active_user_ids(users):
    return [
        user.id
        for user in users
        if user.is_active
    ]
```

## Return a set when:

- uniqueness is the main contract,
- ordering does not matter,
- and all results fit comfortably in memory.

```python
def get_unique_domains(emails):
    return {
        email.rsplit("@", 1)[1]
        for email in emails
    }
```

## Return a generator when:

- the input may be large,
- results can be processed incrementally,
- only one pass is needed,
- or early termination is useful.

```python
def iter_error_lines(file_name):
    for line in read_lines(file_name):
        if "ERROR" in line:
            yield line
```

The return type should match the caller’s needs, not a blanket rule.

---

# 11. Raise Exceptions Instead of Returning Ambiguous `None`

The chapter warns against returning `None` for every unexpected situation.

`None` may mean:

- invalid input,
- missing data,
- no match,
- a file error,
- a parsing failure,
- or normal absence.

When several meanings collapse into one value, callers cannot reliably determine what happened.

---

# 12. Ambiguous File Search Example

A problematic function:

```python
def read_lines_for_python(file_name, file_type):
    if not file_name or file_type not in {"txt", "html"}:
        return None

    with open(file_name, encoding="utf-8") as file_object:
        for line in file_object:
            if "python" in line.lower():
                return "Found Python"
```

This function returns `None` when:

- the filename is missing,
- the type is unsupported,
- the word does not occur,
- or the file has no lines.

These are not the same situation.

---

# 13. Clearer Failure and Return Contracts

A better version separates invalid inputs from the valid “not found” result.

```python
from pathlib import Path


SUPPORTED_FILE_TYPES = {"txt", "html"}


def contains_python(file_name: str, file_type: str) -> bool:
    """Return whether a supported text file contains the word 'python'."""
    if file_type not in SUPPORTED_FILE_TYPES:
        raise ValueError(
            f"Unsupported file type: {file_type!r}"
        )

    if not file_name:
        raise ValueError("file_name must not be empty")

    path = Path(file_name)

    if not path.exists():
        raise FileNotFoundError(path)

    with path.open(encoding="utf-8") as file_object:
        return any(
            "python" in line.lower()
            for line in file_object
        )
```

Now the contract is clear:

- invalid format → `ValueError`,
- missing file → `FileNotFoundError`,
- valid file with no match → `False`,
- valid file with a match → `True`.

---

# 14. Exceptions Should Match the Failure

Use exception types that accurately describe the problem.

| Problem | Appropriate exception |
|---|---|
| Unsupported argument value | `ValueError` |
| Wrong argument type | `TypeError` |
| Missing file | `FileNotFoundError` |
| Missing mapping key | `KeyError` |
| Invalid object state | custom domain exception |
| Failed external service | translated service exception |

Avoid using `IOError` merely because a filename string is empty. An empty argument is generally a `ValueError`.

---

# 15. Default Arguments

Default arguments allow a caller to omit commonly used values.

```python
def calculate_sum(
    first_number=5,
    second_number=10,
):
    return first_number + second_number
```

Calls:

```python
calculate_sum()
# 15

calculate_sum(50)
# 60

calculate_sum(90, 10)
# 100
```

Defaults can make simple APIs convenient.

## 15.1 Defaults should reflect a genuine common case

A default is appropriate when:

- the meaning is obvious,
- the value is safe,
- and omission is a normal usage pattern.

A default is less appropriate when omission might hide a mistake.

```python
def delete_user(user_id=None):
    ...
```

A missing `user_id` is likely an error, so it should probably be required.

---

# 16. Avoid Mutable Default Arguments

The chapter does not discuss this directly, but it is essential when using defaults.

Avoid:

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

The same list is reused across calls.

```python
add_tag("python")
# ["python"]

add_tag("clean-code")
# ["python", "clean-code"]
```

Use `None` as a sentinel:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []

    tags.append(tag)
    return tags
```

This creates a fresh list when no collection is supplied.

---

# 17. Keyword Arguments Improve Call-Site Readability

Long positional calls are difficult to interpret.

```python
analyze_spam_email(
    "ab_from@gmail.com",
    "nb_to@yahoo.com",
    "Is email spam",
    10_000,
    "ab",
    "nb",
)
```

A reader must look up the function signature to understand each value.

Keyword arguments make intent visible:

```python
analyze_spam_email(
    from_address="ab_from@gmail.com",
    to_address="nb_to@yahoo.com",
    subject="Is email spam",
    size_bytes=10_000,
    sender_name="ab",
    receiver_name="nb",
)
```

This is especially useful when:

- arguments share the same type,
- there are more than two or three values,
- Boolean flags are present,
- or the order is not memorable.

---

# 18. Reserved Keywords Cannot Be Parameter Names

The source uses `from` as a parameter name, but `from` is a Python keyword.

Invalid:

```python
def spam_email(from, to):
    ...
```

Valid alternatives:

```python
def spam_email(from_address, to_address):
    ...
```

or, less clearly:

```python
def spam_email(from_, to):
    ...
```

Prefer a domain-specific name such as `from_address`.

---

# 19. Keyword-Only Arguments

Python can require selected arguments to be passed by name.

```python
def analyze_spam_email(
    from_address,
    *,
    to_address,
    subject,
    size_bytes,
    sender_name,
    receiver_name,
):
    ...
```

The `*` marks all following parameters as keyword-only.

Valid:

```python
analyze_spam_email(
    "ab_from@gmail.com",
    to_address="nb_to@yahoo.com",
    subject="Is email spam",
    size_bytes=10_000,
    sender_name="ab",
    receiver_name="nb",
)
```

Invalid:

```python
analyze_spam_email(
    "ab_from@gmail.com",
    "nb_to@yahoo.com",
    "Is email spam",
    10_000,
    "ab",
    "nb",
)
```

Benefits:

- clearer calls,
- safer API evolution,
- fewer argument-order mistakes,
- and more readable Boolean or configuration parameters.

---

# 20. Positional-Only Arguments

Modern Python also supports positional-only arguments with `/`.

```python
def ratio(numerator, denominator, /):
    return numerator / denominator
```

This is useful when parameter names are implementation details and callers should not depend on them.

Most application APIs benefit more from keyword-only arguments than positional-only arguments.

---

# 21. Do Not Return `None` for Invalid Input

The chapter presents functions that either return a valid result or `None`.

```python
def add_numbers(first_number, second_number):
    if (
        isinstance(first_number, int)
        and isinstance(second_number, int)
    ):
        return first_number + second_number

    return None
```

This forces every caller to check:

```python
result = add_numbers(10, "5")

if result is None:
    ...
```

A better contract raises an exception:

```python
def add_numbers(first_number: int, second_number: int) -> int:
    """Return the sum of two integers."""
    if not isinstance(first_number, int):
        raise TypeError("first_number must be an integer")

    if not isinstance(second_number, int):
        raise TypeError("second_number must be an integer")

    return first_number + second_number
```

In many cases, explicit checks are unnecessary because the operation naturally raises `TypeError`:

```python
def add_numbers(first_number, second_number):
    return first_number + second_number
```

Whether explicit validation is worthwhile depends on the API and the clarity of the natural exception.

---

# 22. `None` Can Still Be a Valid Result

The recommendation is not “never return `None`.”

`None` is appropriate when absence is part of the documented contract.

Example:

```python
def find_user_by_email(users, email):
    """Return the matching user, or None when no user matches."""
    for user in users:
        if user.email == email:
            return user

    return None
```

Here, “not found” is an expected result, not a failure.

The important distinction is:

- expected absence → `None` may be appropriate,
- invalid input or failed contract → raise an exception.

---

# 23. Return Empty Collections for Empty Results

If a function’s contract is “return a collection,” an empty collection is often clearer than `None`.

```python
def find_odd_numbers(numbers):
    """Return all odd integers from an iterable."""
    return [
        number
        for number in numbers
        if number % 2 != 0
    ]
```

No odd values:

```python
find_odd_numbers([2, 4, 6])
# []
```

The caller can iterate safely without special checks.

```python
for number in find_odd_numbers(values):
    process(number)
```

---

# 24. Corrected Odd-Number Example

The source’s examples reverse the type check in several places.

A valid sequence-based implementation:

```python
from collections.abc import Iterable


def find_odd_numbers(numbers: Iterable[int]) -> list[int]:
    """Return the odd integers from an iterable."""
    if isinstance(numbers, (str, bytes)):
        raise TypeError(
            "numbers must be an iterable of integers"
        )

    odd_numbers = []

    for number in numbers:
        if not isinstance(number, int):
            raise TypeError(
                "every item must be an integer"
            )

        if number % 2 != 0:
            odd_numbers.append(number)

    return odd_numbers
```

Examples:

```python
find_odd_numbers([2, 4, 7, 8])
# [7]

find_odd_numbers((1, 3, 6))
# [1, 3]

find_odd_numbers([2, 4, 6])
# []
```

This contract accepts any suitable iterable rather than requiring exactly a list.

---

# 25. Defensive Programming

Defensive programming anticipates likely failures and makes them visible.

The chapter highlights two key practices:

- logging,
- unit testing.

Additional defensive techniques include:

- input validation,
- assertions for internal invariants,
- type hints,
- static analysis,
- explicit exception boundaries,
- and immutable data where practical.

Defensive programming should not become excessive checking of every possible condition. The goal is to protect important boundaries and assumptions.

---

# 26. Logging

Logging records useful runtime information.

Unlike `print()`, the logging system supports:

- levels,
- timestamps,
- module names,
- structured output,
- files or remote handlers,
- and configurable verbosity.

## 26.1 Basic configuration

```python
import logging


logger = logging.getLogger(__name__)
```

Application entry point:

```python
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(name)s "
        "%(levelname)s %(message)s"
    ),
)
```

## 26.2 Logging an expected failure

```python
def divide(dividend, divisor):
    try:
        return dividend / divisor
    except ZeroDivisionError:
        logger.exception(
            "Division failed because divisor was zero"
        )
        raise
```

`logger.exception()` should be used inside an exception handler when the traceback is useful.

---

# 27. Logging Levels

Common levels are:

| Level | Typical use |
|---|---|
| `DEBUG` | detailed diagnostic information |
| `INFO` | normal significant events |
| `WARNING` | unexpected condition that did not stop the operation |
| `ERROR` | operation failed |
| `CRITICAL` | application or subsystem may be unable to continue |

Example:

```python
logger.info(
    "User account created",
    extra={"user_id": user.id},
)
```

```python
logger.warning(
    "Retrying request after timeout"
)
```

```python
logger.error(
    "Marketing email delivery failed"
)
```

The level should reflect operational severity.

---

# 28. Corrected Logging Example

The source logging sample contains several syntax errors. A working version:

```python
import logging


logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)

formatter = logging.Formatter(
    "%(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.WARNING)


def divide(dividend, divisor):
    try:
        return dividend / divisor
    except ZeroDivisionError:
        logger.exception("Cannot divide by zero")
        raise
```

Corrections include:

- `import`, not `Import`,
- instantiate `StreamHandler()`,
- `setFormatter`, not `setFromatter`,
- `except`, not `catch`,
- and re-raise after logging unless the failure is intentionally recovered.

---

# 29. Logging Should Add Context

A log message should help answer:

- what operation failed,
- which entity was involved,
- which input was relevant,
- and whether the system recovered.

Weak:

```python
logger.error("Error")
```

Better:

```python
logger.exception(
    "Failed to load customer record",
    extra={"customer_id": customer_id},
)
```

Avoid logging:

- passwords,
- access tokens,
- full payment card numbers,
- health information,
- or unnecessary personal data.

---

# 30. Unit Testing

Unit tests verify small behaviors in isolation.

The chapter mentions:

- `unittest`,
- pytest.

## 30.1 `unittest`

```python
import unittest


def sum_numbers(x, y):
    return x + y


class SumNumbersTest(unittest.TestCase):
    def test_adds_two_numbers(self):
        self.assertEqual(
            sum_numbers(3, 4),
            7,
        )
```

## 30.2 pytest

```python
def sum_numbers(x, y):
    return x + y


def test_sum_numbers_adds_two_values():
    assert sum_numbers(3, 4) == 7
```

The source uses `func(3, 4)`, but the intended call is `sum_numbers(3, 4)`.

---

# 31. Benefits of Unit Tests

The chapter identifies several roles.

## 31.1 Documentation

A clear test demonstrates expected behavior.

```python
def test_find_odd_numbers_returns_empty_list_when_none_exist():
    assert find_odd_numbers([2, 4, 6]) == []
```

## 31.2 Confidence during change

Tests show whether refactoring changed existing behavior.

## 31.3 Regression prevention

When a defect is fixed, a test can preserve the correction.

```python
def test_contains_python_is_case_insensitive(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text(
        "PYTHON is present",
        encoding="utf-8",
    )

    assert contains_python(
        str(file_path),
        "txt",
    )
```

## 31.4 Design feedback

A function that is difficult to test may have:

- hidden dependencies,
- too many responsibilities,
- or direct side effects.

Testing pressure can improve the production design.

---

# 32. Test-Driven Development

Test-driven development follows:

1. write a failing test,
2. write the minimum code needed to pass,
3. refactor while tests remain green.

```text
Red
 ↓
Green
 ↓
Refactor
```

The chapter correctly notes that unit tests are valuable even when a team does not practice TDD.

---

# 33. Lambda Expressions

The chapter warns against lambda overuse.

A lambda is appropriate when:

- the operation is trivial,
- it is used once,
- it does not need a name,
- and it improves the surrounding expression.

Example:

```python
numbers = [-5, 2, -1, 4]

sorted_by_absolute_value = sorted(
    numbers,
    key=abs,
)
```

Here, `abs` is even clearer than a lambda:

```python
key=lambda number: abs(number)
```

Use existing named functions when possible.

---

# 34. Source Example Clarification: Lambda and Sorting

The chapter discourages:

```python
sorted(numbers, key=lambda number: abs(number))
```

and replaces it with:

```python
def sorted_numbers(numbers):
    return sorted(numbers, reverse=True)
```

These do **not** have equivalent behavior.

- `key=abs` sorts by absolute magnitude.
- `reverse=True` sorts by numeric value in descending order.

Equivalent named-function version:

```python
def absolute_value(number):
    """Return the absolute value used for sorting."""
    return abs(number)


sorted_numbers = sorted(
    numbers,
    key=absolute_value,
)
```

Best version:

```python
sorted_numbers = sorted(numbers, key=abs)
```

The broader lesson remains valid:

> Prefer a named function when a lambda becomes difficult to understand.

---

# 35. Avoid Dense Lambda Pipelines

The chapter shows a natural-sort expression built from multiple lambdas and regex operations.

A clearer implementation:

```python
import re
from typing import Union


NaturalPart = Union[int, str]


def convert_natural_part(text: str) -> NaturalPart:
    """Convert a numeric string to an integer."""
    return int(text) if text.isdigit() else text.casefold()


def natural_sort_key(text: str) -> list[NaturalPart]:
    """Return a key that sorts embedded numbers numerically."""
    return [
        convert_natural_part(part)
        for part in re.split(r"(\d+)", text)
    ]


data = ["abc10", "abc9", "abc5", "cba2"]
data.sort(key=natural_sort_key)
```

This version is:

- named,
- testable,
- easier to debug,
- and easier to extend.

---

# 36. Classes and the Single Responsibility Principle

A class should represent one cohesive concept.

The correct class size is determined by:

- responsibility,
- cohesion,
- and reasons to change.

Line count alone is not a reliable measure.

A 200-line class with one focused purpose may be healthier than a 40-line class that mixes unrelated concerns.

---

# 37. Define Class Scope Before Adding Methods

The chapter uses a `UserInformation` example.

Reasonable responsibilities:

- store profile information,
- expose full name,
- update contact details,
- validate profile fields.

Unrelated responsibilities:

- process payments,
- calculate order totals,
- send shipping notifications,
- query every database table.

Those concerns belong in separate components such as:

- `PaymentService`,
- `OrderRepository`,
- `NotificationService`.

A useful question before adding a method is:

> Does this method belong to the concept represented by this class?

---

# 38. Duplicate Code Can Reveal a Missing Class

Suppose several classes repeat database connection logic.

```python
class Payment:
    def load_customer(self, customer_id):
        connection = create_connection()
        ...
```

```python
class Order:
    def load_customer(self, customer_id):
        connection = create_connection()
        ...
```

This may indicate a missing abstraction:

```python
class CustomerRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_by_id(self, customer_id):
        ...
```

Consumers depend on the repository instead of repeating data-access logic.

This improves:

- reuse,
- testing,
- consistency,
- and separation of concerns.

---

# 39. Suggested Class Member Order

The chapter proposes the following class organization:

1. class variables,
2. `__init__`,
3. special methods,
4. class methods,
5. static methods,
6. properties,
7. instance methods,
8. private/internal methods.

This is a convention, not a language requirement.

The most important goals are:

- consistency,
- discoverability,
- and grouping related methods near each other.

A reasonable alternative is to keep a public method next to the private helper it uses when this makes the flow easier to read.

---

# 40. Example Class Structure

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


class Employee:
    POSITIONS = (
        "Supervisor",
        "Manager",
        "CEO",
        "Founder",
    )

    def __init__(
        self,
        employee_id: int,
        name: str,
        department: str,
        birthday: date,
    ) -> None:
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.birthday = birthday

    def __str__(self) -> str:
        return (
            f"Name: {self.name}\n"
            f"Department: {self.department}"
        )

    @classmethod
    def available_positions(
        cls,
        excluded_position: str,
    ) -> list[str]:
        return [
            position
            for position in cls.POSITIONS
            if position != excluded_position
        ]

    @staticmethod
    def is_executive_position(
        position: str,
    ) -> bool:
        return position in {"CEO", "Founder"}

    @property
    def id_with_name(self) -> tuple[int, str]:
        return self.employee_id, self.name

    @property
    def age(self) -> int:
        return self._calculate_age(date.today())

    def change_department(
        self,
        department: str,
    ) -> None:
        self.department = department

    def _calculate_age(self, today: date) -> int:
        years = today.year - self.birthday.year
        birthday_this_year = self.birthday.replace(
            year=today.year
        )

        if today < birthday_this_year:
            years -= 1

        return years
```

This example keeps:

- public state visible,
- computed age behind a property,
- internal calculation in a helper,
- and methods grouped consistently.

---

# 41. Class Variables

Class variables are shared by the class and its instances unless shadowed.

```python
class Employee:
    POSITIONS = (
        "Supervisor",
        "Manager",
        "CEO",
    )
```

They are useful for:

- constants,
- supported values,
- shared configuration,
- and immutable metadata.

Be careful with mutable class variables:

```python
class Team:
    members = []
```

Every instance shares the same list.

Prefer:

```python
class Team:
    def __init__(self):
        self.members = []
```

unless shared state is intentional.

---

# 42. `__init__`

`__init__` establishes a valid instance.

It should communicate:

- required dependencies,
- initial state,
- and important invariants.

```python
class Employee:
    def __init__(
        self,
        employee_id,
        name,
        department,
    ):
        self.employee_id = employee_id
        self.name = name
        self.department = department
```

Avoid performing excessive work in `__init__`, such as:

- network calls,
- expensive database queries,
- file downloads,
- or starting background processes.

Heavy work makes construction:

- slow,
- failure-prone,
- and difficult to test.

Use a factory or class method when construction requires complex preparation.

---

# 43. Special Methods

Special methods integrate a class with Python protocols.

Examples include:

- `__str__`,
- `__repr__`,
- `__len__`,
- `__iter__`,
- `__eq__`,
- `__enter__`,
- and `__exit__`.

```python
class Employee:
    def __str__(self):
        return (
            f"{self.name} "
            f"({self.department})"
        )
```

These methods should preserve predictable Python behavior.

Avoid surprising implementations, such as making `__len__` perform a network request.

---

# 44. Class Methods

A class method receives the class as `cls`.

```python
class User:
    @classmethod
    def from_string(cls, value):
        ...
```

It is commonly used for:

- alternative constructors,
- factory-style creation,
- parsing,
- deserialization,
- or behavior that belongs to the class itself.

Because `cls` is used instead of the concrete class name, subclasses can inherit the method correctly.

---

# 45. Static Methods

A static method receives neither `self` nor `cls`.

```python
class PriceCalculator:
    @staticmethod
    def ratio(numerator, denominator):
        return numerator / denominator
```

Use a static method when:

- the behavior is conceptually tied to the class,
- but it does not need instance or class state.

Use a module-level function when:

- the behavior is broadly reusable,
- it is not central to the class concept,
- or placing it in the class would create an artificial grouping.

---

# 46. Static Method Example

The source places a “price-to-book ratio” method inside `BookPriceCalculator`. The terminology is financially confusing because “book value per share” relates to stock valuation, not the price of a physical book.

A more coherent example:

```python
class BookPriceCalculator:
    PER_PAGE_PRICE = 0.08

    def __init__(self, pages):
        if pages <= 0:
            raise ValueError(
                "pages must be greater than zero"
            )

        self.pages = pages

    @property
    def standard_price(self):
        return self.pages * self.PER_PAGE_PRICE

    @staticmethod
    def apply_discount(
        price,
        discount_rate,
    ):
        if not 0 <= discount_rate <= 1:
            raise ValueError(
                "discount_rate must be between 0 and 1"
            )

        return price * (1 - discount_rate)
```

The static method is related to pricing but does not require a particular book instance.

---

# 47. When a Module Function Is Better

A static method may be unnecessary.

Instead of:

```python
class TextProcessor:
    @staticmethod
    def normalize_whitespace(text):
        return " ".join(text.split())
```

a module function may be clearer:

```python
def normalize_whitespace(text):
    return " ".join(text.split())
```

Choose a static method only when the namespace provides meaningful organization.

---

# 48. Properties

A property exposes method behavior through attribute syntax.

```python
class Temperature:
    def __init__(self, celsius=0.0):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 1.8 + 32
```

Usage:

```python
temperature = Temperature(10)

print(temperature.fahrenheit)
# 50.0
```

The caller sees a value-like attribute rather than an action method.

---

# 49. Properties Should Behave Like Attributes

A getter property should normally:

- return a value,
- be inexpensive,
- avoid surprising side effects,
- and be safe to access repeatedly.

Problematic:

```python
@property
def fahrenheit(self):
    self.celsius = (
        self.celsius * 1.8 + 32
    )
```

Reading the property changes the object.

This violates normal attribute expectations.

Correct:

```python
@property
def fahrenheit(self):
    return self.celsius * 1.8 + 32
```

---

# 50. Property Setters for Validation

Properties can validate assignment while preserving attribute syntax.

```python
class Temperature:
    ABSOLUTE_ZERO_CELSIUS = -273.15

    def __init__(self, celsius=0.0):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if not isinstance(
            value,
            (int, float),
        ):
            raise TypeError(
                "celsius must be numeric"
            )

        if value < self.ABSOLUTE_ZERO_CELSIUS:
            raise ValueError(
                "temperature cannot be below absolute zero"
            )

        self._celsius = float(value)

    @property
    def fahrenheit(self):
        return self.celsius * 1.8 + 32
```

Usage:

```python
temperature = Temperature(20)
temperature.celsius = 25

print(temperature.fahrenheit)
# 77.0
```

---

# 51. Corrected Fahrenheit Setter

The source’s property example uses mismatched names and attempts to raise a string.

Invalid:

```python
raise("Wrong input type")
```

Python exceptions must derive from `BaseException`.

A coherent Fahrenheit setter:

```python
class Temperature:
    def __init__(self, celsius=0.0):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 1.8 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        if not isinstance(
            value,
            (int, float),
        ):
            raise TypeError(
                "fahrenheit must be numeric"
            )

        self.celsius = (
            float(value) - 32
        ) / 1.8
```

Now the getter and setter represent the same logical property.

---

# 52. Do Not Hide Expensive Operations in Properties

Avoid:

```python
@property
def customer_orders(self):
    return database.query_orders(
        self.customer_id
    )
```

A caller may assume property access is cheap.

Prefer an explicit method:

```python
def load_customer_orders(self):
    return database.query_orders(
        self.customer_id
    )
```

Properties are best for:

- derived values,
- validated state,
- backward-compatible attribute evolution,
- and inexpensive calculations.

---

# 53. Abstract Base Classes

An abstract base class defines a required interface for subclasses.

The chapter contrasts two approaches.

## 53.1 Manual `NotImplementedError`

```python
class Fruit:
    def taste(self):
        raise NotImplementedError

    def origin(self):
        raise NotImplementedError
```

This allows accidental construction:

```python
fruit = Fruit()
```

The error occurs only when a missing method is called.

## 53.2 `abc` module

```python
from abc import ABC, abstractmethod


class Fruit(ABC):
    @abstractmethod
    def taste(self) -> str:
        """Return a description of the fruit's taste."""

    @abstractmethod
    def origin(self) -> str:
        """Return the fruit's geographic origin."""
```

Incomplete subclasses cannot be instantiated.

```python
class Apple(Fruit):
    def origin(self):
        return "Central Asia"
```

```python
Apple()
# TypeError: Can't instantiate abstract class Apple
# with abstract method taste
```

Complete implementation:

```python
class Apple(Fruit):
    def taste(self):
        return "sweet and tart"

    def origin(self):
        return "Central Asia"
```

---

# 54. Why Abstract Base Classes Help

They provide:

- an explicit interface,
- early failure,
- clearer documentation,
- consistent subclass behavior,
- and improved static analysis.

They are valuable when multiple implementations must honor the same contract.

Examples:

- payment providers,
- storage backends,
- parsers,
- exporters,
- and notification channels.

---

# 55. Abstract Base Classes Versus Duck Typing

Python does not require every interface to use inheritance.

A function may accept any object with a required method:

```python
def send_report(exporter, report):
    exporter.export(report)
```

This is duck typing.

Use an abstract base class when:

- incomplete implementations must fail early,
- the interface is central and stable,
- shared implementation belongs in the base class,
- or explicit registration is valuable.

Use duck typing or protocols when:

- flexibility matters,
- third-party classes cannot inherit from the base,
- or only structural compatibility is required.

Modern typing also supports `Protocol`:

```python
from typing import Protocol


class Exporter(Protocol):
    def export(self, report) -> None:
        ...
```

---

# 56. Class Methods as Alternative Constructors

A class method can build the same class from a different input format.

```python
class User:
    def __init__(
        self,
        first_name,
        last_name,
    ):
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_string(cls, full_name):
        first_name, last_name = full_name.split(
            maxsplit=1
        )
        return cls(
            first_name,
            last_name,
        )
```

Usage:

```python
user = User.from_string(
    "Larry Page"
)
```

This creates a clear, named construction path.

---

# 57. Multiple Deserialization Constructors

```python
import json
from pathlib import Path


class User:
    def __init__(
        self,
        first_name,
        last_name,
    ):
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_string(cls, full_name):
        first_name, last_name = full_name.split(
            maxsplit=1
        )
        return cls(
            first_name,
            last_name,
        )

    @classmethod
    def from_mapping(cls, data):
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
        )

    @classmethod
    def from_json(cls, json_text):
        return cls.from_mapping(
            json.loads(json_text)
        )

    @classmethod
    def from_file(cls, file_name):
        text = Path(file_name).read_text(
            encoding="utf-8"
        )
        return cls.from_json(text)
```

Usage:

```python
user_from_string = User.from_string(
    "Larry Page"
)

user_from_json = User.from_json(
    '{"first_name": "Grace", '
    '"last_name": "Hopper"}'
)

user_from_file = User.from_file(
    "user.json"
)
```

---

# 58. Why `cls` Matters

Avoid hard-coding the class:

```python
@classmethod
def from_mapping(cls, data):
    return User(
        data["first_name"],
        data["last_name"],
    )
```

Prefer:

```python
@classmethod
def from_mapping(cls, data):
    return cls(
        data["first_name"],
        data["last_name"],
    )
```

A subclass will then receive an instance of the subclass.

```python
class AdminUser(User):
    ...
```

```python
admin = AdminUser.from_mapping(data)
```

Using `cls` preserves inheritance behavior.

---

# 59. Correcting the Source Serialization Example

The source returns `Student` from `User` constructors and splits on an empty string. Both are errors.

A correct implementation should:

- return `cls(...)`,
- split a full name with whitespace,
- parse JSON before constructing,
- and return an instance, not the class object.

Correct:

```python
@classmethod
def from_string(cls, full_name):
    first_name, last_name = full_name.split(
        maxsplit=1
    )
    return cls(first_name, last_name)
```

---

# 60. Public, Internal, and Name-Mangled Attributes

Python does not enforce access modifiers like Java’s:

- `public`,
- `protected`,
- `private`.

Instead, naming conventions communicate intent.

## Public

```python
self.full_name
```

Supported for normal caller use.

## Internal

```python
self._full_name
```

Not intended as part of the stable public API.

## Name-mangled

```python
self.__full_name
```

Transformed to reduce accidental subclass collisions.

It is not true privacy.

---

# 61. Prefer Public Attributes Over Trivial Getters

The chapter warns against Java-style getter methods for every attribute.

Cumbersome:

```python
class Person:
    def __init__(
        self,
        first_name,
        last_name,
    ):
        self._full_name = (
            f"{first_name} {last_name}"
        )

    def get_name(self):
        return self._full_name
```

Simpler:

```python
class Person:
    def __init__(
        self,
        first_name,
        last_name,
    ):
        self.full_name = (
            f"{first_name} {last_name}"
        )
```

Usage:

```python
person = Person(
    "Larry",
    "Page",
)

print(person.full_name)
```

Python callers normally access data attributes directly.

---

# 62. Use a Property When Behavior Is Needed Later

Public attributes can evolve into properties without changing caller syntax.

Initial version:

```python
class Person:
    def __init__(self, full_name):
        self.full_name = full_name
```

Later, validation is required:

```python
class Person:
    def __init__(self, full_name):
        self.full_name = full_name

    @property
    def full_name(self):
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        if not value.strip():
            raise ValueError(
                "full_name must not be empty"
            )

        self._full_name = value.strip()
```

Caller code remains:

```python
person.full_name
```

This is why Python does not require speculative getters and setters.

---

# 63. When to Use a Single Leading Underscore

Use `_name` when an attribute or method:

- is an implementation detail,
- may change without notice,
- should not be relied on by callers,
- or supports public methods internally.

```python
class UserService:
    def create_user(self, data):
        validated = self._validate(data)
        return self._save(validated)

    def _validate(self, data):
        ...
```

The underscore is a communication mechanism, not a security boundary.

---

# 64. When to Use Double Leading Underscores

Double leading underscores are mainly useful to avoid accidental subclass collisions.

```python
class BaseProcessor:
    def __init__(self):
        self.__state = "ready"
```

Python mangles the name approximately to:

```python
_BaseProcessor__state
```

A subclass using its own `__state` receives a different mangled name.

```python
class SpecializedProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.__state = "specialized"
```

This is helpful when:

- designing a base class for inheritance,
- the subclass is outside your control,
- and accidental name conflicts are a realistic concern.

---

# 65. Name Mangling Does Not Make Data Private

The value is still accessible:

```python
processor._BaseProcessor__state
```

Therefore, name mangling should not be used to protect:

- passwords,
- tokens,
- encryption keys,
- or sensitive data.

It is an inheritance-collision mechanism, not access control.

---

# 66. Corrected Inheritance Example

The source’s final example omits required arguments, calls nonexistent methods, and comments inconsistent values.

A valid demonstration:

```python
class Person:
    def __init__(
        self,
        first_name,
        last_name,
    ):
        self.age = 50
        self.full_name = (
            f"{first_name} {last_name}"
        )


class Child(Person):
    def __init__(
        self,
        first_name,
        last_name,
    ):
        super().__init__(
            first_name,
            last_name,
        )
        self.__age = 20

    @property
    def child_age(self):
        return self.__age


child = Child(
    "Ada",
    "Lovelace",
)

print(child.age)
# 50

print(child.child_age)
# 20
```

The subclass’s `__age` does not overwrite the public `age` attribute.

However, this example does not prove that public attributes are inferior. It only demonstrates name separation.

---

# 67. Cohesion and Coupling

Good functions and classes should have:

- high cohesion,
- low coupling.

## High cohesion

Methods and data belong to one concept.

```python
class Invoice:
    def calculate_total(self):
        ...

    def calculate_tax(self):
        ...
```

## Low coupling

The class does not know unnecessary details about other systems.

Instead of:

```python
class Invoice:
    def save(self):
        connection = psycopg2.connect(...)
        ...
```

inject a repository:

```python
class InvoiceService:
    def __init__(self, invoice_repository):
        self._invoice_repository = (
            invoice_repository
        )
```

This makes testing and replacement easier.

---

# 68. Function and Class Contracts

A clean function or class exposes an understandable contract.

A contract includes:

- accepted inputs,
- returned outputs,
- possible exceptions,
- side effects,
- state changes,
- and performance expectations where relevant.

Type hints and docstrings can document the contract:

```python
def find_odd_numbers(
    numbers: Iterable[int],
) -> list[int]:
    """Return all odd integers.

    Raises:
        TypeError: If an item is not an integer.
    """
```

The implementation should honor the documented behavior consistently.

---

# 69. Common Function Smells

A function may need refactoring when it has:

- many unrelated variables,
- several nested loops,
- many conditional branches,
- a long parameter list,
- repeated validation,
- hidden global dependencies,
- mixed I/O and transformation logic,
- several return types,
- or a name that cannot describe it accurately.

Possible responses:

- extract a helper,
- introduce a data object,
- split pure logic from I/O,
- create a generator,
- use keyword-only arguments,
- or move a responsibility into a class.

---

# 70. Common Class Smells

A class may need redesign when it:

- has many unrelated methods,
- changes for several different reasons,
- repeats logic from other classes,
- manages its own infrastructure and business rules,
- exposes many trivial getters and setters,
- relies heavily on global state,
- has many flags controlling different modes,
- or contains large `if`/`elif` blocks based on type or state.

Possible responses:

- extract a collaborator,
- introduce a repository,
- use composition,
- use a state object,
- split a service from a data model,
- or define a clearer interface.

---

# 71. Practical Function Checklist

Before completing a function, ask:

- Can its purpose be described in one sentence?
- Does it mix I/O with business transformation?
- Are all return paths consistent?
- Is `None` meaningful and documented?
- Should a failure raise an exception?
- Would a generator reduce memory use?
- Are more than two or three positional arguments hard to read?
- Should some arguments be keyword-only?
- Are mutable defaults avoided?
- Is the name specific?
- Can the function be tested without external infrastructure?

---

# 72. Practical Class Checklist

Before completing a class, ask:

- What domain concept does it represent?
- What is its one primary responsibility?
- Do all methods belong to that responsibility?
- Are dependencies injected?
- Is `__init__` lightweight?
- Are public attributes sufficient?
- Is a property justified by validation or computation?
- Should an operation be a module function instead of a static method?
- Is a class method a clearer constructor?
- Is an abstract base class needed?
- Are internal methods named consistently?
- Is name mangling solving a real inheritance problem?
- Is the class easy to instantiate in a test?

---

# 73. Important Corrections to the Chapter’s Code

The chapter’s principles are useful, but several listings contain errors.

## 73.1 “Unique” generator does not enforce uniqueness

Yielding all regex matches can produce duplicates. Track a `seen` set when uniqueness is required.

## 73.2 `from` cannot be a parameter name

Use `from_address`.

## 73.3 `sum` shadows the built-in function

Avoid naming a custom function `sum`.

Use:

```python
def add_numbers(...):
    ...
```

## 73.4 Odd-number type checks are reversed

The source raises when the input *is* a list even though it claims to accept lists.

## 73.5 Logging syntax contains multiple typos

Examples include:

- `Import` instead of `import`,
- `catch` instead of `except`,
- missing `StreamHandler()`,
- misspelled `setFormatter`,
- and misspelled variable names.

## 73.6 Lambda replacement changes the sorting behavior

Sorting with `key=abs` is not equivalent to `reverse=True`.

## 73.7 Property setters cannot raise strings

Use `TypeError` or `ValueError`.

## 73.8 Property example uses inconsistent attributes

The setter refers to both `temp` and `self.temp`, and the getter/setter semantics do not align.

## 73.9 Abstract class subclasses must inherit from the abstract base

```python
class Apple(Fruit):
    ...
```

not:

```python
class Apple:
    ...
```

## 73.10 Alternative constructors should return `cls(...)`

They should not return another class such as `Student`.

## 73.11 Double underscore causes name mangling

It does not prevent name mangling.

## 73.12 Final inheritance example is incomplete

It omits required constructor parameters and calls attributes or methods that do not exist.

These corrections are important when using the chapter as a coding reference.

---

# 74. Review Questions

1. Why is function responsibility more important than line count?
2. What responsibilities are separated in the email-extraction example?
3. How does a generator differ from a list-returning function?
4. When should a function return a set instead of a generator?
5. Why can `None` create an ambiguous API?
6. When is `None` an appropriate return value?
7. What is the difference between invalid input and a valid empty result?
8. Why are keyword arguments useful for long calls?
9. How does `*` create keyword-only parameters?
10. Why are mutable default arguments dangerous?
11. What should logging provide beyond a message saying “error”?
12. How do unit tests act as documentation?
13. Why is `sorted(numbers, key=abs)` clearer than a lambda?
14. How do duplicate responsibilities indicate an oversized class?
15. Why should database access often be extracted from a domain class?
16. What ordering of class members does the chapter recommend?
17. What behavior belongs in `__init__`?
18. When is a property appropriate?
19. Why should property access avoid expensive I/O?
20. When should behavior be a static method rather than a module function?
21. How does `abc.ABC` improve abstract classes?
22. When is duck typing preferable to an abstract base class?
23. How do class methods act as alternative constructors?
24. Why should class methods return `cls(...)`?
25. Why are public attributes usually preferred to trivial getters?
26. What does a single leading underscore communicate?
27. What problem does double-underscore name mangling solve?
28. Why does name mangling not provide security?
29. What signs suggest that a function should be split?
30. What signs suggest that a class should be split?

---

# 75. Concise Exam-Style Summary

Chapter 3 explains how to design cleaner functions and classes in Python. Functions should have one clear responsibility, but their size should be judged by purpose rather than a strict line limit. Complex work can be divided into focused helpers, such as separating file reading from email extraction. Generators are useful when data may be large or unknown because they produce values lazily instead of loading everything into memory.

Functions should have explicit return and failure contracts. Invalid input or failed operations should usually raise meaningful exceptions rather than return ambiguous `None`. Empty collections are often better than `None` when a function’s contract is to return a collection. Default and keyword arguments can improve convenience and readability, while keyword-only arguments prevent confusing positional calls. Mutable default values must be avoided.

Defensive programming includes logging and unit tests. Logging should use appropriate levels, include useful context, and preserve tracebacks for failures. Unit tests document expected behavior, prevent regressions, and provide confidence during refactoring. Lambdas should be limited to trivial local expressions; named functions or existing built-ins are clearer for reusable or complex behavior.

Class size should be determined by responsibility and cohesion. A class should not accumulate unrelated behaviors such as user information, payments, orders, and database access. Repeated infrastructure code can indicate a missing collaborator or repository. Consistent class organization helps readers locate class variables, construction logic, special methods, class methods, static methods, properties, public methods, and internal helpers.

Properties are appropriate for inexpensive computed values and validated attributes. Reading a property should not unexpectedly mutate state or perform expensive I/O. Static methods are appropriate only when behavior is conceptually tied to the class but does not need class or instance state. Class methods support alternative constructors and should use `cls` to preserve subclass behavior.

Abstract base classes from the `abc` module enforce required methods at instantiation time. However, duck typing or protocols may be sufficient when only behavioral compatibility is needed. Python normally favors public attributes instead of trivial getter methods. A single underscore marks an internal implementation detail, while a double leading underscore causes name mangling to reduce accidental subclass collisions. Neither provides true privacy or security.

---

# 76. Key Takeaways

1. **Judge function size by responsibility, not only line count.**
2. **Separate file access, parsing, transformation, and output when they are distinct concerns.**
3. **Use generators for large, streamed, or unknown-size data.**
4. **Do not call a generator “unique” unless duplicates are actually removed.**
5. **Raise meaningful exceptions for invalid input and failed contracts.**
6. **Return empty collections for valid empty collection results.**
7. **Use `None` only when absence is a documented, expected outcome.**
8. **Use keyword arguments to make long calls readable.**
9. **Use keyword-only parameters when argument order would be risky.**
10. **Never use mutable objects as default parameter values unless shared state is intentional.**
11. **Use logging for diagnosable runtime context, not vague messages.**
12. **Use unit tests as documentation and regression protection.**
13. **Keep lambdas trivial and local.**
14. **Prefer existing functions such as `abs` over unnecessary lambdas.**
15. **Define class size by responsibility and cohesion.**
16. **Extract repeated infrastructure behavior into collaborators.**
17. **Keep `__init__` lightweight and focused on valid object state.**
18. **Use properties for inexpensive computation and validation.**
19. **Avoid side effects and network or database work in property getters.**
20. **Use static methods only when the class namespace adds meaning.**
21. **Use abstract base classes when implementations must honor an explicit contract.**
22. **Use duck typing or protocols when structural compatibility is enough.**
23. **Use class methods for named alternative constructors.**
24. **Return `cls(...)` from class methods to support subclasses.**
25. **Prefer public attributes over boilerplate getters and setters.**
26. **Use a single underscore to communicate internal APIs.**
27. **Use double underscores only for realistic subclass-name collision concerns.**
28. **Do not treat name mangling as privacy or security.**
29. **Refactor working code after responsibilities become visible.**
30. **Keep interfaces predictable, explicit, and easy to test.**
