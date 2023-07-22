import os
def read_cf_credentials(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            email = lines[0].strip()
            api_key = lines[1].strip()
            zone_id = lines[2].strip()
            subdomain = lines[3].strip()
    else:
        print("cfcredentials.txt file does not exist.")
        email = input("Enter Cloudflare email: ")
        api_key = input("Enter Cloudflare API key: ")
        zone_id = input("Enter Cloudflare zone ID: ")
        subdomain = input("Enter Cloudflare subdomain: ")

    return email, api_key, zone_id, subdomain


