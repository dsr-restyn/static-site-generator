from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    ULIST = "ul"
    OLIST = "ol"


def block_to_blocktype(block: str) -> tuple[BlockType, str|None]:
    block = block.strip()
    if block.startswith("#"):
        return BlockType.HEADING, "#"
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE, "```"
    elif all([c.strip().startswith(">") for c in block.split("\n")]):
        return BlockType.QUOTE, ">"
    elif all([c.strip().startswith("- ") for c in block.split("\n")]):
        return BlockType.ULIST, "- "
    elif all([c.strip().startswith("1. ") for c in block.split("\n")]):
        return BlockType.OLIST, "1. "
    else:
        return BlockType.PARAGRAPH, None
