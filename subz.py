from datetime import date, datetime
import requests, os, sys, shlex, subprocess, argparse, logging, pprint

# Modify these if needed
BBR_API_KEY = "bbrecon api key here"
ports = (
'80,81,300,443,591,593,832,981,1010,1311,2082,2087,2095,2096,2480,3000,3128,3333,4243,4567,4711,4712,\
4993,5000,5104,5108,5800,6543,7000,7396,7474,8000,8001,8008,8014,8042,8069,8080,8081,8088,8090,8091,\
8118,8123,8172,8222,8243,8280,8281,8333,8443,8500,8834,8880,8888,8983,9000,9043,9060,9080,9090,9091,\
9200,9443,9800,9981,12443,16080,18091,18092,20720,28017')

parser = argparse.ArgumentParser(
description="This script will enumerate subdomains of your target TLD. e.g. paypal.com")
parser.add_argument('-t','--target', action="store", default=None, dest='target',
	help="Specify the single domain you'd like to enumerate subdomains for. e.g. uber.com")
parser.add_argument('-s','--scope', action="store", default=None, dest='scope',
	help="Display the in-scope web assets from HackerOne. Specify slug. e.g. 'yelp' or 'verizonmedia'")
parser.add_argument('-d','--mkdirs', action="store_true", default=False, dest='mkdirs',
	help="Create directory structure using in-scope web assets from HackerOne.'")
parser.add_argument('-v','--verbose', action="store_true", default=False, dest='verbose',
	help="Enable slightly more verbose console output")
args = parser.parse_args()

if not len(sys.argv) > 1:
	parser.print_help()
	print()
	exit()

def scanner(args, tool, cmd, outputFile):
	scanStart=datetime.now()

	if args.verbose:
		print("Executing command: {}".format(cmd))
	cmdargs = shlex.split(cmd)
	cmdOutput = subprocess.check_output(cmdargs, encoding='UTF-8')
	if tool == 'assetfinder' or tool == 'chaos':
		with open(outputFile, "w") as f:
			f.write(cmdOutput)

	logger.info("\n{} data retrieval completed in: {}\n".format(tool, datetime.now()-scanStart))

def enumerateSubs():
	tool = 'assetfinder'
	outputFile = "{}.{}.txt".format(tool, args.target)
	cmd = "assetfinder --subs-only {}".format(args.target)
	scanner(args, tool, cmd, outputFile)

	tool = 'subfinder'
	outputFile = "{}.{}.txt".format(tool, args.target)
	cmd = "subfinder -d {} -o {}".format(args.target, outputFile)
	scanner(args, tool, cmd, outputFile)

	tool = 'chaos'
	outputFile = "{}.{}.txt".format(tool, args.target)
	cmd = "chaos -d {} -silent".format(args.target)
	try:
		scanner(args, tool, cmd, outputFile)
	except subprocess.CalledProcessError as e:
		if str(e).find("exit status 1") != -1:
			print("Chaos only works on TLDs. Skipping Chaos...\n")
			logger.warning("Chaos only works on TLDs. Skipping Chaos...\n")

	### may exit with non-zero error code. It may still have results. We can have it continue anyway.
	tool = 'amass'
	outputFile = "{}.{}.txt".format(tool, args.target)
	cmd = "amass enum -active -brute -ipv4 -p {} -src -d {} -o {}".format(ports, args.target, outputFile)
	try:
		scanner(args, tool, cmd, outputFile)
	except subprocess.CalledProcessError as e:
		logger.warning(e)

	print ("\nAll data retrieval completed in: {}\n".format(datetime.now()-scriptStart))

def bbrecon(args):
	makeDirs = []
	pp = pprint.PrettyPrinter(indent=1)
	program = args.scope

	url = "https://api.bugbountyrecon.com:443/v0b/programs/{}".format(program)
	headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
	"X-API-KEY": BBR_API_KEY}

	programData = requests.get(url, headers=headers)
	if programData.status_code != 404:
		if len(programData.json()['inScope']) != 0:
			for scope in (programData.json()['inScope']):
				if scope['type'] == 'web':
					asset = scope['value'].lstrip('www.')
					asset = asset.strip('*.')
					makeDirs.append(asset)
					if not args.mkdirs:
						print(scope['value'])
		else:
			print("The H1 slug is valid but I don't see any 'in scope' web app assets.")
	else:
		print(programData.json()['detail'])

	return makeDirs


### Start the script timer
scriptStart=datetime.now()

### Set the logger up
scriptDir = os.path.dirname(__file__)
logDir = scriptDir + '/logs'
if not os.path.exists(logDir):
	os.makedirs(logDir)
logName = "logs.log"
logfilePath = os.path.join(logDir, logName)
logging.basicConfig(filename=logfilePath, filemode='a',
format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if args.target and not args.scope:
	outputFile = '' # dont change this
	enumerateSubs()

if args.scope and not args.target:
	dirs = bbrecon(args)
	if args.mkdirs:
		print("Creating dirs...")
		for dir in dirs:
			print(dir)
			try:
				os.mkdir(dir)
			except FileExistsError:
				pass
