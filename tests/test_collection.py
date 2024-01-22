from versioned_collection.collection import Collection, Item
import unittest


class TestCollection(unittest.TestCase):
    def setUp(self):
        self.collection = Collection("1.0")

    def test_set_and_get(self):
        self.collection.set("key1", "value1")
        item = self.collection.get("key1")
        self.assertEqual(item.key, "key1")
        self.assertEqual(item.value, "value1")

    def test_get_nonexistent_key(self):
        item = self.collection.get("nonexistent_key")
        self.assertIsNone(item)

    def test_set_with_metadata(self):
        metadata = {"author": "John Doe", "created_at": "2022-01-01"}
        self.collection.set("key2", "value2", metadata=metadata)
        item = self.collection.get("key2")
        self.assertEqual(item.metadata, metadata)

    def test_get_by_hash(self):
        self.collection.set("key3", "value3")
        item = self.collection.get("key3")
        item_by_hash = self.collection.get_by_hash(item.content_hash)
        self.assertEqual(item_by_hash, item)

    def test_list_keys(self):
        self.collection.set("key4", "value4")
        self.collection.set("key5", "value5")
        keys = self.collection.list_keys()
        self.assertEqual(len(keys), 2)
        self.assertIn("key4", keys)
        self.assertIn("key5", keys)

    def test_list_items(self):
        self.collection.set("key6", "value6")
        self.collection.set("key7", "value7")
        items = self.collection.get_items()
        self.assertEqual(len(items), 2)
        self.assertIsInstance(items, set)
        self.assertTrue(all(isinstance(item, Item) for item in items))

    def test_get_version(self):
        version = self.collection.get_version()
        self.assertEqual(version, "1.0")


if __name__ == "__main__":
    unittest.main()
