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
<br>

---
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
<br>

## Display In-scope web app assets
Pulls from HackerOne using valid slug. <br>
Slug is usually the endpoint used to reach the scope page for the program. e.g. 
```bash
python3 subz.py -s paypal
```
![image](https://user-images.githubusercontent.com/24526564/90984072-cab8d580-e540-11ea-8181-1250181f7f72.png)

<br>

## Create directories based on the in-scope web assets
Requires the `-s` flag
```bash
python3 subz.py -s paypal -d
```
![image](https://user-images.githubusercontent.com/24526564/90984506-651a1880-e543-11ea-969a-fc2eba3cd620.png)
