---
title: "From Theory to Automation: WCAG compliance using axe-core, next.js, and GitHub actions"
url: https://medium.com/p/b9f63af8e155
---

# From Theory to Automation: WCAG compliance using axe-core, next.js, and GitHub actions

[Original](https://medium.com/p/b9f63af8e155)

# From Theory to Automation: WCAG compliance using axe-core, next.js, and GitHub actions

[![Marcin Skorek](https://miro.medium.com/v2/resize:fill:64:64/1*Bp2pPUSAT2ei5sxOMnjBaw.jpeg)](/@SkorekM?source=post_page---byline--b9f63af8e155---------------------------------------)

[Marcin Skorek](/@SkorekM?source=post_page---byline--b9f63af8e155---------------------------------------)

7 min read

·

Apr 7, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## Introduction: Why Accessibility Matters

Accessibility in web development is not just a nice-to-have, it should be a must-have. Whether it’s a personal blog or an extensive application, making sure that the site is accessible means creating and caring for the inclusive experience for all users.

Some time ago, I launched my website. I treat it as a playground for different integrations and as a side project that is also a home for my articles ([skorekm.dev](https://www.skorekm.dev/) if you are interested). One Friday evening, I thought: “Let’s hook up some accessibility checks into my website.”. Naturally, I dove back into my [old article](/@SkorekM/guide-to-building-accessible-web-applications-35ee5afd313f) about the WCAG, did more digging on the subject, and realized something. The practical guides, especially for newer versions of React (**axe-core/react** does not support React 18+) or automating the accessibility testing, are hard to find.

That’s what this article is all about. We are shifting from theory and outdated guides toward automation. We’ll explore how to automate the accessibility testing using axe-core library, GitHub Actions, and Next.js.

## Why axe-core? Choosing the right tool for the job

When I decided to integrate accessibility checks into my website, I went down the rabbit hole of testing. From my previous research about the WCAG, I already knew about tools such as Pa11y, Lighthouse, and, of course, axe-core. The latter stood out the most for a number of reasons:

**Company backing** — Deque, the company backing axe-core is known for its presence in the accessibility field.

**Effect** — during my tests, axe-core consistently found more errors. I know it’s not always the benchmark, but in that case, those were meaningful, adequate tests.

**Lighthouse** — While doing the research, I checked how Lighthouse is built, and they do, in fact, have the axe core in their **package.json** file. That’s some big endorsement for the library, if you ask me.

With that being said, Pa11y and Lighthouse are also great options. Lighthouse even has the check actions in their documentation. So if you feel like that’s a better choice, you can go ahead and use theirs to plug into your CI. My inner nerd just wanted to poke around with axe core. Me likey some challenge.

## Automation, my good old friend

Automation can be a lifesaver (or production saver) if set up correctly.  
In terms of my accessibility checks, the idea is pretty simple: Whenever I create the pull request to my`develop` or `master` branch, I want the GitHub Actions to run the accessibility checks. How to do that? Well, here’s a rough idea I had in mind when starting:

* Generate the sitemap for the available pages,
* Parse the XML file with sitemaps to a list of strings,
* Run accessibility checks on each URL

### Sitemaps: The Guide That Knows It All

A sitemap is essentially a list of all the pages on your website. It’s usually used by search engines to index your website. For accessibility testing, it’s a good idea, as sitemaps provide a reliable source of truth for all the pages.

In the next.js apps, it may be like looking for a needle in a haystack. Pages may be scattered all around, and some of them might be dynamic. A sitemap allows us to make sure that no page is left behind untested.

## Step-by-step implementation

Okay, so buckle up. It’s time for the ride of code walkthroughs.

### Generating the sitemap

```
// src/app/sitemap.ts  
export default function sitemap() {  
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;  
  const postsSlugs = getPostsSlugs();  // Gets all my blog posts  
  
  const postsUrls = postsSlugs.map((post) => (  
    {  
      url: `${baseUrl}/blog/${post}`,  
      lastModified,  
    }  
  ));  
  
  return [  
    { url: `${baseUrl}/` },        // Home page  
    { url: `${baseUrl}/about` },   // About page  
    ...postsUrls,                  // Posts urls  
  ]  
}
```

### Parsing the sitemap

After the application is built, what is orchestrated in the workflow, I know the output will be in the XML format. Here’s the script I have written to get the sitemap file and parse URLs. It then saves it in the `.txt` file, and the final script iterates over it.

Side note: This step is opinionated, and it can be approached in a myriad of different ways.

```
// ops/extract-sitemap-url.js  
import fs from 'fs';  
import path from 'path';  
  
// After build, sitemap is in the .next directory  
const sitemapPath = path.resolve(  
  import.meta.dirname,  
  '../.next/server/app/sitemap.xml.body'  
);  
  
try {  
  // Make sure sitemap exists  
  if (!fs.existsSync(sitemapPath)) {  
    console.error(`Sitemap file not found at: ${sitemapPath}`);  
    process.exit(1);  
  }  
  
  // Read and parse the sitemap  
  const sitemapContent = fs.readFileSync(sitemapPath, 'utf8');  
  const urlRegex = /<loc>(.*?)<\/loc>/g;  
  const matches = [...sitemapContent.matchAll(urlRegex)];  
    
  const urls = matches.map(match => match[1]);  
    
  if (urls.length === 0) {  
    console.warn('No URLs found in the sitemap.xml file.');  
    process.exit(1);  
  }  
    
  // Convert URLs to paths for testing  
  const paths = urls.map(url => {  
    try {  
      // Ensure proper URL parsing  
      let processableUrl = url;  
      if (!url.startsWith('http')) {  
        processableUrl = 'http://' + url;  
      }  
      const urlObj = new URL(processableUrl);  
      return urlObj.pathname;  
    } catch (err) {  
      return url.startsWith('/') ? url : `/${url}`;  
    }  
  });  
    
  // Save paths for the testing script  
  const outputPath = path.resolve(process.cwd(), './ops/urls.txt');  
  fs.writeFileSync(outputPath, paths.join('\n'));  
    
  console.log(`Found ${paths.length} URLs to test:`);  
  paths.forEach(path => console.log(`  ${path}`));  
} catch (error) {  
  console.error('Error processing sitemap:', error);  
  process.exit(1);  
}
```

### The accessibility test runner

Now that we do have the URLs parsed, it’s time to run the axe-core against all of our paths. This is the final script that tests all the URLs and throws an error if accessibility issues are found.

```
// ops/run-a11y-tests.js  
import fs from 'fs';  
import { execSync } from 'child_process';  
  
try {  
  // Read the URLs we found earlier  
  const urls = fs.readFileSync('./ops/urls.txt', 'utf8')  
    .split('\n')  
    .filter(path => path.trim() !== '');  
  
  // we'll need it in the end  
  let hasFailures = false;  
  
  // Test each URL  
  for (const url of urls) {      
    console.log('====================================================');  
    console.log(`Testing: ${url}`);  
    console.log('====================================================');  
      
    try {  
      // Run axe-core accessibility tests  
      execSync(`axe "${url}" --exit`, { stdio: 'inherit' });  
    } catch (error) {  
      console.log('Accessibility issues found on this page');  
      hasFailures = true;  
    }  
  }  
  
  // Final report  
  console.log('====================================================');  
  console.log('Accessibility testing complete.');  
  console.log('====================================================');  
  
  // Exit with error if we found any issues  
  process.exit(hasFailures ? 1 : 0);  
} catch (error) {  
  console.error('Error during accessibility testing:', error);  
  process.exit(1);  
}
```

### The workflow

Lastly, it’s time to orchestrate all of those scripts around. I am not going to dive into too much detail on how the workflows work, but rather the main idea of how it’s set up. Firstly, we prepare the environment, then build the application (so that next.js build the sitemap file), we extract URLs, run the next.js app (so that the URLs are accessible by the axe-core), and lastly run accessibility tests.

```
name: Accessibility Tests  
on:  
  push:  
    branches: [main, develop]  
  pull_request:  
    branches: [main, develop]  
  workflow_dispatch:  
  
jobs:  
  axe:  
    name: Axe Accessibility Tests  
    runs-on: ubuntu-22.04  # Using a specific version for consistency  
    steps:  
      - name: Checkout code  
        uses: actions/checkout@v4  
  
      - name: Setup Node.js  
        uses: actions/setup-node@v4  
        with:  
          node-version: '22'  
          cache: 'npm'  # Built-in npm caching  
        
      # Smart caching for faster builds  
      - name: Cache Next.js build  
        uses: actions/cache@v4  
        with:  
          path: ${{ github.workspace }}/.next/cache  
          key: |  
            ${{ runner.os }}-nextjs-v1-${{   
              hashFiles('**/package-lock.json')   
            }}-${{   
              hashFiles('next.config.js')   
            }}  
          restore-keys: |  
            ${{ runner.os }}-nextjs-v1-${{   
              hashFiles('**/package-lock.json')   
            }}  
            ${{ runner.os }}-nextjs-v1-  
  
      - name: Install dependencies  
        run: npm ci  
  
      - name: Install axe-core CLI  
        run: |  
          npm install -g @axe-core/cli  
          npx browser-driver-manager install chrome  
  
      - name: Build Next.js app  
        run: npm run build  
        env:  
          NEXT_PUBLIC_BASE_URL: http://localhost:3000  
  
      - name: Extract sitemap URL  
        run: node ops/extract-sitemap-url.js  
  
      - name: Start Next.js app  
        run: npm run start &  
        timeout-minutes: 2  # Prevents hanging builds  
  
      - name: Run accessibility tests  
        run: |  
          echo "Running accessibility tests..."  
          node ops/run-a11y-tests.js  
          echo "Accessibility tests finished."
```

So this is it. That’s how I approached setting everything up. There are some improvements I could make, but I believe it can serve as a good base. Feel free to take whatever pieces may fit your workflow.

### Additional Tooling (Optional):

**Linting with a11y**Think of it as an extension to what we are doing here with the CI checks and, overall the axe core. The plugin does the static analysis of your JSX and can catch accessibility issues right in the code editor before committing the changes. Duh, you can even configure your workflow so it does not allow you to commit the code if those errors are caught (that’s a topic for another article).

[eslint-](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)[plugin](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)-[jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)

**DevTools Axe**Dequeue, the company behind the Axe, has built some awesome dev tools for accessibility testing. The tool is very useful, and I highly encourage you to check it out.

[DevTools](https://www.deque.com/axe/devtools/)

### Sustaining accessibility beyond automation

It’s important to note that automation is powerful, but it’s not a silver bullet. It works like a charm at catching issues like missing alt text or improper heading structures, but they are no replacement for people.

Automation tools will not tell you whether the alt text makes sense in the given context. So, while our digital assistants are helpful, we still need human insight to catch issues.

Lastly, accessibility is not about running tests and making sure that the tool does not fail the build. It’s about fostering inclusive mindsets throughout the development process. It’s easier to think about whether the color contrast is sufficient. We can prevent the issues rather than fix them later.

### Wrapping up

This research and article were not planned at all. I just had a random thought along the lines of “Hey, let’s plug accessibility tools into my website”. Then, the inner nerd took over, and instead of taking the easy route, I made myself another cup of coffee and dug in. I hope that this comes useful, either by the idea of how I approached the problem, or overall solution. Nevertheless, before diving head first into automation, remember that accessibility is not just a checkbox.

In the meantime, thanks for reading, and till next time!