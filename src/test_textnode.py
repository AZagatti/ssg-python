import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_not_equal_one_url_none(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, None)
        self.assertNotEqual(node, node2)

    def test_eq_both_url_none(self):
        node = TextNode("Plain text", TextType.PLAIN, None)
        node2 = TextNode("Plain text", TextType.PLAIN, None)
        self.assertEqual(node, node2)

    def test_not_equal_different_type_object(self):
        node = TextNode("This is a text node", TextType.BOLD)
        not_a_node = "This is just a string"
        self.assertNotEqual(node, not_a_node)

    def test_repr(self):
        node = TextNode("Test text", TextType.CODE, "https://test.com")
        expected_repr = "TextNode(text=Test text, text_type=code, url=https://test.com)"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_url(self):
        node = TextNode("Plain text", TextType.PLAIN)
        expected_repr = "TextNode(text=Plain text, text_type=plain, url=None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
