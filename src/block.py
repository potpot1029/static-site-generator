from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import text_to_textnodes
from textnode import text_node_to_html_node, text_nodes_to_html_nodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith((
        "# ",
        "## ",
        "### ",
        "#### ",
        "##### ",
        "###### ",
    )) and len(lines) == 1:
        return BlockType.HEADING

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    is_quote = True
    is_unordered_list = True
    is_ordered_list, check_ordered_index = True, 1
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_unordered_list = False
        if not line.startswith(f"{check_ordered_index}. "):
            is_ordered_list = False
        else:
            check_ordered_index += 1
    if is_quote:
        return BlockType.QUOTE
    if is_unordered_list:
        return BlockType.ULIST
    if is_ordered_list:
        return BlockType.OLIST


    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        html_nodes.append(block_to_html_node(block, block_type)) 

    return ParentNode("div", html_nodes)

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:

    children = None
    if block_type != BlockType.CODE:
        lines = block.split("\n")
        cleaned_lines = clean_lines(lines, block_type)
        children = lines_to_html_nodes(cleaned_lines, block_type)

    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", children)
        case BlockType.HEADING:
            level = len(block) - len(block.lstrip("#"))
            return ParentNode(f"h{level}", children)
        case BlockType.CODE:
            return ParentNode("pre", [LeafNode("code", block[4:-3])]) # strip backticks
        case BlockType.QUOTE:
            return ParentNode("blockquote", children)
        case BlockType.ULIST:
            return ParentNode("ul", children)
        case BlockType.OLIST:
            return ParentNode("ol", children)

def lines_to_html_nodes(lines: list[str], block_type: BlockType) -> list[HTMLNode]:
    match block_type:
        case BlockType.PARAGRAPH | BlockType.HEADING | BlockType.QUOTE:
            text = " ".join(lines)
            text_nodes = text_to_textnodes(text)
            return text_nodes_to_html_nodes(text_nodes)
        case BlockType.ULIST | BlockType.OLIST:
            nodes = []
            for line in lines:
                text_nodes = text_to_textnodes(line)
                node = ParentNode("li", text_nodes_to_html_nodes(text_nodes))
                nodes.append(node)
            return nodes
        case _:
            raise ValueError(f"invalid block_type: {block_type}")


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    blocks = []
    for line in lines:
        if line == "":
            continue
        blocks.append(line)

    return blocks

def clean_lines(lines: list[str], block_type: BlockType) -> list[str]:
    match block_type:
        case BlockType.PARAGRAPH:
            return lines
        case BlockType.HEADING:
            lines[0] = lines[0].lstrip("#")[1:]
            return lines
        case BlockType.QUOTE:
            for i, line in enumerate(lines):
                lines[i] = line.lstrip(">").strip()
            return lines
        case BlockType.ULIST:
            for i, line in enumerate(lines):
                lines[i] = line[2:]
            return lines
        case BlockType.OLIST:
            for i, line in enumerate(lines):
                lines[i] = line.lstrip("123456789.")
                lines[i] = lines[i][1:]
            return lines
        case _:
            raise ValueError(f"invalid block type: {block_type}")
