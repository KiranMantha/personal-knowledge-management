---
title: "Microsoft Excel: Basic PowerQuery — Stock Price Data From Google Sheets"
url: https://medium.com/p/7354438c0882
---

# Microsoft Excel: Basic PowerQuery — Stock Price Data From Google Sheets

[Original](https://medium.com/p/7354438c0882)

# Microsoft Excel: Basic PowerQuery — Stock Price Data From Google Sheets

[![Don Tomoff](https://miro.medium.com/v2/resize:fill:64:64/1*2S218mUbiUjOvnvrkDc9Dw@2x.jpeg)](/@dtomoffcpa?source=post_page---byline--7354438c0882---------------------------------------)

[Don Tomoff](/@dtomoffcpa?source=post_page---byline--7354438c0882---------------------------------------)

4 min read

·

Jun 12, 2017

--

5

Listen

Share

More

Many investors and finance professionals work with public company stock quotes.

If that applies to you, here is a simple Google Sheets → Excel PowerQuery combination to simplify and streamline that process for you.

***If you would like a copy of the Excel file — with the PowerQuery import (with modifications),*** [***you can get it here***](https://goo.gl/forms/OLZkNdgC6nWxPgjE3)***.***

## Google Sheets

### Set up Google Spreadsheet

* Set up a Google spreadsheet with the parameters you want. The image below highlights one example using the JM Smucker Company (SJM). Setting the symbol and Start Date as variables gives you the flexibility to change the symbol and generate the same data for a different company.
* So, I enter the symbol (“SJM”) and the Start Date (“January 1, 2000”). The end date is always today’s date — see image below.

Press enter or click to view image in full size

![]()

* The TODAY() function is used to populate the end date.

Press enter or click to view image in full size

![]()

* Now, create the Data Table (we use the =GOOGLEFINANCE function for this).

Press enter or click to view image in full size

![]()

Here is the completed GOOGLEFINANCE function:

**=GOOGLEFINANCE(a2, “all”, B2, C2, “DAILY”)**

* Cell A2 = **SYMBOL**
* **“all”** requests all available historical information
* Cell B2 = **START DATE**
* Cell C2 = **END DATE**
* **“DAILY”** — I want information returned on a DAILY basis (weekly, monthly are other options — Daily provides the most flexibility for analysis purposes)

### Prepare Data to be Queried by Excel (PowerQuery)

**1 — “Publish” the Google Spreadsheet**

Next, I will publish the Google sheet so that I can import the data into Excel (using PowerQuery).

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

## Microsoft Excel

**1 — Import Table into Excel**

Now, we are ready to import data into Excel!

* Access the PowerQuery add-in and select “Get External Data” → “From Web”

Press enter or click to view image in full size

![]()

* Paste the URL link copied earlier into the dialog box that appears.
* Next, select Table with data and select Edit to modify query. This is where we SHAPE the data in format we want for Excel (and analysis purposes).

Press enter or click to view image in full size

![]()

**2 — Edit Query to Shape Data Table**

Press enter or click to view image in full size

![]()

* Final modified query — and data load into Excel

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Now, we are ready to perform some data analysis…and the fun starts!

## Final Notes

* **Updating the Google Sheet** — whenever you open the Google Spreadsheet, the GOOGLEFINANCE function updates the data table. Do this step so that Excel imports the most current data.
* **Want a different Company symbol?** Simply change the symbol to whatever you want. (Make sure you EDIT PowerQuery to show proper symbol in imported table!)
* **Need a longer (or shorter) period of time?** Change the beginning date cell — that’s it!
* This process can be easily modified for multiple symbols — allowing peer group or industry analysis!

### About Don

![]()

> “On a mission to challenge the status quo to a more productive and effective end…”

Don is passionate about helping professionals and organizations keep up and adapt to the changing business world that we operate in.

### “What Do You Do?”

I frequently get this question. My response? [Check it out here!](http://bit.ly/2pQwFdi)

### Connect with Don!

[LinkedIn](https://www.linkedin.com/in/dontomoff), [Flipboard](https://flipboard.com/@dtomoff), [Twitter](https://twitter.com/@dtomoffcpa), [Snapchat](https://www.snapchat.com/add/dtomoff)

[Or, just Google me…I’m everywhere](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=don%20tomoff%2C%20invenio%20advisors)