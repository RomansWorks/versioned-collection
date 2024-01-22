from dataclasses import dataclass
from hashlib import sha256
from typing import Any


@dataclass
class Item:
    """
    An item in a collection.

    An item has a key, a value, a content type, and optional metadata.
    It also has a content (value) hash, which unless provided is computed from the value using sha256.
    """

    key: str
    value: str
    content_type: str
    metadata: Any = None
    content_hash = None

    def __init__(
        self,
        key: str,
        value: str,
        content_type: str,
        metadata: Any = None,
        content_hash: str = None,
    ):
        """
        Create a new item.

        :param key: The key of the item
        :param value: The value of the item
        :param content_type: The content type of the item
        :param metadata: The metadata of the item
        """
        super().__init__()
        self.key = key
        self.value = value
        self.content_type = content_type
        self.metadata = metadata
        self.content_hash = (
            content_hash or sha256(self.value.encode("utf-8")).hexdigest()
        )

    def get_content_hash(self) -> str:
        """
        Get the content hash of the item.

        :return: The content hash of the item
        """
        return self.content_hash

    def __hash__(self) -> int:
        return self.key.__hash__()
