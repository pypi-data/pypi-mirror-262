import os
import ast
from typing import List


def find_defs(path: str) -> List[str]:
    """
    Finds function and class definitions in a file.

    Args:
    path (str): Path to the Python file to analyze.

    Returns:
    List[str]: A list of names of defined functions and classes.

    Example:
    >>> find_defs('my_module.py')
    ['MyClass', 'my_function']
    """
    with open(path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), path)
    return [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]


def run(
    start_path: str, overwrite: bool = True, version: str = None, author: str = None
) -> None:
    """
    Updates all __init__.py files in a package, adding version and author info to the top-level __init__.py.

    Args:
    start_path (str): Root directory of the package.
    overwrite (bool): Whether to overwrite existing __init__.py files.
    version (str): Package version to add.
    author (str): Package author(s) to add.

    Example:
    >>> run(
    ...     'C:/path/to/my_package',
    ...     overwrite=True,
    ...     version="1.0.0",
    ...     author="Minwoo(Daniel) Park <parkminwoo1991@gmail.com>"
    ... )
    Updated: C:/path/to/my_package/submodule/__init__.py
    Added version and author information.
    """
    top_level_init_content = []
    for root, _, files in os.walk(start_path):
        init_content = []
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                defs = find_defs(os.path.join(root, file))
                if defs:
                    rel_path = os.path.relpath(root, start_path).replace(os.sep, ".")
                    module_name = os.path.splitext(file)[0]
                    full_module_path = (
                        f"{rel_path}.{module_name}" if rel_path != "." else module_name
                    )
                    init_content.append(
                        f"from .{full_module_path} import {', '.join(defs)}"
                    )
                    if root == start_path:  # For top-level folder
                        top_level_init_content.append(
                            f"from .{module_name} import {', '.join(defs)}"
                        )

        if init_content:
            init_path = os.path.join(root, "__init__.py")
            if overwrite or not os.path.exists(init_path):
                with open(init_path, "w", encoding="utf-8") as init_file:
                    init_file.write("\n".join(init_content))
                    print(f"Updated: {init_path}")

    if version or author:
        with open(
            os.path.join(start_path, "__init__.py"),
            "a" if overwrite else "w",
            encoding="utf-8",
        ) as init_file:
            if version:
                init_file.write(f'\n__version__ = "{version}"')
            if author:
                init_file.write(f'\n__author__ = "{author}"')
            print("Added version and author information.")
