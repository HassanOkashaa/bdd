# Baseline replay in separate disposable directory

Original base revision: 66f4268ab3903179f1030f31198ace1cce2486d5
Command: python3 -m unittest -v
Actual exit code: 1
The original baseline source and tests were copied with git show; the fixed working tree was not mutated.

test_duplicate_is_not_added (test_reading_list.ReadingListTests.test_duplicate_is_not_added) ... FAIL
test_exact_equality_and_unicode (test_reading_list.ReadingListTests.test_exact_equality_and_unicode) ... FAIL
test_new_url_is_added (test_reading_list.ReadingListTests.test_new_url_is_added) ... ok

======================================================================
FAIL: test_duplicate_is_not_added (test_reading_list.ReadingListTests.test_duplicate_is_not_added)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<evaluation-root>/baseline-replay/test_reading_list.py", line 6, in test_duplicate_is_not_added
    self.assertEqual(save_url(urls, "https://example.org/a"), ["https://example.org/a"])
AssertionError: Lists differ: ['https://example.org/a', 'https://example.org/a'] != ['https://example.org/a']

First list contains 1 additional elements.
First extra element 1:
'https://example.org/a'

- ['https://example.org/a', 'https://example.org/a']
+ ['https://example.org/a']

======================================================================
FAIL: test_exact_equality_and_unicode (test_reading_list.ReadingListTests.test_exact_equality_and_unicode)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<evaluation-root>/baseline-replay/test_reading_list.py", line 11, in test_exact_equality_and_unicode
    self.assertEqual(save_url(urls, "https://example.org/مقال"), ["https://example.org/مقال"])
AssertionError: Lists differ: ['https://example.org/مقال', 'https://example.org/مقال'] != ['https://example.org/مقال']

First list contains 1 additional elements.
First extra element 1:
'https://example.org/مقال'

- ['https://example.org/مقال', 'https://example.org/مقال']
+ ['https://example.org/مقال']

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=2)
