import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_code(self):
        node = LeafNode("code", "print('Hello')")
        self.assertEqual(node.to_html(), "<code>print('Hello')</code>")

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode(
            "img", "Image description", {"src": "image.jpg", "alt": "A sample image"}
        )
        result = node.to_html()
        self.assertIn("<img", result)
        self.assertIn('src="image.jpg"', result)
        self.assertIn('alt="A sample image"', result)
        self.assertIn(">Image description</img>", result)

    def test_leaf_to_html_span_with_class(self):
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        self.assertEqual(
            node.to_html(), '<span class="highlight">Highlighted text</span>'
        )

    def test_leaf_no_children_allowed(self):
        node = LeafNode("p", "Test")
        self.assertIsNone(node.children)


if __name__ == "__main__":
    unittest.main()
