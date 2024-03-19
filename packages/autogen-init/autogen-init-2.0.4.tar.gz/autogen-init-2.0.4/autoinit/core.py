import os
import ast
from typing import List

def find_defs(path: str) -> List[str]:
    """
    Finds function and class definitions in a Python file.

    Args:
        path (str): Path to the Python file to analyze.

    Returns:
        List[str]: A list of names of defined functions and classes.
    """
    with open(path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), path)
    return [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]

def run(start_path: str, overwrite: bool = True, version: str = None, author: str = None) -> None:
    """
    Updates all __init__.py files in a package, making submodules easily accessible from the top-level module,
    and optionally adding version and author information to the top-level __init__.py.

    This function walks through the package directory, updating __init__.py files to include import statements
    for all modules and submodules, facilitating the use of package contents.

    Args:
        start_path (str): Root directory of the package.
        overwrite (bool): Whether to overwrite existing __init__.py files.
        version (str, optional): Package version to add.
        author (str, optional): Package author(s) to add.

    Example:
        # Quick start
        run(
            start_path='C:/path/to/my_package',,
            overwrite=True,
            version="0.0.0",
            author="Minwoo(Daniel) Park <parkminwoo1991@gmail.com>"
        )
    """
    package_name = os.path.basename(os.path.normpath(start_path))
    all_imports = []

    for root, _, files in os.walk(start_path):
        init_content = []
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                defs = find_defs(os.path.join(root, file))
                if defs:
                    module_name = os.path.splitext(file)[0]
                    rel_path = os.path.relpath(root, start_path).replace(os.sep, ".")
                    if root == start_path:  # For top-level folder
                        import_statement = f"from .{module_name} import {', '.join(defs)}"
                        all_imports.append(import_statement)
                    else:  # For submodules
                        import_statement = f"from {package_name}.{rel_path}.{module_name} import {', '.join(defs)}"
                        all_imports.append(f"from .{rel_path}.{module_name} import {', '.join(defs)}")
                    init_content.append(import_statement)

        if init_content:
            init_path = os.path.join(root, "__init__.py")
            with open(init_path, "w" if overwrite else "a", encoding="utf-8") as init_file:
                init_file.write("\n".join(init_content) + "\n")
            print(f"Updated: {init_path}")

    # Update the top-level __init__.py with imports from all submodules
    if overwrite:
        with open(os.path.join(start_path, "__init__.py"), "w", encoding="utf-8") as f:
            f.write("\n".join(all_imports) + "\n")

    # Add version and author information to the top-level __init__.py
    if version or author:
        with open(os.path.join(start_path, "__init__.py"), "a", encoding="utf-8") as f:
            if version:
                f.write(f'\n__version__ = "{version}"\n')
            if author:
                f.write(f'\n__author__ = "{author}"\n')
        print("Added version and author information to the top-level __init__.py")
