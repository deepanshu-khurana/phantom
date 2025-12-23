import requests
import re
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from phantom.utils.ui import PhantomUI

class WraithAnalyzer:
    def __init__(self):
        # Load Data
        base_dir = os.path.dirname(os.path.dirname(__file__))
        
        cve_path = os.path.join(base_dir, 'data', 'cve_db.json')
        with open(cve_path, 'r') as f:
            self.cve_db = json.load(f)
            
        secrets_path = os.path.join(base_dir, 'data', 'secrets_patterns.json')
        with open(secrets_path, 'r') as f:
            self.secrets_db = json.load(f)

    def analyze(self, url, flags):
        PhantomUI.section(f"Wraith Protocol Initiated: {url}")
        
        try:
            # 1. Core / Spectrum (Always Run)
            PhantomUI.info("Fetching target...")
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            self._scan_spectrum(res)
            
            # 2. Arachnid (Spider)
            if flags.get('spider') or flags.get('complete'):
                self._scan_arachnid(url, soup)
                
            # 3. Vortex (API)
            if flags.get('vortex') or flags.get('complete'):
                self._scan_vortex(soup)
                
            # 4. Hunter (Secrets)
            if flags.get('hunter') or flags.get('complete'):
                self._scan_hunter(res.text)

            # 5. Droid (Robots.txt)
            if flags.get('droid') or flags.get('complete'):
                self._scan_droid(url)

        except Exception as e:
            PhantomUI.alert(f"Connection Failed: {e}")

    def _scan_spectrum(self, res):
        """Standard Header & Tech Analysis"""
        PhantomUI.section("Spectrum Analysis (Headers)")
        
        headers = res.headers
        
        # Security Headers Check
        security_headers = {
            'Strict-Transport-Security': 'Missing HSTS (MITM Risk)',
            'Content-Security-Policy': 'Missing CSP (XSS Risk)',
            'X-Frame-Options': 'Missing X-Frame-Options (Clickjacking Risk)',
            'X-Content-Type-Options': 'Missing MIME Sniffing Protection'
        }
        
        for header, alert_msg in security_headers.items():
            if header not in headers:
                PhantomUI.alert(alert_msg)
            else:
                PhantomUI.data(header, "Present")

        # Server Fingerprinting & CVEs
        server = headers.get('Server', 'Unknown')
        PhantomUI.data("Server Technology", server)
        
        # Simple string match for CVE lookup
        for software, cves in self.cve_db.items():
            if software in server:
                for cve in cves:
                    PhantomUI.alert(f"VULNERABILITY DETECTED: {cve}")

    def _scan_arachnid(self, base_url, soup):
        """Spider: Find Internal Links"""
        PhantomUI.section("Arachnid Module (Spider)")
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            # Only internal links
            if base_url in full_url:
                links.add(full_url)
        
        PhantomUI.data("Internal Links Found", len(links))
        count = 0
        for link in links:
            if count < 5: # Limit output
                print(f"  {PhantomUI.DATA_WHITE}- {link}{PhantomUI.RESET}")
            count += 1
        if count > 5:
            print(f"  {PhantomUI.DATA_WHITE}...and {count-5} more.{PhantomUI.RESET}")

    def _scan_vortex(self, soup):
        """API Discovery"""
        PhantomUI.section("Vortex Module (API Discovery)")
        input_string = str(soup)
        
        # Regex patterns for API endpoints
        patterns = [
            r'/api/v\d+/',
            r'/graphql',
            r'/swagger',
            r'\.json'
        ]
        
        found = False
        for pattern in patterns:
            matches = re.findall(pattern, input_string)
            if matches:
                found = True
                unique_matches = set(matches)
                for m in unique_matches:
                     PhantomUI.data("API Endpoint Potential", m)
        
        if not found:
            PhantomUI.info("No obvious API endpoints found in HTML.")

    def _scan_hunter(self, text):
        """Secrets Scanner"""
        PhantomUI.section("Hunter Module (Secrets)")
        found = False
        for name, pattern in self.secrets_db.items():
            matches = re.findall(pattern, text)
            if matches:
                found = True
                PhantomUI.alert(f"POTENTIAL LEAK: {name}")
                # Print first match (truncated for safety)
                masked = matches[0][:4] + "..."
                print(f"    Match: {masked}")
        
        if not found:
            PhantomUI.info("No hardcoded secrets found in response text.")

    def _scan_droid(self, base_url):
        """Robots.txt Analysis"""
        PhantomUI.section("Droid Module (Robots.txt)")
        parsed = urlparse(base_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        try:
            res = requests.get(robots_url, timeout=5)
            if res.status_code == 200:
                PhantomUI.info(f"Found robots.txt at {robots_url}")
                for line in res.text.splitlines():
                    if "Disallow" in line:
                         PhantomUI.data("Disallowed Path", line.split(': ')[1].strip())
            else:
                PhantomUI.info("No robots.txt found (404).")
        except:
            PhantomUI.info("Could not fetch robots.txt")
