from datetime import date, datetime
import os, sys, shlex, subprocess, argparse, logging

parser = argparse.ArgumentParser(
description="This script will enumerate subdomains of your target TLD. e.g. paypal.com"
)
parser.add_argument('-t','--target', action="store", default=None, dest='target',
	help="Specify the target domain you'd like to enumerate subdomains for. e.g. uber.com")
parser.add_argument('-v','--verbose', action="store_true", default=False, dest='verbose',
	help="Enable slightly more verbose console output")
args = parser.parse_args()

if not len(sys.argv) > 1:
	parser.print_help()
	print()
	exit()

ports = (
'80,81,300,443,591,593,832,981,1010,1311,2082,2087,2095,2096,2480,3000,3128,3333,4243,4567,4711,4712,\
4993,5000,5104,5108,5800,6543,7000,7396,7474,8000,8001,8008,8014,8042,8069,8080,8081,8088,8090,8091,\
8118,8123,8172,8222,8243,8280,8281,8333,8443,8500,8834,8880,8888,8983,9000,9043,9060,9080,9090,9091,\
9200,9443,9800,9981,12443,16080,18091,18092,20720,28017'
)

def scanner(args, cmd, outputFile):
	if args.verbose:
		print("Executing command: {}".format(cmd))
	cmdargs = shlex.split(cmd)
	cmdOutput = subprocess.check_output(cmdargs, encoding='UTF-8')
	if cmd.find('assetfinder') != -1:
		with open(outputFile, "w") as f:
			f.write(cmdOutput)

### Start the script timer
scriptStart=datetime.now()

### Set the logger up
if not os.path.exists('logs'):
    os.makedirs('logs')
logfileName = "logs/logs.log"
logging.basicConfig(filename=logfileName, filemode='a',
format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

### Amass
scanStart=datetime.now()
### may exit with non-zero error code. It may still have results. We can have it continue anyway.
outputFile = "amass.{}.txt".format(args.target)
cmd = "amass enum -active -brute -ipv4 -p {} -src -d {} -o {}".format(ports, args.target, outputFile)
try:
	scanner(args, cmd, outputFile)
except subprocess.CalledProcessError as e:
	logger.warning(e)
logger.info("\nAmass data retrieval completed in: {}\n".format(datetime.now()-scanStart))

### assetfinder
scanStart=datetime.now()
outputFile = "assetfinder.{}.txt".format(args.target)
cmd = "assetfinder --subs-only {}".format(args.target)
scanner(args, cmd, outputFile)
logger.info("\nAssetfinder data retrieval completed in: {}\n".format(datetime.now()-scanStart))

### subfinder
scanStart=datetime.now()
outputFile = "subfinder.{}.txt".format(args.target)
cmd = "subfinder -d {} -o {}".format(args.target, outputFile)
scanner(args, cmd, outputFile)
logger.info("\nSubfinder data retrieval completed in: {}\n".format(datetime.now()-scanStart))

print ("\nAll data retrieval completed in: {}\n".format(datetime.now()-scriptStart))
