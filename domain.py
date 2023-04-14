import argparse
import subprocess
import json

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="Target domain", required=True)
args = parser.parse_args()

# Get the target domain from the command-line arguments
target_domain = args.domain

# Run Amass to enumerate subdomains
amass_cmd = f"amass enum -d {target_domain}"
amass_output = subprocess.check_output(amass_cmd, shell=True)

# Run Subfinder to enumerate subdomains
subfinder_cmd = f"subfinder -d {target_domain}"
subfinder_output = subprocess.check_output(subfinder_cmd, shell=True)

# Combine the outputs and split by newlines
all_output = amass_output.decode().strip() + "\n" + 
subfinder_output.decode().strip()
all_subdomains = all_output.split("\n")

# Deduplicate the subdomains and sort them alphabetically
unique_subdomains = sorted(set(all_subdomains))

# Generate permutation-based subdomains using Dnsgen
dnsgen_cmd = f"dnsgen -w words.txt -r 5 {target_domain}"
dnsgen_output = subprocess.check_output(dnsgen_cmd, shell=True)

# Combine the outputs and split by newlines
all_output = "\n".join(unique_subdomains) + "\n" + 
dnsgen_output.decode().strip()
all_subdomains = all_output.split("\n")

# Deduplicate the subdomains and sort them alphabetically
unique_subdomains = sorted(set(all_subdomains))

# Resolve the subdomains using Puredns
puredns_cmd = f"puredns resolve -r resolvers.txt -j 10 subdomain.txt"
puredns_output = subprocess.check_output(puredns_cmd, shell=True)

# Parse the JSON output from Puredns
puredns_results = json.loads(puredns_output.decode())

# Extract the resolved subdomains from the results
resolved_subdomains = []
for result in puredns_results:
    if result["result"]:
        resolved_subdomains.append(result["domain"])

# Write the resolved subdomains to a file
with open("resolved_subdomains.txt", "w") as f:
    f.write("\n".join(resolved_subdomains))
