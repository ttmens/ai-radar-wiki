#!/usr/bin/env python3
"""
Feishu Bitable Writer
Used by Cron jobs to reliably write intelligence data into the AI Radar Database.

Usage:
    python feishu_bitable_writer.py --data '{"Date": "...", "Title": "...", ...}'
    python feishu_bitable_writer.py --batch '[{"..."}, {"..."}]'
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime, timedelta

CONFIG_PATH = "/home/admin/.hermes/config.yaml"

def get_app_secret():
    with open("/home/admin/.hermes/.env") as f:
        for line in f:
            if line.startswith("FEISHU_APP_SECRET="):
                return line.strip().split("=", 1)[1]
    raise ValueError("FEISHU_APP_SECRET not found")

def get_auth_token():
    app_id = "cli_a92b1c361ab8dcee"
    app_secret = get_app_secret()
    resp = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret}
    )
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"Auth failed: {data}")
    return data["app_access_token"]

def add_record_to_bitable(app_token, table_id, record_data, token):
    """
    Adds a record to the Bitable.
    record_data should be a dict matching the field names.
    """
    # Map field names to values with format conversion
    import datetime
    fields = {}
    for k, v in record_data.items():
        if k == "Date" and isinstance(v, str):
            # Convert YYYY-MM-DD to unix timestamp (milliseconds)
            dt = datetime.datetime.strptime(v, "%Y-%m-%d")
            fields[k] = int(dt.timestamp() * 1000)
        elif k == "Link" and isinstance(v, str):
            # Convert string URL to URL object format
            fields[k] = {"text": v.split("/")[-1] or "Link", "link": v}
        else:
            fields[k] = v

    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    payload = {
        "fields": fields
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()
    
    if result.get("code") == 0:
        print(f"Successfully added record: {record_data.get('Title', 'N/A')}")
        return True
    else:
        # Handle common errors
        if "limit" in str(result).lower():
            print(f"Rate limit exceeded. Waiting and retrying...")
        print(f"Failed to add record: {result}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Write to Feishu Bitable")
    parser.add_argument("--data", type=str, help="JSON string of the record")
    parser.add_argument("--batch", type=str, help="JSON list of records")
    args = parser.parse_args()

    try:
        # Config
        app_token = "V1IZbGiLaa4V6ysQW3ycJamjngc"
        table_id = "tblrHRQiNq6gsaJq"
        
        token = get_auth_token()

        if args.data:
            data = json.loads(args.data)
            if isinstance(data, list):
                for item in data:
                    add_record_to_bitable(app_token, table_id, item, token)
            else:
                add_record_to_bitable(app_token, table_id, data, token)
        elif args.batch:
            batch_data = json.loads(args.batch)
            for item in batch_data:
                add_record_to_bitable(app_token, table_id, item, token)
        else:
            print("No data provided.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
