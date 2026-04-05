#!/usr/bin/env python3
import requests
import argparse
from urllib.parse import urljoin

default_dir = [
    "/admin", "/login", "/dashboard", "/wp-admin", "/administrator",
    "/backup", "/config", "/config.php", "/.env", "/phpinfo.php",
    "/images", "/uploads", "/files", "/assets", "/static",
    "/robots.txt", "/sitemap.xml", "/.git", "/.htaccess",
    "/server-status", "/api", "/v1", "/admin.php", "/panel", "/phpmyadmin"
]

def main():
    parser = argparse.ArgumentParser(description="Directory and file scanner ")
    parser.add_argument("url", help="Target URL (ex: http://example.com)")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist (one path per line)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout in seconds (default: 5)")
    args = parser.parse_args()

    base_url = args.url.rstrip('/')

    if args.wordlist:
        try:
            with open(args.wordlist, 'r', encoding='utf-8') as f:
                paths = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"[+] Usando wordlist: {args.wordlist} ({len(paths)} paths)")
        except FileNotFoundError:
            print(f"[!] Wordlist '{args.wordlist}' não encontrada!")
            return
    else:
        paths = default_dir
        print(f"[+] Using {len(paths)} default paths")

    print(f"[+] Scanning → {base_url}")
    print(f"{'STATUS':<8} {'SIZE':<7} | URL")
    print('\033[1;37m┌'+'─'*60+'┐\033[0;0m')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    count = 0

    for path in paths:
        if not path.startswith('/'):
            path = '/' + path

        full_url = urljoin(base_url + '/', path)

        try:
            resp = requests.get(
                full_url,
                timeout=args.timeout,
                allow_redirects=False,
                headers=headers
            )

            if resp.status_code in [200, 301,302,403]:
                color = "\033[1;32m" if resp.status_code == 200 else "\033[1;32m"  
                reset = "\033[0m"
                tamanho = len(resp.content)
                print(f"│{color}{resp.status_code:<8}{tamanho:<7}{reset} │ {full_url} ")
                count += 1

        except requests.exceptions.RequestException:
            continue  
    print ('\033[1;37m└'+'─'*60+'┘\033[0;0m')
    print(f"\n[+] Scan completed! Found ({count}) ")

if __name__ == "__main__":
    main()