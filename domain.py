import argparse
import os

parser = argparse.ArgumentParser(description='scan a target domain')
parser.add_argument('-d', '--domain', type=str, required=True, help='target domain to scan')

args = parser.parse_args()

# Run subfinder and output results to subdomain.txt
os.system(f"subfinder -d {args.domain} -o subdomain.txt")

# Run dnsgen on subdomain.txt with alternate wordlist and output results to allsubdomain.txt
os.system(f"dnsgen -w /root/wordlist/dns/alt.txt -l 4 subdomain.txt > allsubdomain.txt")

# Combine subfinder and dnsgen output into allsubdomain.txt
with open('subdomain.txt', 'r') as subfinder_file, open('allsubdomain.txt', 'a') as allsubdomain_file:
    allsubdomain_file.write(subfinder_file.read())

with open('allsubdomain.txt', 'a') as allsubdomain_file, open('/root/wordlist/dns/alt.txt', 'r') as alt_wordlist:
    allsubdomain_file.write(alt_wordlist.read())

# Resolve all subdomains in allsubdomain.txt with puredns using a list of resolvers and output to subdomain.txt
os.system(f"puredns resolve allsubdomain.txt -w subdomain.txt -r /root/wordlist/resolvers/resolvers.txt")

