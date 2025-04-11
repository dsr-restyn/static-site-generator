import unittest
from src.helpers import markdown_to_html_node, code_block_to_html_node, extract_h1_header

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

    def test_headings(self):
        md = """
        ### HEADING

        ## HEADING

        # HEADING
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>HEADING</h3><h2>HEADING</h2><h1>HEADING</h1></div>",
        )

    # def test_codeblock(self):
    #     md = """
    # ```
    # This is text that _should_ remain
    # the **same** even with inline stuff
    # ```
    # """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )

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
    #         "<pre><code>\n        print(\"Hello, World!\")\n        def foo():\n            return \"bar\"\n        </code></pre>",
    #     )

    # def test_code_block_to_html_node_inline(self):
    #     text = "```print('inline code')```"
    #     node = code_block_to_html_node(text)
    #     html = node.to_html()
    #     self.assertEqual(html, "<pre><code>print('inline code')</code></pre>")

    def test_code_block_to_html_node_missing_closing(self):
        text = """```
        print("Missing closing backticks")"""
        with self.assertRaises(ValueError) as context:
            code_block_to_html_node(text)
        self.assertEqual(str(context.exception), "Code block must start and end with ```")

    def test_code_block_to_html_node_missing_opening(self):
        text = """print("Missing opening backticks")
        ```"""
        with self.assertRaises(ValueError) as context:
            code_block_to_html_node(text)
        self.assertEqual(str(context.exception), "Code block must start and end with ```")

    def test_code_block_to_html_node_empty(self):
        text = "``````"
        node = code_block_to_html_node(text)
        html = node.to_html()
        self.assertEqual(html, "<pre><code></code></pre>")
    
    def test_extract_h1_header_valid(self):
        md = "# This is a header\n\nSome other text"
        result = extract_h1_header(md)
        self.assertEqual(result, "This is a header")

    def test_extract_h1_header_no_h1(self):
        md = "## This is not an H1 header\n\nSome other text"
        with self.assertRaises(ValueError):
            extract_h1_header(md)

    def test_extract_h1_header_multiple_h1(self):
        md = "# First header\n\n# Second header"
        result = extract_h1_header(md)
        self.assertEqual(result, "First header")

    def test_extract_h1_header_empty(self):
        md = ""
        with self.assertRaises(ValueError):
            extract_h1_header(md)

    def test_extract_h1_header_whitespace(self):
        md = "#    Header with leading spaces   \n\nSome other text"
        result = extract_h1_header(md)
        self.assertEqual(result, "Header with leading spaces")

