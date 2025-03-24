import unittest
from helpers import markdown_to_html_node, code_block_to_html_node

class TestHelpers(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        print(node)
        html = node.to_html()
        # print(html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    # def test_code_block_to_html_node_valid(self):
    #     text = """```
    #     print("Hello, World!")
    #     def foo():
    #         return "bar"
    #     ```
    #     """
    #     node = code_block_to_html_node(text)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<pre><code>print(\"Hello, World!\")\ndef foo():\n    return \"bar\"\n</code></pre>",
    #     )

    # def test_code_block_to_html_node_inline(self):
    #     text = "```print('inline code')```"
    #     node = code_block_to_html_node(text)
    #     html = node.to_html()
    #     self.assertEqual(html, "<pre><code>print('inline code')</code></pre>")

    # def test_code_block_to_html_node_missing_closing(self):
    #     text = """```
    #     print("Missing closing backticks")"""
    #     with self.assertRaises(ValueError) as context:
    #         code_block_to_html_node(text)
    #     self.assertEqual(str(context.exception), "Code block must start and end with ```")

    # def test_code_block_to_html_node_missing_opening(self):
    #     text = """print("Missing opening backticks")
    #     ```"""
    #     with self.assertRaises(ValueError) as context:
    #         code_block_to_html_node(text)
    #     self.assertEqual(str(context.exception), "Code block must start and end with ```")

    # def test_code_block_to_html_node_empty(self):
    #     text = "``````"
    #     node = code_block_to_html_node(text)
    #     html = node.to_html()
    #     self.assertEqual(html, "<pre><code></code></pre>")

