import os
from rich.text import Text
from rich.tree import Tree

def get_file_browser(path="."):
    """Get a file browser widget."""
    tree = Tree(path)
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tree.add(f"[bold blue]{item}/[/bold blue]")
            else:
                tree.add(item)
    except PermissionError:
        return Text("Permission denied", style="bold red")
    return tree
