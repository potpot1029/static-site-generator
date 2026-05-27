
import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode(
            "p",
            "hello world",
            None,
            None
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode(
            "p",
            "hello world for repr",
            None,
            { "class": "ok" }
        )
        self.assertEqual("HTMLNode(tag=p, value=hello world for repr, children=None, props={'class': 'ok'})", repr(node))

    def test_props_to_html_one(self):
        node = HTMLNode(
            props = {
                "target": "_blank",
            }
        )
        self.assertEqual(
            ' target="_blank"', node.props_to_html()
        )

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            props = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(
            "", node.props_to_html()
        )

class TestLeafNode(unittest.TestCase):
    def test_values(self):
        node = LeafNode(
            "p",
            "hello world",
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello world")
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = LeafNode(
            "p",
            "hello world for repr",
            { "class": "ok" }
        )
        self.assertEqual("LeafNode(tag=p, value=hello world for repr, props={'class': 'ok'})", repr(node))

    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

if __name__ == "__main__":
    TestHTMLNode()
    TestLeafNode()
