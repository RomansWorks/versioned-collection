from versioned_collection.collection import Collection
from versioned_collection.serialization.yaml import (
    collection_from_yaml,
    collection_to_yaml,
)

"""
This module provides a simple way to store a collection in a single yaml file.
"""


def store(file_path: str, collection: Collection):
    """
    Store a collection to a file.

    :param file_path: The file path
    :param collection: The collection
    """
    # Open the file
    with open(file_path, "w") as f:
        # Write the collection
        f.write(collection_to_yaml())


def load(file_path: str) -> Collection:
    """
    Load a collection from a file.

    :param file_path: The file path
    :return: The collection
    """
    # Open the file
    with open(file_path, "r") as f:
        # Read the file
        content = f.read()
    # Return the collection
    return collection_from_yaml(content)
