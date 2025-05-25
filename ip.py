import requests
import json
from colorama import Fore, Style

# Developer Credits
DEVELOPER = "@ERROR0101r"
VERSION = "v2.0"

def print_banner():
    print(Fore.CYAN + f"""
    ███████╗██╗  ██╗██████╗ ██╗   ██╗███████╗
    ██╔════╝╚██╗██╔╝██╔══██╗██║   ██║██╔════╝
    █████╗   ╚███╔╝ ██████╔╝██║   ██║███████╗
    ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║╚════██║
    ███████╗██╔╝ ██╗██║     ╚██████╔╝███████║
    ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝
    """)
    print(Fore.YELLOW + f"🛠️ IP Intelligence Tool {VERSION}")
    print(Fore.MAGENTA + f"👨‍💻 Developed by {DEVELOPER}\n" + Style.RESET_ALL)

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719")
        data = response.json()
        
        if data["status"] == "success":
            print(Fore.GREEN + "\n🔍 [SUCCESS] IP Information Found:" + Style.RESET_ALL)
            print(Fore.BLUE + "="*50 + Style.RESET_ALL)
            print(Fore.CYAN + f"🌐 {Fore.WHITE}IP Address: {Fore.GREEN}{data['query']}")
            print(Fore.CYAN + f"🏢 {Fore.WHITE}ISP: {Fore.GREEN}{data['isp']}")
            print(Fore.CYAN + f"🏛️ {Fore.WHITE}Organization: {Fore.GREEN}{data['org']}")
            print(Fore.CYAN + f"🆔 {Fore.WHITE}ASN: {Fore.GREEN}{data['as']}")
            print(Fore.CYAN + f"🌍 {Fore.WHITE}Country: {Fore.GREEN}{data['country']} ({data['countryCode']})")
            print(Fore.CYAN + f"📍 {Fore.WHITE}Region: {Fore.GREEN}{data['regionName']} ({data['region']})")
            print(Fore.CYAN + f"🏙️ {Fore.WHITE}City: {Fore.GREEN}{data['city']}")
            print(Fore.CYAN + f"📮 {Fore.WHITE}ZIP Code: {Fore.GREEN}{data['zip']}")
            print(Fore.CYAN + f"⏰ {Fore.WHITE}Timezone: {Fore.GREEN}{data['timezone']}")
            print(Fore.CYAN + f"🧭 {Fore.WHITE}Coordinates: {Fore.GREEN}Lat {data['lat']}, Lon {data['lon']}")
            print(Fore.CYAN + f"🔗 {Fore.WHITE}Reverse DNS: {Fore.GREEN}{data['reverse']}")
            print(Fore.CYAN + f"📱 {Fore.WHITE}Mobile: {Fore.GREEN}{'Yes' if data['mobile'] else 'No'}")
            print(Fore.CYAN + f"🛡️ {Fore.WHITE}Proxy/VPN: {Fore.RED if data['proxy'] else Fore.GREEN}{'Yes' if data['proxy'] else 'No'}")
            print(Fore.BLUE + "="*50 + Style.RESET_ALL)
        else:
            print(Fore.RED + f"\n❌ [ERROR] {data['message']}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n⚡ [ERROR] API Error: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    print_banner()
    print(Fore.YELLOW + "💡 Tip: Press Enter to check your own IP" + Style.RESET_ALL)
    ip = input(Fore.MAGENTA + "\n🔎 Enter IP Address: " + Style.RESET_ALL).strip()
    
    if not ip:
        try:
            ip = requests.get("https://api.ipify.org").text
            print(Fore.GREEN + f"\n🔄 Detected Public IP: {ip}" + Style.RESET_ALL)
        except:
            print(Fore.RED + "\n⚡ Failed to fetch your IP. Try manually." + Style.RESET_ALL)
            exit(1)
    
    get_ip_info(ip)
    print(Fore.CYAN + f"\n✨ Thank you for using IP Lookup Tool by {DEVELOPER}" + Style.RESET_ALL)