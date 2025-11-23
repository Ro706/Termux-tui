from rich.layout import Layout

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(ratio=1, name="main"),
    )

    layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))
    return layout
