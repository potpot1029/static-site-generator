
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_value(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = ParentNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
