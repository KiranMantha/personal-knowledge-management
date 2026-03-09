---
title: "Stop Writing the Same Code Twice — 10 JavaScript Utility Functions You Should Steal"
url: https://medium.com/p/ec33e599c1ae
---

# Stop Writing the Same Code Twice — 10 JavaScript Utility Functions You Should Steal

[Original](https://medium.com/p/ec33e599c1ae)

# Stop Writing the Same Code Twice — 10 JavaScript Utility Functions You Should Steal

## *Your future self will mass thank you for having these ready before the deadline hits.*

[![Frontend Master](https://miro.medium.com/v2/resize:fill:64:64/1*8LZIQBOKWVS-OOTQ7PQtFw.png)](/?source=post_page---byline--ec33e599c1ae---------------------------------------)

[Frontend Master](/?source=post_page---byline--ec33e599c1ae---------------------------------------)

5 min read

·

Jan 29, 2026

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

Every developer has that moment. You’re deep into a new project, momentum is high, and then you need to… format a date. Or debounce an input. Or parse some sketchy JSON from localStorage without blowing up your entire app.

So you open a new tab. You Google it. You find a Stack Overflow answer from 2017. You copy it. You tweak it. You move on.

**Then you do it again next month.**

I got tired of that loop. So I built a personal utility belt — a small collection of functions that travel with me from project to project like carry-on luggage. None of them are clever. All of them are useful. Here are the 10 I refuse to start a project without.

## 1. The Debouncer — Tame Your Trigger-Happy Events

Scroll handlers, resize listeners, search inputs — they all fire way too often. This tiny wrapper makes them behave.

```
export function debounce(func, wait = 300) {  
  let timer;  
  return (...args) => {  
    clearTimeout(timer);  
    timer = setTimeout(() => func.apply(this, args), wait);  
  };  
}
```

**Where I actually use it:**

```
// Search bar that doesn't assault your API  
const onSearch = debounce((query) => fetchResults(query), 400);  
inputEl.addEventListener("input", (e) => onSearch(e.target.value));
```

Without this, a user typing “react hooks” fires 11 API calls. With it, you get one. Your backend will thank you.

## 2. The Date Whisperer — Because `toLocaleDateString` Has Too Many Options

Date formatting in JavaScript is a solved problem that nobody remembers the solution to.

```
export function formatDate(input, locale = "en-US") {  
  return new Date(input).toLocaleDateString(locale, {  
    year: "numeric",  
    month: "short",  
    day: "numeric",  
  });  
}
```

**Output:** `Jan 29, 2026` — clean, human-readable, locale-aware.

No libraries. No `moment.js` (please stop). Just the `Intl` API doing what it was built for.

## 3. The Class Joiner — Conditional CSS Without the Mess

You don’t need `clsx`. You don't need `classnames`. You need five lines.

```
export function cx(...args) {  
  return args.filter(Boolean).join(" ");  
}
```

**In practice:**

```
<div className={cx("card", isSelected && "card--active", isDisabled && "card--muted")}>
```

Falsy values get filtered out. No `undefined` leaking into your class strings. Done.

## 4. The JSON Safety Net — Parse Without Fear

`JSON.parse` throws. That's its whole personality. Wrap it once, never think about it again.

```
export function safeParse(raw, fallback = null) {  
  try {  
    return JSON.parse(raw);  
  } catch {  
    return fallback;  
  }  
}
```

**Real scenario:**

```
const prefs = safeParse(localStorage.getItem("preferences"), { theme: "light" });
```

Corrupted storage? Weird API response? You get a sensible default instead of a white screen of death.

## 5. The Emptiness Detector — Know When an Object Has Nothing

`{}` is truthy in JavaScript. That catches people off guard constantly.

```
export function isEmptyObject(obj) {  
  return obj != null && typeof obj === "object" && Object.keys(obj).length === 0;  
}
```

**Why it matters:**

```
const errors = validate(formData);  
if (isEmptyObject(errors)) {  
  submit(); // safe to proceed  
}
```

Clean conditionals. No ambiguity.

## 6. The Clipboard Hijacker — One-Click Copy, Zero Drama

Every SaaS app has a “Copy to clipboard” button. Here’s the entire implementation:

```
export async function copyText(text) {  
  try {  
    await navigator.clipboard.writeText(text);  
    return true;  
  } catch {  
    return false;  
  }  
}
```

**Usage:**

```
const success = await copyText(shareableLink);  
if (success) showToast("Copied!");
```

The Clipboard API is async and can fail (permissions, insecure context). This handles both paths without drama.

## 7. The Capitalizer — Small Function, Big Polish

Display “pending” as “Pending” in your UI. That’s it. That’s the function.

```
export function capitalize(str) {  
  if (!str) return "";  
  return str[0].toUpperCase() + str.slice(1);  
}
```

You could inline this. But after the third time you write `str.charAt(0).toUpperCase() + str.slice(1)`, you'll wish you hadn't.

## 8. The Async Pause Button — `sleep()` for JavaScript

Sometimes you need to wait. For an animation. For a rate limit. For dramatic effect.

```
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
```

**Practical use:**

```
async function retryWithBackoff(fn, retries = 3) {  
  for (let i = 0; i < retries; i++) {  
    try { return await fn(); }  
    catch (e) {  
      if (i === retries - 1) throw e;  
      await sleep(1000 * 2 ** i); // 1s, 2s, 4s  
    }  
  }  
}
```

One-liner that makes async flows dramatically easier to reason about.

## 9. The Deduplicator — Clean Arrays in One Line

Duplicate values sneak into arrays when you merge user input, API data, or query params. Kill them.

```
export const dedupe = (arr) => [...new Set(arr)];
```

**Common scenario:**

```
const allTags = dedupe([...userTags, ...suggestedTags, ...defaultTags]);
```

For objects, you’ll need something more involved. For primitives, `Set` is unbeatable.

## 10. The Silent Downloader — Trigger File Downloads Programmatically

No server endpoint needed. No `window.open` hacks. Just a clean, invisible download trigger.

```
export function downloadFile(url, filename) {  
  const link = document.createElement("a");  
  link.href = url;  
  link.download = filename;  
  document.body.appendChild(link);  
  link.click();  
  link.remove();  
}
```

**Usage:**

```
downloadFile(blobUrl, "report-2026.csv");
```

Works with blob URLs, data URLs, and regular file paths. The anchor element does the heavy lifting.

## How I Organize These

I keep a `/lib` or `/utils` directory at the root of every project:

```
/lib  
  ├── debounce.ts  
  ├── format.ts        // formatDate, capitalize  
  ├── guards.ts        // isEmptyObject, safeParse  
  ├── clipboard.ts  
  ├── async.ts         // sleep  
  ├── array.ts         // dedupe  
  └── dom.ts           // downloadFile, cx
```

Then a barrel export:

```
// lib/index.ts  
export * from "./debounce";  
export * from "./format";  
export * from "./guards";  
// ...
```

Import what you need, ignore what you don’t. Tree-shaking handles the rest.

## The Real Point

None of these functions are impressive. That’s the point. They’re boring, reliable, and battle-tested. They prevent the kind of bugs that slip through code review because everyone assumes “that part is trivial.”

Trivial code still needs to work.

Build your own utility belt. Steal these. Modify them. Add your own. The best code you’ll ever write is the code you never have to write again.

*If you found this useful, I write about practical JavaScript, React patterns, and developer tooling. Follow along for more no-fluff engineering content.*

Preparing for a tech interview? I run 1:1 mock interviews for frontend, backend, and full-stack roles —   
 designed to sharpen your performance and increase your chances of landing the offer.

<https://allahabadi.dev/frontend-mock-interview/>