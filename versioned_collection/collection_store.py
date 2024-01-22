# CollectionStore allows loading and storing collections, abstracting away versioning, file format and any networking.

# CollectionFormat is an enum that defines the supported formats.
#
from enum import Enum
from urllib.parse import parse_qs, urlparse

from versioned_collection.collection import Collection
from versioned_collection.persistence.json_file import load as load_json_file
from versioned_collection.persistence.json_file import store as store_json_file
from versioned_collection.persistence.yaml_file import load as load_yaml_file
from versioned_collection.persistence.yaml_file import store as store_yaml_file
from versioned_collection.serialization.json import collection_from_json
from versioned_collection.serialization.yaml import collection_from_yaml
from versioned_collection.util.download_file import download_file


class CollectionFormat(Enum):
    """
    The collection format.
    """

    SINGLE_JSON_FILE = "single_json_file"
    SINGLE_YAML_FILE = "single_yaml_file"


class CollectionStore:
    """
    A collection store.
    """

    def __init__(self, url: str, required_version: str, format: CollectionFormat):
        """
        Create a new collection store.

        :param url: The url of the stored collection
        :param required_version: The required version of the collection
        :param format: The format of the store
        """
        if format not in CollectionFormat:
            raise ValueError(f"unsupported format: {format}")

        self.required_version = required_version
        self.format = format
        self.url = url

        # Parse url, extract the scheme, host and path, as well as any query parameters
        scheme, netloc, path, params, query, fragment = urlparse(url)
        self.scheme = scheme
        self.username = netloc.split(":")[0]
        self.password = netloc.split(":")[1] if ":" in netloc else None
        self.host = netloc.split("@")[-1] if "@" in netloc else netloc
        self.path = path
        self.query = parse_qs(query)
        self.fragment = fragment

    async def store(self, collection: Collection):
        """
        Store a collection.

        :param collection: The collection
        """
        match self.scheme:
            case "file":
                match self.format:
                    case CollectionFormat.SINGLE_JSON_FILE:
                        store_json_file(self.path, collection)
                    case CollectionFormat.SINGLE_YAML_FILE:
                        store_yaml_file(self.path, collection)
                    case _:
                        raise ValueError(
                            f"unsupported format: {self.format} for file storing"
                        )
            case "https":
                raise NotImplementedError("https store (upload) is not implemented yet")

    async def load(self) -> Collection:
        """
        Load a collection.

        :return: The collection
        """
        match self.scheme:
            case "file":
                match self.format:
                    case CollectionFormat.SINGLE_JSON_FILE:
                        return load_json_file(self.path)
                    case CollectionFormat.SINGLE_YAML_FILE:
                        return load_yaml_file(self.path)
                    case _:
                        raise ValueError(
                            f"unsupported format: {self.format} for file loading"
                        )
            case "https":
                match self.format:
                    case CollectionFormat.SINGLE_JSON_FILE:
                        file_contents = await download_file(self.url)
                        return collection_from_json(file_contents)
                    case CollectionFormat.SINGLE_YAML_FILE:
                        file_contents = await download_file(self.url)
                        return collection_from_yaml(file_contents)
                    case _:
                        raise ValueError(
                            f"unsupported format: {self.format} for https loading"
                        )
