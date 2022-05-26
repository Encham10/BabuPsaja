from datetime import datetime
from colorama import init, Fore, Style
init(autoreset=True)

def Console(str : str, about : str):
    time = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    print(Style.BRIGHT + Fore.CYAN + time + Fore.YELLOW + f" {str}:" + f" {about}")

def ConsoleERR(about : str):
    time = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    print(Style.BRIGHT + Fore.CYAN + time + Fore.RED + f" ERR:" + f" {about}")

def Console_Sepator():
    time = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
    print(Style.BRIGHT + Fore.CYAN + time + "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")