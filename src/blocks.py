from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    ULIST = "ul"
    OLIST = "ol"

def block_to_blocktype(block: str) -> tuple[BlockType, str | None]:
    block = block.strip()
    if block.startswith("#"):
        return BlockType.HEADING, "#"
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE, "```"
    elif all([c.strip().startswith(">") for c in block.split("\n")]):
        return BlockType.QUOTE, ">"
    elif all([c.strip().startswith("- ") for c in block.split("\n")]):
        return BlockType.ULIST, "- "
    elif all(
        [
            re.match(r"^\d+\. ", c.strip()) for c in block.split("\n")
        ]
    ):
        lines = block.split("\n")
        numbers = [int(c.strip().split(".")[0]) for c in lines if re.match(r"^\d+\. ", c.strip())]
        if numbers == list(range(1, len(numbers) + 1)):  # Check for incrementing numbers
            return BlockType.OLIST, "1. "
    return BlockType.PARAGRAPH, None
