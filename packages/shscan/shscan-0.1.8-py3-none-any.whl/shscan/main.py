import sys
import requests
from requests.exceptions import RequestException
from shscan import main

def get_security_headers(url, ssl=False, cookies=None):
    try:
        if ssl:
            response = requests.get(url, allow_redirects=True, timeout=5, verify=True, cookies=cookies)
        else:
            response = requests.get(url, allow_redirects=True, timeout=5, verify=False, cookies=cookies)
        security_headers = {
             'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
             'Strict-Transport-Security': response.headers.get('Strict-Transport-Security'),
             'Referrer-Policy': response.headers.get('Referrer-Policy'),
             'Feature-Policy': response.headers.get('Feature-Policy'),
             'Permissions-Policy': response.headers.get('Permissions-Policy'),
             'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
             'X-Frame-Options': response.headers.get('X-Frame-Options'),
             'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
             'X-Download-Options': response.headers.get('X-Download-Options'),
             'X-Content-Security-Policy': response.headers.get('X-Content-Security-Policy'),
             'Content-Security-Policy-Report-Only': response.headers.get('Content-Security-Policy-Report-Only'),
             'Clear-Site-Data': response.headers.get('Clear-Site-Data'),
             'Cross-Origin-Embedder-Policy': response.headers.get('Cross-Origin-Embedder-Policy'),
             'Cross-Origin-Opener-Policy': response.headers.get('Cross-Origin-Opener-Policy'),
             'Cross-Origin-Resource-Policy': response.headers.get('Cross-Origin-Resource-Policy'),
             'X-Webkit-CSP': response.headers.get('X-Webkit-CSP'),

        }
        return security_headers
    except RequestException as e:
        print(f"Error requesting {url}: {e}")
        return {}

def display_menu(title, url):

    title_length = len(title) + 2
    url_length = len(url) + 2
    border_length = max(title_length, url_length) + 4
    border = "==" * border_length
    print(f"\n{border}\n {title:^{border_length}} \n")
    print(f" URL: {url:^{border_length}} \n")
    print(border + "\n")

def help_menu():

    print("Usage: python SHScan.py <URL> [-ssl]")
    print("\nOptions:")
    print("  -ssl: Test the URL with SSL enabled.")
    print("  No options: Test the URL without SSL and without cookies.")

def main():
    if len(sys.argv) < 2:
        help_menu()
        sys.exit(1)

    url = sys.argv[1]
    ssl = False

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "-ssl":
            ssl = True
        else:
            help_menu()
            sys.exit(1)
        i += 1

    headers = get_security_headers(url, ssl)

    if headers:
        display_menu("SECURITY HEADERS", url)
        print(f"Security for {url}\n")
        for header, value in headers.items():
            emoji_verde = '\033[32m\U0001F197\033[0m |'
            emoji_vermelho = '\033[31m\u274C\033[0m |'
            print(f"{emoji_verde} {header}:" if value else f"{emoji_vermelho} {header}:", f"{value}" if value is not None else "")

if __name__ == "__main__":
    main()