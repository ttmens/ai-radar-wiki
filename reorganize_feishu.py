#!/usr/bin/env python3
"""Reorganize Feishu radar folder structure"""
import json, os, requests, time

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "").strip()
if not FEISHU_APP_ID:
    raise EnvironmentError("FEISHU_APP_ID not set")

_env_path = "/home/admin/.hermes/.env"
SECRET = None
with open(_env_path) as f:
    for line in f:
        if line.startswith("FEISHU_APP_SECRET="):
            SECRET = line.strip().split("=", 1)[1]
            break

if not SECRET:
    raise ValueError("FEISHU_APP_SECRET not found in .env")

def get_token():
    r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": SECRET})
    return r.json()["tenant_access_token"]

tok = get_token()
headers = {"Authorization": f"Bearer {tok}"}

radar_root = "DkoXfBPqXl4CSXdMDF7czpeNnuc"

# 1. Create new subfolders
new_folders = ["00-每日情报", "06-综合周报", "07-学术论文", "08-商业动态"]
folder_tokens = {}

for name in new_folders:
    r = requests.post("https://open.feishu.cn/open-apis/drive/v1/files",
        headers={**headers, "Content-Type": "application/json"},
        json={"title": name, "folder_token": radar_root})
    print(f"  DEBUG {name}: status={r.status_code}, body={r.text[:200]}")
    try:
        data = r.json()
    except:
        print(f"  Non-JSON response, skipping")
        continue
    if data.get("code") == 0:
        folder_tokens[name] = data["data"]["token"]
        print(f"✅ Created folder: {name} -> {data['data']['token']}")
    else:
        print(f"❌ Failed to create {name}: {data}")
    time.sleep(0.3)

# Existing folders
existing_folders = {
    "01-GitHub 趋势周报": "TNGRfgvUjlIFu5drEqmcsVs3nRh",
    "02-AI 设计工具库": "PYeVfWAxwlwFN0dSdcFc1RwvnCc",
    "03-研发效能工具集": "PhhafjeeqluMjud8utOcJO90nqh",
    "04-技术趋势月报": "MIlpfdlL5lNieNdejyXc37c6nlT",
    "05-产品灵感档案馆": "L1g7fMA22lkQcEdsnv3cRBnjnbe",
}
folder_tokens.update(existing_folders)

# 2. Docs to move: they're at root drive (parent: nodcnfEMCfgGIVX2nJnnoKJ5ZIg)
# Map doc_token -> target_folder_token
docs_to_move = {
    # These are the 6 docs we created
    "A58Gd8ekdoFCWGxAaXgcaK4Inlc": "00-每日情报",      # AI 雷达早报
    "XGisd1z9QoJBmgxmEgFcsZ7fnse": "01-GitHub 趋势周报",  # GitHub 开源项目追踪
    "Mm1IdevDZogiKuxLiIRcSkK5nEg": "03-研发效能工具集",   # AI 研发效能工具库
    "Ko2VdgQloo4iqux1610cSN2knLe": "07-学术论文",         # 学术论文前沿
    "Nv5AdN60BoxjO6x2jQecl7zSnjd": "08-商业动态",        # AI 商业动态
    "JeIydbfrJoesINxoOXNcQpzinne": "06-综合周报",        # 综合周报
}

print("\n=== Moving docs ===")
for doc_token, folder_name in docs_to_move.items():
    target = folder_tokens[folder_name]
    r = requests.patch(
        f"https://open.feishu.cn/open-apis/drive/v1/files/{doc_token}",
        headers={**headers, "Content-Type": "application/json"},
        json={"folder_token": target}
    )
    data = r.json()
    if data.get("code") == 0:
        print(f"✅ Moved doc {doc_token[:10]}... -> {folder_name}")
    else:
        print(f"❌ Failed to move {doc_token[:10]}...: {data}")
    time.sleep(0.3)

# 3. Also move the unnamed doc and verify structure
print("\n=== Verifying folder structure ===")
for name, ftoken in folder_tokens.items():
    r = requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={ftoken}&page_size=50",
        headers=headers)
    items = r.json().get("data",{}).get("files",[])
    print(f"📁 {name} ({len(items)} items):")
    for item in items:
        print(f"    [{item['type']}] {item.get('name','(empty)')[:60]}")

print("\nDone!")
