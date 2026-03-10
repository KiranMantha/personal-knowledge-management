import os
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from urllib.parse import urlparse
from pathlib import Path

# ==================== CONFIG ====================
LISTS_DIR = 'lists'
OUTPUT_BASE_DIR = 'medium_md'

# Paste your cookies exactly as key: value pairs
COOKIES = {
    # You can add more if you have them (e.g. 'optimizelyEndUserId', 'ajs_user_id', etc.)
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://medium.com/',
    'Upgrade-Insecure-Requests': '1',
}

def clean_list_name(filename):
    name = filename.removesuffix('.html')
    if '-' in name:
        parts = name.rsplit('-', 1)
        if len(parts[1]) >= 10:  # likely the ID part
            name = parts[0]
    name = re.sub(r'[-_ ]+', '_', name.strip())
    return name or 'Untitled_List'

def extract_articles_from_html(html_path):
    articles = []
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            if 'medium.com' not in href:
                continue
            if any(x in href for x in ['/m/signin', '/tag/', '/me/', '/topic/']):
                continue

            # Clean tracking params
            if '?' in href:
                href = href.split('?')[0]

            title = a.get_text(strip=True)
            if not title or len(title) < 10:
                title = href.split('/')[-1].replace('-', ' ').title() or 'Untitled'

            articles.append({'url': href, 'title': title})

        # Dedup by URL
        seen = set()
        unique = []
        for art in articles:
            if art['url'] not in seen:
                seen.add(art['url'])
                unique.append(art)
        return unique

    except Exception as e:
        print(f"Parse error {html_path}: {e}")
        return []

def fetch_article_to_markdown(session, url, title):
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()

        if len(resp.text) < 2000:
            print(f"  Suspicious short response ({len(resp.text)} chars) → likely blocked/paywall")
            return None

        soup = BeautifulSoup(resp.text, 'lxml')

        body_selectors = [
            'article',
            '[data-test-id="post-content"]',
            '.postArticle-content',
            'section[role="main"]',
        ]
        body = None
        for sel in body_selectors:
            body = soup.select_one(sel)
            if body:
                break

        if not body:
            print(f"  No article body found for {url}")
            return None

        # Clean
        for tag in ['nav', 'header', 'footer', 'aside', '[data-test-id="reactions"]', 'figure figcaption']:
            for el in body.select(tag):
                el.decompose()

        md = markdownify(str(body), heading_style="ATX", autolinks=True)
        md = re.sub(r'\n{3,}', '\n\n', md.strip())

        frontmatter = f"""---
title: "{title.replace('"', '\\"')}"
url: {url}
---

# {title}

[Original]({url})

"""

        return frontmatter + md

    except requests.exceptions.RequestException as e:
        print(f"  Request failed {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"  Conversion error {url}: {str(e)}")
        return None

def main():
    if not os.path.isdir(LISTS_DIR):
        print(f"Error: '{LISTS_DIR}' not found.")
        return

    session = requests.Session()
    session.cookies.update(COOKIES)
    session.headers.update(HEADERS)

    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    total_saved = 0

    html_files = [f for f in os.listdir(LISTS_DIR) if f.lower().endswith('.html')]
    html_files.sort(key=str.lower)

    print(f"Found {len(html_files)} list files.\n")

    for filename in html_files:
        list_name = clean_list_name(filename)
        print(f"Processing list → {list_name} ({filename})")

        out_dir = os.path.join(OUTPUT_BASE_DIR, list_name)
        os.makedirs(out_dir, exist_ok=True)

        path = os.path.join(LISTS_DIR, filename)
        articles = extract_articles_from_html(path)

        print(f"  Found {len(articles)} articles")

        saved = 0
        for art in articles:
            url = art['url']
            print(f"    → {art['title'][:60]}")
            md = fetch_article_to_markdown(session, url, art['title'])

            if md:
                safe_name = re.sub(r'[<>:"/\\|?*]', '', art['title']).strip()
                safe_name = re.sub(r'\s+', '_', safe_name)[:110]
                fname = f"{safe_name or 'article'}.md"

                fpath = os.path.join(out_dir, fname)
                counter = 1
                while os.path.exists(fpath):
                    base, ext = os.path.splitext(fname)
                    fpath = os.path.join(out_dir, f"{base}_{counter}{ext}")
                    counter += 1

                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(md)
                saved += 1
                total_saved += 1

        print(f"  Saved {saved} articles for '{list_name}'\n")

    print(f"Finished. Total MD files: {total_saved}")
    print(f"Output folder: {os.path.abspath(OUTPUT_BASE_DIR)}")

if __name__ == "__main__":
    main()