from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from nodetonode import markdown_to_blocks, text_to_textnodes, text_node_to_html
from blocks import block_to_blocktype, BlockType

def code_block_to_html_node(text: str) -> ParentNode:
    # remove lines containing ``` from the start and end
    split_text = text.split("\n")
    print(split_text)
    if split_text[0] == "```":
        split_text = split_text[1:]
    print(split_text)
    if split_text[-1] == "```":
        split_text = split_text[:-1]
        # add newline if last index is ```
        split_text[-1] = split_text[-1]+"\n"
    print(split_text)
    text = "\n".join(split_text).strip("`") # remove ``` from start and end in case code block was inline at all
    print(text)
    code_text_node = TextNode(text, TextType.CODE)
    return ParentNode("pre", [text_node_to_html(code_text_node)])

def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    print(nodes)
    children = []
    for node in nodes:
        if node.text_type == TextType.TEXT:
            children.append(LeafNode(None, node.text))
        else:
            children.append(text_node_to_html(node))
    return children

def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    # split md into blocks
    blocks = markdown_to_blocks(markdown)
    # print(blocks)
    # iterate over blocks and create HTMLNodes
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type != BlockType.CODE:
            tag = block_type.value
            if block_type == BlockType.HEADING:
                tag = block_type+block.count("#")
            text_children = text_to_children(block.replace("\n", " "))
            children.append(ParentNode(tag, text_children))
        else:
            # if block is code, create HTMLNode as is without calling text_to_children
            children.append(code_block_to_html_node(block))

    return ParentNode("div", children)
