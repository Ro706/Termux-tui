import asyncio
import os
import sys
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from .ui.layout import make_layout
from .widgets.clock import create_clock
from .widgets.system_info import get_system_info
from .widgets.weather import get_weather
from .widgets.file_browser import get_file_browser
from .utils.commands import run_command, show_help
from .utils.config import get_config
from .utils.plugin_loader import load_plugins

async def main():
    config = get_config()
    theme = config.get("theme", {})
    primary_color = theme.get("primary_color", "cyan")
    secondary_color = theme.get("secondary_color", "magenta")

    console = Console()
    layout = make_layout()
    layout["body"].update(Panel("Welcome to Termux TUI!", title="Output"))

    plugins = load_plugins()
    plugin_commands = {}
    for plugin in plugins:
        for command_name, command_info in plugin.get("commands", {}).items():
            plugin_commands[command_name] = command_info["function"]

    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        if command.lower() == "help":
            show_help(primary_color, secondary_color)
        else:
            # Non-interactive mode doesn't get the fancy layout
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stdout:
                console.print(stdout)
            if stderr:
                console.print(f"[bold red]Error:[/] {stderr}")
        return 0

    command_completer = WordCompleter([
        "pkg update", "pkg upgrade", "pkg install", "ls", "cd", "pwd",
        "termux-setup-storage", "termux-camera-photo", "termux-telephony-deviceinfo",
        "exit", "help"
    ] + list(plugin_commands.keys()))
    session = PromptSession(history=FileHistory(os.path.expanduser("~/.termux_tui_history")), completer=command_completer)
    
    cwd = os.getcwd()
    while True:
        console.clear()
        layout["header"].update(Panel(create_clock(), title="Clock"))
        sidebar = Layout(name="sidebar")
        sidebar.split(
            Panel(get_weather(), title="Weather"),
            Panel(get_system_info(), title="System Info"),
            Panel(get_file_browser(cwd), title="File Browser")
        )
        layout["side"].update(sidebar)

        console.print(layout)

        try:
            
            cmd = await session.prompt_async(f"[{cwd}]> ", auto_suggest=AutoSuggestFromHistory())
            if cmd.lower() == "exit":
                break
            if cmd.lower() == "help":
                show_help(primary_color, secondary_color)
                await session.prompt_async("Press Enter to continue...")
            
            elif cmd.split(" ")[0] in plugin_commands:
                command_function = plugin_commands[cmd.split(" ")[0]]
                command_function(layout, cmd.split(" ")[1:])

            elif cmd:
                await run_command(cmd, layout)
                if cmd.startswith("cd "):
                    path = cmd.split(" ", 1)[1]
                    if os.path.isdir(os.path.expanduser(path)):
                        os.chdir(os.path.expanduser(path))
                        cwd = os.getcwd()

        except (KeyboardInterrupt, EOFError):
            break
    return 0

if __name__ == "__main__":
    asyncio.run(main())
