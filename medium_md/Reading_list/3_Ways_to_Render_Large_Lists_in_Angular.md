---
title: "3 Ways to Render Large Lists in Angular"
url: https://medium.com/p/9f4dcb9b65
---

# 3 Ways to Render Large Lists in Angular

[Original](https://medium.com/p/9f4dcb9b65)

# 3 Ways to Render Large Lists in Angular

## An overview of the available techniques to render large lists of items with Angular

[![Giancarlo Buomprisco](https://miro.medium.com/v2/resize:fill:64:64/1*AIIoORiyf4Knk6jiyHgdQg.png)](https://medium.com/@.gc?source=post_page---byline--9f4dcb9b65---------------------------------------)

[Giancarlo Buomprisco](https://medium.com/@.gc?source=post_page---byline--9f4dcb9b65---------------------------------------)

8 min read

·

Mar 5, 2020

--

9

Listen

Share

More

Press enter or click to view image in full size

![]()

Frameworks in 2020 got better, more efficient and faster. With that said, rendering large lists of items on the Web without causing the Browser to freeze can still be hard even for the fastest frameworks available.

This is one of the many cases where “the framework is fast, your code is slow”.

There are many different techniques that make rendering a large number of items in a non-blocking way for the users. In this article, I want to explore the current techniques available, and which ones are best to use based on particular use-cases.

[![Build in AI speed — Compose enterprise-grade applications, features, and components]()](https://bit.cloud)

Although this article focuses on how to optimize rendering with Angular, these techniques are actually applicable to other frameworks or simply Vanilla Javascript.

> The framework is fast, your code is slow

This article goes in detail about an aspect I talked about in one of my previous articles: rendering too much data.

[## Top Reasons Why Your Angular App Is Slow

### Is your app slow? Learn what to watch out when debugging poor performance in your Angular apps!

blog.bitsrc.io](/top-reasons-why-your-angular-app-is-slow-c36780a0a289?source=post_page-----9f4dcb9b65---------------------------------------)

We will take a look at the following techniques:

* Virtual Scrolling (using the Angular CDK)
* Manual Rendering
* Progressive Rendering

> *💡* Whatever implementation you choose for rendering long lists, make sure you share your reusable Angular components to [**Bit.dev**](https://bit.dev)’s component hub. It will save you time otherwise spent on repeating yourself and will make it easier for you and your team to use tested and performance-optimized code across your Angular projects.

### Learn more here:

[## Build and share independent Angular components with Bit

### Create Angular components with Bit

bit.dev](https://bit.dev/docs/angular-components/components-overview/?source=post_page-----9f4dcb9b65---------------------------------------)

***Also, for a glimpse into Bit and some other Angular dev tools, check out this article:***

[## Top 8 Tools for Angular Development in 2023

blog.bitsrc.io](/top-8-tools-for-angular-development-in-2023-a99d9f3a2e4e?source=post_page-----9f4dcb9b65---------------------------------------)

[![]()](https://bit.dev)

You can read more about it in my previous post:

[## Sharing Components with Angular and Bit

### An Introduction to Bit: Building and sharing Angular components

blog.bitsrc.io](/sharing-components-with-angular-and-bit-b68896806c18?source=post_page-----9f4dcb9b65---------------------------------------)

## 1. Virtual Scrolling

Virtual Scrolling is probably the most efficient way of handling large lists, with a catch. Thanks to the [Angular CDK](https://material.angular.io/cdk/scrolling/overview) and other plugins it is very easy to implement in any component.

The concept is simple, but the implementation is not always the easiest:

* given a container and a list of items, an item is only rendered if it’s within the visible boundaries of the container

To use the CDK’s Scrolling module, we first need to install the module:

```
npm i @angular/cdk
```

Then, we import the module:

```
import { ScrollingModule } from '@angular/cdk/scrolling';@NgModule({  
 ...  
 imports: [ ScrollingModule, ...]  
})  
export class AppModule {}
```

We can now use the components to use virtual scrolling in our components:

```
<cdk-virtual-scroll-viewport itemSize="50">         
 <div *cdkVirtualFor="let item of items">  
   {{ item }}  
 </div>  
</cdk-virtual-scroll-viewport>
```

[## cdk-virtual-scrolling-2 - StackBlitz

### Starter project for Angular apps that exports to the Angular CLI

stackblitz.com](https://stackblitz.com/edit/cdk-virtual-scrolling-2?embed=1&file=src%2Fapp%2Fapp.component.ts&source=post_page-----9f4dcb9b65---------------------------------------)

As you can see, this is extremely easy to use and the results are impressive.The component renders thousands and thousands of items without any problem.

If Virtual Scrolling is so good and easy to achieve, why bother exploring other techniques? This is something I’ve been wondering too — and actually there’s more than one reason as to why.

* The way it’s going to work **is very dependent on implementation**: it’s hard to be able to manage all the possible scenarios with one single implementation.  
  For example, my component depended on the Autocomplete field (built by the same team) and unfortunately, it didn’t work as expected. **The more complex your items, the more difficult it’s going to be**.
* Another module, another **big chunk of code added to your app**.
* Accessibility and Usability: the hidden items are not rendered, and therefore won’t be searchable.

Virtual Scrolling is ideal (when it works) in a number of situations:

* an undefined and possibly enormous list of items (approximately greater than 5k, but it’s highly dependent on the complexity of each item)
* infinite scrolling of items

## 2. Manual Rendering

One of the options I’ve tried to speed up a large list of items is manual rendering using Angular’s API rather than relying on `*ngFor`.

We have a simple ngFor loop template:

```
<tr   
*ngFor="let item of data; trackBy: trackById; let isEven = even; let isOdd = odd"  
    class="h-12"  
    [class.bg-gray-400]="isEven"  
    [class.bg-gray-500]="isOdd"  
>  
  <td>  
    <span class="py-2 px-4">{{ item.id }}</span>  
  </td>  
  
  <td>  
    <span>{{ item.label }}</span>  
  </td>  
  
  <td>  
    <a>  
      <button class="py-2 px-4 rounded (click)="remove(item)">x</button>  
    </a>  
  </td>  
</tr>
```

I’m using a benchmark inspired by [js-frameworks-benchmark](https://github.com/krausest/js-framework-benchmark) to calculate the rendering of 10000 simple items.

The first benchmark run was done with a simple, regular \*ngFor. Here are the results: scripting took 1099ms and rendering took 1553ms, 3ms painting.

Press enter or click to view image in full size

![]()

By using Angular’s API, we can manually render the items.

```
<tbody>  
  <ng-container #itemsContainer></ng-container>  
</tbody><ng-template #item let-item="item" let-isEven="isEven">  
  <tr class="h-12 "  
      [class.bg-gray-400]="isEven"  
      [class.bg-gray-500]="!isEven"  
  >  
    <td>  
      <span class="py-2 px-4">{{ item.id }}</span>  
    </td>  
  
    <td>  
      <span>{{ item.label }}</span>  
    </td>  
  
    <td>  
      <a>  
        <button class="py-2 px-4 rounded" (click)="remove(item)">x</button>  
      </a>  
    </td>  
  </tr>  
</ng-template>
```

The controller’s code changes in the following way:

* we declare our template and our container

```
@ViewChild('itemsContainer', { read: ViewContainerRef }) container: ViewContainerRef;  
@ViewChild('item', { read: TemplateRef }) template: TemplateRef<any>;
```

* when we build the data, we also render it using the *ViewContainerRef* **createEmbeddedView** method

```
private buildData(length: number) {  
  const start = this.data.length;  
  const end = start + length;  
  
  for (let n = start; n <= end; n++) {  
    this.container.createEmbeddedView(this.template, {  
      item: {  
        id: n,  
        label: Math.random()  
      },  
      isEven: n % 2 === 0  
    });  
  }  
}
```

Results show a modest improvement:

* 734ms time spent scripting, 1443 rendering, and 2ms painting

Press enter or click to view image in full size

![]()

In practical terms, though, it’s still super slow! The browser freezes for a few seconds when the button is clicked, delivering a poor user experience to the user.

This is how it looks like (I’m moving the mouse to simulate a loading indicator 😅):

Press enter or click to view image in full size

![]()

Let’s now try *Progressive Rendering* combined with *Manual Rendering*.

## 3. Progressive Rendering

The concept of progressive rendering is simply to render a subset of items progressively and postpone the rendering of other items in the event loop. This allows the browser to smoothly and progressively render all the items.

The code below is simply:

* we create an interval running every 10ms and render 500 items at once
* when all items have been rendered, based on the index, we stop the interval and break the loop

```
private buildData(length: number) {  
  const ITEMS_RENDERED_AT_ONCE = 500;  
  const INTERVAL_IN_MS = 10;  
  
  let currentIndex = 0;  
  
  const interval = setInterval(() => {  
    const nextIndex = currentIndex + ITEMS_RENDERED_AT_ONCE;  
  
    for (let n = currentIndex; n <= nextIndex ; n++) {  
      if (n >= length) {  
        clearInterval(interval);  
        break;  
      }      const context = {  
        item: {  
          id: n,  
          label: Math.random()  
        },  
        isEven: n % 2 === 0  
      };      this.container.createEmbeddedView(this.template, context);  
    }  
  
    currentIndex += ITEMS_RENDERED_AT_ONCE;  
  }, INTERVAL_IN_MS);
```

Notice that the number of items rendered and the interval time **is totally dependent on your circumstances**. For example, if your items are very complex, rendering 500 items at once is certainly going to be very slow.

As you can see below, the stats look certainly worse:

Press enter or click to view image in full size

![]()

What’s not worse though is the user experience. Even though the time it takes to render the list is longer than before, the user can’t tell. We’re rendering 500 items at once, and the rendering happens outside of the container boundaries.

Some issues may arise with the container changing its size or scroll position while that happens, so these issues need to be mitigated in a few cases.

Let’s see how it looks like:

Press enter or click to view image in full size

![]()

## Final Words

The above techniques are certainly useful in some situations and I’ve used them whenever virtual scrolling was not the best option.

With that said, for the most part, virtual scrolling using a great library like Angular’s CDK is definitely the best way to tackle large lists.

If you need any clarifications, or if you think something is unclear or wrong, do please leave a comment!

*I hope you enjoyed this article! If you did, follow me on* [*Medium*](https://medium.com/@.gc), [*Twitter*](https://twitter.com/home) *or my* [*website*](https://frontend.consulting/) *for more articles about Software Development, Front End, RxJS, Typescript and more!*

## Build Angular Apps with reusable components, just like Lego

![]()

[**Bit**](https://bit.cloud/)**’s open-source tool** help 250,000+ devs to build apps with components.

Turn any UI, feature, or page into a **reusable component** — and share it across your applications. It’s easier to collaborate and build faster.

[## Introduction to Angular | Bit

### Documentation page for Introduction to Angular - Bit.

bit.dev](https://bit.dev/docs/angular-introduction?source=post_page-----9f4dcb9b65---------------------------------------#-learn-angular-with-bit-)

**→** [**Learn more**](https://bit.cloud/teambit/angular/content/angular-overview)

Split apps into components to make app development easier, and enjoy the best experience for the workflows you want:

## → [Micro-Frontends](/how-we-build-micro-front-ends-d3eeeac0acfc)

## → [Design System](/how-we-build-our-design-system-15713a1f1833)

## → [Code-Sharing and reuse](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4)

## → [Monorepo](https://www.youtube.com/watch?v=5wxyDLXRho4&t=2041s)

## Learn more:

[## Introducing Angular Component Development Environment

### Learn about the recent upgrades for Angular Developer Experience with Bit, how to modify and extend your configuration…

bit.dev](https://bit.dev/blog/introducing-angular-component-development-environment-lfhd699k?source=post_page-----9f4dcb9b65---------------------------------------)

[## 10 Useful Angular Features You’ve Probably Never Used

### 10 useful Angular features you might have missed.

blog.bitsrc.io](/10-useful-angular-features-youve-probably-never-used-e9e33f5c35a7?source=post_page-----9f4dcb9b65---------------------------------------)

[## Top 8 Tools for Angular Development in 2023

blog.bitsrc.io](/top-8-tools-for-angular-development-in-2023-a99d9f3a2e4e?source=post_page-----9f4dcb9b65---------------------------------------)

[## Getting Started with a New Angular Project in 2023

blog.bitsrc.io](/getting-started-with-a-new-angular-project-in-2023-c6ae93facbd6?source=post_page-----9f4dcb9b65---------------------------------------)

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----9f4dcb9b65---------------------------------------)

[## How to Share Angular Components Between Projects and Apps

### Share and collaborate on NG components across projects, to build your apps faster.

blog.bitsrc.io](/how-to-share-angular-components-between-project-and-apps-5eb0600d99d2?source=post_page-----9f4dcb9b65---------------------------------------)

[## How we Build a Component Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----9f4dcb9b65---------------------------------------)

[## Creating a Developer Website with Bit components

### How I built my portfolio using independent React components.

blog.bitsrc.io](/creating-a-developer-website-with-bit-components-3f4083a7f050?source=post_page-----9f4dcb9b65---------------------------------------)

[## 11 Useful Online Tools for Frontend Developers

### Useful online developer tools I love to use.

blog.bitsrc.io](/12-useful-online-tools-for-frontend-developers-bf98f3bf7c63?source=post_page-----9f4dcb9b65---------------------------------------)

[## 10 Top Chrome Extensions for Front-End Developers

### 10 Useful Chrome DevTools extensions you should know in 2020.

blog.bitsrc.io](/10-top-chrome-extensions-for-front-end-developers-db23a01dce1e?source=post_page-----9f4dcb9b65---------------------------------------)