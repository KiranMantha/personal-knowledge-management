---
title: "How I Built 6 Micro-Tools in Python That Earn Me Passive Income Daily"
url: https://medium.com/p/b9f4f83e9c95
---

# How I Built 6 Micro-Tools in Python That Earn Me Passive Income Daily

[Original](https://medium.com/p/b9f4f83e9c95)

Member-only story

# How I Built 6 Micro-Tools in Python That Earn Me Passive Income Daily

[![Suleman Safdar](https://miro.medium.com/v2/resize:fill:64:64/1*BKwDm_CmQ4ES1PwGhAY4VQ.jpeg)](https://medium.com/@SulemanSafdar?source=post_page---byline--b9f4f83e9c95---------------------------------------)

[Suleman Safdar](https://medium.com/@SulemanSafdar?source=post_page---byline--b9f4f83e9c95---------------------------------------)

4 min read

·

Aug 7, 2025

--

26

Listen

Share

More

*I stopped chasing big projects and started building tiny, high-impact Python scripts. These libraries helped me automate, scale, and monetize fast.*

## 1. Flask + Jinja2: My First $50 Tool Was Just 40 Lines of Code

I launched a micro web app that lets freelancers generate invoice PDFs. No database, no login, just form input → styled HTML → PDF.

**Stack:**

```
pip install flask weasyprint
```

### Code snippet:

```
from flask import Flask, render_template, request  
from weasyprint import HTML  
  
app = Flask(__name__)  
  
@app.route("/", methods=["GET", "POST"])  
def index():  
    if request.method == "POST":  
        html = render_template("invoice.html", data=request.form)  
        HTML(string=html).write_pdf("invoice.pdf")  
        return "Invoice created!"  
    return render_template("form.html")
```

Shared it in 2 Reddit communities. Made $50 by Day 2.

## 2. Streamlit: Turning Python Scripts Into Income-Generating Web Apps

Streamlit turned my data cleaner script into an online app that small Etsy sellers now use to clean their CSV exports.

```
pip install streamlit pandas
```

```
import streamlit as st  
import pandas as pd  
  
uploaded_file = st.file_uploader("Upload your CSV")  
if uploaded_file:  
    df = pd.read_csv(uploaded_file)  
    df_cleaned = df.dropna().drop_duplicates()  
    st.write(df_cleaned)  
    df_cleaned.to_csv("cleaned.csv", index=False)
```

Deployed with Streamlit Cloud → added Payhip checkout before download → $300 in passive downloads.

## 3. FastAPI + Uvicorn: Scalable Backend for My PDF-to-Text API

Created an API that receives a PDF file, extracts text, and returns JSON. Writers and researchers use it.

**Setup:**

```
pip install fastapi uvicorn PyMuPDF
```

```
from fastapi import FastAPI, UploadFile  
import fitz  # PyMuPDF  
  
app = FastAPI()  
  
@app.post("/extract/")  
async def extract_text(file: UploadFile):  
    doc = fitz.open(stream=await file.read(), filetype="pdf")  
    text = "".join([page.get_text() for page in doc])  
    return {"text": text}
```

Added Stripe + rate limiting. $10/month API subscriptions from SEO agencies.

## 4. Selenium + Twilio: My Alert Bot That Texts When Stock Prices Crash

I set up a personal alert system that watches stock prices and sends me a text when anything drops >5%.

**Install:**

```
pip install selenium twilio
```

```
from selenium import webdriver  
from twilio.rest import Client  
  
client = Client("TWILIO_SID", "TWILIO_TOKEN")  
driver = webdriver.Chrome()  
  
driver.get("https://finance.yahoo.com/quote/TSLA")  
price = float(driver.find_element("xpath", '//*[@data-field="regularMarketPrice"]').text)  
  
if price < 600:  
    client.messages.create(  
        body=f"TSLA is below $600: ${price}",  
        from_="+123456789",  
        to="+987654321"  
    )
```

Friends asked for custom versions. I made $180 selling alert bots on Gumroad.

## 5. OpenAI + Gradio: Built a Resume Review App with GPT-4 That Made $400

People upload a resume → it gets critiqued by GPT-4 → feedback shows instantly. Used Gradio for UI and OpenAI API.

```
pip install openai gradio
```

```
import openai, gradio as gr  
  
def review_resume(text):  
    prompt = f"Review this resume and give detailed, actionable feedback:\n\n{text}"  
    res = openai.ChatCompletion.create(  
        model="gpt-4",  
        messages=[{"role": "user", "content": prompt}]  
    )  
    return res['choices'][0]['message']['content']  
  
gr.Interface(fn=review_resume, inputs="textbox", outputs="text").launch()
```

Used LemonSqueezy for $5 one-time payment. Made $400 in 3 weeks from Twitter posts.

## 6. Pandas + Plotly + PDFKit: Monthly Reports for Clients on Autopilot

A B2B client wanted weekly analytics reports. I automated it using `pandas` for data wrangling, `plotly` for charts, and `pdfkit` for rendering.

```
pip install pandas plotly pdfkit
```

```
import pandas as pd, plotly.express as px, pdfkit  
  
df = pd.read_csv("sales.csv")  
fig = px.bar(df, x="week", y="revenue", title="Weekly Revenue")  
fig.write_html("report.html")  
pdfkit.from_file("report.html", "report.pdf")
```

Now I just cron-job it weekly. They pay me $200/month. Total hands-off.

## 7. Python + Notion API: Sell Notion Automation Scripts as Downloads

Used the Notion API to automate dashboards, task resets, and habit logs. Bundled the scripts into downloadable `.py` files with setup instructions.

```
pip install notion-client
```

```
from notion_client import Client  
  
notion = Client(auth="your-secret")  
page = notion.pages.retrieve("page_id")  
print(page["properties"])
```

Packaged 3 automation scripts into a $10 product. Made $850 total via Gumroad and Reddit marketing.

## 8. BeautifulSoup + Flask: Scrape → Render → Sell Niche Web Monitors

Example: A web monitor for local government job listings. Users get notified if new jobs are posted.

```
pip install beautifulsoup4 flask requests
```

```
from bs4 import BeautifulSoup  
import requests  
  
r = requests.get("https://example.com/jobs")  
soup = BeautifulSoup(r.text, "html.parser")  
jobs = soup.find_all("h2", class_="job-title")
```

Flask backend + Google Sheets → Email alerts. Charged $5/month subscription. 20 clients.

## 9. PyPDF2 + OCR + Email Automation: A Document Parser That Clients Love

Lawyers and admins send scanned PDFs → script OCRs them → extracts key info → sends a summary by email.

**OCR Flow:**

* `pdf2image` to convert PDF to image
* `pytesseract` to read text
* `smtplib` to send email

Got two recurring freelance clients ($600/month combined) from just demoing it on Upwork.

## 10. Creating a SaaS With Python + Stripe + Heroku (No JavaScript!)

Used Python for everything. Flask handles the frontend and backend, Stripe handles billing, and Heroku handles deployment.

**Stack:**

* Flask
* Stripe Python SDK
* SQLite
* Bootstrap via CDN

Made a mini-SaaS called “InvoiceMailer” and started getting $5/month users. Scaled to $100 MRR without touching React.

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 200k supporters? **We do not get paid by Medium**!

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder) **and** [**Instagram**](https://instagram.com/sunilsandhu). And before you go, don’t forget to **clap** and **follow** the writer️!