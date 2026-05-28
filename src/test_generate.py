import unittest

from generate import extract_title


class TestGenerate(unittest.TestCase):
    def test_extract_title(self):
        md = """
# this is the **title**

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        title = extract_title(md)
        self.assertEqual(title, "this is the **title**")

    def test_extract_no_title(self):
        md = """
## this is not the **title**

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
