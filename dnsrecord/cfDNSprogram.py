import json
import requests
import concurrent.futures
import time
from typing import List
def addNewCloudflareRecord(email: str, api_key: str, zone_id: str, subdomain: str, ip: str) -> None:
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    data = {
        "type": "A",
        "name": subdomain,
        "content": ip,
        "ttl": 3600,
        "proxied": False
    }
    retries = 0
    max_retries = 9999
    while retries < max_retries:
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException:
            retries += 1
            if retries < max_retries:
                print(f"Retrying... (Attempt {retries} of {max_retries})")
                time.sleep(1)
    else:
        print(f"Failed to post data after {max_retries} attempts.")


def getCloudflareExistingRecords(email, api_key, zone_id, subdomain):
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={subdomain}&per_page=50000"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return json.loads(response.text)["result"]


def deleteCloudflareExistingRecord(email: str, api_key: str, zone_id: str, record_id: str) -> None:
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    retries = 0
    max_retries = 9999
    while retries < max_retries:
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException:
            retries += 1
            if retries < max_retries:
                print(f"Retrying... (Attempt {retries} of {max_retries})")
                time.sleep(1)
    else:
        print(f"Failed to delete the record after {max_retries} attempts.")


def addAllCloudflareRecords(email: str, api_key: str, zone_id: str, subdomain: str, ips: List[str]) -> None:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(addNewCloudflareRecord, email, api_key, zone_id, subdomain, ip) for ip in ips]
        concurrent.futures.wait(futures)