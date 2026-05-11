import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
CONTENT_DIR = Path("content/blog/3-finalized")
OUTPUT_FILE = Path("knowledge/3-pipeline/internal-link-dashboard.md")
INDEX_FILE = Path("knowledge/3-pipeline/anchor-index.md")

# Regex
LINK_REGEX = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def get_anchor_index():
    index = {} # filename -> {exact: "", partial: []}
    if not INDEX_FILE.exists():
        return index
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "|" in line and "[" in line:
                cells = [c.strip() for c in line.split("|")]
                if len(cells) >= 4:
                    file_match = re.search(r'\[(.*?)\]', cells[1])
                    if file_match:
                        filename = file_match.group(1)
                        exact = cells[2].lower()
                        partials = [p.strip().lower() for p in cells[3].split(",")]
                        index[filename] = {"exact": exact, "partial": partials}
    return index

def classify_anchor(anchor, filename, index):
    anchor_clean = anchor.lower().strip()
    entry = index.get(filename, {})
    if anchor_clean == entry.get("exact", ""): return "Exact"
    if anchor_clean in entry.get("partial", []): return "Partial"
    return "Generic/Title"

def audit():
    index = get_anchor_index()
    if not CONTENT_DIR.exists():
        print("Content directory not found.")
        return
    
    files = list(CONTENT_DIR.glob("*.md"))
    data = {}

    for file_path in files:
        rel_path = file_path.name
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if rel_path not in data:
            data[rel_path] = {"out_links": [], "in_links": []}

        links = LINK_REGEX.findall(content)
        for anchor, url in links:
            if "Final-" in url or "3-finalized" in url:
                dest_file = os.path.basename(url)
                data[rel_path]["out_links"].append({"anchor": anchor, "dest": dest_file})
                
                if dest_file not in data:
                    data[dest_file] = {"out_links": [], "in_links": []}
                data[dest_file]["in_links"].append({"anchor": anchor, "source": rel_path})

    # Generate Report
    report = "# Internal Linking Dashboard\n"
    report += f"> Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "| Page (File) | Out | In | Distribution (E/P/T) | Health |\n"
    report += "| :--- | :---: | :---: | :--- | :--- |\n"

    for file_name in sorted(data.keys()):
        stats = data[file_name]
        in_count = len(stats["in_links"])
        exact = sum(1 for il in stats["in_links"] if classify_anchor(il["anchor"], file_name, index) == "Exact")
        partial = sum(1 for il in stats["in_links"] if classify_anchor(il["anchor"], file_name, index) == "Partial")
        title = in_count - exact - partial
        
        ratio_str = f"{exact/in_count:.0%}/{partial/in_count:.0%}/{title/in_count:.0%}" if in_count > 0 else "0/0/0"
        health = "✅ Healthy" if in_count >= 3 else "🔍 Needs Links"
        report += f"| `{file_name}` | {len(stats['out_links'])} | {in_count} | {ratio_str} | {health} |\n"

    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Audit completed: {OUTPUT_FILE}")

if __name__ == "__main__":
    audit()
