---
title: "I Built a React App Without useState (And It’s Faster)"
url: https://medium.com/p/0d98ddc51c3b
---

# I Built a React App Without useState (And It’s Faster)

[Original](https://medium.com/p/0d98ddc51c3b)

Member-only story

# I Built a React App Without useState (And It’s Faster)

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](/@Iggy01?source=post_page---byline--0d98ddc51c3b---------------------------------------)

[Ignatius Sani](/@Iggy01?source=post_page---byline--0d98ddc51c3b---------------------------------------)

8 min read

·

Jun 12, 2026

--

2

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0d98ddc51c3b&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40Iggy01%2Fi-built-a-react-app-without-usestate-and-its-faster-0d98ddc51c3b&source=---header_actions--0d98ddc51c3b---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

No useState, no useReducer, no Context. Just vanilla JavaScript and React rendering. Here’s why it works.

Every React tutorial teaches the same pattern:

```
const [data, setData] = useState(initialData);
```

State in React. Updates via setState. Re-renders when state changes.

I’ve written thousands of components this way. Never questioned it.

Then I built a dashboard with 50+ interactive components. useState everywhere. The app was slow. Profiling showed 300+ re-renders on every action.

So I tried something radical: **What if state lived outside React entirely?**

No useState. No useReducer. No Context.

Just a vanilla JavaScript object that notifies React when it changes.

The result: 5x faster. Simpler code. Fewer bugs.

Here’s how it works.

## The Problem with React State

React re-renders components when state changes. That’s the whole point.

But React doesn’t know **which components** care about which state. So it re-renders **all** components that might care.

**Example:**

```
function App() {  
  const [user…
```