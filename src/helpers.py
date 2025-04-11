from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from nodetonode import markdown_to_blocks, text_to_textnodes, text_node_to_html
from blocks import block_to_blocktype, BlockType

def code_block_to_html_node(text: str) -> ParentNode:
    # Strip leading and trailing whitespace/newlines
    text = text.strip().strip("\n")
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    text = text.strip("`")
    code_text_node = TextNode(text, TextType.CODE)
    return ParentNode("pre", [text_node_to_html(code_text_node)])

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        else:
            children.append(text_node_to_html(node))
    return children

def strip_block_of_delimiters(block: str, delimiter: str) -> str:
    if delimiter == ">":
        print(f"strip_block_of_delimiters: {block=}")
        lines = block.split("\n")
        for line in lines:
            print(f"strip_block_of_delimiters: {line=}")
        return "\n".join([line.strip().lstrip(delimiter) for line in block.split("\n")])
    return block.strip(delimiter).strip()

def get_block_delimiter(block: str) -> str:
    return block[0]

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block = block.strip()
        block_type, md_delimiter = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            heading_level = block.count("#")
            tag = block_type.value + str(heading_level)
            block = strip_block_of_delimiters(block, "#" * heading_level + " ")
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(tag, text_children))
        elif block_type == BlockType.CODE:
            children.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            block = strip_block_of_delimiters(block, ">")
            text_children = text_to_children(block)
            children.append(ParentNode(block_type.value, text_children))
        elif block_type in [BlockType.ULIST, BlockType.OLIST]:
            list_items = block.split("\n")
            list_children = []
            for item in list_items:
                item = strip_block_of_delimiters(item, md_delimiter if md_delimiter else "")
                list_children.append(ParentNode("li", text_to_children(item)))
            children.append(ParentNode(block_type.value, list_children))
        else:
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(block_type.value, text_children))
    return ParentNode("div", children)
