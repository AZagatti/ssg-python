import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        expected = 'class="container" '
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://example.com", "target": "_blank", "class": "link"},
        )
        result = node.props_to_html()
        self.assertIn('href="https://example.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertIn('class="link"', result)

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="div")
        with self.assertRaises(AttributeError):
            node.props_to_html()

    def test_props_to_html_empty_props(self):
        node = HTMLNode(tag="div", props={})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_special_characters(self):
        node = HTMLNode(
            tag="input",
            props={"value": "hello world", "placeholder": "Enter text here"},
        )
        result = node.props_to_html()
        self.assertIn('value="hello world"', result)
        self.assertIn('placeholder="Enter text here"', result)

    def test_htmlnode_repr(self):
        node = HTMLNode(tag="p", value="Hello", props={"class": "text"})
        expected = "HTMLNode(tag=p, props={'class': 'text'}, children=None)"
        self.assertEqual(repr(node), expected)

    def test_htmlnode_with_children(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2], props={"id": "parent"})

        self.assertEqual(parent.tag, "div")
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Child 1")
        self.assertEqual(parent.children[1].value, "Child 2")

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
