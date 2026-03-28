import os

# Configuration
input_file = 'list.txt'
output_file = 'adguard_list.txt'

def clean_domain(raw_line):
    """
    Cleans a line to extract just the domain name.
    Handles: https://, http://, trailing slashes, and paths.
    """
    # 1. Remove protocol
    domain = raw_line.replace('https://', '').replace('http://', '')
    
    # 2. Split by '/' and take the first part (removes trailing / or paths)
    domain = domain.split('/')[0]
    
    # 3. Clean whitespace and convert to lowercase for DNS consistency
    return domain.strip().lower()

def convert():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    seen_domains = set()
    output_lines = []

    # Add AdGuard Header
    output_lines.append("! Title: Umair's Custom AdGuard Blocklist")
    output_lines.append("! Description: Cleaned and De-duplicated pfBlockerNG source")
    output_lines.append("! Last Updated: (Managed by GitHub Actions)")
    output_lines.append("! Expires: 1 day\n")

    with open(input_file, 'r') as f_in:
        for line in f_in:
            line = line.strip()
            
            # Handle empty lines
            if not line:
                output_lines.append("")
                continue
                
            # Handle comments (PFBlocker uses #, AdGuard uses !)
            if line.startswith('#'):
                output_lines.append(f"! {line[1:].strip()}")
                continue
            
            # Process potential domains
            domain = clean_domain(line)
            
            if domain and domain not in seen_domains:
                seen_domains.add(domain)
                output_lines.append(f"||{domain}^")
            elif domain in seen_domains:
                print(f"Skipping duplicate: {domain}")

    # Write the cleaned list
    with open(output_file, 'w') as f_out:
        f_out.write("\n".join(output_lines))
    
    print(f"Success: {len(seen_domains)} unique domains processed.")

if __name__ == "__main__":
    convert()
