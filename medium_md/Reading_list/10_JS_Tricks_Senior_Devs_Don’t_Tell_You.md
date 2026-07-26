---
title: "10 JS Tricks Senior Devs Don’t Tell You"
url: https://medium.com/p/dedbab8fb630
---

# 10 JS Tricks Senior Devs Don’t Tell You

[Original](https://medium.com/p/dedbab8fb630)

# 10 JS Tricks Senior Devs Don’t Tell You

[![devonmobile](https://miro.medium.com/v2/resize:fill:64:64/1*y8dGyx2R432It6C--ujVCg.png)](/@devonmobile?source=post_page---byline--dedbab8fb630---------------------------------------)

[devonmobile](/@devonmobile?source=post_page---byline--dedbab8fb630---------------------------------------)

5 min read

·

Apr 23, 2026

--

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Ddedbab8fb630&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40devonmobile%2F10-js-tricks-senior-devs-dont-tell-you-dedbab8fb630&source=---header_actions--dedbab8fb630---------------------post_audio_button------------------)

Share

## The patterns that separate 10x engineers from the rest hidden in plain sight inside the language you use every day.

After a decade writing JavaScript at scale from scrappy startups to systems handling millions of requests I’ve collected a set of patterns that consistently **separate junior from senior code**. Most of these aren’t taught in tutorials. They’re passed down silently through code reviews, or discovered painfully at 2am during an outage.

This is the list I wish someone had handed me on day one.

## 1. Nullish Coalescing vs. OR They’re Not the Same

Nearly every developer uses `||` for default values. But it silently discards `0`, `false`, and `""`values that are falsy but often *intentional*. Use `??` instead.

```
// ❌ Dangerous with falsy-but-valid values  
const volume = userSettings.volume || 50;  // 0 becomes 50 — BUG!  
// ✅ Correct: only fires on null / undefined  
const volume = userSettings.volume ?? 50;  // 0 stays 0  
// Chain it with optional chaining for power moves  
const theme = user?.prefs?.theme ?? 'dark';
```

> ***Pro Insight:*** *This bug hits hardest in audio players, form inputs, and config systems where* `0` *and* `false` *are valid, meaningful states.*

## 2. Object Lookup Tables Beat Long if/else Chains

Long `if/else if` chains are a smell. They grow without limit and bury logic. Replace them with a lookup table it's faster, cleaner, and instantly extensible.

```
// ❌ Classic junior code  
function getStatusLabel(status) {  
  if (status === 'pending') return 'Waiting...';  
  else if (status === 'active') return 'Live!';  
  else if (status === 'closed') return 'Done';  
  else return 'Unknown';  
}  
  
// ✅ Senior pattern - O(1) lookup, zero branching  
const STATUS_LABELS = {  
  pending: 'Waiting...',  
  active:  'Live!',  
  closed:  'Done',  
};  
const getStatusLabel = (s) => STATUS_LABELS[s] ?? 'Unknown';
```

This scales to dozens of cases without touching the function. Adding a new status is a one-line config change, not a logic rewrite.

## 3. Promise.allSettled() is What You Actually Want

`Promise.all()` is a trap one failure aborts everything. `Promise.allSettled()` waits for all promises to resolve *or* reject, giving you full visibility without silent crashes.

```
const results = await Promise.allSettled([  
  fetchUser(id),  
  fetchOrders(id),  
  fetchPreferences(id),  
]);  
  
results.forEach((result) => {  
  if (result.status === 'fulfilled') process(result.value);  
  if (result.status === 'rejected')  logError(result.reason);  
});
```

> ***Pro Insight:*** *Use this for dashboard calls, batch operations, or anywhere partial failure is acceptable. Your users get data faster and your app doesn’t crater on one bad network request.*

## 4. Memoize Expensive Functions with a One-Liner Cache

You don’t need a library for memoization. A closure and a `Map` is all it takes to cache results and skip redundant computation.

```
function memoize(fn) {  
  const cache = new Map();  
  return (...args) => {  
    const key = JSON.stringify(args);  
    if (cache.has(key)) return cache.get(key);  
    const result = fn(...args);  
    cache.set(key, result);  
    return result;  
  };  
}  
  
const expensiveCalc = memoize((n) => /* heavy work */);
```

Write this utility once, paste it into every project. It’s one of those functions that never stops earning its keep.

> “The best JavaScript isn’t clever. It’s the kind the next developer reads and thinks ‘of course it works like that.’”

## 5. console.table() Will Change How You Debug Arrays

Stop printing raw arrays to the console. `console.table()` renders them as a proper table sortable, scannable, and immediately useful for spotting anomalies in data sets.

```
const users = [  
  { id: 1, name: 'Alice', role: 'admin'  },  
  { id: 2, name: 'Bob',   role: 'editor' },  
];  
  
// ❌ Prints a useless collapsed object  
console.log(users);  
// ✅ Renders a clean, scannable table in DevTools  
console.table(users);  
// Show only specific columns  
console.table(users, ['name', 'role']);
```

Once you see this in DevTools, you’ll never go back to `console.log` for arrays.

## 6. structuredClone() for Deep Copying Objects

Forget the `JSON.parse(JSON.stringify())` hack. It breaks on Dates, functions, and `undefined`. The native `structuredClone()` is the real deep copy you've been waiting for.

```
const original = {  
  name: 'Alice',  
  dob: new Date('1990-01-01'),  
  scores: [95, 87, 92],  
};  
  
// ❌ Breaks Date objects - turns them into strings  
const bad = JSON.parse(JSON.stringify(original));  
// ✅ Native deep clone - handles Dates, Sets, Maps  
const clone = structuredClone(original);  
clone.scores.push(88);  
console.log(original.scores); // [95, 87, 92] - untouched ✓
```

Supported in all modern browsers and Node 17+. No excuses.

## 7. Logical Assignment Operators Compress Your Defaults

ES2021 brought three operators that collapse assignment-with-fallback into a single expression: `||=`, `&&=`, and `??=`. They're criminally underused.

```
let config = { debug: null, retries: 0 };  
  
// ??= only assigns if null or undefined  
config.debug   ??= false;   // null  → false  
config.retries ??= 3;       // 0     → stays 0 (not null/undefined)  
// ||= assigns if falsy  
config.timeout ||= 5000;    // undefined → 5000  
// &&= assigns only if truthy  
config.debug &&= 'verbose'; // false → stays false
```

These are especially powerful in config setup, React state initialization, and anywhere you’re conditionally setting defaults.

## 8. Use AbortController to Cancel Stale Requests

In any type-ahead search or navigation-heavy app, old requests can return after newer ones causing data races. `AbortController` lets you cancel in-flight fetches cleanly.

```
let controller;  
  
async function search(query) {  
  // Cancel any pending request  
  controller?.abort();  
  controller = new AbortController();  
  try {  
    const res = await fetch(`/api/search?q=${query}`, {  
      signal: controller.signal  
    });  
    return await res.json();  
  } catch (e) {  
    if (e.name !== 'AbortError') throw e;  
  }  
}
```

> ***Pro Insight:*** *This is the secret behind every snappy autocomplete widget. Without it, a slow network turns your search into a flickering nightmare of stale results.*

## 9. Array.at() for Negative Indexing

Getting the last element of an array used to require `arr[arr.length - 1]`awkward and error-prone. `Array.at(-1)` is the clean, modern way.

```
const stack = ['a', 'b', 'c', 'd'];  
  
// ❌ The old way  
stack[stack.length - 1];  // 'd'  
// ✅ Clean and expressive  
stack.at(-1);   // 'd'  
stack.at(-2);   // 'c'  
// Works on strings too!  
'Hello'.at(-1);  // 'o'
```

Small improvement, massive readability gain. Use it everywhere.

## 10. Wrap Async/Await with a Safe Handler Utility

Wrapping every `await` in a try/catch bloats your code. This utility functioninspired by Go-style error handling returns `[error, data]` tuples, keeping your async code flat and readable.

```
// The utility  
const safe = (promise) =>  
  promise.then((data) => [null, data])  
         .catch((err) => [err,  null]);  
// Usage - no more nested try/catch pyramids  
async function loadDashboard(userId) {  
  const [userErr, user] = await safe(fetchUser(userId));  
  if (userErr) return showError('User load failed');  
  const [ordErr, orders] = await safe(fetchOrders(user.id));  
  if (ordErr) return showError('Orders load failed');  
  render({ user, orders });  
}
```

> ***Pro Insight:*** *Once you write this utility, it gets copied into every project. It’s the function that outlasts frameworks.*

## The Real Takeaway

These aren’t just tricks they’re signals. When I see these patterns in a codebase, I know the person writing it is thinking about **the next developer**, not just getting something to work today.

The gap between junior and senior JavaScript isn’t about knowing more APIs. It’s about caring more about clarity, resilience, and the long game.

If even two of these changed how you think about your code, **share this with a teammate**. The best codebases are built through this kind of quiet, deliberate knowledge transfer.

*Follow for more deep dives on JavaScript, architecture, and the patterns that actually matter at scale.*