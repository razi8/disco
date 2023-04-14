import argparse
import subprocess

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="target domain", required=True)
args = parser.parse_args()

# Get the target domain from the command-line arguments
target_domain = args.domain

# Run Subfinder to enumerate subdomains
subfinder_cmd = f"subfinder -d {target_domain}"
subfinder_output = subprocess.check_output(subfinder_cmd, shell=True)

# Combine the outputs and split by newlines
all_output = subfinder_output.decode().strip()
all_subdomains = all_output.split("\n")

# Deduplicate the subdomains and sort them alphabetically
unique_subdomains = sorted(set(all_subdomains))

# Write the unique subdomains to a file
with open("subdomain.txt", "w") as f:
    f.write("\n".join(unique_subdomains))
