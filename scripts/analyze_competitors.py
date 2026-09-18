#!/usr/bin/env python3
"""
Competitor SERP Analysis Script - DSC Content System
Crawls competitor URLs, filters out HTTP errors and thin content, 
and extracts structured headings, word counts per section, and compact outlines.
Minimizes token consumption for LLM context.
"""

import sys
import os
import re
import json
import argparse
import urllib.request
import urllib.error
import ssl
from html.parser import HTMLParser

# Reconfigure stdout for UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Create SSL context that ignores self-signed cert issues if any
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
}

NOISE_TAGS = {'script', 'style', 'header', 'footer', 'nav', 'aside', 'noscript', 'form', 'svg'}

class ConciseHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.in_title = False
        self.ignored_depth = 0
        
        # Current state
        self.current_heading_level = None # 'h1', 'h2', 'h3', 'h4'
        self.current_heading_text = []
        
        # Extracted sections
        self.sections = []
        self.current_section = {'level': 'intro', 'title': 'Introduction/Sapo', 'text_parts': []}
        
        self.all_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        if tag in NOISE_TAGS:
            self.ignored_depth += 1
            return
            
        if self.ignored_depth > 0:
            return

        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attr_dict.get('name', '').lower()
            prop = attr_dict.get('property', '').lower()
            if name == 'description' or prop == 'og:description':
                if not self.description:
                    self.description = attr_dict.get('content', '').strip()

        elif tag in ('h1', 'h2', 'h3', 'h4'):
            self.current_heading_level = tag
            self.current_heading_text = []

    def handle_endtag(self, tag):
        if tag in NOISE_TAGS and self.ignored_depth > 0:
            self.ignored_depth -= 1
            return
            
        if self.ignored_depth > 0:
            return

        if tag == 'title':
            self.in_title = False
        elif tag in ('h1', 'h2', 'h3', 'h4'):
            heading_title = " ".join(self.current_heading_text).strip()
            heading_title = re.sub(r'\s+', ' ', heading_title)
            if heading_title:
                # Store finished current section
                if self.current_section and (self.current_section['text_parts'] or self.current_section['title'] != 'Introduction/Sapo'):
                    self.sections.append({
                        'level': self.current_section['level'],
                        'title': self.current_section['title'],
                        'content': " ".join(self.current_section['text_parts']).strip()
                    })
                # Start new section
                self.current_section = {
                    'level': self.current_heading_level,
                    'title': heading_title,
                    'text_parts': []
                }
            self.current_heading_level = None

    def handle_data(self, data):
        if self.ignored_depth > 0:
            return
            
        text = data.strip()
        if not text:
            return

        if self.in_title:
            self.title += " " + text
        elif self.current_heading_level:
            self.current_heading_text.append(text)
        else:
            self.current_section['text_parts'].append(text)
            self.all_text.append(text)

    def finalize(self):
        if self.current_section and (self.current_section['text_parts'] or self.current_section['title'] != 'Introduction/Sapo'):
            self.sections.append({
                'level': self.current_section['level'],
                'title': self.current_section['title'],
                'content': " ".join(self.current_section['text_parts']).strip()
            })
        self.title = re.sub(r'\s+', ' ', self.title).strip()


def count_words(text):
    if not text:
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def analyze_url(url, min_words=200):
    print(f"\n[FETCHING] {url}")
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        with urllib.request.urlopen(req, timeout=12, context=ssl_context) as response:
            status = response.getcode()
            if status != 200:
                print(f"  [SKIP HTTP {status}] {url}")
                return None
                
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                print(f"  [SKIP NON-HTML] Content-Type: {content_type}")
                return None
                
            raw_bytes = response.read()
            charset = 'utf-8'
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1].split(';')[0].strip()
            
            try:
                html_str = raw_bytes.decode(charset, errors='replace')
            except Exception:
                html_str = raw_bytes.decode('utf-8', errors='replace')
                
    except urllib.error.HTTPError as e:
        print(f"  [SKIP HTTP ERROR {e.code}] {url}")
        return None
    except urllib.error.URLError as e:
        print(f"  [SKIP URL ERROR {e.reason}] {url}")
        return None
    except Exception as e:
        print(f"  [SKIP ERROR {str(e)}] {url}")
        return None

    # Parse HTML
    parser = ConciseHTMLParser()
    try:
        parser.feed(html_str)
        parser.finalize()
    except Exception as e:
        print(f"  [PARSER WARNING] {e}")

    full_text = " ".join(parser.all_text)
    total_words = count_words(full_text)

    # Check thin content
    if total_words < min_words:
        print(f"  [SKIP THIN CONTENT] Total words: {total_words} (< min {min_words} words threshold)")
        return None

    print(f"  [VALID] Title: '{parser.title}' | Total words: ~{total_words} | Sections: {len(parser.sections)}")

    # Format structured sections
    structured_outline = []
    for sec in parser.sections:
        w_count = count_words(sec['content'])
        structured_outline.append({
            'level': sec['level'].upper(),
            'title': sec['title'],
            'word_count': w_count,
            'snippet': sec['content'][:150] + "..." if len(sec['content']) > 150 else sec['content']
        })

    return {
        'url': url,
        'title': parser.title,
        'description': parser.description,
        'total_words': total_words,
        'sections_count': len(parser.sections),
        'outline': structured_outline
    }


def main():
    parser = argparse.ArgumentParser(description="Competitor SERP Crawler & Structure Analyzer")
    parser.add_argument("urls", nargs="+", help="Competitor URLs to analyze")
    parser.add_argument("--min-words", type=int, default=200, help="Minimum word count threshold (default: 200)")
    parser.add_argument("--output", type=str, default="knowledge/raw/competitors_analysis.json", help="Output JSON path")

    args = parser.parse_args()

    results = []
    for url in args.urls:
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            continue
        analyzed = analyze_url(url, min_words=args.min_words)
        if analyzed:
            results.append(analyzed)

    print(f"\n==========================================")
    print(f"ANALYSIS SUMMARY: {len(results)} / {len(args.urls)} URLs valid")
    print(f"==========================================")

    for idx, item in enumerate(results, 1):
        print(f"\n--- Competitor #{idx}: {item['url']} ---")
        print(f"Title      : {item['title']}")
        print(f"Total Words: ~{item['total_words']} words")
        print(f"Outline Structure:")
        for sec in item['outline']:
            indent = "  " if sec['level'] in ('H2', 'INTRO') else "    "
            print(f"{indent}- [{sec['level']}] {sec['title']} (~{sec['word_count']} words)")

    # Ensure target dir exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nSaved structured report to: {args.output}")

if __name__ == "__main__":
    main()

