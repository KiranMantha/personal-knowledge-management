---
title: "Demystifying JSX: building your own JSX parser from scratch"
url: https://medium.com/p/caecf58d7cbd
---

# Demystifying JSX: building your own JSX parser from scratch

[Original](https://medium.com/p/caecf58d7cbd)

# Demystifying JSX: building your own JSX parser from scratch

## Because why not?!

[![Fernando Doglio](https://miro.medium.com/v2/resize:fill:64:64/1*gOZB0_zGrIvTLT20MtP6uA.jpeg)](https://deleteman123.medium.com/?source=post_page---byline--caecf58d7cbd---------------------------------------)

[Fernando Doglio](https://deleteman123.medium.com/?source=post_page---byline--caecf58d7cbd---------------------------------------)

7 min read

·

Dec 27, 2022

--

8

Listen

Share

More

Press enter or click to view image in full size

![]()

While it’s not a web standard and Web Components are somewhat trying to replace it, JSX is an amazing technology that came with React to simplify the way we write HTML and JavaScript together.

But how does it work exactly? I mean, yes, we can return JSX from a React component, but we all know that’s not standard JavaScript, so how does it exactly work? What kind of wizardry is behind it?

I personally love when technology “just works”, but if my job depends on it, I try to understand it as much as I can. And one way of doing it, is trying to reverse engineer how it works and write your own version of it.

You get to learn a lot through that process!

So in this article, I’m going to show you how you can write your own version of a JSX parser that can turn a JSX “component” into a JavaScript one that actually returns valid HTML.

Let’s go!

[![Build in AI speed — Compose enterprise-grade applications, features, and components]()](https://bit.cloud)

## The JSX we’ll be parsing

Let’s start at the end, let’s look at the JSX file we’ll be parsing.

If you were to write this in React, you’d have something like this:

Honestly, the only changing part is the initial import, and we’ll actually get to see WHY we need to import React when we want to write JSX.

While the parsing itself takes a bit of work, the logic behind it is actually quite simple. If you look at Rect’s documentation, they’ll show you the output from parsing JSX.

Press enter or click to view image in full size

![]()

Notice how essentially you’re turning each JSX element into a call to `React.createElement` . Yes! That’s why you need to import `React` even though you’re not directly using it, once parsed, the resulting JavaScript *will* be using it.

Now that we got that mystery solved, let’s keep going.

The first attribute of the method is the tag name of the element to create. The second one is an object with all the properties associated with the element being created, and finally, the rest of the attributes (you can have one or more here) will be the direct children of this element (they can be plain text or other elements).

And that’s it, the challenge here is to:

1. Capture the JSX inside the JavaScript.
2. Parse it into a tree-like structure that we can traverse and query.
3. Translate that structure into JavaScript code (text) that will be written in place of the JSX.
4. Save the output from step 3 to disk into a file with a `.js` extension.

Let’s get coding!

## Extracting and parsing the JSX from the component

The first step involves extracting the JSX somehow from the component and parsing it into a tree-like structure.

Granted, those are two steps, but we’ll do them together.

The first thing we’ll need to do is to read the JSX file, and then using a Regular Expression (yes, we’ll be using a few throughout this article), we’ll capture the JSX code.

Once we have it, we can use an HTML parser to understand it.

Keep in mind that we can do that here, because at this point, all we care about is the structure, not the actual features of JSX. So we’ll use the `fs` module from Node to read the file, and the `node-html-parser` package.

The function looks like this:

This function is using a RegExp to look for the opening tag of the first component inside the `(...)` section of the function. On line 10, we call the `parse` function that returns a `root` element where the `firstChild` is the root element from our JSX (in our case, the wrapping `div` ).

Now that we have the tree-like structure, let’s start translating it to code. For that, we’ll call the `translate` function.

## Translating the HTML to JS code

Since we’re dealing with a somewhat limited depth in our tree-like structure, we’ll safely use recursion to traverse this tree.

Here is what the function looks like, we’ll analyze it below:

First, we’ll go through all the children and we’ll call the `translate` function on them. If the children are empty, then that call will return `null` and we’ll filter those results on line 7.

Once we’ve dealt with the children, let’s take a look at line 9, where we do a quick sanity check for the type of the node. If the type is 3, that means this is a Text Node, which is fancy talk for “just text”, so we’ll return the parsed text.

Why are we calling the `parseText` function? Because even inside the text nodes, we need to look out for JSX expressions inside `{…}` . So this function will take care of checking and properly changing the returned string if required.

After that, meaning, we’re not really dealing with a Text Node, we’ll get the tag name (line 14), and we’ll parse the attributes (line 16). Parsing the attributes means we’ll take that raw string and turn it into a proper JSON.

Finally, we’ll return the line of code we want to generate (i.e the call to `createElement` with the right parameters). That’s what happens on line 18.

Remember that we’re writing the code, not actually running it. That’s why it’s all inside strings.

Finally, the last detail to notice about this function, is that the generated code calls the `createElement` method from the `MyLib` module. That’s why we have the `import * as MyLib from './MyLib.js’` inside the JSX file.

We now have to start dealing with strings to replace the JSX expressions, both inside the text nodes and the properties object of each element.

*Did you like what you read? Consider subscribing to my* ***FREE newsletter*** *where I share my 2 decades’ worth of wisdom in the IT industry with everyone. Join “*[*The Rambling of an old developer*](https://fernandodoglio.substack.com/)*” !*

## Parsing expressions

The type of JSX expression I’m supporting in this implementation is the easiest one. As you see in the example, you can add JS variables inside these expressions, and they will remain as variables in the final output.

Here are the functions that do that:

If we have interpolations (i.e variables inside curly braces) then we call the `replaceInterpolation` function, which runs through all the matching interpolations and replaces them with the properly formatted string (essentially leaving the variable name in a way that will generate a JS variable when written into the JS file).

We use these functions also with the attributes object. Since we’re using the `JSON.stringify` method when returning the JS code, that function will turn all values into strings (well, almost all of them, but definitely the ones that we defined as single variables). So instead, we’ll parse the string returned by the `stringify` method and we’ll make sure to replace the interpolated variables properly.

You can look at the `getAttrs` function [here](https://github.com/deleteman/jsx-parser/blob/main/index.js#L9), to understand how that’s done.

Let’s now look at the output code from parsing our JSX file.

## The JavaScript code

The output from reading and parsing my silly JSX code, is the following:

The really interesting bit about this code, are the generated calls to `createElement` . You can see how they’re nested and they’re referencing the variables I had interpolated back in the JSX file.

If we execute this code, the output will be:

But the last question remains unanswered: how is the `createElement` method implemented? Well, I do have a simplified version of it as well:

Essentially, I’m creating a wrapper element with the `tag` value, adding the properties for it (if there are any) and finally, I’ll go through the list of children (which is a rest attribute containing all the attributes added) and during this process, I’ll simply return those values as strings (line 9).

And that’s IT, the magic is revealed!

JSX is one of my favorite technologies, and it definitely simplifies working with and creating HTML from inside JS files.

Of course, you can always write your code using the `createElement` method directly, but that would not be easy nor would it look good for complex applications.

Remember that you can look at [the full source code of this project here](https://github.com/deleteman/jsx-parser), and if you have any questions about it, leave a comment here and we can talk about it!

## Build apps with reusable components like Lego

[![]()](https://bit.cloud)

[**Bit**](https://bit.cloud)**’s open-source tool** help 250,000+ devs to build apps with components.

Turn any UI, feature, or page into a **reusable component** — and share it across your applications. It’s easier to collaborate and build faster.

**→** [**Learn more**](https://bit.dev)

Split apps into components to make app development easier, and enjoy the best experience for the workflows you want:

### → [Micro-Frontends](/how-we-build-micro-front-ends-d3eeeac0acfc)

### → [Design System](/how-we-build-our-design-system-15713a1f1833)

### → [Code-Sharing and reuse](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4)

### → [Monorepo](https://www.youtube.com/watch?v=5wxyDLXRho4&t=2041s)

## Learn more

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----caecf58d7cbd---------------------------------------)

[## How we Build a Component Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----caecf58d7cbd---------------------------------------)

[## How to reuse React components across your projects

### Finally, you completed the task of creating a fantastic input field for the newsletter in your app. You are happy with…

bit.cloud](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l3bhezsg?source=post_page-----caecf58d7cbd---------------------------------------)

[## 5 Ways to Build a React Monorepo

### Build a production-grade React monorepo: From fast builds to code-sharing and dependencies.

blog.bitsrc.io](/5-ways-to-build-a-react-monorepo-a294b6c5b0ac?source=post_page-----caecf58d7cbd---------------------------------------)

[## How to Create a Composable React App with Bit

### In this guide, you’ll learn how to build and deploy a full-blown composable React application with Bit. Building a…

bit.cloud](https://bit.cloud/blog/how-to-create-a-composable-react-app-with-bit-l7ejpfhc?source=post_page-----caecf58d7cbd---------------------------------------)