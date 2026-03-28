import os

# Configuration
input_file = 'list.txt'  # the original file
output_file = 'adguard_list.txt' # The formatted file

def convert():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        f_out.write("! Title: Umair's Custom AdGuard Blocklist\n")
        f_out.write("! Description: Converted from pfBlockerNG format\n")
        f_out.write("! Expires: 1 day\n\n")

        for line in f_in:
            clean_line = line.strip()
            
            # Handle empty lines or comments
            if not clean_line:
                f_out.write("\n")
                continue
            if clean_line.startswith('#'):
                # Convert # to ! for AdGuard comment syntax
                f_out.write("! " + clean_line[1:].strip() + "\n")
                continue
            
            # Clean domain (strip trailing slashes, spaces)
            domain = clean_line.rstrip('/')
            
            # Format as AdGuard Wildcard
            f_out.write(f"||{domain}^\n")

if __name__ == "__main__":
    convert()
