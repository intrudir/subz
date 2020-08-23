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
- Chaos
  - https://github.com/projectdiscovery/chaos-client
  
# Optional:
- BBRecon API key
  - https://bugbountyrecon.com/
  - Add the API key into BBR_API_KEY  in the script.


# Usage:
```bash
usage: subz.py [-h] [-t TARGET] [-s SCOPE] [-d] [-v]

Programatically uses a few subdomain recon tools to enumerate subdomains for a
target domain

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Specify the single domain you'd like to enumerate
                        subdomains for. e.g. uber.com
  -s SCOPE, --scope SCOPE
                        Display the in-scope web assets from HackerOne.
                        Specify slug. e.g. 'yelp' or 'verizonmedia'
  -d, --mkdirs          Create directory structure using in-scope web assets
                        from HackerOne. Requires '-s' flag.'
  -v, --verbose         Enable slightly more verbose console output
```
