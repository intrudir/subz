# subz
Programatically uses a few subdomain recon tools to enumerate subdomains for a target domain

# Requirements:
You need the following subdomain recon tools installed and in your PATH:
- Amass
  - https://github.com/OWASP/Amass
- Subfinder
  - https://github.com/projectdiscovery/subfinder
- Assetfinder
  - https://github.com/tomnomnom/assetfinder

# Usage:
```bash
usage: subz.py [-h] [-t TARGET] [-v]

This script will enumerate subdomains of your target TLD. e.g. paypal.com

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Specify the target domain you'd like to enumerate
                        subdomains for. e.g. uber.com
  -v, --verbose         Enable slightly more verbose console output
```
