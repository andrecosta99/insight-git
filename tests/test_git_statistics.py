import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from insight_git.plugins.git_statistics import display_git_statistics, extract_git_stats


@pytest.fixture()
def git_repo_mock():
    """
    Mock the Git repository for testing statistics extraction.

    Yields:
        MagicMock object: A mock of the Repo object with predefined commits and stats, including branch information.
    """
    with patch("insight_git.plugins.git_statistics.Repo") as mock_repo:
        mock_commit = MagicMock()
        mock_commit.committed_datetime = datetime.now() - timedelta(days=1)
        mock_commit.stats.total = {"insertions": 10, "deletions": 5}
        mock_commit.author.email = "author@example.com"
        mock_commit.message = "Initial commit"

        mock_commit_2 = MagicMock()
        mock_commit_2.committed_datetime = datetime.now() - timedelta(days=2)
        mock_commit_2.stats.total = {"insertions": 20, "deletions": 10}
        mock_commit_2.author.email = "author2@example.com"
        mock_commit_2.message = "Added new features"

        mock_branch = MagicMock()
        mock_branch.name = "main"
        mock_branch.commit = mock_commit

        mock_branch_2 = MagicMock()
        mock_branch_2.name = "dev"
        mock_branch_2.commit = mock_commit_2

        mock_repo.return_value.iter_commits.return_value = [mock_commit, mock_commit_2]
        mock_repo.return_value.branches = [mock_branch, mock_branch_2]
        yield mock_repo


def test_extract_git_stats_success(git_repo_mock):
    """
    Test successful git statistics extraction including branch details.
    """
    repo_path = "dummy/path/to/repo"
    stats = extract_git_stats(repo_path)
    assert stats["total_commits"] == 2
    assert len(stats["commit_dates"]) == 2
    assert stats["average_lines_per_commit"] == 22.5
    assert stats["total_branches"] == 2
    assert stats["branch_details"][0]["name"] == "main"
    assert "Initial commit" in stats["branch_details"][0]["last_commit_message"]


def test_extract_git_stats_failure(git_repo_mock):
    """
    Test the behavior of the statistics extraction function when an error occurs.
    """
    git_repo_mock.side_effect = Exception("An error occurred")
    repo_path = "dummy/path/to/repo"
    stats = extract_git_stats(repo_path)
    assert "error" in stats
    assert stats["error"] == "An error occurred"


def test_display_git_statistics_success(git_repo_mock):
    """
    Test the successful display of git statistics in a Dash component, including branch details.
    """
    repo_path = "dummy/path/to/repo"
    component = display_git_statistics(repo_path)
    assert "Total Commits: 2" in str(component)
    assert "Average Lines per Commit: 22.50" in str(component)
    assert "Total Branches: 2" in str(component)
    assert "main: Last commit" in str(component)


def test_display_git_statistics_failure(git_repo_mock):
    """
    Test the display function when an error occurs during statistics extraction.
    """
    git_repo_mock.side_effect = Exception("Display error")
    repo_path = "dummy/path/to/repo"
    component = display_git_statistics(repo_path)
    assert "Error: Display error" in str(component)
