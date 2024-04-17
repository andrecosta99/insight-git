# For Developers

Welcome to the developer documentation for Insight Git. This section provides detailed instructions on setting up your development environment, running tests, and creating plugins.

## Setting Up for Development

### Clone the Repository:

Clone the Insight Git repository using the following command:

```bash
git clone https://github.com/andrecosta99/insight-git
```

### Create and Activate a Virtual Environment:

Navigate to the project directory:

```bash
cd insight-git
```

Create a virtual environment:

```bash
python -m venv env
```

Activate the virtual environment:

On Windows:

```bash
env\Scripts\activate
```

On Unix or MacOS:

```bash
source env/bin/activate
```

### Install Development Dependencies:

Install the project and its dependencies in editable mode:

```shell
pip install -e ".[dev]"
```

## Running Tests

To ensure the functionality of your code, run the included tests:

Execute the tests using:

```shell
pytest
```

For a coverage report, use:

```shell
pytest --cov=insight_git --cov-report=html
```

This generates a coverage report in the `htmlcov` directory.

## Creating Plugins

To create a new plugin for Insight Git, follow these steps:

### Plugin Development:

1. Create a new Python file in the `insight_git/plugins` directory. For example, `new_feature.py`.
2. Implement your plugin functionality. Typically, this involves writing a function that processes data from a Git repository and returns a Dash component that visualizes this data.

### Register the Plugin:

Open the `pyproject.toml` file.

Add your plugin under `[project.entry-points."insight_git.plugins"]` to make it discoverable by the application. Format it as follows:

```toml
new_feature = "insight_git.plugins.new_feature:display_function"
```

Replace `display_function` with the function in your plugin file that returns the Dash component.

### Using the Plugin:

Once registered, your plugin will be available within the Insight Git application. Users can select your plugin from the interface to view its output based on the provided repository data.

## Contributing Guidelines

If you wish to contribute enhancements or fixes:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit changes to your branch.
4. Push the branch to your fork and open a pull request.

## Additional Information

- **Documentation Changes**: If you modify or enhance documentation, ensure compatibility with MkDocs.
- **License**: Insight Git is licensed under the MIT License. See the LICENSE file for more details.

Thank you for contributing to Insight Git! Your contributions help improve the tool and enrich the community.
