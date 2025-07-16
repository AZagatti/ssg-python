import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "main"}
        )
        result = parent_node.to_html()
        self.assertIn("<div", result)
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn("><span>child</span></div>", result)

    def test_to_html_nested_parents(self):
        leaf1 = LeafNode("strong", "Bold")
        leaf2 = LeafNode(None, " and ")
        leaf3 = LeafNode("em", "italic")

        inner_parent = ParentNode("span", [leaf1, leaf2, leaf3])
        outer_parent = ParentNode("p", [LeafNode(None, "Text: "), inner_parent])

        expected = "<p>Text: <span><strong>Bold</strong> and <em>italic</em></span></p>"
        self.assertEqual(outer_parent.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have a tag", str(context.exception))

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_mixed_children_types(self):
        leaf = LeafNode("strong", "Bold")
        nested_parent = ParentNode("span", [LeafNode("em", "italic")])
        parent = ParentNode("p", [leaf, LeafNode(None, " text "), nested_parent])

        expected = "<p><strong>Bold</strong> text <span><em>italic</em></span></p>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_no_value_allowed(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertIsNone(parent_node.value)

    def test_complex_nested_structure(self):
        header = ParentNode("h1", [LeafNode(None, "Title")])
        paragraph1 = ParentNode(
            "p",
            [
                LeafNode(None, "This is "),
                LeafNode("strong", "important"),
                LeafNode(None, " text."),
            ],
        )
        paragraph2 = ParentNode(
            "p",
            [
                LeafNode(None, "Visit "),
                LeafNode("a", "our site", {"href": "https://example.com"}),
                LeafNode(None, " for more info."),
            ],
        )

        article = ParentNode("article", [header, paragraph1, paragraph2])

        result = article.to_html()
        self.assertIn("<article>", result)
        self.assertIn("<h1>Title</h1>", result)
        self.assertIn("<strong>important</strong>", result)
        self.assertIn('href="https://example.com"', result)
        self.assertIn("</article>", result)


if __name__ == "__main__":
    unittest.main()
