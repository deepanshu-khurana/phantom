# Phantom ⚔️

**Phantom** is a Cross-Platform lightweight cybersecurity toolkit designed for reconnaissance and situational awareness. It features a custom interactive shell that reacts to your commands.

> **Author**: Deepanshu Khurana

## Features

### 👻 Wraith (Web Reconnaissance)
A suite of tools to analyze web targets:
-   **Arachnid**: Spider/Crawler to map internal links.
-   **Vortex**: Discovers potential API endpoints (`/api/v1`, `/graphql`, etc.).
-   **Hunter**: Scans for accidentally leaked secrets (API keys, tokens).
-   **Droid**: Parses `robots.txt` for sensitive paths.

### 📶 Spectral (WiFi Scanner)
Passively scans for local wireless networks (SSID, Signal, Channel, Security).

## Platform Limitations
-   **WSL (Windows Subsystem for Linux)**: The `wifi` command relies on hardware access. Since WSL is a virtual machine, it cannot access the host's WiFi adapter directly. For WiFi scanning, please use **Windows Native** (PowerShell/CMD) or a standard Linux installation.
-   **Linux**: Requires `nmcli` (NetworkManager) to be installed.

## Installation

### Prerequisites
-   Python 3.8+
-   `pip`

### Setup
Clone the repository and install the package:

```bash
git clone https://github.com/deepanshu-khurana/phantom.git
cd phantom
pip install .
```

## Usage

### 1. Interactive Phantom Shell
Launch the immersive environment:

```bash
phantom
```
*   **Startup**: The "Heavy Sword" initializes (Sheathed).
*   **Commands**: Type `wifi` or `analyze` to unsheathe the blade.

### 2. Command Line (CLI) Examples

**Test Case 1: Web Analysis**
Run a complete audit on a target:
```bash
ghost@phantom:~$ analyze https://google.com -spider
Expected Output: The Sword will **Unsheathe** (Open Blade). The tool will run Spectrum and Arachnid modules sequentially.

____   _   _    _    _   _     ||       ___  __  __
|  _ \| | | |  / \  | \ | | ========   / _ \|  \/  |
| |_) | |_| | / _ \ |  \| |   |||     | | | | |\/| |
|  __/|  _  |/ ___ \| |\  |   |||     | |_| | |  | |
|_|   |_| |_/_/   \_\_| \_|   |||      \___/|_|  |_|
                               V

=== Wraith Protocol Initiated: https://google.com ===
[*] Fetching target...

=== Spectrum Analysis (Headers) ===
[!] CRITICAL: Missing HSTS (MITM Risk)
[!] CRITICAL: Missing CSP (XSS Risk)
  > X-Frame-Options: Present
[!] CRITICAL: Missing MIME Sniffing Protection
  > Server Technology: gws

=== Arachnid Module (Spider) ===
  > Internal Links Found: 6
  > Internal Links Found: 6
  - https://google.com/intl/en/ads/
  - https://google.com/intl/en/policies/terms/
  - https://google.com/intl/en/policies/privacy/
  - https://google.com/preferences?hl=en
  - https://google.com/intl/en/about.html
  - https://google.com/advanced_search?hl=en-IN&authuser=0
```

**Test Case 2: WiFi Scan**
Scan for local networks:
```bash
phantom wifi
Expected Output: The Sword will Unsheathe. A list of available WiFi networks (SSID, Signal, Channel, Security) will be displayed.
____   _   _    _    _   _     ||       ___  __  __
|  _ \| | | |  / \  | \ | | ========   / _ \|  \/  |
| |_) | |_| | / _ \ |  \| |   |||     | | | | |\/| |
|  __/|  _  |/ ___ \| |\  |   |||     | |_| | |  | |
|_|   |_| |_/_/   \_\_| \_|   |||      \___/|_|  |_|
                               V
=== Spectral Protocol Initiated: WiFi Scan ===
[WIFI] Khurana265_5G        MAC: 20:0c:86:b5:df:69 | Sig: 87%% | Ch: 60 | WPA2-Personal
```
## Development

1.  **Clone the repo**: `git clone ...`
2.  **Install dependencies**: `pip install -r requirements.txt`
3.  **Run locally**: `python -m phantom.main`

## Contributing
Contributions are welcome!
1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## Security and Legal
**Disclaimer**: Phantom is designed for **educational purposes and authorized security testing only**.
*   Do not use this tool against targets you do not have explicit permission to test.
*   The author (Deepanshu Khurana) is not responsible for any misuse or damage caused by this tool.
*   Always adhere to local laws and regulations regarding cybersecurity and network scanning.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


