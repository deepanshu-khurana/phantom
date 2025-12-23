import argparse
import sys
import time
from phantom.utils.ui import PhantomUI
from phantom.modules.wraith import WraithAnalyzer
from phantom.modules.spectral import SpectralScanner

def interactive_mode():
    # Startup: Show Sheathed Sword (Covered)
    PhantomUI.show_sheathed()
    print(f"{PhantomUI.NEON_PURPLE}[+] System Online...{PhantomUI.RESET}")
    print("Welcome to the Phantom Shell.")
    
    # State tracking
    is_unsheathed = False

    while True:
        try:
            cmd_input = input(f"{PhantomUI.NEON_GREEN}ghost@phantom:~${PhantomUI.RESET} ").strip()
            
            if not cmd_input:
                continue

            parts = cmd_input.split()
            cmd = parts[0].lower()
            
            if cmd == "exit" or cmd == "quit":
                if is_unsheathed:
                    PhantomUI.animate_sheathe()
                print(f"{PhantomUI.ALERT_RED}Terminating session...{PhantomUI.RESET}")
                break
            
            elif cmd == "help":
                print("\nAvailable Commands:")
                # Detailed help as requested
                print("  analyze <url> [flags]    : Web Reconnaissance Module")
                print("    -spider                : Spider/Crawler - recursively finds internal links (max depth 2)")
                print("    -vortex                : API Discovery - scans HTML/JS for patterns like /api/v1, /graphql")
                print("    -hunter                : Secrets Scanner - looks for accidentally leaked keys/tokens")
                print("    -droid                 : Robots.txt Analyzer - parses for Disallow entries")
                print("    -complete              : FULL AUDIT - Executes all modules sequentially")
                print("")
                print("  wifi                     : WiFi Spectral Scanner")
                print("                             Passive scan of local wireless networks.")
                print("                             Displays SSID, Signal, Channel, Band, and Security.")
                print("")
                print("  clear                    : Reset screen")
                print("  exit                     : Terminate session")
                print("\n")

            elif cmd == "wifi":
                if not is_unsheathed:
                    PhantomUI.animate_unsheathe()
                    is_unsheathed = True
                
                print("")
                tool = SpectralScanner()
                tool.scan()
            
            elif cmd == "analyze":
                if len(parts) < 2:
                    PhantomUI.alert("Usage: analyze <url> [flags]")
                    continue
                
                if not is_unsheathed:
                    PhantomUI.animate_unsheathe()
                    is_unsheathed = True
                
                url = parts[1]
                flags = {
                    'spider': '-spider' in parts or '-complete' in parts,
                    'vortex': '-vortex' in parts or '-complete' in parts,
                    'hunter': '-hunter' in parts or '-complete' in parts,
                    'droid': '-droid' in parts or '-complete' in parts,
                    'complete': '-complete' in parts
                }
                
                tool = WraithAnalyzer()
                tool.analyze(url, flags)
                
            elif cmd == "clear":
                print("\033[H\033[J", end="")
                if is_unsheathed:
                    PhantomUI.show_unsheathed()
                else:
                    PhantomUI.show_sheathed()
            
            else:
                PhantomUI.alert(f"Unknown command: {cmd}")

        except KeyboardInterrupt:
            print("\nTerminating...")
            break

def main():
    parser = argparse.ArgumentParser(description="Phantom Security CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Analyze Command
    analyze_parser = subparsers.add_parser("analyze", help="Web Reconnaissance")
    analyze_parser.add_argument("url", help="Target URL")
    analyze_parser.add_argument("-spider", action="store_true", help="Run Arachnid Spider")
    analyze_parser.add_argument("-vortex", action="store_true", help="Run Vortex API Discovery")
    analyze_parser.add_argument("-hunter", action="store_true", help="Run Hunter Secret Scanner")
    analyze_parser.add_argument("-droid", action="store_true", help="Run Droid Robots.txt Analyzer")
    analyze_parser.add_argument("-complete", action="store_true", help="Run ALL modules")

    # WiFi Command
    wifi_parser = subparsers.add_parser("wifi", help="WiFi Sniffer")

    # If no arguments, run interactive
    if len(sys.argv) == 1:
        interactive_mode()
        return

    args = parser.parse_args()

    if args.command == "analyze":
        # Convert args to dict for the analyzer
        flags = {
            'spider': args.spider,
            'vortex': args.vortex,
            'hunter': args.hunter,
            'droid': args.droid,
            'complete': args.complete
        }
        
        # Show Unsheathed Sword for CLI commands
        PhantomUI.show_unsheathed()
        tool = WraithAnalyzer()
        tool.analyze(args.url, flags)

    elif args.command == "wifi":
        PhantomUI.show_unsheathed()
        tool = SpectralScanner()
        tool.scan()

def entry_point():
    """
    Entry point for the console script 'phantom'.
    """
    try:
        main()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
