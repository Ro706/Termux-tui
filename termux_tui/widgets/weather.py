from rich.text import Text
from rich.table import Table

def get_weather():
    """Get weather information for Nagpur."""
    table = Table.grid(expand=True)
    table.add_row("City:", "Nagpur")
    table.add_row("Temperature:", "29°C")
    table.add_row("Condition:", "Mostly Sunny")
    table.add_row("Humidity:", "41%")
    table.add_row("Chance of Rain:", "0%")
    return table