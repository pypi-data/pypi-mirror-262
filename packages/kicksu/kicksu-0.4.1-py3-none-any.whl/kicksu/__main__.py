import requests
import time
import os
import rich
import subprocess
from rich.pretty import pprint as PP
from rich.console import Console
from rich.table import Table
import sys

IS_MACOS = "DARWIN" in sys.platform.upper()
IS_WIN = "WIN32" in sys.platform.upper()
IS_LINUX = "LINUX" in sys.platform.upper()

# written by robert degen
# 2015-2024
# notes:
# c:\cygwin64\bin\mintty.exe -w max -s 80x25  -e python -m dcx
# vs code / xdebug php extension + devsense php extension

CONSOLE = Console()

home = os.getenv("HOME")

OP=os.path.join(home, "_kicksu")
OD=os.makedirs(OP, exist_ok=True)

def tryversion(pkg):
    import importlib.metadata
    try:
        res = pkg + '-' + importlib.metadata.version(pkg)
    except:
        res = pkg + '-dev'
    return res


t = Table(title=tryversion("kicksu"))
t.add_column("#")
t.add_column("File")
t.add_row("pfc", "preflightcheck")
t.add_row("1", "docker")
t.add_section()
t.add_row("q", "QUIT")

while True:
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print("")
    CONSOLE.print(t)

    x = CONSOLE.print()
    x = CONSOLE.input(' (q=QUIT) # ')

    if x == "pfc": # preflightcheck
        pfc_list_macos = [
            'chrome',
            'thunderbird',
            'macos'
        ]

        if IS_MACOS:
            input("Press RETURN to open Chrome's Update Page...")
            subprocess.call("""open -a 'Google Chrome.app' 'chrome://settings/help' """, shell=True)
            input("Press RETURN when checking with Chrome is done...")
            input("Press RETURN to open Firefox's Update Page...")
            subprocess.call("""open -a 'Firefox.app' 'chrome://browser/content/aboutDialog.xhtml' """, shell=True)
            input("Press RETURN when checking with Firefox is done...")

    if x == "1": # docker

        if IS_MACOS:
            outfile = os.path.join(OP, "Docker.dmg")
            cmd = 'curl -C - -L -o "%s" "https://desktop.docker.com/mac/main/arm64/Docker.dmg"' % outfile
            subprocess.call(cmd, shell=True)
            run_confirm = CONSOLE.input('run it? type "run" to execute or anything else to exit # ')
            if run_confirm == "run" or run_confirm == "r":
                subprocess.call("open %s" % outfile, shell=True)

    if x == "q":
        CONSOLE.print("")
        CONSOLE.print("")
        CONSOLE.print("Quit.")
        break
