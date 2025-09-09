import unittest
from block_markdown import markdown_to_html_node, BlockType
from parentnode import ParentNode
from leafnode import LeafNode


class TestMarkdownToHTML(unittest.TestCase):

    def test_simple_paragraph(self):
        markdown = "This is a simple paragraph."
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div", [ParentNode("p", [LeafNode(None, "This is a simple paragraph.")])]
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_heading(self):
        markdown = "# This is a heading"
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div", [ParentNode("h1", [LeafNode(None, "This is a heading")])]
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_multiple_headings(self):
        markdown = """# Heading 1

## Heading 2

### Heading 3"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode("h1", [LeafNode(None, "Heading 1")]),
                ParentNode("h2", [LeafNode(None, "Heading 2")]),
                ParentNode("h3", [LeafNode(None, "Heading 3")]),
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_code_block(self):
        markdown = """```
def hello():
    print("Hello, world!")
```"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "pre",
                    [LeafNode("code", 'def hello():\n    print("Hello, world!")\n')],
                )
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_quote_block(self):
        markdown = """> This is a quote
> with multiple lines"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "blockquote",
                    [LeafNode(None, "This is a quote with multiple lines")],
                )
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_unordered_list(self):
        markdown = """* Item 1
* Item 2
* Item 3"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "Item 1")]),
                        ParentNode("li", [LeafNode(None, "Item 2")]),
                        ParentNode("li", [LeafNode(None, "Item 3")]),
                    ],
                )
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_ordered_list(self):
        markdown = """1. First item
2. Second item
3. Third item"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "First item")]),
                        ParentNode("li", [LeafNode(None, "Second item")]),
                        ParentNode("li", [LeafNode(None, "Third item")]),
                    ],
                )
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_paragraph_with_inline_formatting(self):
        markdown = "This has **bold** and _italic_ and `code` text."
        result = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This has "),
                        LeafNode("b", "bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italic"),
                        LeafNode(None, " and "),
                        LeafNode("code", "code"),
                        LeafNode(None, " text."),
                    ],
                )
            ],
        )
        self.assertEqual(result.to_html(), expected.to_html())

    def test_mixed_content(self):
        markdown = """# My Document

This is a paragraph with **bold** text.

## Code Example

```
print("Hello, world!")
```

### List

* Item 1
* Item 2

> This is a quote"""

        result = markdown_to_html_node(markdown)

        # Verify structure by checking HTML output
        html = result.to_html()
        self.assertIn("<h1>My Document</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text.</p>", html)
        self.assertIn("<h2>Code Example</h2>", html)
        self.assertIn('<pre><code>print("Hello, world!")\n</code></pre>', html)
        self.assertIn("<h3>List</h3>", html)
        self.assertIn("<ul><li>Item 1</li><li>Item 2</li></ul>", html)
        self.assertIn("<blockquote>This is a quote</blockquote>", html)

    def test_empty_markdown(self):
        markdown = ""
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", [])
        self.assertEqual(result.to_html(), expected.to_html())


if __name__ == "__main__":
    unittest.main()
