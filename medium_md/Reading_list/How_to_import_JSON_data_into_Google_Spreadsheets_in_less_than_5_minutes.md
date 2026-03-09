---
title: "How to import  JSON data into Google Spreadsheets in less than 5 minutes"
url: https://medium.com/p/a3fede1a014a
---

# How to import  JSON data into Google Spreadsheets in less than 5 minutes

[Original](https://medium.com/p/a3fede1a014a)

# How to import JSON data into Google Spreadsheets in less than 5 minutes

[![Paul Gambill](https://miro.medium.com/v2/resize:fill:64:64/2*OgMEVtAXUpWAq8vQGvBdRQ.jpeg)](/@paulgambill?source=post_page---byline--a3fede1a014a---------------------------------------)

[Paul Gambill](/@paulgambill?source=post_page---byline--a3fede1a014a---------------------------------------)

2 min read

·

Mar 14, 2014

--

102

Listen

Share

More

I’m writing this only a day after getting home from SXSW 2014. My company, [Deloitte Digital](http://www.deloittedigital.com/), sent me because I led a project to build the [Deloitte Round-Up apps](http://sxsw.deloitte.com/) in conjunction with Deloitte’s sponsorship of the conference. One of the main functions of the microsite we built was to capture recruiting prospects from people visiting the Deloitte booth. We stored the prospect info in a database on [Parse](https://parse.com/).

Almost immediately, the request came in from the recruiting team to get that prospect data. So I exported the table into a JSON file, but felt bad about just handing a JSON file to non-technologists. I had to quickly figure out how to get the data into a spreadsheet.

Using the awesome [ImportJSON](http://blog.fastfedora.com/projects/import-json) tool in combination with this wonderful [script](https://gist.github.com/chrislkeller/5719258), I was able to get the data into a spreadsheet in a matter of minutes. Here’s how:

1. Create a new Google Spreadsheet.
2. Click on Tools -> Script Editor.
3. Click Create script for Spreadsheet.
4. Delete the placeholder content and paste the code from [this script](https://gist.github.com/paulgambill/cacd19da95a1421d3164).
5. Rename the script to ImportJSON.gs and click the save button.
6. Back in the spreadsheet, in a cell, you can type “=ImportJSON()” and begin filling out it’s parameters.

**Example:**

*=ImportJSON(“http://date.jsontest.com", “/date”, “noInherit, noTruncate”)*

with the following raw JSON from [date.jsontest.com](http://date.jsontest.com/):

*{*

*“time”: “05:27:57 AM”,*

*“milliseconds\_since\_epoch”: 1394774877499,*

*“date”: “03-14-2014"*

*}*

will yield:

Press enter or click to view image in full size

![]()

You can read more about the various parameter options at the ImportJSON [project page](http://blog.fastfedora.com/projects/import-json).

Since I was dealing with a JSON data dump, I had to host the file somewhere. The easiest option was Dropbox. It’s important to remember that if you drop a file onto Dropbox and want the raw data supported, you have to change the *www.dropbox.com* portion of the URL to *dl.dropboxusercontent.com.*

Now, when I did this, for various reasons, I had to be able to send an Excel file. Exporting the Google Spreadsheet as an Excel file didn’t work for me in Office for Mac because the macro carried through instead of the raw data. It did, however, work when I opened the .xlsx file in Numbers. I opened it there and then exported to Excel, and voila, I had an Excel spreadsheet with all the JSON data neatly formatted.

> Was this useful to you? If so, would you please recommend this article so that others can benefit from it too? My other articles can be found [here](/@paulgambill).