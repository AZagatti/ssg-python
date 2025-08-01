import unittest

from extract_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)
from textnode import TextNode, TextType


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_image_empty_alt_text(self):
        text = "Image with empty alt text ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_image_no_images(self):
        text = "This text has no images, just regular text"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_image_with_spaces_in_alt(self):
        text = "![alt text with spaces](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("alt text with spaces", "https://example.com/image.jpg")], matches
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_single_link(self):
        text = "Check out [this awesome site](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("this awesome site", "https://example.com")], matches)

    def test_extract_link_empty_anchor_text(self):
        text = "Link with empty text [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_link_no_links(self):
        text = "This text has no links, just regular text"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_links_not_images(self):
        text = "![image](https://example.com/image.png) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_images_not_links(self):
        text = "![image](https://example.com/image.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/image.png")], matches)

    def test_extract_mixed_content(self):
        text = "Here's an ![image](https://example.com/pic.jpg) and a [link](https://example.com) together"

        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)

        self.assertListEqual([("image", "https://example.com/pic.jpg")], image_matches)
        self.assertListEqual([("link", "https://example.com")], link_matches)

    def test_extract_link_with_special_characters(self):
        text = "Visit [GitHub - @username](https://github.com/username)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("GitHub - @username", "https://github.com/username")], matches
        )

    def test_extract_image_with_special_characters(self):
        text = "![Screenshot #1 - Main Page](https://example.com/screenshot-1.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("Screenshot #1 - Main Page", "https://example.com/screenshot-1.png")],
            matches,
        )

    def test_extract_url_with_query_params(self):
        text = "[Search](https://example.com/search?q=test&sort=date)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("Search", "https://example.com/search?q=test&sort=date")], matches
        )

    def test_extract_multiple_links_same_line(self):
        text = "Links: [first](https://first.com), [second](https://second.com), [third](https://third.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "https://first.com"),
            ("second", "https://second.com"),
            ("third", "https://third.com"),
        ]
        self.assertListEqual(expected, matches)

    def test_extract_nested_brackets_in_url(self):
        text = "![image](https://example.com/path/to/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("image", "https://example.com/path/to/image.png")], matches
        )

    def test_extract_local_file_paths(self):
        text = "![local image](./images/local.png) and [local link](./pages/about.html)"

        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)

        self.assertListEqual([("local image", "./images/local.png")], image_matches)
        self.assertListEqual([("local link", "./pages/about.html")], link_matches)


class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_single(self):
        node = TextNode("![single image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("single image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_single(self):
        node = TextNode("[single link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("single link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_no_images(self):
        node = TextNode("This text has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_no_links(self):
        node = TextNode("This text has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [node]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_beginning(self):
        node = TextNode(
            "![start image](https://example.com/start.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("start image", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_beginning(self):
        node = TextNode(
            "[start link](https://example.com) followed by text", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("start link", TextType.LINK, "https://example.com"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_ending(self):
        node = TextNode(
            "Text before ![end image](https://example.com/end.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end image", TextType.IMAGE, "https://example.com/end.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_ending(self):
        node = TextNode("Text before [end link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_nodes_non_text_unchanged(self):
        nodes = [
            TextNode(
                "Text with ![image](https://example.com/image.png)", TextType.TEXT
            ),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Code text", TextType.CODE),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_mixed_nodes_links(self):
        nodes = [
            TextNode("Text with [link](https://example.com)", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More [links](https://test.com) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("Bold text", TextType.BOLD),
            TextNode("More ", TextType.TEXT),
            TextNode("links", TextType.LINK, "https://test.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Image with empty alt ![](https://example.com/image.png) text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Image with empty alt ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_empty_anchor_text(self):
        node = TextNode(
            "Link with empty text [](https://example.com) here", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Link with empty text ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_consecutive_images(self):
        node = TextNode(
            "![first](https://example.com/1.png)![second](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("second", TextType.IMAGE, "https://example.com/2.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_consecutive_links(self):
        node = TextNode(
            "[first](https://example.com/1)[second](https://example.com/2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode("second", TextType.LINK, "https://example.com/2"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_images_doesnt_affect_links(self):
        node = TextNode(
            "![image](https://example.com/image.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and [link](https://example.com)", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_links_doesnt_affect_images(self):
        node = TextNode(
            "![image](https://example.com/image.png) and [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("![image](https://example.com/image.png) and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_text(self):
        text = "This is just plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is just plain text with no formatting", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold text**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_italic(self):
        text = "_italic text_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_code(self):
        text = "`code block`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("code block", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_image(self):
        text = "![image](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_only_link(self):
        text = "[link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_multiple_same_type(self):
        text = "**bold1** and **bold2** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_mixed_delimiters(self):
        text = "**bold** and _italic_ and `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_complex_example(self):
        text = "Start **bold** then _italic_ with `code` and ![img](https://test.com/img.png) plus [link](https://test.com) end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://test.com/img.png"),
            TextNode(" plus ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://test.com"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_adjacent_formatting(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = []
        self.assertListEqual(expected, nodes)

    def test_text_to_textnodes_whitespace_only(self):
        text = "   "
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("   ", TextType.TEXT),
        ]
        self.assertListEqual(expected, nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is just a single paragraph with no separating lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["This is just a single paragraph with no separating lines."]
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_with_extra_newlines(self):
        md = """

First block


Second block



Third block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block", "Third block"])

    def test_markdown_to_blocks_with_leading_trailing_whitespace(self):
        md = """
  First block with spaces

  Second block with tabs

  Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["First block with spaces", "Second block with tabs", "Third block"]
        )

    def test_markdown_to_blocks_complex_example(self):
        md = """# Heading 1

This is a paragraph with **bold** text and _italic_ text.

## Heading 2

Another paragraph here.
This continues the same paragraph.

- List item 1
- List item 2
- List item 3

Code block:
```
print("hello world")
```

Final paragraph."""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading 1",
            "This is a paragraph with **bold** text and _italic_ text.",
            "## Heading 2",
            "Another paragraph here.\nThis continues the same paragraph.",
            "- List item 1\n- List item 2\n- List item 3",
            'Code block:\n```\nprint("hello world")\n```',
            "Final paragraph.",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_preserve_internal_newlines(self):
        md = """First line
Second line
Third line

Another block
With multiple lines"""
        blocks = markdown_to_blocks(md)
        expected = [
            "First line\nSecond line\nThird line",
            "Another block\nWith multiple lines",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_mixed_content(self):
        md = """# Title

Paragraph with [link](https://example.com) and ![image](https://example.com/img.png).

> This is a quote block
> with multiple lines

1. Numbered list
2. Second item"""
        blocks = markdown_to_blocks(md)
        expected = [
            "# Title",
            "Paragraph with [link](https://example.com) and ![image](https://example.com/img.png).",
            "> This is a quote block\n> with multiple lines",
            "1. Numbered list\n2. Second item",
        ]
        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()
