import unittest
from reading_list import save_url

class SaveTests(unittest.TestCase):
    def test_duplicate_does_not_append(self):
        urls = ["https://example.org/a"]
        self.assertEqual(save_url(urls, "https://example.org/a"), ["https://example.org/a"])
    def test_new_url_is_saved(self):
        self.assertEqual(save_url([], "https://example.org/b"), ["https://example.org/b"])

if __name__ == "__main__":
    unittest.main()
