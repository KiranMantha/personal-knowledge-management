---
title: "Angular Pro Tip: How to dynamically create components in <body>"
url: https://medium.com/p/ba200cc289e6
---

# Angular Pro Tip: How to dynamically create components in <body>

[Original](https://medium.com/p/ba200cc289e6)

# Angular Pro Tip: How to dynamically create components in <body>

[![Carlos Roso](https://miro.medium.com/v2/resize:fill:64:64/2*ieZduxEeN_EjF-UEgxAMfw.jpeg)](/@caroso1222?source=post_page---byline--ba200cc289e6---------------------------------------)

[Carlos Roso](/@caroso1222?source=post_page---byline--ba200cc289e6---------------------------------------)

4 min read

·

Jun 24, 2017

--

19

Listen

Share

More

![]()

**Update:** I wrote another blog post in which I explain how to achieve this exact same result using Portals from the Angular CDK. Please take a [look at it](https://hackernoon.com/a-first-look-into-the-angular-cdk-67e68807ed9b). If you’re not into magic and you want to know how to do it from scratch, then keep reading this article.

## **Just show me the code**

If you’re somewhat like me, you just want to see the code and you’ll figure it out, so here you go. The following service has just one simple method `appendComponentToBody` which will append your component as a direct child of the body and also add it to the Angular’s component tree (so that it can be included in the Angular’s change detection cycle). **See working plunker at the end of this post.**

## **Cool, but, da heck was that?**

If you got here after checking the code, then it means you need some explanation for what’s happening in that gist.

### A little bit of a context

I first came across this problem a while ago when trying to add modals to my web app. I couldn’t find good documentation to dynamically add components to the body of my document. Some of the alternatives suggested adding *helper* components at the `app.component.html` level to act as host containers, some others suggested passing the `viewRef` in `app.component.ts` to a custom service so that `app-root` could be used later as an anchor, etc. None of them I liked, though. I then traveled to ng-conf looking for an answer and asked Jeremy Elbourn (@jelbourn) about this where he pointed me to a couple of utility classes inside Angular Material.

### Navigating Angular Material

Simply put, the angular material repo is **one hell of a good resource**. You should be studying it on a daily basis if you truly want to understand how to build robust and well written Angular components: <https://github.com/angular/material2>.

Finding how they append components to the body took me a while to understand, though. They call a bunch of methods, from a bunch of files, but I’m here to break it down for you. Let’s jump right in.

## Breaking down the gist

Check the code snippet again and see the numbers in the comments. I’ll use those numbers to run the explanation.

### **1. Create a component reference**

Use the `ComponentFactoryResolver` to create a reference of your component. As you’ll be adding your component to the `AppRef` (see step 2), you need to create this component using the Angular’s default Injector which is provided in the constructor.

**Please note** that, at this point, you can use the `componentRef` to bind data to your component’s inputs as `componentRef.instance.myInput = 'yay!'` .

### 2. Attach component to Application Ref

At this point, you have a reference to your component, but it doesn’t live in Angular’s world yet. The component is not inside the ng component tree so Angular won’t run change detection on it. To allow change detection on our component we should attach it to the `ApplicationRef` .

### 3. Get the DOM element from the Component Ref

We’re almost there. We have a `componentRef` and it’s also living in Angular’s world. Now we want to see it rendered in the page and for that we have to get the DOM element out of the component. The code is pretty verbose to let TypeScript understand what we’re trying to achieve but, basically, we’re doing this to get the component’s DOM element: `componentRef.hostView.rootnodes[0]` .

### 4. Append the component body

**TL;DR.** Use the good old `document.body.appendChild` using the DOM element we got from step 3.

**Some remarks about this**. It’s been told that Angular is a platform and that no `<body>` exists when running Angular on the server, on a Web Worker, on mobile (?), etc. But, having said that, I’m having a hard time trying to find a use case in which a dynamically created component will have to be rendered server-side, or some other context. I don’t know how it will work in Ionic, but for sure there’s a parent anchor DOM element which you can replace by `body` to make this work.

### 5. (Optional) Nuke it

This is let you know how to remove the component in just two steps:

1. Detach the view from the `ApplicationRef` so that no change detection will be performed by Angular.
2. Destroy the Component Ref. This will automatically remove the DOM element from the document.

**Very important:** You will have to add your component to `entryComponents` in your main module declaration. This will allow Angular to create your component on the fly.

**Working plunker:** <https://plnkr.co/edit/Yc1ijM6shHt2JAPi7Fdg>

**Angular plugin using this approach:** <https://github.com/jdjuan/ng-notyf>

Show some love if you liked it. Leave a comment. Reach out to me at Twitter @caroso1222.