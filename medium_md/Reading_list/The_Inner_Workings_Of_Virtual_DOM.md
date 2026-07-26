---
title: "The Inner Workings Of Virtual DOM"
url: https://medium.com/p/666ee7ad47cf
---

# The Inner Workings Of Virtual DOM

[Original](https://medium.com/p/666ee7ad47cf)

# The Inner Workings Of Virtual DOM

[![rajaraodv](https://miro.medium.com/v2/resize:fill:64:64/1*HIuWP_7gy9QvnssCalFT4g.png)](/?source=post_page---byline--666ee7ad47cf---------------------------------------)

[rajaraodv](/?source=post_page---byline--666ee7ad47cf---------------------------------------)

11 min read

·

Dec 11, 2016

--

22

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D666ee7ad47cf&operation=register&redirect=https%3A%2F%2Frajaraodv.medium.com%2Fthe-inner-workings-of-virtual-dom-666ee7ad47cf&source=---header_actions--666ee7ad47cf---------------------post_audio_button------------------)

Share

![]()

Virtual DOM (VDOM aka VNode) is magical ✨ but is also complex and hard to understand😱. [React](https://facebook.github.io/react/), [Preact](https://preactjs.com) and similar JS libraries use them in their core. Unfortunately I couldn’t find any good article or doc that explains it in a detailed-yet-simple-to-understand fashion. So I thought of writing one myself.

> Note: This is a LONG post. I’ve added tons of pictures to make it simple but it also makes the post appear even longer.
>
> I’m using [Preact’s](https://github.com/developit/preact/) code and VDOM as it is small and you can look at it yourself with ease in the future. **But I think most of the concepts applies to React as well.**
>
> **My hope is that once you read this, you’ll be able to better understand and hopefully contribute to libraries like React and Preact.**

In this blog, I’ll take a simple example and go over various scenarios to give you an idea as to how they actually work. Specifically, I’ll go over:

1. Babel and JSX
2. Creating VNode — A single virtual DOM element
3. Dealing with components and sub-components
4. Initial rendering and creating a DOM element
5. Re-rendering
6. Removing DOM element.
7. Replacing a DOM element.

## The app:

The app a simple [filterable Search app](http://codepen.io/rajaraodv/pen/BQxmjj) that contains two components “**FilteredList**” and “**List**”. The List renders a list of items (default: “California” and “New York”). The app has a search field that filters the list based on the characters in the field. Pretty straight forward.

Press enter or click to view image in full size

![]()

> Live app: <http://codepen.io/rajaraodv/pen/BQxmjj>

## The Big Picture

At a high-level, we write components in JSX(html in JS), that gets converted to pure JS by CLI tool [Babel](http://babeljs.io). Then Preact’s “h” ([hyperscript](https://github.com/dominictarr/hyperscript)) function, converts it into VDOM tree (aka VNode). And finally Preact’s Virtual DOM algorithm, creates real DOM from the VDOM that creates our app.

Press enter or click to view image in full size

![]()

**Before we get into the weeds of the VDOM lifecycle, let’s understand JSX as it provides the starting point for the library.**

## 1. Babel And JSX

In React, Preact like libraries, there is no HTML and instead **everything is JavaScript**. So we need to write even the HTML in JavaScript. But writing DOM in pure JS is a nightmare!😱

For our app we’ll have to write HTML like below:

> Note: I’ll explain “h” soon

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

That’s where JSX comes in. JSX essentially allows us to write HTML in JavaScript! And also allows us to use JS within that by curly braces{}.

JSX helps us easily write our components like below:

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

### Converting JSX tree to JavaScript

JSX is cool but it’s not a valid JS, but ultimately we need REAL DOM. JSX only helps in writing a *representation* of real DOM and otherwise it’s useless.

So we a way need to convert into a corresponding JSON object (VDOM, which is also a tree) so we can eventually use it as an input to create real DOM. We need a function to do that.

And that function is the [“h” function](https://github.com/developit/preact/blob/master/src/h.js) in Preact. It’s the equivalent to “[React.createElement](https://facebook.github.io/react/docs/react-api.html#createelement)” in React.

> “h” stands for [hyperscript](https://github.com/dominictarr/hyperscript) — one of the first libs to create HTML in JS (VDOM)

But how to convert JSX into “h” function calls? And that’s where [Babel](http://babeljs.io) comes in. Babel simply goes through each JSX node and converts them to “h” function calls.

Press enter or click to view image in full size

![]()

### **Babel JSX (React Vs Preact)**

By default, Babel converts JSX to React.createElement calls because it defaults to React.

Press enter or click to view image in full size

![]()

But we can easily change the name of the function to anything we want (like “h” for Preact) by adding “[Babel Pragma](https://babeljs.io/docs/plugins/transform-react-jsx/)” like below:

```
Option 1:  
//.babelrc  
{   "plugins": [  
      ["transform-react-jsx", { "pragma": "h" }]  
     ]   
}Option 2:  
//Add the below comment as the 1st line in every JSX file  
/** @jsx h */
```

Press enter or click to view image in full size

![]()

### Main Mount To real DOM

Not only the code in “render” methods of the components are converted to “h” functions, but also the starting mount!

**And this is where the execution start and everything begins!**

```
//Mount to real DOM  
render(<FilteredList/>, document.getElementById(‘app’));//Converted to "h":  
render(h(FilteredList), document.getElementById(‘app’));
```

### The Output of “h” function

The “h” function takes the output of JSX and creates something called a “VNode” (React’s “createElement” creates ReactElement). A Preact’s “VNode” (or a React’s “Element”) is simply a JS object representation of a single DOM node with it’s properties and children.

It looks like this:

```
{  
   "nodeName": "",  
   "attributes": {},  
   "children": []  
}
```

For example, VNode for our app’s Input looks like this:

```
{  
   "nodeName": "input",  
   "attributes": {  
    "type": "text",  
    "placeholder": "Search",  
    "onChange": ""  
   },  
   "children": []  
  }
```

> **Note: “h” function doesn’t create the entire tree!** It simply creates JS object for a given node. But since the “**render**” method already has the DOM JSX in a tree fashion, the end result will be a VNode with children and grand children that looks like a tree.
>
> ***Reference Code:***
>
> ***“h” :***[*https://github.com/developit/preact/blob/master/src/h.js*](https://github.com/developit/preact/blob/master/src/h.js)
>
> **VNode**: <https://github.com/developit/preact/blob/master/src/vnode.js>
>
> ***“render”:*** [*https://github.com/developit/preact/blob/master/src/render.js*](https://github.com/developit/preact/blob/master/src/render.js)
>
> **“buildComponentFromVNode:** <https://github.com/developit/preact/blob/master/src/vdom/diff.js#L102>

OK, let’s see how Virtual DOM works.

## Virtual DOM Algorithm Flowchart For Preact

In the flowchart below shows how components (and child components) are created, updated and deleted by Preact. It also shows when lifecycle events like “componentWillMount” and so on are called.

> Note: We’ll go over each section in a step-by-step manner so don’t worry if it looks complicated

Press enter or click to view image in full size

![]()

Yes, it’s hard to understand all at once. So let’s go over various sections of the flowchart by going through various scenarios in a step-by-step manner.

> Note: I’ll highlight sections of the lifecycle in “yellow” when discussing specific steps.

## Scenario 1: Initial Creation Of The App

### 1.1 — Creating VNode (Virtual DOM) For A Given Component

The highlighted section shows the initial loop that creates VNode (Virtual DOM) tree for a given component. Note that this doesn’t create VNode for sub-components (that’s a different loop).

Press enter or click to view image in full size

![]()

The picture below shows what happens when our app loads for the first time. The library ends up creating a VNode with children and attributes for the main FilteredList component.

> Note: Along the way it also calls “componentWillMount” and “render” lifecycle methods (see the green blocks in the picture above).

Press enter or click to view image in full size

![]()

At this point, we have a VNode that has a “**div**” parentNode that has an “**input**” and a “**List**” child nodes.

> **Reference code:**
>
> *Most lifecycle events like: componentWillMount, render and so on:* [*https://github.com/developit/preact/blob/master/src/vdom/component.j*](https://github.com/developit/preact/blob/master/src/vdom/component.js#L101)*s*

### 1.2 — If Not A Component, create a REAL DOM

In this step, it’ll simply create real DOM for the parent node (div) and repeat process for child nodes (“input” and “List”).

Press enter or click to view image in full size

![]()

At this point, we have just “div” as shown in the picture below:

Press enter or click to view image in full size

![]()

> **Reference code:**
>
> document.createElement: <https://github.com/developit/preact/blob/master/src/dom/recycler.js>

### 1.3 — Repeat for all children

At this point, the loop is repeated for all children. In our app, it’ll be repeated for “input” and “List” items.

Press enter or click to view image in full size

![]()

### 1.4 — Process Child And Append To Parent.

In this step, we’ll process leaf. Since “input” has a parent (“div”), we’ll append input as a child to div. Then the control stops and return to create “List” (which is the 2nd child of “div”).

Press enter or click to view image in full size

![]()

At this point, our app looks like below:

Press enter or click to view image in full size

![]()

> Note: that after “input” is created, since it doesn’t have any children, it doesn’t immediately loop and create “List”! Instead it’ll first append “input” to the parent “div” and then goes back to process “List”
>
> **Reference code:**
>
> appendChild: <https://github.com/developit/preact/blob/master/src/vdom/diff.js>

### 1.5 Process child component(s)

The control goes back to step 1.1 and starts all 0ver again for “List” component. But since “List” is a component, it calls the **render** method of the “List” component to get new set of VNodes that look like below.

Press enter or click to view image in full size

![]()

That loop completes for the List component and returns List’s VNode that looks like below:

Press enter or click to view image in full size

![]()

> **Reference Code:**
>
> **“buildComponentFromVNode:** <https://github.com/developit/preact/blob/master/src/vdom/diff.js#L102>

### 1.6 Repeat steps 1.1 through 1.4 for all the Child Nodes

It’ll repeat the above steps again for each node. Once it reaches the leaf node, it appends it to the node’s parent and repeats the process.

Press enter or click to view image in full size

![]()

The below picture shows how each node is added (hint: depth-first).

![]()

### 1.7 Finish processing

At this point, It’s done processing. It simply calls “componentDidMount” for all the components (starting from child components to parent components) and stops.

Press enter or click to view image in full size

![]()

> **Important Note:** Once everything is done, a reference to the real DOM is added to each of the component instances. This reference is used for remaining updates (create, update, delete) to compare and avoid recreating the same DOM nodes.

## SCENARIO 2: Delete Leaf Node

Say we typed “cal” and hit enter. This will remove the 2nd list node, a leaf node (New York) while keeping all other parent nodes.

Press enter or click to view image in full size

![]()

Let’s see how the flow looks for this scenario.

### 2.1 Create VNodes like before.

After initial rendering, every change in the future is an “update”. When it comes to creating VNodes, the update cycle works very similar to create cycle and **creates VNodes all over again.**

But since it’s an update (and not creation) of the component, it makes “componentWillReceiveProps”, “shouldComponentUpdate”, and “componentWillUpdate” calls to each component and sub-component.

**In addition, update cycle, doesn’t recreate DOM elements if those elements are already there.**

Press enter or click to view image in full size

![]()

> **Reference Code**
>
> **removeNode:** <https://github.com/developit/preact/blob/master/src/dom/index.js#L9>
>
> **insertBefore:** <https://github.com/developit/preact/blob/master/src/vdom/diff.js#L253>

### 2.2 Use the reference real DOM node and avoid creating duplicate nodes

As mentioned earlier, each component has a reference to corresponding real DOM tree that was created during initial loading. The picture below shows how references look for our app at this point.

Press enter or click to view image in full size

![]()

And when VNodes created, each VNode’s attributes are compared w/ the attributes of the REAL DOM at that node**. If real DOM exists, the loop moves on to the next node.**

Press enter or click to view image in full size

![]()

> **Reference Code**
>
> innerDiffNode: <https://github.com/developit/preact/blob/master/src/vdom/diff.js#L185>

### 2.3 Remove node if there are extra nodes in the REAL DOM

The picture below shows the difference in REAL DOM V/s VNode.

Press enter or click to view image in full size

![]()

And since there is a difference, the “New York” node in REAL DOM is removed by the algorithm as shown in the workflow below. The algorithm also calls “componentDidUpdate” lifecycle event once everything is done.

Press enter or click to view image in full size

![]()

## SCENARIO 3 — Unmounting Entire Component

Use case: Let’s say if we typed **blabla** in the filter, since it doesn’t match “California” or “New York”, we won’t render the child component “List” at all. This means, we need to unmount the entire component.

![]()

Press enter or click to view image in full size

![]()

Deleting a component is similar to Deleting a single node. Except, when we delete a node that has a reference to a component, then the framework calls “componentWillUnmount” and then recursively deletes all the DOM elements. After all the elements are removed from the real DOM, it calls “componentDidUnmount” method of the referenced component.

The picture below shows the reference to “List” component on the real DOM “ul”.

Press enter or click to view image in full size

![]()

The below picture highlights the section in the flowchart to show how deleting/unmounting a component works.

Press enter or click to view image in full size

![]()

> **Reference code**
>
> unmountComponent: <https://github.com/developit/preact/blob/master/src/vdom/component.js#L250>

### **Final Notes:**

I hope that this post gave you enough idea as to how Virtual DOM works (at least in Preact).

Please note that while these scenarios covers major ones, I haven’t covered some of the optimizations in the code.

🙏🏼 Thank you!

### If this was useful, please click the clap 👏 button down below a few times to show your support! ⬇⬇⬇ 🙏🏼

## My Other Posts

### ECMAScript 2015+

1. [*Check out these useful ECMAScript 2015 (ES6) tips and tricks*](https://medium.freecodecamp.org/check-out-these-useful-ecmascript-2015-es6-tips-and-tricks-6db105590377)
2. [*5 JavaScript “Bad” Parts That Are Fixed In ES6*](https://medium.com/@rajaraodv/5-javascript-bad-parts-that-are-fixed-in-es6-c7c45d44fd81#.7e2s6cghy)
3. [*Is “Class” In ES6 The New “Bad” Part?*](https://medium.com/@rajaraodv/is-class-in-es6-the-new-bad-part-6c4e6fe1ee65#.4hqgpj2uv)

### Terminal Improvements

1. [*How to Jazz Up Your Terminal — A Step By Step Guide With Pictures*](https://medium.freecodecamp.org/jazz-up-your-bash-terminal-a-step-by-step-guide-with-pictures-80267554cb22)
2. [*Jazz Up Your “ZSH” Terminal In Seven Steps — A Visual Guide*](https://medium.freecodecamp.org/jazz-up-your-zsh-terminal-in-seven-steps-a-visual-guide-e81a8fd59a38)

### WWW

1. [*A Fascinating And Messy History Of The Web And JavaScript*](https://medium.freecodecamp.org/a-fascinating-and-messy-history-of-the-web-and-javascript-video-8978dc7bda75)

### Virtual DOM

1. [*Inner Workings Of The Virtual DOM*](https://medium.com/@rajaraodv/the-inner-workings-of-virtual-dom-666ee7ad47cf)

### React Performance

1. [*Two Quick Ways To Reduce React App’s Size In Production*](https://medium.com/@rajaraodv/two-quick-ways-to-reduce-react-apps-size-in-production-82226605771a#.6lepbl7ae)
2. [*Using Preact Instead Of React*](https://medium.com/@rajaraodv/using-preact-instead-of-react-70f40f53107c#.7fzp0lyo3)

### Functional Programming

1. [*JavaScript Is Turing Complete — Explained*](https://medium.com/@rajaraodv/javascript-is-turing-complete-explained-41a34287d263#.6t0b2w66p)
2. [*Functional Programming In JS — With Practical Examples (Part 1)*](https://medium.com/@rajaraodv/functional-programming-in-js-with-practical-examples-part-1-87c2b0dbc276#.fbgrmoa7g)
3. [*Functional Programming In JS — With Practical Examples (Part 2)*](https://medium.freecodecamp.org/functional-programming-in-js-with-practical-examples-part-2-429d2e8ccc9e)
4. [*Why Redux Need Reducers To Be “Pure Functions”*](https://medium.com/@rajaraodv/why-redux-needs-reducers-to-be-pure-functions-d438c58ae468#.bntrywxrf)

### WebPack

1. [*Webpack — The Confusing Parts*](https://medium.com/@rajaraodv/webpack-the-confusing-parts-58712f8fcad9#.6ot6deo2b)
2. [*Webpack & Hot Module Replacement [HMR]*](https://medium.com/@rajaraodv/webpack-hot-module-replacement-hmr-e756a726a07#.y667mx4lg) *(under-the-hood)*
3. [*Webpack’s HMR And React-Hot-Loader — The Missing Manual*](https://medium.com/@rajaraodv/webpacks-hmr-react-hot-loader-the-missing-manual-232336dc0d96#.fbb1e7ehl)

### Draft.js

1. [*Why Draft.js And Why You Should Contribute*](https://medium.com/@rajaraodv/why-draft-js-and-why-you-should-contribute-460c4a69e6c8#.jp1tsvsqc)
2. [*How Draft.js Represents Rich Text Data*](https://medium.com/@rajaraodv/how-draft-js-represents-rich-text-data-eeabb5f25cf2#.hh0ue85lo)

### React And Redux :

1. [*Step by Step Guide To Building React Redux Apps*](https://medium.com/@rajaraodv/step-by-step-guide-to-building-react-redux-apps-using-mocks-48ca0f47f9a#.s7zsgq3u1)
2. [*A Guide For Building A React Redux CRUD App*](https://medium.com/@rajaraodv/a-guide-for-building-a-react-redux-crud-app-7fe0b8943d0f#.g99gruhdz) *(3-page app)*
3. [*Using Middlewares In React Redux Apps*](https://medium.com/@rajaraodv/using-middlewares-in-react-redux-apps-f7c9652610c6#.oentrjqpj)
4. [*Adding A Robust Form Validation To React Redux Apps*](https://medium.com/@rajaraodv/adding-a-robust-form-validation-to-react-redux-apps-616ca240c124#.jq013tkr1)
5. [*Securing React Redux Apps With JWT Tokens*](https://medium.com/@rajaraodv/securing-react-redux-apps-with-jwt-tokens-fcfe81356ea0#.xci6o9s6w)
6. [*Handling Transactional Emails In React Redux Apps*](https://medium.com/@rajaraodv/handling-transactional-emails-in-react-redux-apps-8b1134748f76#.a24nenmnt)
7. [*The Anatomy Of A React Redux App*](https://medium.com/@rajaraodv/the-anatomy-of-a-react-redux-app-759282368c5a#.7wwjs8eqo)
8. [*Why Redux Need Reducers To Be “Pure Functions”*](https://medium.com/@rajaraodv/why-redux-needs-reducers-to-be-pure-functions-d438c58ae468#.bntrywxrf)
9. [*Two Quick Ways To Reduce React App’s Size In Production*](https://medium.com/@rajaraodv/two-quick-ways-to-reduce-react-apps-size-in-production-82226605771a#.6lepbl7ae)

If you have questions, please feel free to ask me on Twitter: <https://twitter.com/rajaraodv>

### If this was useful, please click the clap 👏 button below a few times to show your support! ⬇⬇⬇ 🙏🏼