---
title: "The Python Tool I Built in a Weekend That Now Pays My Rent"
url: https://medium.com/p/bbc5b81a0bdd
---

# The Python Tool I Built in a Weekend That Now Pays My Rent

[Original](https://medium.com/p/bbc5b81a0bdd)

Member-only story

# The Python Tool I Built in a Weekend That Now Pays My Rent

## How I turned a tiny automation script into a paid product using libraries, clean OOP, and a little C++ speed where it mattered

[![Suleman Safdar](https://miro.medium.com/v2/resize:fill:64:64/1*BKwDm_CmQ4ES1PwGhAY4VQ.jpeg)](https://medium.com/@SulemanSafdar?source=post_page---byline--bbc5b81a0bdd---------------------------------------)

[Suleman Safdar](https://medium.com/@SulemanSafdar?source=post_page---byline--bbc5b81a0bdd---------------------------------------)

6 min read

·

Aug 12, 2025

--

94

Listen

Share

More

Press enter or click to view image in full size

![]()

I built this thing because I was tired of doing the same boring clicks every week. I wanted a tool that would: watch a folder, extract data from PDFs, enrich it, push reports, and — ideally — bill somebody for the time it saved. Two weekends, a few libraries, and many later I had a product people actually paid for.

Below I’ll show you the exact stack, architecture, monetization moves, and code patterns I used so you can build something similar. Expect practical code, OOP structure, and one small C++ trick for when Python alone felt sluggish.

## 1. The problem I solved (and why you should pick a small, painful task)

Most automation projects die because they try to fix everything. Instead, pick one repetitive pain with a measurable ROI. Mine was:

* Client sends invoices as scattered PDFs every day.
* I manually open them, extract vendor, date, amount, and drop into a Google Sheet.
* ~20 minutes/day wasted.

> **Goal:** reduce that to zero human-minutes and offer it as a paid service.

## 2. The quick MVP — building a file-watcher + PDF extractor

Start small: watch a folder, detect new PDF, extract text. Use `watchdog` + `PyMuPDF` (fitz).

```
pip install watchdog pymupdf
```

```
# file_watcher.py  
import time  
from watchdog.observers import Observer  
from watchdog.events import FileSystemEventHandler  
import fitz  # pymupdf  
  
class PDFHandler(FileSystemEventHandler):  
    def on_created(self, event):  
        if event.src_path.lower().endswith(".pdf"):  
            print(f"[+] New PDF: {event.src_path}")  
            text = extract_text(event.src_path)  
            print(text[:200], "...\n")  # quick preview  
  
def extract_text(path: str) -> str:  
    doc = fitz.open(path)  
    pages = []  
    for page in doc:  
        pages.append(page.get_text())  
    doc.close()  
    return "\n".join(pages)  
  
if __name__ == "__main__":  
    observer = Observer()  
    handler = PDFHandler()  
    observer.schedule(handler, path="./inbox", recursive=False)  
    observer.start()  
    try:  
        while True:  
            time.sleep(1)  
    except KeyboardInterrupt:  
        observer.stop()  
    observer.join()
```

That single script already cut my daily work to 5 minutes — mostly for review.

## 3. Make the extractor robust: OCR + text fallback

Some PDFs are scanned images. Add `pytesseract` fallback.

```
pip install pytesseract pillow  
# tesseract must also be installed on the system (apt / brew / choco)
```

```
from PIL import Image  
import pytesseract  
import fitz  
  
def extract_text_with_ocr(path: str) -> str:  
    doc = fitz.open(path)  
    aggregated = []  
    for page in doc:  
        text = page.get_text()  
        if text.strip():  
            aggregated.append(text)  
        else:  
            pix = page.get_pixmap(dpi=200)  
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  
            aggregated.append(pytesseract.image_to_string(img))  
    doc.close()  
    return "\n".join(aggregated)
```

This hybrid approach (text layer -> OCR) made the tool reliable across 95% of invoices I saw.

## 4. Structure with OOP — build a plugin-friendly pipeline

If you want to productize, make your pipeline modular. Each step is a class: Loader → Parser → Enricher → Sink. This lets you swap storage (Google Sheets, DB, webhook) without rewriting.

```
# pipeline.py  
from abc import ABC, abstractmethod  
from typing import Dict  
  
class Step(ABC):  
    @abstractmethod  
    def run(self, data: Dict) -> Dict:  
        pass  
  
class Loader(Step):  
    def __init__(self, path): self.path = path  
    def run(self, data):   
        data['text'] = extract_text_with_ocr(self.path)  
        return data  
  
class Parser(Step):  
    def run(self, data):  
        # naive example; replace with regex or NLP later  
        text = data['text']  
        data['vendor'] = find_vendor(text)  
        data['amount'] = find_amount(text)  
        return data  
  
class Sink(Step):  
    def run(self, data):  
        push_to_google_sheet(data)  
        return data  
  
class Pipeline:  
    def __init__(self, steps):  
        self.steps = steps  
    def execute(self, initial):  
        data = initial  
        for step in self.steps:  
            data = step.run(data)  
        return data
```

> This pattern scales: add `ClassifierStep` for language detection, `TranslatorStep` for non-English docs, etc.

## 5. Enrichment and extraction — regex then ML

Start with deterministic parsing (regex). If invoices are messy or multi-layout, add an ML model (or use `layout-parser`). Example regex snippet:

```
import re  
  
AMOUNT_RE = re.compile(r"(?<!\d)(?:USD|EUR|\$)?\s?([\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b")  
  
def find_amount(text: str) -> float | None:  
    m = AMOUNT_RE.search(text.replace("\n", " "))  
    if m:  
        s = m.group(1).replace(',', '')  
        return float(s)  
    return None
```

For more reliability, use `spacy` + custom NER or `layout-parser` to detect invoice fields spatially.

## 6. Web automation and scraping — Playwright for downloads & dashboards

When invoices are behind web dashboards, automate downloads with Playwright.

```
pip install playwright  
playwright install
```

```
from playwright.sync_api import sync_playwright  
  
def login_and_download(url, user, password, download_path):  
    with sync_playwright() as p:  
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()  
        page.goto(url)  
        page.fill('#username', user)  
        page.fill('#password', password)  
        page.click('#login')  
        page.wait_for_selector('a.download')  
        with page.expect_download() as download_info:  
            page.click('a.download')  
        download = download_info.value  
        download.save_as(download_path)  
        browser.close()
```

This lets your service collect source PDFs automatically — critical if you want to run a subscription where the system fetches customer docs each morning.

## 7. Packaging the tool — CLI with `Typer` / `Click`

For distribution, wrap functionality as a CLI so non-dev customers can run it locally or you can run it on servers.

```
pip install typer
```

```
# cli.py  
import typer  
from pipeline import Pipeline, Loader, Parser, Sink  
  
app = typer.Typer()  
  
@app.command()  
def process(path: str):  
    steps = [Loader(path), Parser(), Sink()]  
    p = Pipeline(steps)  
    p.execute({})  
    typer.echo("Processed!")  
  
if __name__ == "__main__":  
    app()
```

Build a `setup.py` / `pyproject.toml` and publish to PyPI, or package as a wheel / Docker image.

## 8. When Python is too slow — speed it up with C++ (pybind11) or Cython

For heavy image processing or large-scale OCR pre-processing, Python can be a bottleneck. I had one step (a custom image transform) that needed to run on thousands of pages/day. I rewrote it in C++ and exposed it to Python via `pybind11`.

Sketch of approach:

1. Write the heavy function in C++.
2. Wrap with `pybind11`.
3. Import the compiled module in Python normally.

This tiny rewrite reduced that step from ~120ms/page to ~10ms/page.

## 9. Scale with workers: Celery + Redis (or FastAPI + background tasks)

When your user base grows, run processing work in worker queues instead of blocking everything.

```
pip install celery redis
```

```
# tasks.py  
from celery import Celery  
from pipeline import Pipeline, Loader, Parser, Sink  
  
app = Celery('tasks', broker='redis://localhost:6379/0')  
  
@app.task  
def process_file(path):  
    steps = [Loader(path), Parser(), Sink()]  
    Pipeline(steps).execute({})
```

Your web front-end/API enqueues `process_file.delay(path)` and returns immediately. Workers pick up processing and push results to storage.

## 10. Observability & reliability — logs, metrics, retriable steps

Use `loguru` + structured logs, and export metrics (Prometheus) for uptime, queue lengths, and failure rates.

```
pip install loguru
```

```
from loguru import logger  
logger.add("service.log", rotation="10 MB", level="INFO")  
  
try:  
    process_file("/tmp/a.pdf")  
except Exception as e:  
    logger.exception("Processing failed")
```

Design your pipeline steps to be idempotent and retriable (so retries don’t duplicate downstream side effects).

## 11. Monetization strategies — from gigs to SaaS

How I turned this into money:

* **Freelance gigs (early revenue):** I offered to automate invoice processing for a few local clients. Quick wins, minimal support.
* **Per-document pricing:** charge per processed invoice (e.g., $0.10–$0.50) — great for volume clients.
* **Monthly subscription:** host the service, run ingestion (Playwright or SFTP), and charge for convenience + SLA.
* **White-label / enterprise:** integrate into an accounting platform; charge setup + monthly fee.
* **Market/Template sales:** sell trained parsers / prompt templates (e.g., “Indian GST invoice parser”) as one-time purchases.

Key tactics that helped me convert leads:

* Two-week free trial (ingest their first 50 invoices for free).
* Transparent accuracy report (show parsed vs manual).
* Offer human-in-the-loop correction for low-confidence matches (adds revenue).

## Appendix — a minimal repo skeleton (big code block — your starting point)

Use this as the scaffold for a real project.

```
invoice-automator/  
├─ pyproject.toml  
├─ README.md  
├─ src/  
│  ├─ automator/  
│  │  ├─ __init__.py  
│  │  ├─ cli.py  
│  │  ├─ pipeline.py  
│  │  ├─ loaders.py        # Loader classes (filesystem, download)  
│  │  ├─ parsers.py        # regex / NLP parsers  
│  │  ├─ ocr.py            # OCR utils and fallback  
│  │  ├─ enrichers.py      # currency normalization, vendor lookup  
│  │  ├─ sinks.py          # google sheets / db / webhook sinks  
│  │  └─ utils.py  
│  └─ tests/  
│     ├─ test_parsers.py  
│     └─ test_pipeline.py  
├─ docker/  
│  ├─ Dockerfile  
│  └─ prod-compose.yml  
└─ infra/  
   └─ celery_worker.yml
```

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!