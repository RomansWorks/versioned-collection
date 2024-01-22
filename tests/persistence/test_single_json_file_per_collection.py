import unittest
import tempfile
import os
from versioned_collection.persistence.json_file import (
    load,
    store,
)
from versioned_collection.collection import Collection, Item


class TestSingleJsonFilePerCollection(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, "test_collection.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_store_and_load(self):
        # Create a collection, store it, and load it.
        # Assert that the loaded collection is the same as the original.
        # The collection should include keys with values, keys with values and metadata, and keys with values and metadata and content type.

        collection = Collection("1.0")
        collection.set("key1", "value1")
        collection.set(
            "key2",
            "value2",
            metadata={"author": "John Doe", "created_at": "2022-01-01"},
        )
        collection.set(
            "key3",
            "value3",
            metadata={"author": "John Doe", "created_at": "2022-01-01"},
            content_type="text/plain",
        )
        store(self.temp_file, collection)
        loaded_collection = load(self.temp_file)
        self.assertEqual(loaded_collection.get_version(), "1.0")
        self.assertEqual(len(loaded_collection.list_keys()), 3)
        self.assertEqual(loaded_collection.get("key1").value, "value1")
        self.assertEqual(loaded_collection.get("key2").value, "value2")
        self.assertEqual(
            loaded_collection.get("key2").metadata,
            {"author": "John Doe", "created_at": "2022-01-01"},
        )
        self.assertEqual(loaded_collection.get("key3").value, "value3")
        self.assertEqual(
            loaded_collection.get("key3").metadata,
            {"author": "John Doe", "created_at": "2022-01-01"},
        )
        self.assertEqual(loaded_collection.get("key3").content_type, "text/plain")


if __name__ == "__main__":
    unittest.main()
