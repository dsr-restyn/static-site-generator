import unittest
from nodetonode import text_node_to_html, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, TextType.BOLD)
        self.assertIsNone(node.url)
        self.assertEqual(node2.text, "This is a link node")
        self.assertEqual(node2.text_type, TextType.LINK)
        self.assertEqual(node2.url, "https://www.example.com")

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode('This is a text node', bold, None)")
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        self.assertEqual(repr(node2), "TextNode('This is a link node', link, https://www.example.com)")

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        node3 = TextNode("This is another text node", TextType.BOLD)
        node4 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    # region text_node_to_html
    def test_text_node_to_html_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(text_node_to_html(node).to_html(), '<strong>This is a text node</strong>')
        node2 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        self.assertEqual(text_node_to_html(node2).to_html(), '<a href="https://www.example.com">This is a link node</a>')
        node3 = TextNode("This is a code node", TextType.CODE)
        self.assertEqual(text_node_to_html(node3).to_html(), '<code>This is a code node</code>')
        node4 = TextNode("this is alt text", TextType.IMAGE, "https://www.example.com")
        self.assertEqual(text_node_to_html(node4).to_html(), '<img src="https://www.example.com" alt="this is alt text"></img>')
    # endregion
    # region split_nodes_delimiter
    def test_split_single_delimiter(self):
        nodes = [
            TextNode("this node has a `code` block", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("this node has a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT)
        ])

    def test_split_multiple_delimiters(self):
        nodes = [
            TextNode("this node has `code` and `more code` blocks", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("this node has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ])

    def test_split_no_delimiters(self):
        nodes = [
            TextNode("this node has no code blocks", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("this node has no code blocks", TextType.TEXT),
        ])

    def test_split_empty_text(self):
        nodes = [
            TextNode("", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("", TextType.TEXT),
        ])

    def test_split_mixed_text_types(self):
        nodes = [
            TextNode("this node has `code` block", TextType.TEXT),
            TextNode("this is **bold** text", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("this node has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("this is **bold** text", TextType.TEXT),
        ])
        second_pass = split_nodes_delimiter(split_nodes, '**', TextType.BOLD)
        self.assertEqual(second_pass, [
            TextNode("this node has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_split_delimiter_at_start_and_end(self):
        nodes = [
            TextNode("`code` block at start and end `code`", TextType.TEXT),
        ]
        split_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(split_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block at start and end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ])

    #endregion

    # region extract_markdown_images
    def test_extract_markdown_images_single(self):
        text = "Here is an image: ![alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = (
            "First image: ![first](https://example.com/first.png), "
            "Second image: ![second](https://example.com/second.png)"
        )
        result = extract_markdown_images(text)
        self.assertEqual(result, [
            ("first", "https://example.com/first.png"),
            ("second", "https://example.com/second.png"),
        ])

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_malformed(self):
        text = "Malformed image: ![alt text](https://example.com/image.png"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    # endregion

    # region extract_markdown_links
    def test_extract_markdown_links_single(self):
        text = "Here is a link: [example](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("example", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = (
            "First link: [first](https://example.com/first), "
            "Second link: [second](https://example.com/second)"
        )
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ("first", "https://example.com/first"),
            ("second", "https://example.com/second"),
        ])

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_malformed(self):
        text = "Malformed link: [example](https://example.com"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
    # endregion

if __name__ == "__main__":
    unittest.main()
