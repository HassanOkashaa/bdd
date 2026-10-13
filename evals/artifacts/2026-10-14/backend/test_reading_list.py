import unittest
from reading_list import save_url
class ReadingListTests(unittest.TestCase):
    def test_duplicate_is_not_added(self):
        urls = ["https://example.org/a"]
        self.assertEqual(save_url(urls, "https://example.org/a"), ["https://example.org/a"])
    def test_new_url_is_added(self):
        self.assertEqual(save_url([], "https://example.org/b"), ["https://example.org/b"])
    def test_exact_equality_and_unicode(self):
        urls = ["https://example.org/مقال"]
        self.assertEqual(save_url(urls, "https://example.org/مقال"), ["https://example.org/مقال"])
if __name__ == "__main__": unittest.main()
