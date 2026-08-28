import re
import os

def parse_instincts_file(archive_path):
    with open(archive_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    instincts = []
    current_instinct = None
    
    for line in lines:
        stripped = line.strip()
        
        # Check for start of a new instinct
        if line.startswith('### '):
            title = line[4:].strip()
            # Ignore template and empty headings
            if title == '[Tên ngắn gọn]' or not title:
                continue
                
            if current_instinct:
                instincts.append(current_instinct)
                
            current_instinct = {
                'title': title,
                'status': '',
                'source': '',
                'user_feedback': '',
                'instinct_lines': [],
                'scope': 'Global',
                'parsing_instinct': False
            }
            continue
            
        if current_instinct is not None:
            if stripped.startswith('- **Trạng thái:**'):
                current_instinct['status'] = stripped.replace('- **Trạng thái:**', '').strip()
                current_instinct['parsing_instinct'] = False
            elif stripped.startswith('- **Nguồn:**'):
                current_instinct['source'] = stripped.replace('- **Nguồn:**', '').strip()
                current_instinct['parsing_instinct'] = False
            elif stripped.startswith('- **Phản hồi từ User:**'):
                current_instinct['user_feedback'] = stripped.replace('- **Phản hồi từ User:**', '').strip()
                current_instinct['parsing_instinct'] = False
            elif stripped.startswith('- **Bản năng:**'):
                current_instinct['parsing_instinct'] = True
                content = stripped.replace('- **Bản năng:**', '').strip()
                if content:
                    current_instinct['instinct_lines'].append(content)
            elif stripped.startswith('- **Phạm vi:**'):
                current_instinct['scope'] = stripped.replace('- **Phạm vi:**', '').strip()
                current_instinct['parsing_instinct'] = False
            elif current_instinct['parsing_instinct']:
                # We are parsing instinct lines. Preserve the raw line (with its leading indentation)
                # but strip the trailing newline character
                current_instinct['instinct_lines'].append(line.rstrip('\r\n'))
                
    if current_instinct:
        instincts.append(current_instinct)
        
    return instincts

def run():
    instincts_file = r'e:\project\seo-writer-agent-main\.antigravity\memory\instincts.md'
    archive_file = r'e:\project\seo-writer-agent-main\.antigravity\memory\instincts-archive.md'
    
    if not os.path.exists(archive_file):
        print(f"Error: {archive_file} not found. Please create it first.")
        return
        
    instincts = parse_instincts_file(archive_file)
    print(f"Parsed {len(instincts)} instincts from archive.")
    
    categories = {
        "Văn phong & Ngôn từ (Style & Tone)": [],
        "Cấu trúc & Định dạng (Structure & Formatting)": [],
        "SEO & Liên kết (SEO & Internal Links)": [],
        "Sản phẩm & Thương hiệu (Products & Brand Context)": []
    }
    
    style_keywords = [
        "vĩ mô", "ngoặc kép", "chiến lược thay cho", "cơ chế truyền dẫn", "xương máu", "rõ ràng"
    ]
    seo_keywords = [
        "link", "sitemap", "đường dẫn", "tiêu đề seo", "seo title"
    ]
    format_keywords = [
        "heading", "dài đoạn", "list/table", "sapo", "dòng trống", "dấu câu", "latex", "công thức", "dấu hai chấm", "dấu chấm", "phân biệt"
    ]
    
    for inst in instincts:
        # Only process ACTIVE instincts
        if inst['status'].upper() != 'ACTIVE':
            continue
            
        title_lower = inst['title'].lower()
        
        # Combine instinct lines to check keywords
        instinct_text = " ".join(inst['instinct_lines']).lower()
        
        if any(kw in title_lower or kw in instinct_text for kw in style_keywords):
            categories["Văn phong & Ngôn từ (Style & Tone)"].append(inst)
        elif any(kw in title_lower or kw in instinct_text for kw in seo_keywords):
            categories["SEO & Liên kết (SEO & Internal Links)"].append(inst)
        elif any(kw in title_lower or kw in instinct_text for kw in format_keywords):
            categories["Cấu trúc & Định dạng (Structure & Formatting)"].append(inst)
        else:
            categories["Sản phẩm & Thương hiệu (Products & Brand Context)"].append(inst)
            
    condensed = """# Continuous Learning: Instincts (Bản năng rút gọn)

> **Bắt buộc:** Mọi agent, skill, và workflow đều phải đọc file này trước khi thực thi để tránh lặp lại lỗi cũ.
> **Tối ưu hóa Token:** File này đã được rút gọn để chỉ chứa các quy tắc hành động trực tiếp nhằm tiết kiệm token tối đa. Chi tiết lịch sử, feedback gốc và nguồn được lưu trữ tại [.antigravity/memory/instincts-archive.md](file:///.antigravity/memory/instincts-archive.md).

---

"""
    
    for cat_name, items in categories.items():
        if not items:
            continue
        condensed += f"## {cat_name}\n\n"
        for item in items:
            scope_suffix = f" *(Phạm vi: {item['scope']})*" if item['scope'] != 'Global' else ""
            condensed += f"### {item['title']}{scope_suffix}\n"
            
            # Format and output the instinct lines
            # If the first line starts with spacing/indent or numbers, or is empty, we handle it
            lines = item['instinct_lines']
            if not lines:
                condensed += "- (Chưa cấu hình nội dung bản năng)\n\n"
                continue
                
            first_line = lines[0].strip()
            
            # Check if first line already represents a list/bullet or starts with number
            # We want to prefix with "- " if it's not already a list bullet, or keep formatting
            if len(lines) == 1:
                if first_line.startswith('-') or first_line.startswith('*'):
                    condensed += f"{lines[0]}\n\n"
                else:
                    condensed += f"- {first_line}\n\n"
            else:
                # Multi-line instinct
                # If first line has a bullet, write it, otherwise write it as a bullet
                if first_line.startswith('-') or first_line.startswith('*') or re.match(r'^\d+\.', first_line):
                    # We output it directly, but let's make sure it is indented nicely or has bullet
                    for line in lines:
                        condensed += f"{line}\n"
                else:
                    # Output first line as bullet, others indented
                    condensed += f"- {lines[0]}\n"
                    for line in lines[1:]:
                        # Preserve indent
                        condensed += f"  {line}\n"
                condensed += "\n"
                
    with open(instincts_file, 'w', encoding='utf-8') as f:
        f.write(condensed)
    print("Updated instincts.md with condensed active rules successfully.")

if __name__ == '__main__':
    run()
