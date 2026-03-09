---
title: "15 Python Nano-Scripts That Automate Actual Business Problems (3-Lines or Less)"
url: https://medium.com/p/5bbaa2c3716f
---

# 15 Python Nano-Scripts That Automate Actual Business Problems (3-Lines or Less)

[Original](https://medium.com/p/5bbaa2c3716f)

Member-only story

# 15 Python Nano-Scripts That Automate Actual Business Problems (3-Lines or Less)

## Scripts Used by Fortune 500 Companies

[![Abdur Rahman](https://miro.medium.com/v2/resize:fill:64:64/1*L6qxuEdgGIfD_4Jbg_1U9g.jpeg)](https://medium.com/@abdur.rahman12?source=post_page---byline--5bbaa2c3716f---------------------------------------)

[Abdur Rahman](https://medium.com/@abdur.rahman12?source=post_page---byline--5bbaa2c3716f---------------------------------------)

3 min read

·

Jul 5, 2025

--

11

Listen

Share

More

Press enter or click to view image in full size

![]()

> Most folks think you need 10,000 lines of code to build something useful.  
> But Fortune 500s? They run on scripts barely longer than your coffee order.

In this post, I’ll share 15 ultra-compact Python snippets — each under 3 lines — that automate real workflows used by companies you’ve definitely heard of. These are the kinds of things that save hours in enterprise operations but look deceptively simple on the surface. And that’s the point.

Let’s go.

## 1. Auto-Cleanup Email Attachments (Outlook Integration)

🧹 *Used by finance teams to sort incoming vendor invoices.*

```
import win32com.client    
[att.SaveAsFile(f"C:/invoices/{att.FileName}") for att in win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI").Folders.Item("Inbox").Items if att.Attachments.Count]
```

## 2. Download Daily Stock Prices (via Yahoo Finance)

💹 *Pulled into dashboards at several hedge funds.*

```
import yfinance as yf    
yf.download("AAPL", period="1d").to_csv("aapl_today.csv")
```

## 3. Auto-Generate PDF Reports from Excel

📊 *Used weekly by ops teams.*

```
import pandas as pd; import pdfkit    
pdfkit.from_string(pd.read_excel("report.xlsx").to_html(), "summary.pdf")
```

## 4. Slack Notification on File Drop

📥 *Triggers when a CSV lands in a folder. Yes, it works cross-platform.*

```
import os, time, requests    
while not os.path.exists("report.csv"): time.sleep(5)    
requests.post("https://slack.webhook.url", json={"text": "New report.csv uploaded!"})
```

## 5. Merge Multiple PDFs into One

🧾 *HR uses this for onboarding packets.*

```
from PyPDF2 import PdfMerger    
PdfMerger().append("a.pdf"); PdfMerger().append("b.pdf"); PdfMerger().write("merged.pdf")
```

## 6. Auto-Resize All Images in a Folder

🖼️ *Used by the creative team*

```
from PIL import Image    
[Image.open(f).resize((800,600)).save(f"resized_{f}") for f in os.listdir() if f.endswith(".png")]
```

## 7. Summarize a Legal Document in Plain English

📃 *Legal teams at tech firms use this to draft summaries before client calls.*

```
import openai    
print(openai.ChatCompletion.create(model="gpt-4o", messages=[{"role":"user","content":open("nda.txt").read()+"\nSummarize in plain English."}]))
```

## 8. Extract Key Points from Zoom Transcripts

🎙️ *Sales teams run this after every demo call.*

```
import openai    
transcript = open("zoom_transcript.txt").read()    
print(openai.ChatCompletion.create(model="gpt-4o", messages=[{"role":"user","content":f"Summarize this call:\n{transcript}"}]))
```

## 9. Auto-Send Reminder Emails from Excel List

📬 *Still the easiest CRM workaround on Earth.*

```
import pandas as pd, smtplib    
[smtplib.SMTP("smtp.gmail.com",587).sendmail("me@gmail.com", row["email"], "Reminder!") for _, row in pd.read_excel("contacts.xlsx").iterrows()]
```

## 10. Quick Sentiment Score on Tweets

🐦 *Marketing analysts use this to track brand mood swings.*

```
from textblob import TextBlob    
print([TextBlob(tweet).sentiment.polarity for tweet in open("tweets.txt")])
```

## 11. Create Word Clouds from Annual Reports

☁️ *Data viz interns eat this up.*

```
from wordcloud import WordCloud    
WordCloud().generate(open("10K.txt").read()).to_file("cloud.png")
```

## 12. Keyword Frequency Counter for Competitor Websites

🔍 *Product teams use this to reverse-engineer feature language.*

```
import requests; from collections import Counter    
print(Counter(requests.get("https://competitor.com").text.lower().split()))
```

## 13. Auto-Classify Customer Support Tickets

🎫 *Saved one client over 40 hours/week in triage.*

```
import openai, pandas as pd    
df = pd.read_csv("tickets.csv"); df["category"] = df["text"].apply(lambda x: openai.ChatCompletion.create(model="gpt-4o", messages=[{"role":"user","content":f"Classify: {x}"}])["choices"][0]["message"]["content"])
```

## 14. One-Click Web Scraper for Job Listings

💼 *Recruiting teams love this one.*

```
import requests; from bs4 import BeautifulSoup    
print([job.text for job in BeautifulSoup(requests.get("https://example.com/jobs").text, "html.parser").find_all("h2")])
```

## 15. Auto-Back Up Google Sheets to Local CSV

🔐 *Seriously underrated. Even execs use this one.*

```
import gspread; import pandas as pd    
df = pd.DataFrame(gspread.service_account().open("Sheet1").sheet1.get_all_records()); df.to_csv("backup.csv", index=False)
```

> [**Master Python Faster! 🚀 Grab Your FREE Ultimate Python Cheat Sheet — Click Here to Download!**](https://abdurrahman12.gumroad.com/l/cheat-sheat)

*If you enjoyed reading, be sure to give it* ***50******CLAPS!******Follow*** *and don’t miss out on any of my future posts —* ***subscribe*** *to my profile for must-read blog updates!*

***Thanks for reading!***

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/@InPlainEnglish) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Twitch**](https://twitch.tv/inplainenglish)
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)