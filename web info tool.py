import requests
import socket
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import Fore, Style, init
import pyfiglet
import ssl
import re

# Initialize colorama
init(autoreset=True)

def get_website_info(url):
    """Fetch comprehensive information about a website"""
    try:
        # Ensure URL has proper scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # Get DNS information
        dns_info = {
            'A': [],
            'MX': [],
            'NS': []
        }
        try:
            dns_info['A'] = [str(r) for r in dns.resolver.resolve(domain, 'A')]
            dns_info['MX'] = [str(r) for r in dns.resolver.resolve(domain, 'MX')]
            dns_info['NS'] = [str(r) for r in dns.resolver.resolve(domain, 'NS')]
        except:
            pass

        # Get website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get SSL certificate info (alternative to WHOIS)
        ssl_info = get_ssl_info(domain)

        # Estimate capacity
        capacity = estimate_capacity(response, ssl_info)

        # Get title
        title = soup.title.string if soup.title else "No title found"

        # Get server info
        server = response.headers.get('Server', 'Not detected')

        return {
            'url': url,
            'domain': domain,
            'title': title,
            'server': server,
            'ip_addresses': dns_info['A'],
            'mx_records': dns_info['MX'],
            'name_servers': dns_info['NS'],
            'ssl': ssl_info,
            'capacity': capacity,
            'response_time': response.elapsed.total_seconds(),
            'status_code': response.status_code
        }
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return None

def get_ssl_info(domain):
    """Get basic SSL certificate information"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

                issuer = dict(x[0] for x in cert['issuer'])
                subject = dict(x[0] for x in cert['subject'])

                return {
                    'issuer': issuer.get('organizationName', 'Unknown'),
                    'valid_from': cert['notBefore'],
                    'valid_to': cert['notAfter'],
                    'subject': subject.get('commonName', domain)
                }
    except:
        return {
            'issuer': 'Unknown',
            'valid_from': 'Unknown',
            'valid_to': 'Unknown',
            'subject': 'Unknown'
        }

def estimate_capacity(response, ssl_info):
    """Estimate website capacity based on various factors"""
    try:
        server = response.headers.get('Server', '').lower()

        capacity = {
            'daily_visitors': 'Unknown',
            'hosting_type': 'Unknown',
            'capacity_level': 'Unknown'
        }

        # Check for common hosting providers in server headers
        if 'cloudflare' in server:
            capacity['hosting_type'] = 'Cloudflare (CDN)'
            capacity['capacity_level'] = 'High (Enterprise-grade)'
            capacity['daily_visitors'] = '100,000+'
        elif 'nginx' in server:
            capacity['hosting_type'] = 'NGINX (Likely VPS or Dedicated)'
            capacity['capacity_level'] = 'Medium to High'
            capacity['daily_visitors'] = '10,000-100,000'
        elif 'apache' in server:
            capacity['hosting_type'] = 'Apache (Shared or VPS)'
            capacity['capacity_level'] = 'Low to Medium'
            capacity['daily_visitors'] = '1,000-10,000'

        # Check SSL issuer for cloud providers
        issuer = ssl_info.get('issuer', '').lower()
        if 'amazon' in issuer:
            capacity['hosting_type'] = 'Amazon Web Services'
            capacity['capacity_level'] = 'High (Scalable)'
        elif 'google' in issuer:
            capacity['hosting_type'] = 'Google Cloud'
            capacity['capacity_level'] = 'High (Scalable)'
        elif 'microsoft' in issuer:
            capacity['hosting_type'] = 'Microsoft Azure'
            capacity['capacity_level'] = 'High (Scalable)'

        return capacity
    except:
        return {
            'daily_visitors': 'Unknown',
            'hosting_type': 'Unknown',
            'capacity_level': 'Unknown'
        }

def print_website_info(info):
    """Display website information with nice formatting"""
    if not info:
        print(f"{Fore.RED}❌ Failed to get website information{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🌐 Website Information{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

    # Basic Info
    print(f"\n{Fore.GREEN}📌 {Fore.BLUE}Basic Information:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}• Website Title:{Style.RESET_ALL} {info.get('title', 'N/A')}")
    print(f"  {Fore.MAGENTA}• URL:{Style.RESET_ALL} {info.get('url', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Domain:{Style.RESET_ALL} {info.get('domain', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Status Code:{Style.RESET_ALL} {info.get('status_code', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Response Time:{Style.RESET_ALL} {info.get('response_time', 'N/A')} seconds")

    # Server Info
    print(f"\n{Fore.GREEN}🖥️ {Fore.BLUE}Server Information:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}• Web Server:{Style.RESET_ALL} {info.get('server', 'N/A')}")
    print(f"  {Fore.MAGENTA}• IP Addresses:{Style.RESET_ALL}")
    for ip in info.get('ip_addresses', []):
        print(f"    - {ip}")

    # SSL Info
    print(f"\n{Fore.GREEN}🔒 {Fore.BLUE}SSL Certificate:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}• Issuer:{Style.RESET_ALL} {info['ssl'].get('issuer', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Valid From:{Style.RESET_ALL} {info['ssl'].get('valid_from', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Valid To:{Style.RESET_ALL} {info['ssl'].get('valid_to', 'N/A')}")

    # Capacity Info
    print(f"\n{Fore.GREEN}📊 {Fore.BLUE}Capacity Estimation:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}• Hosting Type:{Style.RESET_ALL} {info['capacity'].get('hosting_type', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Estimated Daily Visitors:{Style.RESET_ALL} {info['capacity'].get('daily_visitors', 'N/A')}")
    print(f"  {Fore.MAGENTA}• Capacity Level:{Style.RESET_ALL} {info['capacity'].get('capacity_level', 'N/A')}")

    # DNS Info
    print(f"\n{Fore.GREEN}🔗 {Fore.BLUE}DNS Information:{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}• Name Servers:{Style.RESET_ALL}")
    for ns in info.get('name_servers', []):
        print(f"    - {ns}")

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

def main():
    """Main function"""
    # Display fancy title
    try:
        title = pyfiglet.figlet_format("Website Info", font="slant")
        print(f"{Fore.BLUE}{title}{Style.RESET_ALL}")
    except:
        print(f"{Fore.BLUE}=== Website Information Tool ==={Style.RESET_ALL}")

    print(f"{Fore.YELLOW}🔍 Enter a website URL to get detailed information (or 'quit' to exit){Style.RESET_ALL}")

    while True:
        url = input(f"\n{Fore.GREEN}🌐 Enter Website URL (e.g., example.com): {Style.RESET_ALL}").strip()

        if url.lower() in ['quit', 'exit', 'q']:
            print(f"{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
            break

        if not url:
            print(f"{Fore.RED}❌ Please enter a URL{Style.RESET_ALL}")
            continue

        print(f"\n{Fore.YELLOW}⏳ Fetching information for {url}...{Style.RESET_ALL}")
        website_info = get_website_info(url)
        print_website_info(website_info)

if __name__ == "__main__":
    main()