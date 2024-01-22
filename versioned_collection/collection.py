from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Set, Union
from hashlib import sha256

from versioned_collection.item import Item

RELOADER_TYPE = Union[Callable[[], Awaitable[Set[Item]]], None]
ON_CHANGED_TYPE = Union[Callable[[], Awaitable[None]], None]
# WATCHER_TYPE = Callable[["Collection"], Awaitable[None]]


class Collection:
    """
    A collection Items, arranged by key.

    The collection can be reloaded from a source, and can be watched for changes.
    """

    _version: str
    _kv: Dict[str, Item]
    _reloader: RELOADER_TYPE
    _on_changed: ON_CHANGED_TYPE
    # _watcher: WATCHER_TYPE

    def __init__(
        self,
        version,
        items: Set[Item] or None = None,
        on_changed: ON_CHANGED_TYPE = None,
        reloader: RELOADER_TYPE = None,
        # watcher: WATCHER_TYPE = None,
    ):
        """
        Create a new collection.

        :param version: the version of the collection
        :param items: a set of Items
        :param reloader: a function that reloads the items from the source and returns them
        # :param watcher: a function that installs a watch on the source and calls `reload()` when the source changes
        """
        self._version = version
        if items:
            self._kv = {item.key: item for item in items}
        else:
            self._kv = {}
        self._on_changed = on_changed
        self._reloader = reloader
        # self._watcher = watcher

    async def reload(self) -> None:
        """
        Reload the collection from the source.
        """
        if self._reloader:
            items = await self._reloader()
            self._kv = {item.key: item for item in items}
            if self._on_changed:
                await self._on_changed()

    def get(self, key: str) -> Item or None:
        """
        Get an item from the collection.

        :param key: The key of the item
        :return: The item, or None if not found
        """
        return self._kv.get(key)

    def set(
        self,
        key: str,
        value: str,
        content_type: str = "text/plain",
        metadata: Any = None,
    ) -> None:
        """
        Set an item in the collection.

        :param key: The key of the item
        :param value: The value of the item
        """
        self._kv[key] = Item(key, value, content_type, metadata)

    def get_by_hash(self, content_hash: str) -> Item or None:
        """
        Get an item by its content hash. Useful to find items by content.

        :param hash: The hash of the item
        :return: The item, or None if not found
        """
        for item in self._kv.values():
            if item.get_content_hash() == content_hash:
                return item
        return None

    def list_keys(self) -> Set[str]:
        """
        List all keys in the collection.

        :return: A set of keys
        """
        return set(self._kv.keys())

    def get_items(self) -> Set[Item]:
        """
        Get all items in the collection.

        :return: A set of items
        """
        return set(self._kv.values())

    def get_version(self) -> str:
        """
        Get the version of the collection.

        :return: The version of the collection
        """
        return self._version
