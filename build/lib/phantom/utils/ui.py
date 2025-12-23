import sys
import time
import random
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

class PhantomUI:
    # Color Palette
    NEON_GREEN = Fore.GREEN + Style.BRIGHT
    NEON_PURPLE = Fore.MAGENTA + Style.BRIGHT
    NEON_YELLOW = Fore.YELLOW + Style.BRIGHT # Brown-ish
    ALERT_RED = Fore.RED + Style.BRIGHT
    DATA_WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

    @staticmethod
    def _print_sword_frame(stage="sheathed"):
        """
        Helper to print the sword in various stages.
        """
        # Colors
        g = PhantomUI.NEON_GREEN
        p = PhantomUI.NEON_PURPLE
        w = PhantomUI.DATA_WHITE
        b = PhantomUI.NEON_YELLOW # Handle & Sheath
        r = PhantomUI.RESET

        # Banner Letters (P H A N) - 5 Lines + 1 Empty
        l1 = r" ____  _   _    _    _   _ "
        l2 = r"|  _ \| | | |  / \  | \ | |"
        l3 = r"| |_) | |_| | / _ \ |  \| |"
        l4 = r"|  __/|  _  |/ ___ \| |\  |"
        l5 = r"|_|   |_| |_/_/   \_\_| \_|"
        l6 = r"                           " # Spacer for sword tip line

        # O M (Right side) - 5 Lines + 1 Empty
        # Shifted slightly to accommodate wider sword/guard
        o1 = r"   ___  __  __ "
        o2 = r"  / _ \|  \/  |"
        o3 = r" | | | | |\/| |"
        o4 = r" | |_| | |  | |"
        o5 = r"  \___/|_|  |_|"
        o6 = r"               "

        # Sword Components
        # Handle: Brown ||
        # Guard: Purple ===||=== (6 equals total)
        # Blade: White |||
        # Sheath: Brown |||
        
        # Line 1: Handle
        s1 = f"{b}    ||    {r}"
        
        # Line 2: Guard (Solid equals)
        s2 = f"{p} ======== {r}" 

        # Blade Body (Lines 3, 4, 5) + Tip (Line 6)
        if stage == "sheathed":
            # Solid Purple Sheath (|||) - High Contrast
            s3_sub = "   |||    "
            s3_col = p
            s4_sub = "   |||    "
            s4_col = p
            s5_sub = "   |||    " 
            s5_col = p
            tip_sub = "    V     "
            tip_col = p
        
        elif stage == "drawing_1":
            # Partially drawn
            s3_sub = "   |||    "
            s3_col = w # Revealed
            s4_sub = "   |||    "
            s4_col = w # Revealed (faster draw)
            s5_sub = "   |||    "
            s5_col = p # Covered
            tip_sub = "    V     "
            tip_col = p
        
        else: # Full (Uncovered)
            s3_sub = "   |||    "
            s3_col = w
            s4_sub = "   |||    "
            s4_col = w
            s5_sub = "   |||    "
            s5_col = w
            tip_sub = "    V     "
            tip_col = w

        s3 = f"{s3_col}{s3_sub}{r}"
        s4 = f"{s4_col}{s4_sub}{r}"
        s5 = f"{s5_col}{s5_sub}{r}"
        s6 = f"{tip_col}{tip_sub}{r}"

        # Clear Screen (ANSI)
        print("\033[H\033[J", end="")
        
        # Print Lines
        print(f"{g}{l1}{s1}{g}{o1}{r}")
        print(f"{g}{l2}{s2}{g}{o2}{r}")
        print(f"{g}{l3}{s3}{g}{o3}{r}")
        print(f"{g}{l4}{s4}{g}{o4}{r}")
        print(f"{g}{l5}{s5}{g}{o5}{r}")
        print(f"{l6}{s6}{o6}") # Line 6 (Tip)
        print("\n")

    @staticmethod
    def animate_unsheathe():
        """
        Animates the sword Unsheathing (Purple -> White).
        """
        frames = ["sheathed", "drawing_1", "full"]
        for stage in frames:
            PhantomUI._print_sword_frame(stage)
            time.sleep(0.4) # Slower
        time.sleep(0.2)
    
    @staticmethod
    def show_sheathed():
        PhantomUI._print_sword_frame("sheathed")

    @staticmethod
    def show_unsheathed():
        PhantomUI._print_sword_frame("full")

    @staticmethod
    def banner():
        PhantomUI.show_sheathed()

    @staticmethod
    def animate_sheathe():
        """
        Animates the sword Sheathing (White -> Purple).
        """
        frames = ["full", "drawing_1", "sheathed"]
        for stage in frames:
            PhantomUI._print_sword_frame(stage)
            time.sleep(0.4) # Slower
    
    @staticmethod
    def typewriter(text, color=None, speed=0.01):
        if color:
            sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write(PhantomUI.RESET + "\n")

    @staticmethod
    def alert(msg):
        print(f"{PhantomUI.ALERT_RED}[!] CRITICAL: {msg}{PhantomUI.RESET}")

    @staticmethod
    def info(msg):
        print(f"{PhantomUI.NEON_GREEN}[*] {msg}{PhantomUI.RESET}")
    
    @staticmethod
    def data(label, value):
        print(f"{PhantomUI.NEON_GREEN}  > {label}: {PhantomUI.DATA_WHITE}{value}{PhantomUI.RESET}")

    @staticmethod
    def wifi_entry(ssid, bssid, signal, security, channel="?", band="?"):
        sec_color = PhantomUI.DATA_WHITE
        if "Open" in security or "WEP" in security:
            sec_color = PhantomUI.ALERT_RED
        
        # Clean channel/band if unknown
        details = f"MAC: {bssid} | Sig: {signal}% | Ch: {channel} | {sec_color}{security}{PhantomUI.RESET}"
        print(f"{PhantomUI.NEON_PURPLE}[WIFI] {ssid:<20} {PhantomUI.DATA_WHITE}{details}")

    @staticmethod
    def section(title):
        print(f"\n{PhantomUI.NEON_PURPLE}=== {title} ==={PhantomUI.RESET}")
