import unittest
from hashlib import sha256
from versioned_collection.collection import Item


class ItemTestCase(unittest.TestCase):
    def setUp(self):
        self.item = Item("key", "value", "text/plain", {"author": "John Doe"})

    def test_hash(self):
        expected_hash = sha256(self.item.value.encode("utf-8")).hexdigest()
        self.assertEqual(self.item.get_content_hash(), expected_hash)


if __name__ == "__main__":
    unittest.main()
