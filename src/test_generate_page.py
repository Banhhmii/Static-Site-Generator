import unittest
from generate_page import extract_title


class TestGenPage(unittest.TestCase):

    def test_extract_title(self):
        md = "# This is a header"
        self.assertEqual(extract_title(md), "This is a header")
    
    def test_extract_title_in_middle(self):
        md = """
This is a paragraph
> quotes
> more quotes
# This is a title
"""
        self.assertEqual(extract_title(md), "This is a title")
        

if __name__ == "__main__":
    unittest.main()