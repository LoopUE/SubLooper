import requests
import concurrent.futures
import argparse
from urllib.parse import urlparse
import os

def extract_domain_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        return parsed_url.netloc
    else:
        return parsed_url.path.split("/")[0]

def check_subdomain(subdomain, domain):
    full_subdomain = f"{subdomain}.{domain}"
    url = f"http://{full_subdomain}"
    try:
        response = requests.get(url)
        if response.status_code == 200 or response.status_code == 403:
            print(f"[{response.status_code}] {full_subdomain}")
            return full_subdomain
    except requests.RequestException:
        pass
    return None

def brute_force_subdomains(domain, subdomain_list):
    found_subdomains = set()  # Use a set to store unique subdomains

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Use ThreadPoolExecutor to parallelize subdomain checks
        futures = {executor.submit(check_subdomain, subdomain, domain): subdomain for subdomain in subdomain_list}

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found_subdomains.add(result)

    return found_subdomains

def save_to_file(subdomains, output_file):
    with open(output_file, "w") as file:
        for subdomain in subdomains:
            file.write(subdomain + "\n")

def print_logo():
    print("""
    
    
    """)
    print("SubLooper")
    print("         By")
    print("            LoopUE")
    print("                   Telegram")
    print("                             @LoopUE")
    print("""
    
    
    
    """)

if __name__ == "__main__":
    print_logo()

    parser = argparse.ArgumentParser(description="Brute Force Subdomains")
    parser.add_argument("target", help="Enter the target URL or domain")
    parser.add_argument("-o", "--output", help="Specify an output file to save the subdomains")
    args = parser.parse_args()

    domain = extract_domain_from_url(args.target)

    if not domain:
        print("Invalid input. Please enter a valid URL or domain.")
    else:
        with open("SubLooper.txt", "r") as subdomains_file:
            subdomains = [line.strip() for line in subdomains_file]

        found_subdomains = brute_force_subdomains(domain, subdomains)

        if found_subdomains:
            print(f"Found {len(found_subdomains)} subdomains in total.")
            if args.output:
                save_to_file(found_subdomains, args.output)
                print(f"Subdomains saved to {args.output}")
            else:
                print("\nSubdomains found:")
                for index, subdomain in enumerate(found_subdomains, start=1):
                    print(f"{index}. {subdomain}")

        else:
            print("No subdomains found.")
