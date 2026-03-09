---
title: "I Copy These 10 Code Snippets Into Every Project"
url: https://medium.com/p/8410176ca560
---

# I Copy These 10 Code Snippets Into Every Project

[Original](https://medium.com/p/8410176ca560)

Member-only story

# I Copy These 10 Code Snippets Into Every Project

[![Babar saad](https://miro.medium.com/v2/resize:fill:64:64/1*dOGn91DVBmBvh_Psd_4o3w.jpeg)](https://sa82912045.medium.com/?source=post_page---byline--8410176ca560---------------------------------------)

[Babar saad](https://sa82912045.medium.com/?source=post_page---byline--8410176ca560---------------------------------------)

3 min read

·

Aug 18, 2025

--

8

Listen

Share

More

## The tiny utilities that save me from bugs, wasted time, and StackOverflow rabbit holes

Press enter or click to view image in full size

![]()

You know that feeling when you spin up a new repo and think:  
 **“Didn’t I already write this function somewhere before?”**

Yeah — I’ve been there. Too many times.

So after building dozens of React, Node, and full-stack apps, I stopped reinventing the wheel. I curated a **toolbox of 10 battle-tested snippets** that I now paste into every single project.

They’re not flashy. They’re not frameworks.  
 But they’re the helpers I trust the most.

Here they are — with real-world use cases.

## 1. Debounce Function

Prevents over-triggering on scroll, resize, or input change events.

```
export function debounce(func, delay = 300) {  
  let timeout;  
  return (...args) => {  
    clearTimeout(timeout);  
    timeout = setTimeout(() => func(...args), delay);  
  };  
}
```

**Use case:** Live search that waits for users to stop typing.

```
const handleChange = debounce((val) => searchUsers(val), 400);
```

## 2. Format Date to Readable String

Never Google date formatting again.

```
export function formatDate(dateStr, locale = "en-US") {  
  return new Date(dateStr).toLocaleDateString(locale, {  
    year: "numeric",  
    month: "short",  
    day: "numeric",  
  });  
}
```

**Use case:** Showing `Apr 22, 2025` in dashboards or receipts.

## 3. ClassNames Utility

Because conditional classes shouldn’t look messy.

```
export function classNames(...args) {  
  return args.filter(Boolean).join(" ");  
}
```

**Use case:**

```
<button className={classNames("btn", isActive && "btn-primary")} />
```

## 4. Safe JSON Parse

Handles malformed localStorage or API responses without crashing.

```
export function safeJsonParse(str, fallback = {}) {  
  try {  
    return JSON.parse(str);  
  } catch {  
    return fallback;  
  }  
}
```

**Use case:**

```
const user = safeJsonParse(localStorage.getItem("user"));
```

## 5. IsEmpty Object

Better than `Object.keys(obj).length === 0`.

```
export function isEmpty(obj) {  
  return obj && Object.keys(obj).length === 0 && obj.constructor === Object;  
}
```

**Use case:**

```
if (isEmpty(formErrors)) submitForm();
```

## 6. Copy to Clipboard

Because every app has a “copy link” button.

```
export async function copyToClipboard(text) {  
  try {  
    await navigator.clipboard.writeText(text);  
    return true;  
  } catch (err) {  
    console.error("Copy failed:", err);  
    return false;  
  }  
}
```

**Use case:**

```
<button onClick={() => copyToClipboard(url)}>Copy</button
```

## 7. Capitalize First Letter

Tiny detail. Big polish.

```
export function capitalize(str) {  
  return str.charAt(0).toUpperCase() + str.slice(1);  
}
```

**Use case:**

```
capitalize("pending"); // "Pending"
```

## 8. Sleep Helper

For throttled operations, loaders, or animations.

```
export function sleep(ms) {  
  return new Promise((resolve) => setTimeout(resolve, ms));  
}
```

**Use case:**

```
await sleep(1000);  
// show loader for minimum 1
```

## 9. Remove Duplicates From Array

Keep arrays clean with zero boilerplate.

```
export function uniqueArray(arr) {  
  return [...new Set(arr)];  
}
```

**Use case:**

```
const tags = uniqueArray([...userTags, ...defaultTags]);
```

## 10. Download Any File from URL

Instantly trigger file downloads.

```
export function downloadFile(url, filename) {  
  const a = document.createElement("a");  
  a.href = url;  
  a.download = filename;  
  document.body.appendChild(a);  
  a.click();  
  document.body.removeChild(a);  
}
```

**Use case:**

```
downloadFile("/resume.pdf", "MyResume.pdf");
```

## Bonus: Keep Them Organized

I drop these into `/utils` in most React/Next.js projects:

```
/utils  
  ├── debounce.js  
  ├── formatDate.js  
  ├── classNames.js  
  ├── jsonHelpers.js  
  ├── clipboard.js  
  └── etc...
```

Then I import as needed:

```
import { debounce, formatDate, copyToClipboard } from "@/utils";
```

## Why These Matter

* Prevent sneaky bugs
* Keep code clean and consistent
* Save hours of StackOverflow searching
* Work across any frontend or full-stack project

You don’t need 1,000 helper functions.  
 You just need **10 you actually trust**.

## Takeaways

* Curate your own snippet library
* Build a starter kit for new projects
* Use small utilities to avoid big bugs

These 10 won’t make you a 10x dev.  
 But they’ll make you a **10x faster one**.

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!