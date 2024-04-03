# Available Plugins Functions and Documentation

Insight Git provides a set of functionalities to analyze Git repositories, offering insights through statistics and visualizations. This document details the available functions and their usage.

## extract_contributors

Extracts contributor data from a repository, showing the number of commits made by each contributor.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- `Counter`: A counter object where keys are author names and values are the number of commits made by each author.

### Usage

from insight-git.plugins.contributors import extract_contributors
contributors = extract_contributors("/path/to/repo")

## display_contributors

Displays contributor data in a Dash component.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- Dash component containing the list of contributors and their commit counts.

### Usage

from insight_git.plugins.contributors import display_contributors
component = display_contributors("/path/to/repo")

## extract_git_stats

Extracts various statistics from a local Git repository, such as total commits, commit dates, and average lines changed per commit.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- `Dictionary`: A dictionary containing various statistics about the repository.

### Usage

from insight_git.plugins.git_statistics import extract_git_stats
stats = extract_git_stats("/path/to/repo")

## display_git_statistics

Displays Git statistics in a Dash component.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- Dash component containing the Git statistics visualization.

### Usage

from insight_git.plugins.git_statistics import display_git_statistics
component = display_git_statistics("/path/to/repo")

## extract_commit_types

Extracts and categorizes commit types based on commit messages from a local Git repository.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- `Counter`: A Counter object mapping commit types (e.g., Bug Fix, Feature) to their frequencies.

### Usage

from insight_git.plugins.commit_type import extract_commit_types
commit_types = extract_commit_types("/path/to/repo")

## display_commit_type

Creates a Dash HTML component to display the distribution of commit types in a repository.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- Dash HTML component containing the list of commit types and their counts.

### Usage

from insight_git.plugins.commit_type import display_commit_type
component = display_commit_type("/path/to/repo")

## display_commit_graph

Generates and displays a graph of commits over time.

### Parameters

- `repo_path`: String. The path to the local Git repository.

### Returns

- Dash component containing the commit graph.

### Usage

from insight_git.plugins.commit_graph import display_commit_graph
component = display_commit_graph("/path/to/repo")
