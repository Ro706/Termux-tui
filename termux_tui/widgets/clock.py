from datetime import datetime
from rich.text import Text

def create_clock():
    return Text(datetime.now().ctime(), style="bold magenta", justify="center")
