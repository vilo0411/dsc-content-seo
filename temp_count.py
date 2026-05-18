import sys, re
def count_content_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    content = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if re.match(r'^-? ?\[.*\]\(.*\) *$', line) or line.startswith('http'):
            continue
        content.append(line)
    text = ' '.join(content)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', text)
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'[*_`#>|~\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())

for f in sys.argv[1:]:
    print(f'{f[-15:]}: {count_content_words(f)}')
