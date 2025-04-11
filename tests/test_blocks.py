import unittest
from src import blocks

class TestBlocks(unittest.TestCase):
    def test_block_to_blocktype(self):
        self.assertEqual(blocks.block_to_blocktype("# heading"), (blocks.BlockType.HEADING, '#'))
        self.assertEqual(blocks.block_to_blocktype("```code```"), (blocks.BlockType.CODE, "```"))
        self.assertEqual(blocks.block_to_blocktype("> quote"), (blocks.BlockType.QUOTE, '>'))
        self.assertEqual(blocks.block_to_blocktype("- ulist"), (blocks.BlockType.ULIST, '- '))
        self.assertEqual(blocks.block_to_blocktype("1. olist"), (blocks.BlockType.OLIST, '1. '))
        self.assertEqual(blocks.block_to_blocktype("paragraph"), (blocks.BlockType.PARAGRAPH, None))
        self.assertEqual(blocks.block_to_blocktype("1. olist\n2. olist2"), (blocks.BlockType.OLIST, '1. '))
        self.assertEqual(blocks.block_to_blocktype("1. olist\n3. olist2"), (blocks.BlockType.PARAGRAPH, None))
        self.assertEqual(blocks.block_to_blocktype("> quote\nnot a quote"), (blocks.BlockType.PARAGRAPH, None))

if __name__ == "__main__":
    unittest.main()