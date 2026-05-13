#!/usr/bin/env python3
"""Clean up and reorganize AI 产品设计雷达 folder structure"""
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
headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
radar_root = "DkoXfBPqXl4CSXdMDF7czpeNnuc"

def safe_json(r):
    try:
        return r.json()
    except:
        return {"raw": r.text[:200]}

def delete_doc(token, name):
    """Delete a Feishu docx document"""
    r = requests.delete(f"https://open.feishu.cn/open-apis/docx/v1/documents/{token}", headers=headers)
    d = safe_json(r)
    if d.get("code") == 0:
        print(f"  ✅ Deleted doc: {name}")
        return True
    else:
        # Try as file (might be a folder)
        r2 = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/{token}/batch_delete",
            headers=headers, json={"ignore_app_token": True})
        d2 = safe_json(r2)
        if d2.get("code") == 0:
            print(f"  ✅ Deleted (drive): {name}")
            return True
        else:
            print(f"  ⚠️ Could not delete {name}: {d}")
            return False

def delete_folder(token, name):
    """Delete a folder via drive API"""
    r = requests.post(f"https://open.feishu.cn/open-apis/drive/v1/files/{token}/batch_delete",
        headers=headers, json={"ignore_app_token": True})
    d = safe_json(r)
    if d.get("code") == 0:
        print(f"  ✅ Deleted folder: {name}")
        return True
    else:
        print(f"  ⚠️ Could not delete folder {name}: {d}")
        return False

# ============== STEP 1: Delete everything inside radar folder ==============
print("=== Step 1: Clean up radar folder ===")

docs_to_delete = [
    ("HFYSdwO8coWUPbxh9KJcxyM5nkv", "AI 雷达早报 (old)"),
    ("T6cidSLCRoC0DEx3zbFcNMEVngc", "综合周报 (old)"),
    ("Ci2mdGQ7woCPg4xdZomcY9gnnng", "商业动态 (old)"),
    ("MkVBdIJvMo5sXVxHtrccWYBBnjb", "学术论文前沿 (old)"),
    ("HQqvd8EkCoi99CxIh5Tc48benyb", "研发效能工具库 (old)"),
    ("BtrNdzq2zoNRIsx7VwFcLTZDncg", "GitHub 开源项目追踪 (old)"),
    ("A72td7BXvo2iDVxRBxwc264nnqc", "Test Doc"),
    ("Ndb9dFGEPofP3Yx1OhCcfiUXnGl", "Empty doc"),
    ("Bdfzd00qDoPpNHxruwocfMYSnvh", "总索引 (old)"),
    ("Nh8wdlZHaoS962xzRn8cRntbnjc", "GitHub 趋势周报 (in subfolder)"),
]

for token, name in docs_to_delete:
    delete_doc(token, name)
    time.sleep(0.15)

# Delete old subfolders
folders_to_delete = [
    ("TNGRfgvUjlIFu5drEqmcsVs3nRh", "01-GitHub 趋势周报"),
    ("L1g7fMA22lkQcEdsnv3cRBnjnbe", "05-产品灵感档案馆"),
    ("MIlpfdlL5lNieNdejyXc37c6nlT", "04-技术趋势月报"),
    ("PhhafjeeqluMjud8utOcJO90nqh", "03-研发效能工具集"),
    ("PYeVfWAxwlwFN0dSdcFc1RwvnCc", "02-AI 设计工具库"),
]

for token, name in folders_to_delete:
    delete_folder(token, name)
    time.sleep(0.2)

# ============== STEP 2: Create new folder structure ==============
print("\n=== Step 2: Create new folder structure ===")

# New structure: each category gets a subfolder with one doc inside
structure = {
    "01-每日情报": "AI 雷达早报",
    "02-GitHub 开源项目": "GitHub 项目追踪",
    "03-研发效能工具": "AI 研发效能工具库",
    "04-学术论文": "学术论文前沿",
    "05-商业动态": "AI 商业动态",
    "06-综合周报": "AI 产品设计雷达 · 周报",
}

folder_tokens = {}
doc_tokens = {}

for folder_name, doc_title in structure.items():
    # Create folder
    r = requests.post("https://open.feishu.cn/open-apis/drive/v1/files",
        headers=headers, json={"title": folder_name, "folder_token": radar_root, "type": "folder"})
    d = safe_json(r)
    if d.get("code") == 0:
        folder_token = d["data"]["token"]
        folder_tokens[folder_name] = folder_token
        print(f"  ✅ Created folder: {folder_name}")

        # Create doc inside folder
        r2 = requests.post("https://open.feishu.cn/open-apis/docx/v1/documents",
            headers=headers, json={"title": doc_title, "folder_token": folder_token})
        d2 = safe_json(r2)
        if d2.get("code") == 0:
            doc_token = d2["data"]["document"]["document_id"]
            doc_tokens[folder_name] = doc_token
            print(f"     ✅ Created doc: {doc_title} -> {doc_token}")

            # Add initial content
            blocks = [
                {"block_type": 2, "text": {"elements": [{"text_run": {"content": f"📅 最后更新: {time.strftime('%Y-%m-%d %H:%M')}", "text_element_style": {}}}]}},
                {"block_type": 22, "divider": {}},
                {"block_type": 2, "text": {"elements": [{"text_run": {"content": "自动同步中，数据会持续追加到此文档。", "text_element_style": {}}}]}},
            ]
            r3 = requests.post(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children",
                headers=headers, json={"children": blocks, "index": -1})
            print(f"     ✅ Added initial content")
        else:
            print(f"     ❌ Failed to create doc: {d2}")
    else:
        print(f"  ❌ Failed to create folder: {d}")
    time.sleep(0.3)

# ============== STEP 3: Verify ==============
print("\n=== Step 3: Verify final structure ===")
time.sleep(1)
r = requests.get(f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={radar_root}&page_size=100",
    headers={"Authorization": f"Bearer {tok}"}, timeout=10)
data = safe_json(r)
items = sorted(data.get("data",{}).get("files",[]), key=lambda x: x.get("name",""))

print(f"\n📁 AI 产品设计雷达 ({len(items)} items):\n")
for item in items:
    name = item.get("name", "(empty)")[:50]
    t = item["type"]
    print(f"  📁 [{t:6s}] {name}")

    # Check subfolder contents
    if t == "folder":
        r2 = requests.get(
            f"https://open.feishu.cn/open-apis/drive/v1/files?folder_token={item['token']}&page_size=20",
            headers={"Authorization": f"Bearer {tok}"}, timeout=5)
        subs = safe_json(r2).get("data",{}).get("files",[])
        for s in subs:
            print(f"      📄 [{s['type']:6s}] {s.get('name', '(empty)')[:50]}")

print("\n=== Done! ===")
