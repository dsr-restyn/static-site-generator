import unittest
from src import textnode, nodetonode

# TODO:
# Move tests out of src directory


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        node2 = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        self.assertEqual(node, node2)

    def test_default(self):
        node = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        node2 = textnode.TextNode("This is a link node", textnode.TextType.LINK, "https://www.example.com")
        self.assertEqual(node.text, "This is a text node")
        self.assertEqual(node.text_type, textnode.TextType.BOLD)
        self.assertIsNone(node.url)
        self.assertEqual(node2.text, "This is a link node")
        self.assertEqual(node2.text_type, textnode.TextType.LINK)
        self.assertEqual(node2.url, "https://www.example.com")

    def test_repr(self):
        node = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        self.assertEqual(repr(node), "TextNode('This is a text node', bold, None)")
        node2 = textnode.TextNode("This is a link node", textnode.TextType.LINK, "https://www.example.com")
        self.assertEqual(repr(node2), "TextNode('This is a link node', link, https://www.example.com)")

    def test_eq_false(self):
        node = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        node2 = textnode.TextNode("This is a link node", textnode.TextType.LINK, "https://www.example.com")
        node3 = textnode.TextNode("This is another text node", textnode.TextType.BOLD)
        node4 = textnode.TextNode("This is another text node", textnode.TextType.ITALIC)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    # region text_node_to_html
    def test_text_node_to_html_bold(self):
        node = textnode.TextNode("This is a text node", textnode.TextType.BOLD)
        self.assertEqual(nodetonode.text_node_to_html(node).to_html(), '<b>This is a text node</b>')
        node2 = textnode.TextNode("This is a link node", textnode.TextType.LINK, "https://www.example.com")
        self.assertEqual(nodetonode.text_node_to_html(node2).to_html(), '<a href="https://www.example.com">This is a link node</a>')
        node3 = textnode.TextNode("This is a code node", textnode.TextType.CODE)
        self.assertEqual(nodetonode.text_node_to_html(node3).to_html(), '<code>This is a code node</code>')
        node4 = textnode.TextNode("this is alt text", textnode.TextType.IMAGE, "https://www.example.com")
        self.assertEqual(nodetonode.text_node_to_html(node4).to_html(), '<img src="https://www.example.com" alt="this is alt text"></img>')
    # endregion
    # region split_nodes_delimiter
    def test_split_single_delimiter(self):
        nodes = [
            textnode.TextNode("this node has a `code` block", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("this node has a ", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode(" block", textnode.TextType.TEXT)
        ])

    def test_split_multiple_delimiters(self):
        nodes = [
            textnode.TextNode("this node has `code` and `more code` blocks", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("this node has ", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode(" and ", textnode.TextType.TEXT),
            textnode.TextNode("more code", textnode.TextType.CODE),
            textnode.TextNode(" blocks", textnode.TextType.TEXT),
        ])

    def test_split_no_delimiters(self):
        nodes = [
            textnode.TextNode("this node has no code blocks", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("this node has no code blocks", textnode.TextType.TEXT),
        ])

    def test_split_empty_text(self):
        nodes = [
            textnode.TextNode("", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("", textnode.TextType.TEXT),
        ])

    def test_split_mixed_text_types(self):
        nodes = [
            textnode.TextNode("this node has `code` block", textnode.TextType.TEXT),
            textnode.TextNode("this is **bold** text", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("this node has ", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode(" block", textnode.TextType.TEXT),
            textnode.TextNode("this is **bold** text", textnode.TextType.TEXT),
        ])
        second_pass = nodetonode.split_nodes_delimiter(split_nodes, '**', textnode.TextType.BOLD)
        self.assertEqual(second_pass, [
            textnode.TextNode("this node has ", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode(" block", textnode.TextType.TEXT),
            textnode.TextNode("this is ", textnode.TextType.TEXT),
            textnode.TextNode("bold", textnode.TextType.BOLD),
            textnode.TextNode(" text", textnode.TextType.TEXT),
        ])

    def test_split_delimiter_at_start_and_end(self):
        nodes = [
            textnode.TextNode("`code` block at start and end `code`", textnode.TextType.TEXT),
        ]
        split_nodes = nodetonode.split_nodes_delimiter(nodes, '`', textnode.TextType.CODE)
        self.assertEqual(split_nodes, [
            textnode.TextNode("", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode(" block at start and end ", textnode.TextType.TEXT),
            textnode.TextNode("code", textnode.TextType.CODE),
            textnode.TextNode("", textnode.TextType.TEXT),
        ])

    #endregion

    # region extract_markdown_images
    def test_extract_markdown_images_single(self):
        text = "Here is an image: ![alt text](https://example.com/image.png)"
        result = nodetonode.extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.png")])

    def test_extract_markdown_images_multiple(self):
        text = (
            "First image: ![first](https://example.com/first.png), "
            "Second image: ![second](https://example.com/second.png)"
        )
        result = nodetonode.extract_markdown_images(text)
        self.assertEqual(result, [
            ("first", "https://example.com/first.png"),
            ("second", "https://example.com/second.png"),
        ])

    def test_extract_markdown_images_none(self):
        text = "This text has no images."
        result = nodetonode.extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_malformed(self):
        text = "Malformed image: ![alt text](https://example.com/image.png"
        result = nodetonode.extract_markdown_images(text)
        self.assertEqual(result, [])
    # endregion

    # region extract_markdown_links
    def test_extract_markdown_links_single(self):
        text = "Here is a link: [example](https://example.com)"
        result = nodetonode.extract_markdown_links(text)
        self.assertEqual(result, [("example", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = (
            "First link: [first](https://example.com/first), "
            "Second link: [second](https://example.com/second)"
        )
        result = nodetonode.extract_markdown_links(text)
        self.assertEqual(result, [
            ("first", "https://example.com/first"),
            ("second", "https://example.com/second"),
        ])

    def test_extract_markdown_links_none(self):
        text = "This text has no links."
        result = nodetonode.extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_malformed(self):
        text = "Malformed link: [example](https://example.com"
        result = nodetonode.extract_markdown_links(text)
        self.assertEqual(result, [])
    # endregion

if __name__ == "__main__":
    unittest.main()
