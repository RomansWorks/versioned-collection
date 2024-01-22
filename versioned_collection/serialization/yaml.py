import yaml
from versioned_collection.collection import Collection, Item


FORMAT_VERSION = "1.0"


def collection_to_yaml(collection: Collection) -> str:
    """
    Convert the collection to a YAML string.

    :return: The json string
    """
    return yaml.safe_dump(
        {
            "format_version": FORMAT_VERSION,
            "version": collection.get_version(),
            "items": [item.__dict__ for item in collection.get_items()],
        }
    )


def collection_from_yaml(yaml_str: str) -> "Collection":
    """
    Create a new collection from a json string.

    :param json_str: The json string to parse
    :return: A new collection
    """

    data = yaml.safe_load(yaml_str)
    if data["format_version"] != FORMAT_VERSION:
        raise ValueError("Unsupported format version")
    version = data["version"]
    kv = {}
    for item in data["items"]:
        kv[item["key"]] = Item(**item)
    return Collection(version, kv)
