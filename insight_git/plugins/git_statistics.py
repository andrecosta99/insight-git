import logging

from dash import html
from git import Repo


def extract_git_stats(repo_path):
    """
    Extracts comprehensive Git statistics from a repository's commit history including branch details.

    This function collects data on the number of commits, commit dates, total lines added and deleted across all commits,
    and computes the average lines changed per commit. It also provides dates for the first and last commit and detailed
    information on each branch.

    Args:
        repo_path (str): The file system path to the local Git repository.

    Returns:
        dict: A dictionary containing statistics about the repository including the total number of commits,
              a list of commit dates, the first and last commit date, total and average lines changed per commit,
              total branches, and details of each branch.
              If an error occurs, returns a dictionary with an 'error' key containing the error message.
    """
    try:
        repo = Repo(repo_path)
        commits = list(repo.iter_commits())

        # Collect commit dates
        commit_dates = [commit.committed_datetime for commit in commits]
        total_lines_added = sum(commit.stats.total["insertions"] for commit in commits)
        total_lines_deleted = sum(commit.stats.total["deletions"] for commit in commits)
        total_lines_changed = total_lines_added + total_lines_deleted
        average_lines_per_commit = (
            (total_lines_changed / len(commits)) if commits else 0
        )

        # Dates for the first and last commit
        first_commit_date = commit_dates[-1] if commits else None
        last_commit_date = commit_dates[0] if commits else None

        # Branch details
        branches = repo.branches
        branch_details = [
            {
                "name": branch.name,
                "last_commit": branch.commit.hexsha,
                "last_commit_message": branch.commit.message.strip(),
            }
            for branch in branches
        ]

        return {
            "total_commits": len(commits),
            "commit_dates": commit_dates,
            "first_commit_date": first_commit_date,
            "last_commit_date": last_commit_date,
            "total_lines_added": total_lines_added,
            "total_lines_deleted": total_lines_deleted,
            "total_lines_changed": total_lines_changed,
            "average_lines_per_commit": average_lines_per_commit,
            "total_branches": len(branches),
            "branch_details": branch_details,
        }

    except Exception as e:
        logging.error(f"Error extracting git statistics: {e}")
        return {"error": str(e)}


def display_git_statistics(repo_path):
    """
    Creates a Dash HTML component displaying general Git statistics for a repository including branch information.

    This function uses the `extract_git_stats` function to gather statistics about a repository's commit history and branches,
    then constructs a Dash HTML component to visually present these statistics.

    Args:
        repo_path (str): The file system path to the local Git repository.

    Returns:
        dash.html.Div: A Dash HTML component containing the visual representation of the repository's general statistics.
                       If an error occurs during statistics extraction, the component will display the error message.
    """
    stats = extract_git_stats(repo_path)
    if "error" in stats:
        return html.Div(f"Error: {stats['error']}")

    branch_list = html.Ul(
        [
            html.Li(
                f"{branch['name']}: Last commit {branch['last_commit']} ({branch['last_commit_message']!r})"
            )
            for branch in stats["branch_details"]
        ]
    )

    return html.Div(
        [
            html.H5("General Statistics"),
            html.Ul(
                [
                    html.Li(f"Total Commits: {stats['total_commits']}"),
                    html.Li(f"First Commit Date: {stats['first_commit_date']}"),
                    html.Li(f"Last Commit Date: {stats['last_commit_date']}"),
                    html.Li(f"Total Lines Added: {stats['total_lines_added']}"),
                    html.Li(f"Total Lines Deleted: {stats['total_lines_deleted']}"),
                    html.Li(f"Total Lines Changed: {stats['total_lines_changed']}"),
                    html.Li(
                        f"Average Lines per Commit: {stats['average_lines_per_commit']:.2f}"
                    ),
                    html.Li(f"Total Branches: {stats['total_branches']}"),
                ]
            ),
            html.H6("Branch Details"),
            branch_list,
        ],
        className="mt-4",
    )
