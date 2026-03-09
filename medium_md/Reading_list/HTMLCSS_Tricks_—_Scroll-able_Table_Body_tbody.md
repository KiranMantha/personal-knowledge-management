---
title: "HTML/CSS Tricks — Scroll-able Table Body <tbody>"
url: https://medium.com/p/d23182ae0fbc
---

# HTML/CSS Tricks — Scroll-able Table Body <tbody>

[Original](https://medium.com/p/d23182ae0fbc)

# HTML/CSS Tricks — Scroll-able Table Body <tbody>

[![Rajan V](https://miro.medium.com/v2/resize:fill:64:64/1*_-jfZY0ru3ERO2yRUd2SOA.jpeg)](/?source=post_page---byline--d23182ae0fbc---------------------------------------)

[Rajan V](/?source=post_page---byline--d23182ae0fbc---------------------------------------)

1 min read

·

Sep 5, 2017

--

32

Listen

Share

More

This simple tricks to solve the problem of making table body scroll-able with fixed table headers. This makes the data table easier to use. Fixed table header when user scroll provides the context to user on what column the user is on.

Press enter or click to view image in full size

![]()

*Overflow* property doesn’t apply to table grouping element thead, tbody , tfoot by default. You can see this for yourself in the below pen,

To make it working,

first step will be : setting `<tbody>` to `display:block` so that we can apply the height and overflow property.

next step will be : setting the `<thead><tr>` to `display:block`

So final CSS will be,

```
.fixed_header tbody{  
  display:block;  
  overflow:auto;  
  height:200px;  
  width:100%;  
}.fixed_header thead tr{  
  display:block;  
}
```

The example below,

The markup to create table is simple and semantic. And solves the problem without JavaScript dependency.

***If you have any suggestions for improvements or find any issues please let me know in the comments.***