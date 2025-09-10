import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_title_simple(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Title with spaces   "
        result = extract_title(markdown)
        self.assertEqual(result, "Title with spaces")

    def test_extract_title_with_content(self):
        markdown = """# Main Title

This is some content.

## Sub heading

More content here."""
        result = extract_title(markdown)
        self.assertEqual(result, "Main Title")

    def test_extract_title_multiline_before(self):
        markdown = """Some initial content

# The Real Title

More content."""
        result = extract_title(markdown)
        self.assertEqual(result, "The Real Title")

    def test_extract_title_with_leading_whitespace(self):
        markdown = "   # Indented Title   "
        result = extract_title(markdown)
        self.assertEqual(result, "Indented Title")

    def test_extract_title_no_h1_raises_exception(self):
        markdown = """## Sub heading

This has no h1.

### Another sub heading

No main title here."""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_empty_h1_raises_exception(self):
        markdown = "# "
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_only_hashtag_raises_exception(self):
        markdown = "#"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_h2_not_h1(self):
        markdown = """## This is h2

### This is h3

No h1 here."""
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertIn("No h1 header found", str(context.exception))

    def test_extract_title_first_h1_wins(self):
        markdown = """# First Title

Some content

# Second Title

More content"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

    def test_extract_title_real_content(self):
        markdown = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**."""
        result = extract_title(markdown)
        self.assertEqual(result, "Tolkien Fan Club")


if __name__ == "__main__":
    unittest.main()
