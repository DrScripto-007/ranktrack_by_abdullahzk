import sys
import time
import pyfiglet
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.05)
    print()

def good_night_message():
    # Clear screen (optional, improves effect)
    print("\033[H\033[J") 
    
    # Create ASCII art
    ascii_art = pyfiglet.figlet_format("Good Night", font="starwars")
    ascii_name = pyfiglet.figlet_format("Brother Saim", font="slant")

    # Print the "Good Night" part in Cyan
    print(Fore.CYAN + Style.BRIGHT + ascii_art)
    time.sleep(0.5)
    
    # Print the Name part in Yellow
    print(Fore.YELLOW + Style.BRIGHT + ascii_name)
    time.sleep(0.5)

    # Print a sweet sub-message slowly
    print(Fore.MAGENTA + "-" * 50)
    print_slow(Fore.WHITE + "   Rest well and dream big. See you tomorrow! 🌙 ✨")
    print(Fore.MAGENTA + "-" * 50)

if __name__ == "__main__":
    good_night_message()
