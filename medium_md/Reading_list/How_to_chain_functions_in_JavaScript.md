---
title: "How to chain functions in JavaScript"
url: https://medium.com/p/6644d44793fd
---

# How to chain functions in JavaScript

[Original](https://medium.com/p/6644d44793fd)

# How to chain functions in JavaScript

[![Jamis Charles](https://miro.medium.com/v2/resize:fill:64:64/2*Hm_iSUpRQU74V2ne_Q50pw.jpeg)](/@jamischarles?source=post_page---byline--6644d44793fd---------------------------------------)

[Jamis Charles](/@jamischarles?source=post_page---byline--6644d44793fd---------------------------------------)

1 min read

·

Aug 12, 2018

--

2

Listen

Share

More

*Originally published at* [*jamischarles.com*](https://jamischarles.com/posts/how-to-chain-functions-in-javascript)*.*

Here’s a question you’ll sometimes encounter in interviews: *How do you write a chaining function similar to jQuery in JavaScript?*

Press enter or click to view image in full size

![]()

The benefit is that we can mutate the same element with several method calls. The key detail is that each method call must return an object with methods we can call.

Here’s how you do it:

Press enter or click to view image in full size

![]()

That’s it.

[![]()](http://eepurl.com/glRNYL)

You should [follow me on twitter](https://twitter.com/jamischarles).