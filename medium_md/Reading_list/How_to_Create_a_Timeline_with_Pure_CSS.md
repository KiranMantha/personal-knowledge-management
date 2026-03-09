---
title: "How to Create a Timeline with Pure CSS"
url: https://medium.com/p/862ffea5b99b
---

# How to Create a Timeline with Pure CSS

[Original](https://medium.com/p/862ffea5b99b)

# How to Create a Timeline with Pure CSS

## Create a web timeline component hands-on using CSS styles

[![Dulanka Karunasena](https://miro.medium.com/v2/resize:fill:64:64/1*CGb7gkA51oALOedboKiBHg.jpeg)](https://medium.com/@dulanka?source=post_page---byline--862ffea5b99b---------------------------------------)

[Dulanka Karunasena](https://medium.com/@dulanka?source=post_page---byline--862ffea5b99b---------------------------------------)

7 min read

·

Apr 5, 2021

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Timelines have become a common feature in many web designs, and users find them very attractive. However, implementing these timelines is not that easy since clients always request something unique for their websites.

But you don't have to start everything from scratch if you have a basic foundation. So in this article, I will guide you through the steps to create a customizable horizontal timeline with pure CSS.

I’ve created the [slider as an independent component](https://bit.dev/enlear/randoms/ui/timeline) and shared it with Bit. Feel free to examine it, install it, or import it into your own Bit workspace.

[![]()](https://bit.dev/enlear/randoms/ui/timeline)

### Learn more about building reusable CSS components here:

[## Tutorial: Create Reusable CSS Components with Bit

### This tutorial guides you through the process of creating reusable CSS components with Bit and SCSS. Learn how to…

bit.dev](https://bit.dev/blog/how-to-create-reusable-css-components-with-bit-lhdn5jpc/?source=post_page-----862ffea5b99b---------------------------------------)

[![Build in AI speed — Create and maintain an enterprise-grade design system at ease]()](https://bit.cloud)

## Step 1: Creating the Basic Structure

I will start off things by creating the basic structure of the timeline. First, I will design the middle line and then arrange the Date and Event inside the Container Box.

Then I will combine multiple Container Boxes to form the flow of events. You will be able to create the basic structure as it is in the diagram using the below code.

## Step 2: Adjusting the Heights and Widths

Now, I will create a wrapper for the timeline to fix its height and width. According to the below example, `timeline-wrapper` has a 300px height, and it will take the entire width of the screen. By setting `margin: auto` the timeline will be horizontally centered.

```
.timeline-wrapper {  
  position: relative;  
  width: 100%;  
  margin: auto;  
  height: 300px;  
}
```

> Tip: Make sure to set `position: relative` for parent elements and `position: absolute` for child elements so that the child elements can be properly arranged relative to their parent.

## Step 3: Drawing the Middle Line

As the third step, I will be adding the styles to the middle line. The `middle-line` will take the entire width of the `timeline-wrapper` and it will have a height of 5px. It is positioned to the exact middle of the `timeline-wrapper` by setting `top: 50%` and `transform: translateY(-50%)`.

```
.timeline-wrapper .middle-line {  
  position: absolute;  
  width: 100%;  
  height: 5px;  
  top: 50%;  
  transform: translateY(-50%);  
  background: #d9d9d9;  
}
```

> Tip: Giving `top: 50%` isn’t enough to position the middle line to the exact middle. As it has a height of 5px, the middle line will stretch downwards from the center of the timeline. A translation of -50% along Y-axis is essential to position the middle line to the exact center.

## Step 4: Positioning the Dates

Now let’s position the dates in the timeline! First, I will break the timeline into several parts.

I have set the width of the box as 17% so that I can divide the timeline into six parts — also, the `float` property is set as `right` to arrange the elements horizontally.

```
.box {  
  width: 17%;  
  position: relative;  
  min-height: 300px;  
  float: right;  
}
```

> Tip: The `box` class should be positioned `relative` as it will be the parent element for `date` and `box-content` classes.

The `date` class is positioned to the middle of the timeline using `top: 50%` and `transform: translateY(-50%)`. The `border-radius` is set to 100% to design the circular border around the date. The date is placed inside paragraph tags with centered text.

```
.box .date {  
  position: absolute;  
  top: 50%;  
  left: 0px;  
  transform: translateY(-50%);  
  width: 50px;  
  height: 50px;  
  border-radius: 100%;  
  background: #fff;  
  border: 2px solid #d9d9d9;  
}.date p {  
  text-align: center;  
  margin-top: 3px;  
  margin-bottom: 0px;  
}
```

Let’s see what we have achieved so far!

Press enter or click to view image in full size

![]()

Impressive right? 😃.But, I think we can do better than this. So, let’s do some modifications to our awesome timeline more to give it a better look.

## Step 5: Styling the Event Boxes

Next I will style the `box-content` with a `width` of 180px and background color set to `#00b0bd`. The `border-radius` will be set to 5px to get the rounded corners.

The box-content is positioned -77px away from the left of the box to align with dates properly. Margin is set to 0, and font color to white for the paragraphs inside the box-content.

```
.box .box-content {  
  border-radius: 5px;  
  background-color: #00b0bd;  
  width: 180px;  
  position: absolute;  
  left: -77px;  
  padding: 15px;  
}.box-content p {  
  margin: 0;  
  color: white;  
}
```

I thought it would be better to move the boxes to either side of the centerline. So I moved the `box-content` of `box-bottom` 65% down from the top of the `box` element.

```
.box-bottom .box-content {  
  top: 65%;  
}
```

Press enter or click to view image in full size

![]()

Now I will add some icing to the Event Boxes in the timeline by styling the `box-content` a little bit more. For that, I used `::before` selector. It will contain whitespace as `content` and a `border` of 10px, which will add a small triangular shape to the top or bottom of the `box-content`.

`left: 50%;` and `transform: translateX(-50%);` will align the content to the exact center of `box-content`.

```
.box-content::before {  
  content: " ";  
  position: absolute;  
  left: 50%;  
  transform: translateX(-50%);  
  border: 10px solid transparent;  
}
```

You might not see any change in the Event Boxes yet. But we are almost there! I colored the relevant border and positioned the `::before` selector -20px away from top or bottom of `box-content` depending on its position.

```
.box-bottom .box-content::before {  
  border-bottom-color: #00b0bd;  
  top: -20px;  
}.box-top .box-content::before {  
  border-top-color: #00b0bd;  
  bottom: -20px;  
}
```

Press enter or click to view image in full size

![]()

Bingo! We have designed a horizontal timeline from scratch using pure CSS. Find the complete source code from [here](https://github.com/Dulanka-K/Horizontal-Timeline.git).

## Summary

This article is a comprehensive and hands-on guide on how to develop a timeline using pure CSS. I have followed a horizontal approach since you might not find them abundant on the web.

In addition to the above steps, we can bring more additions to the timeline, such as horizontal scrolling, by adding a bit of JavaScript. You could also try to make it responsive, but I will not recommend it as it will break the timeline, and the process will be tedious.

I believe you managed to design a cool timeline with the help of this guide. See you again in another awesome article. Until then, happy coding! 💻

## Build better Component Libs and Design Systems

![]()

[**Bit**](https://bit.cloud/)**’s open-source tool** help 250,000+ devs to build apps with components.

Turn any UI, feature, or page into a **reusable component** — and share it across your applications. It’s easier to collaborate and build faster.

**→** [**Learn more**](https://bit.dev/)

Split apps into components to make app development easier, and enjoy the best experience for the workflows you want:

## → [Micro-Frontends](/how-we-build-micro-front-ends-d3eeeac0acfc)

## → [Design System](/how-we-build-our-design-system-15713a1f1833)

## → [Code-Sharing and reuse](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4)

## → [Monorepo](https://www.youtube.com/watch?v=5wxyDLXRho4&t=2041s)

## Learn More

[## Improve Page Rendering Speed Using Only CSS

### 4 Important CSS tips for faster page rendering

blog.bitsrc.io](/improve-page-rendering-speed-using-only-css-a61667a16b2?source=post_page-----862ffea5b99b---------------------------------------)

[## Pure CSS to Make a Button “Shine” and Gently Change Colors Over Time

### Because animations and gradients in CSS are delightful.

blog.bitsrc.io](/pure-css-to-make-a-button-shine-and-gently-change-colors-over-time-5b685d9c6a7e?source=post_page-----862ffea5b99b---------------------------------------)

[## Creating morphing animations with CSS clip-path

### Learn how to implement morphing, a technique for transforming one appearance into another, using CSS.

blog.bitsrc.io](/creating-morphing-animations-with-css-clip-path-3c3bf5e4335f?source=post_page-----862ffea5b99b---------------------------------------)

[## Independent Components: The Web’s New Building Blocks

### Why everything you know about Microservices, Micro Frontends, Monorepos, and even plain old component libraries, is…

blog.bitsrc.io](/independent-components-the-webs-new-building-blocks-59c893ef0f65?source=post_page-----862ffea5b99b---------------------------------------)

[## Creating a Developer Website with Bit components

### How I built my portfolio using independent React components.

blog.bitsrc.io](/creating-a-developer-website-with-bit-components-3f4083a7f050?source=post_page-----862ffea5b99b---------------------------------------)

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----862ffea5b99b---------------------------------------)

[## How we Build a Component Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----862ffea5b99b---------------------------------------)

[## How to reuse React components across your projects

### How to create reusable React components that can be distributed and used across all projects in your company.

bit.dev](https://bit.dev/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4/?source=post_page-----862ffea5b99b---------------------------------------)

[## 5 Ways to Build a React Monorepo

### Build a production-grade React monorepo: From fast builds to code-sharing and dependencies.

blog.bitsrc.io](/5-ways-to-build-a-react-monorepo-a294b6c5b0ac?source=post_page-----862ffea5b99b---------------------------------------)

[## How to Create a Composable React App with Bit

### In this guide, you'll learn how to build and deploy a full-blown composable React application with Bit. Building a…

bit.dev](https://bit.dev/blog/how-to-create-a-composable-react-app-with-bit-l7ejpfhc/?source=post_page-----862ffea5b99b---------------------------------------)

[## How to Reuse and Share React Components in 2023: A Step-by-Step Guide

### Learn how easy code sharing and collaboration can be, with Bit’s intuitive approach to reusable React components.

blog.bitsrc.io](/how-to-reuse-and-share-react-components-in-2023-a-step-by-step-guide-85642e543afa?source=post_page-----862ffea5b99b---------------------------------------)

[## 5 Tools for Building React Component Libraries in 2023

### Learn what options are there to make your life easier when trying to create your own component library

blog.bitsrc.io](/5-tools-for-building-react-component-libraries-in-2023-d8fb8e4c13b4?source=post_page-----862ffea5b99b---------------------------------------)