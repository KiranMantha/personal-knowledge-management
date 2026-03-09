---
title: "Why 100vh Is Still Broken on Mobile and How to Fix 100vh"
url: https://medium.com/p/054b290270e7
---

# Why 100vh Is Still Broken on Mobile and How to Fix 100vh

[Original](https://medium.com/p/054b290270e7)

Member-only story

# Why 100vh Is Still Broken on Mobile and How to Fix 100vh on Mobile Safari

## **The simplest CSS unit turns into chaos the moment Safari shows a URL bar**

[![Sanjeevani Bhandari](https://miro.medium.com/v2/resize:fill:64:64/1*Sj1DOUmlNi9JaXsD5oKm1w.jpeg)](/@sanjeevanibhandari3?source=post_page---byline--054b290270e7---------------------------------------)

[Sanjeevani Bhandari](/@sanjeevanibhandari3?source=post_page---byline--054b290270e7---------------------------------------)

2 min read

·

Jan 11, 2026

--

Listen

Share

More

Press enter or click to view image in full size

![]()

You build a clean hero section.

Full screen.  
Perfectly centered.  
Looks amazing on desktop.

Then you open it on mobile… and suddenly the layout jumps like it’s possessed.

Your “100vh” section becomes too tall.  
Or too short.  
Or it changes height while scrolling.

And the worst part?

**It doesn’t look broken in dev tools.  
It looks broken only when real humans touch it.**

## So why is `100vh` still broken?

Because mobile browsers don’t treat height like desktop browsers do.

On desktop:

* `100vh` = visible browser viewport height

On mobile:

* the browser has UI controls (address bar, bottom nav)
* those controls expand and collapse while scrolling
* the “visible area” changes constantly

But `100vh` often uses the *largest possible height* (including the hidden browser chrome), not the currently visible screen.

So your layout is sized for a screen that doesn’t actually exist most of the time.

## The classic symptom

```
.hero {  
  height: 100vh;  
}
```

On mobile Safari/Chrome, this can:

* push content under the bottom bar
* cause extra scroll
* create weird whitespace
* jump when the address bar hides

It feels like the page is breathing.

## The modern fix (finally)

Use the new viewport units:

```
.hero {  
  height: 100dvh;  
}
```

* `dvh` = dynamic viewport height (updates as UI changes)
* `svh` = small viewport height (safe, smallest view)
* `lvh` = large viewport height (max possible view)

Most of the time, `100dvh` **is what you wanted** `100vh` **to be**.

## `"100vh` isn’t wrong”

> Mobile viewports are.

And once you accept that the browser UI is part of the layout problem, you stop fighting ghosts and start using the right units.

***Thanks for reading. If this saved you a layout headache, feel free to follow.***