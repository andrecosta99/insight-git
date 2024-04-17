from collections import Counter
from unittest.mock import MagicMock, patch

import pytest
from dash import html
from dash.exceptions import PreventUpdate
from git import Repo

from insight_git.plugins.contributors_info import (
    display_contributors_info,
    display_updated_contributors,
    extract_contributors,
    update_contributors_data,
)


class MockCommit:
    """Mock object for simulating git commits in tests."""

    def __init__(self, name):
        """Initialize with a fake author name."""
        self.author = MagicMock()
        self.author.name = name


@pytest.fixture
def mock_repo():
    """Fixture to mock Repo object from GitPython."""
    with patch("insight_git.plugins.contributors_info.Repo") as mock:
        yield mock


def test_extract_contributors_with_valid_data(mock_repo):
    """
    Test extracting contributors with valid data to ensure correct counts.
    """
    mock_repo.return_value.iter_commits.return_value = [
        MockCommit("Alice"),
        MockCommit("Bob"),
        MockCommit("Alice"),
    ]
    expected_result = Counter({"Alice": 2, "Bob": 1})
    assert extract_contributors("dummy_repo_path") == expected_result


def test_extract_contributors_with_exception(mock_repo):
    """
    Test extracting contributors when an exception occurs to handle errors gracefully.
    """
    mock_repo.side_effect = Exception("Error accessing repository")
    assert extract_contributors("dummy_repo_path") == {
        "error": "Error accessing repository"
    }


def test_display_contributors_with_valid_data(mock_repo):
    """
    Test the display of contributor data in the UI with valid input.
    """
    mock_repo.return_value.iter_commits.return_value = [
        MockCommit("Alice"),
        MockCommit("Bob"),
        MockCommit("Alice"),
    ]
    result = display_contributors_info("dummy_repo_path")
    assert isinstance(result, html.Div)
    assert "Alice: 2" in str(result)
    assert "Bob: 1" in str(result)


def test_display_contributors_with_error(mock_repo):
    """
    Test the display of an error message when contributor data extraction fails.
    """
    mock_repo.side_effect = Exception("Error accessing repository")
    result = display_contributors_info("dummy_repo_path")
    assert "Error: Error accessing repository" in str(result)


def test_update_contributors_data_no_input():
    """
    Test the update function without input to ensure it prevents updates.
    """
    with pytest.raises(PreventUpdate):
        update_contributors_data(1, {}, None, None, None)


def test_update_contributors_data_successful_change():
    """
    Test successful update of contributor names in the data store.
    """
    initial_data = {"Alice": 1, "Bob": 2}
    updated_data = update_contributors_data(1, initial_data, None, "Alice", "Alicia")
    assert updated_data == {"Alicia": 1, "Bob": 2}


def test_display_updated_contributors_no_data():
    """
    Test handling no data case for the display of updated contributors.
    """
    with pytest.raises(PreventUpdate):
        display_updated_contributors(None)


def test_display_updated_contributors_valid_data():
    """
    Test the display of updated contributors with valid data.
    """
    updated_data = {"Alice": 1, "Bob": 2}
    result = display_updated_contributors(updated_data)
    assert len(result) == 2
    assert "Alice: 1" in str(result)
    assert "Bob: 2" in str(result)
