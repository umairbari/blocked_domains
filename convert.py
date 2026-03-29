import os

# Configuration
input_files = {
    'list.txt': 'adguard_list.txt',
    'allowed.txt': 'adguard_allowed.txt'
}

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

def get_header(file_type):
    """Generate appropriate header based on file type."""
    if file_type == 'blocked':
        return [
            "! Title: Umair's Custom AdGuard Blocklist",
            "! Description: Cleaned and De-duplicated pfBlockerNG source",
            "! Last Updated: (Managed by GitHub Actions)",
            "! Expires: 1 day\n"
        ]
    else:  # allowed
        return [
            "! Title: Umair's Custom AdGuard Allowlist",
            "! Description: Cleaned and De-duplicated allowed domains",
            "! Last Updated: (Managed by GitHub Actions)",
            "! Expires: 1 day\n"
        ]

def convert_file(input_file, output_file, file_type):
    """Convert a single file from input format to AdGuard format."""
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    seen_domains = set()
    output_lines = []

    # Add appropriate header
    output_lines.extend(get_header(file_type))

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
    
    print(f"Success: {len(seen_domains)} unique domains processed from {input_file} to {output_file}.")

def convert():
    """Convert all configured input files."""
    for input_file, output_file in input_files.items():
        file_type = 'blocked' if 'list.txt' in input_file else 'allowed'
        print(f"Processing {input_file}...")
        convert_file(input_file, output_file, file_type)

if __name__ == "__main__":
    convert()