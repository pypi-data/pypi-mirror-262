# Foundation Model Inferencing


### Setting up Pre-commit for this Repository

Pre-commit helps to manage and maintain code quality by running hooks that perform various checks before a commit is made.

To set up pre-commit for this repository, follow these steps:

1. Install pre-commit. If you're using pip, you can do this by running:
    ```
    pip install pre-commit
    ```

2. Navigate to the root directory of the repository where the .pre-commit-config.yaml file is located.

3. Run the following command to install the git hook scripts:
    ```
    pre-commit install
    ```

Now, pre-commit will run automatically on git commit. If you want to manually run all pre-commit hooks on a repository, run:
    ```
    pre-commit run --all-files
    ```

To run a specific pre-commit hook on all files, you can use the run command followed by the ID of the hook. Here's the general syntax:
    ```
    pre-commit run <hook_id> --all-files
    ```

For example, if you want to run the black hook on all files, you would use:
    ```
    pre-commit run black --all-files
    ```

This command will run the black hook on every file in your repository.


### Hooks Used in this Repository

This repository uses a variety of hooks to maintain code quality:

- check-added-large-files: Prevents committing large files.
- end-of-file-fixer: Ensures files end with a newline.
- trailing-whitespace: Removes trailing whitespace.
- check-ast: Checks Python AST for syntax errors.
- check-docstring-first: Ensures the first thing in a Python file is a docstring.
- isort: Sorts Python imports.
- add-trailing-comma: Adds trailing commas to Python data structures.
- black: Formats Python code to conform to the PEP 8 style guide.
- flake8: Lints Python code for errors and code style violations.
- pydocstyle: Checks Python docstring conventions.

These hooks are run automatically before each commit once pre-commit is installed.
