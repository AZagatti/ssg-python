import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()
