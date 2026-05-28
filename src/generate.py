import os

from block import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("missing h1 header, cannot extract title")

def generate_page_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        full_item = os.path.join(dir_path_content, item)

        new_dest = os.path.join(dest_dir_path, item)

        if os.path.isfile(full_item):
            name, _ = os.path.splitext(new_dest)

            generate_page(full_item, template_path, name + ".html", basepath)
        else:
            generate_page_recursively(full_item, template_path, new_dest, basepath)
        

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"[log] generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as mdf:
        md = mdf.read()

    with open(template_path, "r") as tpf:
        template = tpf.read()

    md_html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", md_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as dsf:
        dsf.write(template)
