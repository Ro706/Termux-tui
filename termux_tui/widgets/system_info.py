import subprocess
import re
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text

def get_system_info():
    """Get system information."""
    table = Table.grid(expand=True)
    try:
        # CPU
        with open('/proc/stat', 'r') as f:
            cpu_lines = [line for line in f if line.startswith('cpu')]
            if cpu_lines:
                cpu_line = cpu_lines[0]
                parts = cpu_line.split()
                user = int(parts[1])
                nice = int(parts[2])
                system = int(parts[3])
                idle = int(parts[4])
                iowait = int(parts[5])
                irq = int(parts[6])
                softirq = int(parts[7])
                total = user + nice + system + idle + iowait + irq + softirq
                idle_percent = (idle / total) * 100
                cpu_percent = 100 - idle_percent
                table.add_row("CPU:", ProgressBar(total=100, completed=cpu_percent, width=10))

        # Memory
        with open('/proc/meminfo', 'r') as f:
            meminfo = f.read()
            mem_total_match = re.search(r'MemTotal:\s+(\d+)', meminfo)
            mem_available_match = re.search(r'MemAvailable:\s+(\d+)', meminfo)
            if mem_total_match and mem_available_match:
                mem_total = int(mem_total_match.group(1))
                mem_available = int(mem_available_match.group(1))
                mem_used = mem_total - mem_available
                mem_percent = (mem_used / mem_total) * 100
                table.add_row("Memory:", ProgressBar(total=100, completed=mem_percent, width=10))

        # Battery
        result = subprocess.run(['termux-battery-status'], capture_output=True, text=True)
        if result.returncode == 0:
            import json
            battery_info = json.loads(result.stdout)
            if battery_info:
                table.add_row("Battery:", ProgressBar(total=100, completed=battery_info['percentage'], width=10))
        return table
    except (FileNotFoundError, PermissionError, IndexError, ValueError):
        return Text("System info not available", justify="center")
