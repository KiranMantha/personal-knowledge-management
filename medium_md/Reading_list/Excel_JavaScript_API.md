---
title: "Excel JavaScript API"
url: https://medium.com/p/49d4d1fbf787
---

# Excel JavaScript API

[Original](https://medium.com/p/49d4d1fbf787)

# Excel JavaScript API

[![Peter James](https://miro.medium.com/v2/resize:fill:64:64/0*JzmzqdSJBW57Zb5Z.jpg)](/@phunt6056?source=post_page---byline--49d4d1fbf787---------------------------------------)

[Peter James](/@phunt6056?source=post_page---byline--49d4d1fbf787---------------------------------------)

3 min read

·

Aug 5, 2019

--

1

Listen

Share

More

![]()

Excel is a very popular way of manipulating and presenting data and writing macros in VBA provided a way of automating Excel tasks.

In Excel 2016, Microsoft released an additional way of automating tasks in Excel, using the Excel JavaScript API. As a high-level overview, looking at Excel from a Developer perspective, Excel is an Object. Excel has properties such as a workbook, the workbook has properties, such as worksheets, those worksheets have properties, such as a name, and methods such as ‘add’. The API allows you to use and manipulate those objects, as you previously would do with VBA, but using JavaScript.

Press enter or click to view image in full size

![]()

> But why learn this?

Increasingly, people are moving into Excel Online to make it easier to share and use workbooks, and VBA does not run in the cloud, you have to save down the workbook to run macros, which slows down the process if you need a quick update. Add-ins do.

VBA can be thought of as manipulating the Excel Object Library with Visual Basics, which is a programming language, just not as widely used as JS. JavaScript is often polled as one of the most popular programming languages, so if you are investing your time into learning a programming language, JavaScript might give a wider range of application.

**Modern features**

It ties in with using a different language, but JavaScript does make some very common data manipulation tasks easier, such as arrow functions. In Excel, if you have a collection of objects, and you need to return the objects where the value is greater than 50 and the currency is GBP, then you need to iterate through each criteria and add these to a new collection. In JavaScript, you can pull these off in a one liner.

```
const filteredObjects = origionalData.filter(m=>m.value>50 && m.fx === ‘GBP’)
```

**Professional feel**

Press enter or click to view image in full size

![]()

I have spent weeks working on projects in VBA to turn around a robust, well thought out macro, but it doesn’t have the professional feel of many modern day applications. Excel Add-Ins use web technology (HTML, CSS, JavaScript) to create the user interface, so you can create professional user interfaces with features of modern websites.

**Heads up**

What are the catches? In terms of conceptualising to production, turning around a macro would be quicker. Macro’s live in the spreadsheet, hitting ‘ALT-F11’ shows all the code that lives in the workbook. Add-Ins are, basically, mini web-applications, they need to be hosted and live in the cloud on a service such as Amazons AWS or Microsoft’s Azure platforms. Visual Studio does make this easy to do with a workflow aimed at making deployment as easy as possible, but it does create additional headwinds you would not have if you created a macro. It might make it easier in the long run to push changes to all your users, but it’s another hurdle none the less.

**Value add**

The real value in Add-Ins comes from the potential to integrate better with other online offerings, for example creating APIs to send data to a central database or linking up with other providers APIs. Using the Script Lab Add-in is a great way to get started.