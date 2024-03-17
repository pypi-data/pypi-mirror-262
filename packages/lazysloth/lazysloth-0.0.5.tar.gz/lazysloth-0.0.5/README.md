# lazysloth: Lazy and Immutable Variable Library for Python

`lazysloth` is a Python library designed to facilitate the use of lazy initialization patterns and immutable variables in Python applications. It provides two main functionalities through its `LazyVariable` and `ImmutableVariable` classes, allowing developers to defer expensive computations until absolutely necessary and to create variables that cannot be modified after initialization.

## Status

### WIP

Super early. At the time of writing this, this is not production-ready or anything close to that. This is a pet project I started 2 days ago. Hopefully, it will be production-ready in a few weeks.

## Why

Too many things in Python evaluate at the time the code is loaded to memory, from global variables to the default values of function arguments. Sometimes, it's great; sometimes, it creates bugs that might be hard to find the first time or two before it's been burned into your experience. You can work around it with a slight refactor, which often involves wrapping some code in a function, a class, or a dictionary. I found myself writing these too many times in too many different projects, so I decided to write it once.

This time, my need came from wanting control over a singleton global variable holding the config.

I have a `my_config.py` file where I load my configuration, usually from files and environment variables. 

```python
from lazysloth import LazyVariable
from configlib import loader

settings = LazyVariable(loader.load_files, load_files=['settings.yml', 'settings.toml'])
```

```python
from my_config import settings
from my_cli import get_current_run_cli_arguments



settings._kwargs['load_files'].append(
  get_current_run_cli_arguments()['--config-override-file']
)
```





## Installation

```bash
pip install lazysloth
```

Replace `lazysloth` with the correct package name if published on PyPI or provide specific instructions if the library is to be installed directly from a source repository.

## Features

- **LazyVariable:** Enables lazy initialization of variables, where the value is only computed upon the first access.
- **ImmutableVariable:** Wraps values in an immutable container, preventing changes after initialization.

## Quick Start

Here's a quick example to get started with `lazysloth`, demonstrating the lazy loading behavior:

```python
from lazysloth import LazyVariable

def expensive_computation():
    print("Expensive computation is now being executed...")
    return {"data": 42}

# Initialize a LazyVariable with the expensive computation.
lazy_var = LazyVariable(expensive_computation)

print("LazyVariable has been initialized.")
print("Accessing the variable to trigger computation...")

# The expensive computation is executed only upon this access.
print(lazy_var.data)  # Outputs: Expensive computation is now being executed... \n 42

```

## Usage

```python
def expensive_operation():
    print("Performing an expensive operation that takes time...")
    return "Result of the operation"

lazy_operation = LazyVariable(expensive_operation)

print("LazyVariable initialized, but expensive operation hasn't run yet.")
# At this point, the expensive operation has not been executed.

# Accessing the LazyVariable to trigger the expensive operation.
result = lazy_operation()
print(f"Operation result: {result}")
# Now, the expensive operation is executed, and its result is accessed.

```

## Features

- **LazyVariable:** Enables lazy initialization of variables, where the value is only computed upon the first access.
- **ImmutableVariable:** Wraps values in an immutable container, preventing changes after initialization.

### LazyVariable

`LazyVariable` is intended for situations where a variable's initialization is computationally expensive and not always necessary. The variable's value is computed only on the first access.

#### Initialization

```python
lazy_var = LazyVariable(initializer_function, *args, **kwargs)
```

- `initializer_function`: A callable that returns the value to be lazily initialized.
- `*args` and `**kwargs`: Arguments passed to the `initializer_function`.

#### Access

Access attributes or items of the lazily initialized value as if `LazyVariable` were the value itself:

```python
result = lazy_var.attribute
result = lazy_var['item']
```

#### Callable Support

If the lazily initialized value is callable, `LazyVariable` can be called directly:

```python
result = lazy_var(*args, **kwargs)
```

### ImmutableVariable

`ImmutableVariable` ensures that the wrapped value cannot be modified after initialization. It's useful for creating read-only data structures.

- `value`: The value to be made immutable.

#### Access

Access the immutable value's attributes or items directly:

```python
result = immutable_var.attribute
result = immutable_var['item']
```

Attempting to modify the wrapped value results in an `AttributeError`.

## Advanced Usage

- **Resetting a `LazyVariable`:** If your use case requires re-initializing a `LazyVariable`, you can extend its functionality to support resetting.

## Contributing

Contributions to `lazysloth` are welcome! Please refer to the contributing guidelines for more information on how to submit pull requests, report issues, or request features.