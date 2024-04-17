from unittest.mock import MagicMock, patch

import pytest
from dash import html

from insight_git.plugins.branch_information import (
    display_branch_information,
    extract_branches_info,
)


@pytest.fixture
def git_repo_mock():
    with patch("insight_git.plugins.branch_information.Repo") as mock_repo:
        mock_main_branch = MagicMock()
        mock_develop_branch = MagicMock()

        # Assigning names directly to mock objects for branches
        mock_main_branch.name = "main"
        mock_develop_branch.name = "develop"

        # Mock the iter_commits to return a list of mocks representing commits
        mock_repo.return_value.branches = [mock_main_branch, mock_develop_branch]
        mock_repo.return_value.iter_commits.side_effect = lambda branch: (
            [MagicMock() for _ in range(10)]
            if branch.name == "main"
            else [MagicMock() for _ in range(5)]
        )

        yield mock_repo


def test_extract_branches_info_success(git_repo_mock):
    """Test successful extraction of branch information."""
    repo_path = "dummy/path/to/repo"
    branches_info = extract_branches_info(repo_path)
    expected_output = {"main": 10, "develop": 5}
    assert (
        branches_info == expected_output
    ), "Branch information extraction did not match expected output."


def test_display_branch_information_success(git_repo_mock):
    """Test correct display of branch information in the interface."""
    repo_path = "dummy/path/to/repo"
    result = display_branch_information(repo_path)
    assert "main: 10 commits" in str(
        result
    ), "Information for 'main' branch is incorrectly displayed."
    assert "develop: 5 commits" in str(
        result
    ), "Information for 'develop' branch is incorrectly displayed."


def test_display_branch_information_failure(git_repo_mock):
    """Test display of error message when branch information extraction fails."""
    with patch(
        "insight_git.plugins.branch_information.extract_branches_info",
        return_value={"error": "Error accessing repository"},
    ):
        repo_path = "dummy/path/to/repo"
        result = display_branch_information(repo_path)
        assert "Error: Error accessing repository" in str(
            result
        ), "Error message is not displayed correctly."
