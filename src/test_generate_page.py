import unittest
import tempfile
import os
import shutil
from generate_page import generate_page


class TestGeneratePage(unittest.TestCase):

    def setUp(self):
        """Set up temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_generate_page_basic(self):
        """Test basic page generation."""
        # Create test markdown file
        markdown_content = """# Test Title

This is **bold** text and this is _italic_ text.

## Subtitle

- Item 1
- Item 2"""

        markdown_path = os.path.join(self.temp_dir, "test.md")
        with open(markdown_path, "w") as f:
            f.write(markdown_content)

        # Create test template
        template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ Title }}</title>
</head>
<body>
    <main>{{ Content }}</main>
</body>
</html>"""

        template_path = os.path.join(self.temp_dir, "template.html")
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate page
        output_path = os.path.join(self.temp_dir, "output.html")
        generate_page(markdown_path, template_path, output_path)

        # Read generated file
        with open(output_path, "r") as f:
            result = f.read()

        # Verify content
        self.assertIn("<title>Test Title</title>", result)
        self.assertIn("<h1>Test Title</h1>", result)
        self.assertIn("<b>bold</b>", result)
        self.assertIn("<i>italic</i>", result)
        self.assertIn("<h2>Subtitle</h2>", result)
        self.assertIn("<ul>", result)
        self.assertIn("<li>Item 1</li>", result)

    def test_generate_page_creates_directories(self):
        """Test that generate_page creates necessary directories."""
        # Create test files
        markdown_content = "# Test"
        template_content = "<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>"

        markdown_path = os.path.join(self.temp_dir, "test.md")
        template_path = os.path.join(self.temp_dir, "template.html")

        with open(markdown_path, "w") as f:
            f.write(markdown_content)
        with open(template_path, "w") as f:
            f.write(template_content)

        # Generate page in nested directory that doesn't exist
        nested_dir = os.path.join(self.temp_dir, "nested", "deep")
        output_path = os.path.join(nested_dir, "output.html")

        generate_page(markdown_path, template_path, output_path)

        # Verify file was created
        self.assertTrue(os.path.exists(output_path))

        # Verify content
        with open(output_path, "r") as f:
            result = f.read()
        self.assertIn("<title>Test</title>", result)
        self.assertIn("<h1>Test</h1>", result)

    def test_generate_page_real_content(self):
        """Test with real Tolkien content."""
        markdown_content = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""

        template_content = """<!DOCTYPE html>
<html>
  <head>
    <title>{{ Title }}</title>
    <link href="/index.css" rel="stylesheet" />
  </head>
  <body>
    <article>{{ Content }}</article>
  </body>
</html>"""

        markdown_path = os.path.join(self.temp_dir, "index.md")
        template_path = os.path.join(self.temp_dir, "template.html")
        output_path = os.path.join(self.temp_dir, "index.html")

        with open(markdown_path, "w") as f:
            f.write(markdown_content)
        with open(template_path, "w") as f:
            f.write(template_content)

        generate_page(markdown_path, template_path, output_path)

        with open(output_path, "r") as f:
            result = f.read()

        # Verify expected content
        self.assertIn("<title>Tolkien Fan Club</title>", result)
        self.assertIn("<h1>Tolkien Fan Club</h1>", result)
        self.assertIn(
            '<img src="/images/tolkien.png" alt="JRR Tolkien sitting">', result
        )
        self.assertIn("<b>I like Tolkien</b>", result)
        self.assertIn("<blockquote>", result)
        self.assertIn('"I am in fact a Hobbit in all but size."', result)


if __name__ == "__main__":
    unittest.main()
