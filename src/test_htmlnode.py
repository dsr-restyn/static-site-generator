import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node, node2)

    def test_default(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "This is a link")
        self.assertIsNone(node2.children)
        self.assertEqual(node2.props, {"href": "https://www.example.com"})

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(repr(node), "HTMLNode(p, This is a paragraph, None, None)")
        node2 = HTMLNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(repr(node2), "HTMLNode(a, This is a link, None, {'href': 'https://www.example.com'})")

    def test_eq_false(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("a", "This is a link", props={"href": "https://www.example.com"})
        node3 = HTMLNode("p", "This is another paragraph")
        node4 = HTMLNode("p", "This is another paragraph", props={"href": "https://www.example.com"})
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode("p", "This is a paragraph").to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.example.com"')
        node2 = HTMLNode("a", "This is a link", props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node2.props_to_html(), 'href="https://www.example.com" target="_blank"')
    # region LeafNode
    def test_leaf_eq(self):
        node = LeafNode("p", "This is a paragraph")
        node2 = LeafNode("p", "This is a paragraph")
        self.assertEqual(node, node2)

    def test_leaf_default(self):
        node = LeafNode("p", "This is a paragraph")
        node2 = LeafNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node2.tag, "a")
        self.assertEqual(node2.value, "This is a link")
        self.assertIsNone(node2.children)
        self.assertEqual(node2.props, {"href": "https://www.example.com"})

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(repr(node), "LeafNode(p, This is a paragraph, None)")
        node2 = LeafNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(repr(node2), "LeafNode(a, This is a link, {'href': 'https://www.example.com'})")

    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
        node2 = LeafNode("a", "This is a link", props={"href": "https://www.example.com"})
        self.assertEqual(node2.to_html(), '<a href="https://www.example.com">This is a link</a>')
    # endregion

    # region ParentNode
    def test_parent_eq(self):
        node = ParentNode("p", [LeafNode("strong", "This is a bold text")])
        node2 = ParentNode("p", [LeafNode("strong", "This is a bold text")])
        self.assertEqual(node, node2)

    def test_parent_to_html(self):
        node = ParentNode("p", [LeafNode("strong", "This is a bold text")])
        self.assertEqual(node.to_html(), "<p><strong>This is a bold text</strong></p>")
        node2 = ParentNode("p", [LeafNode("a", "This is a link", props={"href": "https://www.example.com"})])
        self.assertEqual(node2.to_html(), '<p><a href="https://www.example.com">This is a link</a></p>')
        node3 = ParentNode("p", [ParentNode("ul", [LeafNode("li", "This is a list item")])])
        self.assertEqual(node3.to_html(), "<p><ul><li>This is a list item</li></ul></p>")
        node4 = ParentNode("p", [ParentNode("ul", [LeafNode("li", "This is a list item"), LeafNode("li", "This is another list item")]), ParentNode("p", [LeafNode("strong", "This is a bold text")])])
        self.assertEqual(node4.to_html(), "<p><ul><li>This is a list item</li><li>This is another list item</li></ul><p><strong>This is a bold text</strong></p></p>")
    # endregion
