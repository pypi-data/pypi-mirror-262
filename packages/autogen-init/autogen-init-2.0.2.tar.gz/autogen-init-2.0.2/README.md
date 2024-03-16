# Autogen Init: Streamline Your Package Setup

Autogen-Init is a Python tool designed to make `__init__.py` file updates seamless across your package, ensuring imports are clean and easy to access. It scans your package's directories to automatically update `__init__.py` files with all necessary class and function imports. Plus, it simplifies adding version and author details to your top-level `__init__.py`, boosting package metadata.

## Features

- **Auto Updates**: Instantly refreshes `__init__.py` files with internal imports.
- **Metadata Enhancements**: Adds version and author info effortlessly.
- **Flexible Overwrites**: Choose to update or append `__init__.py` files as needed.

## 📦 Installation

Get Autogen-Init with pip for a smooth integration:

```
pip install autogen-init
```

## Usage

Activate Autogen-Init with the `run` command, setting your package's root as the start path. Opt to overwrite `__init__.py` files and add version and author data.

```python
from autogen_init import run

# Quick start
run(
    start_path='C:/path/to/my_package',
    overwrite=True,
    version="1.0.0",
    author="Minwoo(Daniel) Park <parkminwoo1991@gmail.com>"
)
```

### Arguments

- `start_path (str)`: Your package's root directory.
- `overwrite (bool)`: Flag to overwrite `__init__.py` files, default is `True`.
- `version (str)`: Package version for the top-level `__init__.py`.
- `author (str)`: Package author(s) for the top-level `__init__.py`.

## Contributing

Your contributions are welcome! For bug reports, feature suggestions, or submissions, don't hesitate to get in touch or open a pull request.

## ©️ License

Autogen-Init is MIT licensed — see the LICENSE file for details.
