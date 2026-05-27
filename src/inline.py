import re

from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 != 1:
            raise ValueError(f"invalid markdown syntax: missing matching delimiter {delimiter}")

        split_nodes = []
        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            else:
                split_nodes.append(TextNode(text, text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
       
        cur_text = old_node.text
        for (alt_text, image_link) in images:
            before, after = cur_text.split(f"![{alt_text}]({image_link})", 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_link))
           
            cur_text = after
        if cur_text != "":
            new_nodes.append(TextNode(cur_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
       
        cur_text = old_node.text
        for (anchor_text, link) in links:
            before, after = cur_text.split(f"[{anchor_text}]({link})", 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link))
           
            cur_text = after
        if cur_text != "":
            new_nodes.append(TextNode(cur_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

