import unittest

from block import (BlockType, block_to_block_type, markdown_to_blocks,
                   markdown_to_html_node)


class TestMarkdownToBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_strip(self):
        md = """
This is **bolded** paragraph


   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line   


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# this is a heading!"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_not_heading(self):
        block = "# this is not a heading!\n test"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\nthis is some code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_not_code(self):
        block = "```\nthis is not some code\n``"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = "> this is a quote\n>with many lines\n> in the quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_not_quote(self):
        block = "> this is not a quote\nwith many lines\n> in the quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- this is a list\n- with many items\n- here is one more item"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_block_to_block_type_not_unordered_list(self):
        block = "- this is not a list\n- with many items\n-here is one more item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. this is a ordered list\n2. with many items\n3. here is one more item"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_block_to_block_type_not_ordered_list(self):
        block = "1. this is a ordered list\n4. with many items\n3. here is one more item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):
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
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# this is a heading

and this is a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is a heading</h1><p>and this is a paragraph</p></div>",
        )

    def test_quote(self):
        md = """
>this is a quote 
> this is another line of the quote

and this is a paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote this is another line of the quote</blockquote><p>and this is a paragraph</p></div>",
        )

    def test_list(self):
        md = """
- list item
- list item

1. list item
2. list item
3. list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>list item</li><li>list item</li></ul><ol><li>list item</li><li>list item</li><li>list item</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()
