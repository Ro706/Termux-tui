#!/usr/bin/env python3

import asyncio
import sys
from termux_tui.main import main

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))