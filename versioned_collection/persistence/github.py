import os
import tempfile
import shutil
import requests

from versioned_collection.collection import Collection, Item
from versioned_collection.persistence.json_file import (
    load as load_json,
    store as store_json,
)

"""
This module provides a simple way to load a collection from github.
Note that git credentials need to be configured externally in advance.
"""


def load(git_repo_url: str, path_in_repo: str, commit_or_tag: str) -> Collection:
    """
    Load a collection from a git repository.

    :param git_repo_url: The git repository url
    :param path_in_repo: The path in the repository
    :param commit_or_tag: The commit or tag
    """

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Clone the repository
    repo = github.Repo.clone_from(git_repo_url, temp_dir)

    # Get the file path
    file_path = os.path.join(temp_dir, path_in_repo)

    # Check out the commit or tag
    repo.git.checkout(commit_or_tag)

    # Load the collection
    collection = load_json(file_path)

    # Delete the temporary directory
    shutil.rmtree(temp_dir)

    # Return the collection
    return collection


def load_file_from_github(
    github_repo_url: str, path_in_repo: str, branch: str = "master"
) -> str:
    """
    Load a file from a GitHub repository.

    :param github_repo_url: The GitHub repository url
    :param path_in_repo: The path in the repository
    :param branch: The branch to fetch from
    :return: The content of the file
    """
    # Parse the repository name from the url
    repo_name = github_repo_url.split("github.com/")[-1]

    # Construct the url to the raw file
    file_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/{path_in_repo}"

    # Send a GET request to the url
    response = requests.get(file_url)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Return the content of the file
    return response.text
