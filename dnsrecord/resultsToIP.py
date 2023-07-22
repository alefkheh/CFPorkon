import re

def extract_ip_addresses(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            match = re.search(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
            if match:
                ip_address = match.group(1)
                f_out.write(ip_address + '\n')