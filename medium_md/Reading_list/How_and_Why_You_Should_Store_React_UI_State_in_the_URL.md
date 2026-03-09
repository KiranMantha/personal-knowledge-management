---
title: "How and Why You Should Store React UI State in the URL"
url: https://medium.com/p/f2013a204cb2
---

# How and Why You Should Store React UI State in the URL

[Original](https://medium.com/p/f2013a204cb2)

# How and Why You Should Store React UI State in the URL

## Deep linking in React, as simple as useState

[![Sidney Alcantara](https://miro.medium.com/v2/resize:fill:64:64/1*96FrONQWUqDoAWynbp_Uew.jpeg)](/@notsidney?source=post_page---byline--f2013a204cb2---------------------------------------)

[Sidney Alcantara](/@notsidney?source=post_page---byline--f2013a204cb2---------------------------------------)

5 min read

·

Dec 9, 2021

--

8

Listen

Share

More

Press enter or click to view image in full size

![Diagram showing React state being reflected in the rendered UI as a modal opens, and in the URL as a hash parameter]()

Have you ever used a complex web app with many features, modal windows, or side panels? Where you get to the perfect state with just the right information on the screen after a few clicks through different screens, but then you accidentally close the tab? (Or Windows decides to update?)

It would be great if there were a way to return to this state without going through the same tedious process. Or be able to share that state so a teammate can work on the same thing you are.

This problem could be solved with deep linking, which is used today in mobile apps to open the app to a specific page or UI state. But why does this not exist in many web apps?

[Click here to skip to the solution and code snippets.](#694f)

## Bring back deep linking on the web

The emergence of single-page applications (SPAs) has allowed us to craft new user experiences that are instantly interactive on the web. By doing more on the client side using JavaScript, we can respond to user events immediately, from opening custom dialog windows to live text editors like Google Docs.

Traditional server-rendered websites send a request to get a new HTML page every single time. An excellent example is Google, which sends a request to its servers with the user’s search query in the URL: `https://www.google.com/search?q=your+query+here`. What’s great about this model is that if I filter by results from the past week, I can share the same search query by simply sharing the URL: `https://www.google.com/search?q=react+js&tbs=qdr:w`. And this paradigm is entirely natural for web users — sharing links has been part of the worldwide web ever since it was invented!

Press enter or click to view image in full size

![Annotated screenshot of a Google search page. The search term input is highlighted and an arrow points to the corresponding part in the URL that stores the search term. The results are filtered to only show those from the past week, and another arrow points to the corresponding part in the URL that stores this data.]()

When SPAs came along, we didn’t need to store this data in the URL since we no longer need to make a server request to change what is displayed on the screen (hence *single-page*). But this made it easy to lose a unique experience of the web, the shareable link.

Desktop and mobile apps never really had a standardized way to link to specific parts of the app, and modern implementations of deep linking rely on URLs on the web. So when we build web apps that function more like native apps, why would we throw away the deep linking functionality of URLs that we’ve had for decades?

## Dead-Simple Deep Linking

When building a web app that has multiple pages, the minimum you should do is change the URL when a different page is displayed, such as `/login` and `/home`. In the React ecosystem, [React Router](https://reactrouter.com/) is perfect for client-side routing like this, and [Next.js](https://nextjs.org/) is an excellent fully-featured React framework that also supports server-side rendering.

But I’m talking about deep linking, right down to the UI state after a few clicks and keyboard inputs. This is a killer feature for productivity-focused web apps, as it allows users to return right to the exact spot they were at even after closing the app or sharing it with someone else so they can start work without any friction.

Press enter or click to view image in full size

![Screen recording of a modal window being opened, causing the URL to update to add `#modal=”webhooks”`, which is the internal state that triggers the modal to open.]()

You could use npm packages like [query-string](https://www.npmjs.com/package/query-string) and write a basic React Hook to sync URL query parameters to your state, and there are [plenty](/swlh/using-react-hooks-to-sync-your-component-state-with-the-url-query-string-81ccdfcb174f) of [tutorials](https://www.npmjs.com/package/use-query-params) for [this](https://dev.to/gaels/an-alternative-to-handle-global-state-in-react-the-url--3753), but there’s a more straightforward solution.

While exploring modern state management libraries for React for an architecture rewrite of our React app [Rowy](https://rowy.io/?utm_source=medium.com&utm_medium=blog&utm_campaign=How+and+why+you+should+store+React+UI+state+in+the+URL), I came across [Jotai](https://jotai.org/), a tiny atom-based state library inspired by the React team’s [Recoil](https://recoiljs.org/) library.

The main benefit of this model is that state atoms are declared independent from the component hierarchy and can be manipulated from anywhere in the app. This solves the issue with React Context causing unnecessary re-renders, which I [previously worked around with](https://betterprogramming.pub/how-to-useref-to-fix-react-performance-issues-4d92a8120c09) `useRef`. You can read more about the atomic state concept in [Jotai’s docs](https://jotai.org/docs/basics/concepts) and a more technical version in [Recoil’s](https://recoiljs.org/docs/introduction/motivation).

## The Code

Jotai has a type of atom called `atomWithHash`, which syncs the state atom to the URL hash.

Suppose we want a modal’s open state stored in the URL. Let’s start by creating an atom:

Then in the modal component itself, we can use this atom just like `useState`:

And here’s how it looks:

Press enter or click to view image in full size

![Screen recording of a modal being opened, causing the URL to update to reflect the UI state, with `#modalOpen=true` being appeneded. When the modal is closed, it is replaced with `modalOpen=false`.]()

And that’s it! It’s that simple.

What’s fantastic about Jotai’s `atomWithHash` is that it can store any data that `useState` can, and it automatically stringifies objects to be stored in the URL. So I can store a more complex state in the URL, making it sharable.

In [Rowy](https://rowy.io/?utm_source=medium.com&utm_medium=blog&utm_campaign=How+and+why+you+should+store+React+UI+state+in+the+URL), we used this technique to implement a UI for cloud logs. We’re building an open-source platform that makes backend development easier and eliminates friction for common workflows. So, reducing friction for sharing logs was perfect for us. You can see this in action on our demo, where I can link you to a specific deploy log:

```
https://demo.rowy.io/table/roadmap#modal="cloudLogs"&cloudLogFilters={"type"%3A"build"%2C"timeRange"%3A{"type"%3A"days"%2C"value"%3A7}%2C"buildLogExpanded"%3A1}
```

Press enter or click to view image in full size

![Screen recording of the deep link opening the Rowy demo web app to the cloud logs modal being open.]()

Decoding the URL component reveals the exact state used in React:

A side effect of `atomWithHash` is that it pushes the state to the browser history by default, so the user can click the back and forward buttons to go between UI states.

Press enter or click to view image in full size

![Screen recording of the user clicking the back button in the browser repeatedly, causing the UI state to change with modals being opened and closed.]()

This behavior is optional and can be disabled using the `replaceState` [option](https://jotai.org/docs/api/utils#atom-with-hash):

Thanks for reading! I hope this has convinced you to expose more of your UI state in the URL, making it easily shareable and reducing friction for your users — especially since it’s effortless to implement.

```
Want to Connect With the Author?You can follow me on Mastodon @notsidney@indieweb.social for more articles and threads about front-end engineering.
```