---
title: "I Built a JavaScript Tool in One Night That Solved a Problem I’d Struggled With for Months"
url: https://medium.com/p/87e8049ad319
---

# I Built a JavaScript Tool in One Night That Solved a Problem I’d Struggled With for Months

[Original](https://medium.com/p/87e8049ad319)

Member-only story

# I Built a JavaScript Tool in One Night That Solved a Problem I’d Struggled With for Months

[![Arslan Qutab](https://miro.medium.com/v2/resize:fill:64:64/1*A0qsvGWoXRVdhyLk8YQDEw.jpeg)](https://medium.com/@arslanshoukatali?source=post_page---byline--87e8049ad319---------------------------------------)

[Arslan Qutab](https://medium.com/@arslanshoukatali?source=post_page---byline--87e8049ad319---------------------------------------)

4 min read

·

Sep 1, 2025

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

For months, I had the same frustration every night. I’d spend hours coding, downloading docs, saving random snippets, and bookmarking articles, only to wake up the next morning to a complete mess on my laptop. My “Downloads” folder was a junkyard, my browser tabs looked like a graveyard, and finding that one file I actually needed felt like playing hide-and-seek with myself.

That night, I finally snapped. I brewed a cup of coffee at 11 PM, opened up my editor, and told myself: *I’m not going to sleep until I’ve fixed this.* By sunrise, I had built a JavaScript tool that automated the mess away. What had been haunting me for months was gone in a single night.

Here’s how it happened.

## The Problem Wasn’t Just Laziness

I used to think I was just lazy. But the real problem was workflow friction. Every file I saved, every snippet I copied, and every note I wrote down was scattered across different places.

The truth is, developers don’t just need discipline; we need systems. A system that cleans up the chaos while we focus on the actual work.

So, I decided to automate it.

## Step 1: Watching My Downloads Without Watching Them

The first part was obvious: my downloads folder. I wanted files to automatically move into the right place the second they landed. PDFs into “Research,” images into “Assets,” and scripts into “Code.”

Here’s a snippet of the code that did exactly that:

```
const fs = require("fs");  
const path = require("path");  
  
const downloads = "C:/Users/Arslan/Downloads";  
const rules = {  
  ".pdf": "C:/Projects/Research",  
  ".png": "C:/Projects/Assets",  
  ".js": "C:/Projects/Code"  
};  
  
fs.watch(downloads, (event, file) => {  
  if (event === "rename") {  
    const ext = path.extname(file);  
    if (rules[ext]) {  
      const oldPath = path.join(downloads, file);  
      const newPath = path.join(rules[ext], file);  
      fs.renameSync(oldPath, newPath);  
      console.log(`Moved ${file} to ${rules[ext]}`);  
    }  
  }  
});
```

This script runs silently in the background. Every time I download something, it’s immediately placed where it belongs. No clicks, no dragging, no wasted time.

## Step 2: Capturing Code Snippets Like a Developer’s Clipboard

I also had a bad habit: copying random code snippets from Stack Overflow and then losing them forever. I wanted every snippet I copied to automatically save into a single “snippets.json” file.

Here’s how I built it:

```
const clipboardy = require("clipboardy");  
const fs = require("fs");  
  
setInterval(() => {  
  const text = clipboardy.readSync();  
  if (text.includes(";") || text.includes("{")) {  
    fs.appendFileSync("snippets.json", text + "\n---\n");  
    console.log("Snippet saved!");  
  }  
}, 5000);
```

Now, every time I copy a block of code, it’s stored. Later, I can search, reuse, or even feed it into an AI for quick testing.

## Step 3: Keeping Tabs on My Browser Tabs

Tabs were another monster. I’d open 30 of them while researching, only to forget why I opened them in the first place.

To fix this, I wrote a tiny script that saves all open tabs (from Chrome) into a markdown file whenever I hit a shortcut key.

```
const { exec } = require("child_process");  
const fs = require("fs");  
  
exec("chrome-cli list links", (err, stdout) => {  
  if (err) return;  
  fs.writeFileSync("tabs.md", stdout);  
  console.log("Tabs saved to tabs.md");  
});
```

Now, instead of cluttering my browser, I can archive tabs into a file and revisit them when I need them.

## Step 4: Stitching Everything Into One Workflow

Separately, these scripts were useful. But the magic happened when I combined them.

One Node.js script now runs as my personal automation assistant. It:

1. Organizes files as they download

2. Saves copied snippets automatically

3. Archives open tabs on demand

With this system, my workflow feels lighter. Nothing slips through the cracks anymore.

## The Lesson I Didn’t Expect

I thought I was solving a “productivity” issue. But really, I was designing a workflow that respected my brain. Instead of forcing myself to remember everything, I let code handle the boring parts.

As developers, we’re quick to learn frameworks, libraries, or syntax, but the biggest upgrade comes from solving our own problems with code. That one night taught me more about automation than months of tutorials ever did.

**Pro Tip:** Build small, personal automations before you chase big projects. They’re faster, more motivating, and often far more impactful than you expect.

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!