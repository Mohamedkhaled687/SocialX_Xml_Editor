import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the ASCII art banner for the application."""
    banner = f"""
{Fore.CYAN}███████╗ ██████╗  ██████╗██╗ █████╗ ██╗           ██╗    ██╗  ██╗    ██╗  
██╔════╝██╔═══██╗██╔════╝██║██╔══██╗██║          ██╔╝    ╚██╗██╔╝    ╚██╗ 
███████╗██║   ██║██║     ██║███████║██║         ██╔╝      ╚███╔╝      ╚██╗
╚════██║██║   ██║██║     ██║██╔══██║██║         ╚██╗      ██╔██╗      ██╔╝
███████║╚██████╔╝╚██████╗██║██║  ██║███████╗     ╚██╗    ██╔╝ ██╗    ██╔╝{Style.RESET_ALL}
"""
    print(banner)

def launch_gui():
    """Launch the graphical user interface."""
    from gui import AppManager
    manager = AppManager()
    manager.run()

def launch_cli():
    """Launch the command-line interface with usage instructions."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Command-Line Interface (CLI) Mode{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}Available Commands:{Style.RESET_ALL}\n")
    
    commands_info = [
        ("verify", "Verify the structure of the XML file", 
         "python cli.py verify -i input.xml [-o output.xml] [-f]"),
        ("format", "Format the XML file to standard format",
         "python cli.py format -i input.xml [-o output.xml]"),
        ("json", "Transform XML file to JSON format",
         "python cli.py json -i input.xml [-o output.json]"),
        ("mini", "Strip spaces in XML file (minify)",
         "python cli.py mini -i input.xml [-o output.xml]"),
        ("compress", "Compress XML file",
         "python cli.py compress -i input.xml -o output.compressed"),
        ("decompress", "Decompress XML file",
         "python cli.py decompress -i input.compressed -o output.xml"),
    ]
    
    for cmd, desc, example in commands_info:
        print(f"  {Fore.GREEN}{cmd:<12}{Style.RESET_ALL} - {desc}")
        print(f"    {Fore.WHITE}Example: {example}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Note:{Style.RESET_ALL} Use 'python cli.py <command> --help' for detailed help on each command.\n")

def print_help():
    help_text = f"""
{Fore.YELLOW}{"SocialX: An XML Editor and Visualizer".center(60)}{Style.RESET_ALL}

{Fore.CYAN}Usage:{Style.RESET_ALL}
    Select the desired mode by entering the corresponding number.

{Fore.CYAN}Modes:{Style.RESET_ALL}
    {Fore.GREEN}1.{Style.RESET_ALL} GUI  - Launch the graphical user interface.
    {Fore.GREEN}2.{Style.RESET_ALL} CLI  - Launch the command-line interface.
    {Fore.GREEN}3.{Style.RESET_ALL} Help - Show this help information.
    {Fore.GREEN}4.{Style.RESET_ALL} Exit - Exit the application.

{Fore.CYAN}Instructions:{Style.RESET_ALL}
    - Enter the number corresponding to your choice and press Enter.
    - For example, enter '1' to launch the GUI.
"""
    print(help_text)

def app():
    print_banner()
    print_help()
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}Enter your choice (1/2/3/4): {Style.RESET_ALL}").strip()
            if choice == '1':
                print(f"{Fore.BLUE}Launching GUI...{Style.RESET_ALL}")
                launch_gui()
                break  # Exit after launching GUI
            elif choice == '2':
                print(f"{Fore.BLUE}Launching CLI...{Style.RESET_ALL}")
                launch_cli()
                break  # Exit after launching CLI
            elif choice == '3':
                print_help()
            elif choice == '4':
                print(f"{Fore.LIGHTRED_EX}Exiting application. Goodbye!{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2, 3, or 4.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTRED_EX}Exiting application. Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    app()