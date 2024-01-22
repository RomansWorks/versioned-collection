import json
from versioned_collection.collection import Collection, Item


FORMAT_VERSION = "1.0"


def collection_to_json(collection: Collection) -> str:
    """
    Convert the collection to a json string.

    :return: The json string
    """
    return json.dumps(
        {
            "format_version": FORMAT_VERSION,
            "version": collection.get_version(),
            "items": [item.__dict__ for item in collection.get_items()],
        }
    )


def collection_from_json(json_str: str) -> "Collection":
    """
    Create a new collection from a json string.

    :param json_str: The json string to parse
    :return: A new collection
    """

    data = json.loads(json_str)
    if data["format_version"] != FORMAT_VERSION:
        raise ValueError("Unsupported format version")
    version = data["version"]
    items = [Item(**item) for item in data["items"]]
    return Collection(version, items)
