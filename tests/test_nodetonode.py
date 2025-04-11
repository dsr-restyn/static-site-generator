import unittest

from src import nodetonode, textnode

from src.textnode import TextNode, TextType

# TODO:
# Move tests out of src directory

class TestNodeToNode(unittest.TestCase):
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

    def test_split_images(self):
        node = textnode.TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            textnode.TextType.TEXT,
        )
        new_nodes = nodetonode.split_nodes_image([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with an ", textnode.TextType.TEXT),
                textnode.TextNode("image", textnode.TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                textnode.TextNode(" and another ", textnode.TextType.TEXT),
                textnode.TextNode(
                    "second image", textnode.TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        nodes = [
        textnode.TextNode("This is the first node", textnode.TextType.TEXT),
        textnode.TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                textnode.TextType.TEXT,
            ),
        textnode.TextNode("This is the last node", textnode.TextType.TEXT)
        ]

        new_nodes = nodetonode.split_nodes_image(nodes)

        self.assertListEqual(
            [
                textnode.TextNode("This is the first node", textnode.TextType.TEXT),
                textnode.TextNode("This is text with an ", textnode.TextType.TEXT),
                textnode.TextNode("image", textnode.TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                textnode.TextNode(" and another ", textnode.TextType.TEXT),
                textnode.TextNode("second image", textnode.TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                textnode.TextNode("This is the last node", textnode.TextType.TEXT)
            ], new_nodes
        )

    def test_split_links(self):
        node =textnode.TextNode(
            "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com)",
            textnode.TextType.TEXT,
        )
        new_nodes = nodetonode.split_nodes_link([node])
        self.assertListEqual(
            [
                textnode.TextNode("This is text with a ", textnode.TextType.TEXT),
                textnode.TextNode("link", textnode.TextType.LINK, "https://www.example.com"),
                textnode.TextNode(" and another ", textnode.TextType.TEXT),
                textnode.TextNode(
                    "second link", textnode.TextType.LINK, "https://www.example.com"
                ),
            ],
            new_nodes,
        )
        nodes = [
        textnode.TextNode("This is the first node", textnode.TextType.TEXT),
        textnode.TextNode(
                "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com)",
                textnode.TextType.TEXT,
            ),
        textnode.TextNode("This is the last node", textnode.TextType.TEXT)
        ]

        new_nodes = nodetonode.split_nodes_link(nodes)

        self.assertListEqual(
            [
            textnode.TextNode("This is the first node", textnode.TextType.TEXT),
            textnode.TextNode("This is text with a ", textnode.TextType.TEXT),
            textnode.TextNode("link", textnode.TextType.LINK, "https://www.example.com"),
            textnode.TextNode(" and another ", textnode.TextType.TEXT),
            textnode.TextNode("second link", textnode.TextType.LINK, "https://www.example.com"),
            textnode.TextNode("This is the last node", textnode.TextType.TEXT)
            ], new_nodes
        )

    def test_split_links_mixed(self):
        node =textnode.TextNode(
            "This is text with a [link](https://www.example.com) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            textnode.TextType.TEXT,
        )
        new_nodes = nodetonode.split_nodes_link([node])
        new_nodes = nodetonode.split_nodes_image(new_nodes)
        self.assertListEqual(
            [
            textnode.TextNode("This is text with a ", textnode.TextType.TEXT),
            textnode.TextNode("link", textnode.TextType.LINK, "https://www.example.com"),
            textnode.TextNode(" and another ", textnode.TextType.TEXT),
            textnode.TextNode(
                    "image", textnode.TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_non_link_split(self):
        nodes = [
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text and text and text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        ]
        link_split_nodes = nodetonode.split_nodes_link(nodes)
        self.assertEqual(link_split_nodes, [
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text and text and text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        ])

    def test_non_image_split(self):
        nodes = [
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text and text and text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        ]
        image_split_nodes = nodetonode.split_nodes_image(nodes)
        self.assertEqual(image_split_nodes, [
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text and text and text", textnode.TextType.TEXT),
        textnode.TextNode("This is just Text", textnode.TextType.TEXT),
        ])

    def test_split_empty_arr(self):
        nodes = []
        link_split_nodes = nodetonode.split_nodes_link(nodes)
        self.assertEqual(link_split_nodes, [])
        image_split_nodes = nodetonode.split_nodes_image(nodes)
        self.assertEqual(image_split_nodes, [])

    def test_split_malformed_link(self):
        nodes = [
        textnode.TextNode("This is a [malformed link](https://example.com", textnode.TextType.TEXT),
        ]
        link_split_nodes = nodetonode.split_nodes_link(nodes)
        self.assertEqual(link_split_nodes, nodes)

    def test_split_malformed_image(self):
        nodes = [
        textnode.TextNode("This is a ![malformed image](akjshdkasd", textnode.TextType.TEXT),
        ]
        image_split_nodes = nodetonode.split_nodes_image(nodes)
        self.assertEqual(image_split_nodes, nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = nodetonode.text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_markdown_to_blocks(self):
        md = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """
        blocks = nodetonode.markdown_to_blocks(md)

        self.assertEqual(blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ])

        md2 = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks2 = nodetonode.markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        # md3 = """
        # ```
        # This is text that _should_ remain
        # the **same** even with inline stuff
        # ```
        # """
        # blocks3 = nodetonode.markdown_to_blocks(md3)
        # self.assertEqual(blocks3, ["```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"])


if __name__ == "__main__":
    unittest.main()
