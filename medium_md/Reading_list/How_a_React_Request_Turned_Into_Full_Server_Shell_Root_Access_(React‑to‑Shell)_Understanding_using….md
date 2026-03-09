---
title: "How a React Request Turned Into Full Server Shell Root Access (React‑to‑Shell) Understanding using…"
url: https://medium.com/p/4e11ceb58b73
---

# How a React Request Turned Into Full Server Shell Root Access (React‑to‑Shell) Understanding using…

[Original](https://medium.com/p/4e11ceb58b73)

# **How a React Request Turned Into Full Server Shell Root Access (React‑to‑Shell) Understanding using an actual exploit script.**

[![Muhammad Abdul Rehman](https://miro.medium.com/v2/resize:fill:64:64/1*Q5bcwVfJF_UogDvN0aTm0A.jpeg)](/@dev-abdulrehman?source=post_page---byline--4e11ceb58b73---------------------------------------)

[Muhammad Abdul Rehman](/@dev-abdulrehman?source=post_page---byline--4e11ceb58b73---------------------------------------)

3 min read

·

Dec 19, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

As we know, React is no longer “just frontend”. With **Next.js Server Actions and React Server Components**, React now runs directly on the server, and that shift introduces a new class of vulnerabilities known as **React-to-Shell**.

In short:  
 A bug in React’s server-side deserialization can end in **full OS command execution**.

## What Is React-to-Shell?

React-to-Shell is a vulnerability chain where:

**React server deserialization → JavaScript execution → Node.js access → Shell access**

The CVEs **CVE-2025–55182** and **CVE-2025–66478** are examples of this pattern, where unsafe object reconstruction inside the React / Next.js runtime allows attackers to escape into Node.js internals.

## ⚠️ Warning About the Script

The exploit script shared in the following repository is **for educational and research purposes only**:

👉 [**https://github.com/chrahman/react2shell-CVE-2025-55182-full-rce-script**](https://github.com/chrahman/react2shell-CVE-2025-55182-full-rce-script)

* The script itself is **not malicious**
* It only works if the target app is already vulnerable
* Using it on systems without permission is **illegal**

Use it only in labs, local testing, or authorized research.

## About the Script (Important Clarification)

The bash script is just a **delivery tool**:

* Sends a crafted request
* Triggers the vulnerable logic
* Prints the response

The same thing could be done using `curl` or Postman.

**The real danger is inside** `payload.json`**.**

## Why This Works in JavaScript

A key reason this vulnerability is possible is a core JavaScript rule:  
***In JavaScript, almost everything is an object.***

Functions are objects.  
Promises are objects.  
Even errors and arrays are objects.

## The Role of `__proto__`

Every JavaScript object has a hidden link called `__proto__`:

* It points to another object (its prototype)
* If you modify it, you change how many objects behave

This is called **prototype pollution**.

In this vulnerability, the payload abuses `__proto__` Ultimately, React ends up executing attacker-controlled logic while rebuilding objects.

## The Role of `constructor`

Every object also has a `constructor`.

If you follow this chain:

```
obj.constructor.constructor
```

```
Function("any JavaScript code here")()
```

At this point, **arbitrary JavaScript execution** is possible.

## From JavaScript to Full Server Access

Once arbitrary JS runs on the server:

Node.js internals become accessible

`process` becomes available

child\_process. execSync() can execute OS commands

This is how a React request turns into **full server shell access**.

## Current Status of This Vulnerability

* ✅ **Fixed by the React team** in patched releases
* ✅ **Vercel added platform-level protections** to block such requests instantly
* ⚠️ **Self-hosted and non-Vercel deployments** remain vulnerable if running affected versions

If you’re not patched, you’re still at risk.

## Why This Still Matters

This is not a UI bug.  
This is **server-side RCE**.

Unpatched apps can still allow attackers to:

* Read secrets and environment variables
* Run system commands
* Install backdoors
* Move laterally inside infrastructure

## Defensive Takeaway

* Upgrade React / Next.js immediately
* Avoid exposing Server Actions publicly
* Never trust serialized RSC input
* Run apps with least privilege
* Monitor abnormal Server Action behavior

## Final Thought

React-to-Shell exists because **JavaScript’s flexibility meets framework-level trust**.

The script is just a messenger.  
 The payload is the weapon.  
 The vulnerability is the open door.

Close the door, and the exploit stops working.