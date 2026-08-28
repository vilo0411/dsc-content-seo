import re

sitemap_path = r"C:\Users\loc.nv\.gemini\antigravity\brain\732b6c0c-fa35-4596-8408-9a2e6f001931\.system_generated\steps\72\content.md"

with open(sitemap_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

urls_to_check = [
    "profit"
]

print("Checking URLs in sitemap:")
for url in urls_to_check:
    matches = re.findall(rf"https://www\.dsc\.com\.vn/kien-thuc/[^\s<]*{url}[^\s<]*", content)
    if matches:
        print(f"FOUND: {url} -> {matches[0]}")
    else:
        print(f"NOT FOUND: {url}")

