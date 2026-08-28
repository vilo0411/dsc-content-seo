import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dirs = [
    r"e:\project\seo-writer-agent-main\knowledge\4-content\2-drafts",
    r"e:\project\seo-writer-agent-main\knowledge\4-content\3-finalized"
]

for d in dirs:
    if not os.path.exists(d):
        continue
    for filename in os.listdir(d):
        if filename.endswith(".md"):
            file_path = os.path.join(d, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            for idx, line in enumerate(lines):
                if "cập nhật tháng 8/2026" in line or "thông tin phân tích cập nhật" in line:
                    print(f"{os.path.basename(d)}/{filename}:{idx+1}: {line.strip()}")
