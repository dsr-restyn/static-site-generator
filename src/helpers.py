from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from nodetonode import markdown_to_blocks, text_to_textnodes, text_node_to_html
from blocks import block_to_blocktype, BlockType

def code_block_to_html_node(text: str) -> ParentNode:
    # Strip leading and trailing whitespace/newlines
    # print(f"code_block_to_html_node:\n\n{text}")
    text = text.strip().strip("\n")
    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    text = text.strip("`")
    code_text_node = TextNode(text, TextType.CODE)
    return ParentNode("pre", [text_node_to_html(code_text_node)])

def text_to_children(text: str) -> list[HTMLNode]:
    print(f"text_to_children: {text}")
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        # print(f"node {node}")
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        else:
            children.append(text_node_to_html(node))
    return children

def strip_block_of_delimiters(block: str, delimiter: str) -> str:
    split_lines = block.split("\n")
    return "\n".join([line.strip(delimiter) for line in split_lines])
    return block.strip(delimiter).strip()

def get_block_delimiter(block: str) -> str:
    return block[0]

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    # split md into blocks
    blocks = markdown_to_blocks(markdown)
    # print(blocks)
    # iterate over blocks and create HTMLNodes
    for block in blocks:
        block = block.strip()
        block_type, md_delimiter = block_to_blocktype(block)
        if block_type != BlockType.CODE:
            tag = block_type.value
            if block_type == BlockType.HEADING:
                heading_level = block.count("#")
                tag = block_type.value+str(heading_level)
                block = strip_block_of_delimiters(block, "#"*heading_level+" ")
            else:
                pass
                # if md_delimiter:
                #     block = strip_block_of_delimiters(block, md_delimiter)
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(tag, text_children))
        else:
            # print(f"block: {block}")
            # if block is code, create HTMLNode as is without calling text_to_children
            children.append(code_block_to_html_node(block))

    return ParentNode("div", children)
