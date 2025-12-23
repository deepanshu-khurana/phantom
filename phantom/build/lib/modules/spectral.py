import subprocess
import platform
import shutil
from phantom.utils.ui import PhantomUI

class SpectralScanner:
    def scan(self):
        PhantomUI.section("Spectral Protocol Initiated: WiFi Scan")
        
        os_type = platform.system()
        
        if os_type == "Windows":
            self._scan_windows()
        elif os_type == "Linux":
            self._scan_linux()
        else:
            PhantomUI.alert(f"Unsupported OS: {os_type}")

    def _scan_windows(self):
        try:
            # We use 'netsh wlan show networks mode=bssid' to see all neighbors
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                capture_output=True,
                text=True,
                check=True
            )
            self._parse_netsh(result.stdout)
            
        except subprocess.CalledProcessError:
             PhantomUI.alert("Failed to execute WiFi scan.")
        except Exception as e:
             PhantomUI.alert(f"Spectral Error: {e}")

    def _scan_linux(self):
        # Check for nmcli
        if not shutil.which("nmcli"):
            PhantomUI.alert("nmcli (NetworkManager) not found. Cannot scan.")
            return

        try:
            # -t: Terse (colon separated)
            # -f: Fields
            cmd = ['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL,SECURITY,CHAN,FREQ', 'dev', 'wifi']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')
            found = False
            
            for line in lines:
                if not line: continue
                # SSID:BSSID:SIGNAL:SECURITY:CHAN:FREQ
                # NOTE: SSID might contain colons, but usually nmcli escapes or handles it.
                # simpler split for now.
                parts = line.split(':')
                # We expect at least 6 parts, but SSID could have colons. 
                # nmcli terse mode usually escapes colons with backslash.
                # For robust parsing we'd need a complex regex. 
                # For this MVP, let's assume standard SSIDs or grab from back.
                
                # However, nmcli output is strictly ordered by fields.
                # If we assume SSID is parts[0], BSSID is parts[1]... this fails if SSID has colon.
                # Proper way: nmcli escapes ':' as '\:'.
                
                # Let's try to map generic columns.
                # If we assume BSSID format xx:xx:xx:xx:xx:xx (5 colons).
                
                # Let's just do a simple split and hope. Or use a cleaner library?
                # No external libs allowed besides requirements.txt.
                
                # Let's rely on standard split for now.
                # SSID, BSSID, SIGNAL, SECURITY, CHAN, FREQ
                
                # BSSID is index 1? No, SSID is index 0.
                
                # A trick: use different delimiter if possible? nmcli doesn't support custom delim easily in -t mode.
                # Actually, we can just print it raw? No, we need UI formatting.
                
                # Let's assume SSID is everything before the BSSID pattern?
                # BSSID is 17 chars long usually.
                
                # Let's keep it simple:
                # parts[0] = SSID
                # ...
                
                # Re-constructing based on fields requested: SSID,BSSID,SIGNAL,SECURITY,CHAN,FREQ
                # But BSSID itself has colons! 00:11:22...
                # So splitting by ':' is dangerous for BSSID.
                
                # Better approach: Don't use -t. Use table and fixed width? Hard to parse.
                # Better: nmcli -g (get) ?
                
                # Alternative: iwlist? "sudo iwlist scan" -> needs sudo.
                
                # Let's stick to nmcli but be careful.
                # In terse mode, BSSID colons are escaped as \:
                # wait, really? Let's check docs. 
                # "Colons in values are escaped with backslash"
                
                # So we can split by `(?<!\\):` (negative lookbehind)
                
                import re
                # pattern: colon not preceded by backslash
                parts = re.split(r'(?<!\\):', line)
                
                # Unescape parts
                parts = [p.replace(r'\:', ':') for p in parts]
                
                if len(parts) >= 6:
                    ssid = parts[0]
                    bssid = parts[1]
                    sig = parts[2]
                    sec = parts[3]
                    chan = parts[4]
                    freq = parts[5] # Band hint
                    
                    band = "2.4GHz" if freq.startswith("2") else "5GHz" if freq.startswith("5") else freq
                    
                    PhantomUI.wifi_entry(ssid, bssid, sig, sec, chan, band)
                    found = True
            
            if not found:
                PhantomUI.info("No networks found.")

        except Exception as e:
            PhantomUI.alert(f"Linux Scan Error: {e}")

    def _parse_netsh(self, output):
        """
        Parses the raw text output from netsh into structured data.
        Buffering approach to handle field ordering.
        """
        lines = output.split('\n')
        
        # State
        current_ssid = "Unknown"
        current_auth = "Unknown" # Auth is usually per SSID in netsh output
        
        # Pending BSSID data
        pending_entry = None

        def flush():
            nonlocal pending_entry
            if pending_entry:
                # We have a BSSID to print
                PhantomUI.wifi_entry(
                   ssid=pending_entry.get('ssid', 'Unknown'),
                   bssid=pending_entry.get('bssid', 'Unknown'),
                   signal=pending_entry.get('signal', '?'),
                   security=pending_entry.get('auth', 'Unknown'),
                   channel=pending_entry.get('channel', '?'),
                   band=pending_entry.get('band', '?')
                )
                pending_entry = None
                return True
            return False

        found_any = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("SSID"):
                # New SSID block implies end of previous BSSIDs
                if flush(): found_any = True
                
                parts = line.split(":", 1)
                if len(parts) > 1:
                    val = parts[1].strip()
                    if val:
                        current_ssid = val
                    else:
                        current_ssid = "Hidden Network"
                current_auth = "Unknown" # Reset until found

            elif line.startswith("Authentication"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_auth = parts[1].strip()
                    # If we have a pending entry that belongs to this SSID (rare in netsh structure, 
                    # usually Auth is above BSSID), update it.
                    # Actually Auth is under SSID, BSSID is under SSID. 
                    # So Auth applies to all subsequent BSSIDs until new SSID.

            elif line.startswith("BSSID"):
                # New BSSID block
                if flush(): found_any = True
                
                parts = line.split(":", 1)
                if len(parts) > 1:
                    bssid_val = parts[1].strip()
                else:
                    bssid_val = "Unknown"
                
                # Start new entry
                pending_entry = {
                    'ssid': current_ssid,
                    'auth': current_auth,
                    'bssid': bssid_val,
                    'channel': '?',
                    'band': '?',
                    'signal': '?'
                }

            elif line.startswith("Signal"):
                parts = line.split(":", 1)
                if len(parts) > 1 and pending_entry:
                    pending_entry['signal'] = parts[1].strip()

            elif line.startswith("Channel") and "Utilization" not in line:
                parts = line.split(":", 1)
                if len(parts) > 1 and pending_entry:
                    pending_entry['channel'] = parts[1].strip()

            elif line.startswith("Radio type"):
                 parts = line.split(":", 1)
                 if len(parts) > 1 and pending_entry:
                    pending_entry['band'] = parts[1].strip()
        
        # Final flush
        if flush(): found_any = True

        if not found_any:
            PhantomUI.info("No networks found. Ensure WiFi is enabled.")
