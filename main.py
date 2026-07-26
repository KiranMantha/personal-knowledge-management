import os
import re
import json
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from urllib.parse import urlparse
from pathlib import Path

# ==================== CONFIG ====================
LISTS_DIR = 'lists'
OUTPUT_BASE_DIR = 'medium_md'
INDEX_PATH = os.path.join(OUTPUT_BASE_DIR, 'index.json')

STATUS_SAVED = 'saved'
STATUS_REMOVED = 'removed'   # permanent failure (blog gone), never retry
STATUS_FAILED = 'failed'     # transient failure, retry next run

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

def load_index():
    if not os.path.isfile(INDEX_PATH):
        return {}
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  Could not read index {INDEX_PATH}: {e}")
        return {}

def save_index(index):
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, sort_keys=True)

def read_frontmatter_url(fpath):
    """Parse the url: value out of a saved article's --- frontmatter block."""
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = [next(f, '').strip() for _ in range(10)]
    except Exception:
        return None

    if not lines or lines[0] != '---':
        return None

    for line in lines[1:]:
        if line == '---':
            break
        if line.startswith('url:'):
            return line.removeprefix('url:').strip()
    return None

def find_md_for_url(out_dir, url):
    """Scan out_dir's .md files for one whose frontmatter url: matches. Used only during index bootstrap."""
    if not os.path.isdir(out_dir):
        return None
    for fname in os.listdir(out_dir):
        if not fname.lower().endswith('.md'):
            continue
        fpath = os.path.join(out_dir, fname)
        if read_frontmatter_url(fpath) == url:
            return fname
    return None

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

            # Skip bare homepage/domain links (not an actual article)
            if urlparse(href).path.strip('/') == '':
                continue

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
    """Returns (status, markdown_or_None). status is one of STATUS_SAVED/STATUS_REMOVED/STATUS_FAILED."""
    try:
        resp = session.get(url, timeout=15)

        if resp.status_code in (404, 410):
            print(f"  Gone ({resp.status_code}) → treating as removed")
            return STATUS_REMOVED, None

        resp.raise_for_status()

        if len(resp.text) < 2000:
            print(f"  Suspicious short response ({len(resp.text)} chars) → likely blocked/paywall")
            return STATUS_FAILED, None

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
            return STATUS_FAILED, None

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

        return STATUS_SAVED, frontmatter + md

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else None
        if status_code in (404, 410):
            print(f"  Gone ({status_code}) → treating as removed")
            return STATUS_REMOVED, None
        print(f"  Request failed {url}: {str(e)}")
        return STATUS_FAILED, None
    except requests.exceptions.RequestException as e:
        print(f"  Request failed {url}: {str(e)}")
        return STATUS_FAILED, None
    except Exception as e:
        print(f"  Conversion error {url}: {str(e)}")
        return STATUS_FAILED, None

def save_markdown(out_dir, title, md):
    safe_name = re.sub(r'[<>:"/\\|?*]', '', title).strip()
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
    return os.path.basename(fpath)

def main():
    if not os.path.isdir(LISTS_DIR):
        print(f"Error: '{LISTS_DIR}' not found.")
        return

    session = requests.Session()
    session.cookies.update(COOKIES)
    session.headers.update(HEADERS)

    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
    total_saved = 0
    index = load_index()

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

        list_index = index.setdefault(list_name, {})

        saved = 0
        skipped = 0
        removed = 0
        failed = 0

        for art in articles:
            url = art['url']
            entry = list_index.get(url)

            # Already known (from a previous run) — never re-fetch saved or removed.
            if entry and entry.get('status') in (STATUS_SAVED, STATUS_REMOVED):
                skipped += 1
                continue

            # URL not yet in the index (or index has no file for it): check disk
            # directly, before making any network call, so a file already saved
            # there — from a previous run, crash, or manual copy — is never re-fetched
            # or duplicated.
            existing_fname = find_md_for_url(out_dir, url)
            if existing_fname:
                list_index[url] = {'status': STATUS_SAVED, 'title': art['title'], 'file': existing_fname}
                skipped += 1
                continue

            print(f"    → {art['title'][:60]}")
            status, md = fetch_article_to_markdown(session, url, art['title'])

            if status == STATUS_SAVED and md:
                fname = save_markdown(out_dir, art['title'], md)
                list_index[url] = {'status': STATUS_SAVED, 'title': art['title'], 'file': fname}
                saved += 1
                total_saved += 1
            elif status == STATUS_REMOVED:
                list_index[url] = {'status': STATUS_REMOVED, 'title': art['title']}
                removed += 1
            else:
                list_index[url] = {'status': STATUS_FAILED, 'title': art['title']}
                failed += 1

            # Persist after every article so a crash/interrupt never loses progress
            # or forces a re-fetch/duplicate on the next run.
            save_index(index)

        print(f"  Saved {saved}, skipped {skipped}, removed {removed}, failed {failed} for '{list_name}'\n")

    print(f"Finished. Total MD files: {total_saved}")
    print(f"Output folder: {os.path.abspath(OUTPUT_BASE_DIR)}")

if __name__ == "__main__":
    main()
