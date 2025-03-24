from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    ULIST = "ul"
    OLIST = "ol"
    

def block_to_blocktype(block: str) -> BlockType:
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all([c.startswith(">") for c in block.split("\n")]):
        return BlockType.QUOTE
    elif all([c.startswith("- ") for c in block.split("\n")]):
        return BlockType.ULIST
    elif all([c[0].isdigit() and c[1] == "." for c in block.split("\n")]):
        count = 1
        for i in block.split("\n"):
            if i[0] != str(count):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH
