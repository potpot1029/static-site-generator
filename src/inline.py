from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
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
