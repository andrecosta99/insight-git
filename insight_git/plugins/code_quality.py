import os
import subprocess

from dash import html
from git import Repo


def run_code_quality_analysis(repo_path):
    """
    Runs code quality analysis using Flake8 on a given Git repository. This function checks the repository's
    directory existence, initializes the Git repository object, and then runs the Flake8 command to analyze
    code quality, returning the output of the analysis.

    Args:
        repo_path (str): The file system path to the Git repository to be analyzed.

    Returns:
        str: A string containing the output from the Flake8 analysis. If the repository directory does not exist,
             or the repository is empty, it returns an appropriate error message. If Flake8 does not find any issues,
             it returns 'No issues found by Flake8.'
    """

    try:
        # Ensure the repository exists
        if not os.path.isdir(repo_path):
            raise Exception("Repository directory not found.")

        # Initialize the Git repository object
        repo = Repo(repo_path)
        if repo.bare:
            raise Exception("The Git repository is empty.")

        # Run Flake8 command
        result = subprocess.run(["flake8", repo_path], capture_output=True, text=True)

        # Return Flake8 output
        return result.stdout if result.stdout else "No issues found by Flake8."
    except Exception as e:
        return f"Error: {e}"


def display_code_quality(repo_path):
    """
    Creates and returns a Dash HTML component displaying the results of the Flake8 code quality analysis
    for a specified Git repository. This function is intended to present the code quality report within
    a web interface, providing an easily accessible way for users to review the code quality of their repository.

    Args:
        repo_path (str): The file system path to the Git repository whose code quality is to be analyzed and displayed.

    Returns:
        dash.html.Div: A Dash HTML component containing the results of the Flake8 code quality analysis.
                       If an error occurs during the analysis, the returned component will display the error message.
    """

    quality_report = run_code_quality_analysis(repo_path)
    return html.Div(
        [
            html.H5("Code Quality Analysis (Flake8)"),
            html.Pre(
                quality_report,
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )
