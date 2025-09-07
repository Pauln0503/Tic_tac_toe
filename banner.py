from rich.console import Console
import pyfiglet
import shutil
console = Console()

def print_banner():

    ascii_banner = pyfiglet.figlet_format("TIC_TAC_TOE", font="slant")
    lines = ascii_banner.splitlines()
    columns, _ = shutil.get_terminal_size()

    for line in lines:
        console.print(line.center(columns), style="bold green")

    by_line = "By Paul Ngo"
    console.print(by_line.center(columns), style="bold yellow")
