import os
import subprocess
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

def show_help(primary_color="cyan", secondary_color="magenta"):
    console = Console()
    table = Table(title=f"[bold {primary_color}]Common Termux Commands[/bold {primary_color}]")
    table.add_column("Command", style=primary_color, no_wrap=True)
    table.add_column("Description", style=secondary_color)

    commands = {
        "pkg update": "Update the package list.",
        "pkg upgrade": "Upgrade installed packages.",
        "pkg install <package>": "Install a new package.",
        "ls": "List files and directories.",
        "cd <directory>": "Change the current directory.",
        "pwd": "Print the current working directory.",
        "termux-setup-storage": "Set up access to device storage.",
        "termux-camera-photo": "Take a photo.",
        "termux-telephony-deviceinfo": "Get device info.",
        "exit": "Exit the TUI."
    }

    for cmd, desc in commands.items():
        table.add_row(cmd, desc)

    console.print(table)

import asyncio
import os
import subprocess
from rich.panel import Panel
from rich.console import Console
from rich.table import Table

def show_help(primary_color="cyan", secondary_color="magenta"):
    console = Console()
    table = Table(title=f"[bold {primary_color}]Common Termux Commands[/bold {primary_color}]")
    table.add_column("Command", style=primary_color, no_wrap=True)
    table.add_column("Description", style=secondary_color)

    commands = {
        "pkg update": "Update the package list.",
        "pkg upgrade": "Upgrade installed packages.",
        "pkg install <package>": "Install a new package.",
        "ls": "List files and directories.",
        "cd <directory>": "Change the current directory.",
        "pwd": "Print the current working directory.",
        "termux-setup-storage": "Set up access to device storage.",
        "termux-camera-photo": "Take a photo.",
        "termux-telephony-deviceinfo": "Get device info.",
        "exit": "Exit the TUI."
    }

    for cmd, desc in commands.items():
        table.add_row(cmd, desc)

    console.print(table)

async def run_command(command, layout):
    try:
        if command.startswith("cd "):
            try:
                path = command.split(" ", 1)[1]
                os.chdir(os.path.expanduser(path))
                layout["body"].update(Panel(f"Changed directory to {os.getcwd()}", title="[bold green]Output[/bold green]"))
            except IndexError:
                layout["body"].update(Panel("[bold red]Error:[/] Please provide a directory.", title="[bold red]Error[/bold red]"))
            except FileNotFoundError:
                layout["body"].update(Panel(f"[bold red]Error:[/] Directory not found: {path}", title="[bold red]Error[/bold red]"))
            return

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if stdout:
            layout["body"].update(Panel(stdout.decode(), title=f"[bold green]Output of '{command}'[/bold green]"))
        if stderr:
            layout["body"].update(Panel(stderr.decode(), title=f"[bold red]Error in '{command}'[/bold red]"))
    except Exception as e:
        layout["body"].update(Panel(str(e), title="[bold red]An error occurred[/bold red]"))
