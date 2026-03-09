---
title: "Adventures in the Virtual DOM — Part 2: The Diff/Render Loop"
url: https://medium.com/p/dac7f879bb21
---

# Adventures in the Virtual DOM — Part 2: The Diff/Render Loop

[Original](https://medium.com/p/dac7f879bb21)

![]()

# Adventures in the Virtual DOM — Part 2: The Diff/Render Loop

[![Kevin B. Greene](https://miro.medium.com/v2/resize:fill:64:64/0*Hci_FcPBZcwkJ-5k.jpeg)](/@KevinBGreene?source=post_page---byline--dac7f879bb21---------------------------------------)

[Kevin B. Greene](/@KevinBGreene?source=post_page---byline--dac7f879bb21---------------------------------------)

26 min read

·

Jul 8, 2018

--

1

Listen

Share

More

Source on Github: [Virtual DOM Tutorial — Diff/Render Loop](https://github.com/kevinbgreene/virtual-dom-tutorial/tree/part-2-diff-render-loop)

### More Posts in This Series

1. [Part 1 — Defining the Problem](/@KevinBGreene/adventures-in-the-virtual-dom-part-1-defining-the-problem-88f5154be5e7)
2. [Part 3 — Testing and Scheduling](/@KevinBGreene/adventures-in-the-virtual-dom-part-3-testing-and-scheduling-4648aa3865e)
3. [Part 4 — Rendering Attributes](/@KevinBGreene/adventures-in-the-virtual-dom-part-4-rendering-attributes-a58010a6c74f)

## **Introduction**

Welcome back for more fun with the virtual DOM. In this post we are going to start looking at how to render nodes and how to find the difference between two nodes. This library is going to build up in layers. We are going to build up some working code and come back later to add additional features and abstractions. I think it’s important to sketch out the basics first so we can see all the pieces.

We are going to call the process of taking a virtual DOM node and constructing an actual DOM node “rendering”. We are going to call the process of finding the changes between two virtual DOM nodes as “diffing”. Our library will really boil down to doing these two things in a loop. We render, the user creates a new view, we diff and we render again… and so on. As you can imagine the diffing side of the equation is where we will spend our most time.

Our goal for this post is to get our first pass at rendering and diffing up and working. Once we have these two pieces we are free to use our library to create declarative UIs. Once we have rendering working we’ll need to set up a test runner that knows how to set up a browser environment to actually write tests for the thing (sigh, my least favorite thing about web development).

## **Taking Another Look at Our Project**

I’m building upon the same code I wrote in [Part 1: Defining the Problem](/@KevinBGreene/adventures-in-the-virtual-dom-part-1-defining-the-problem-88f5154be5e7). All the code we have written so far is located in `src/main/index.ts`. This worked fine to get started quickly and just see some code run. This is going to become a fairly large and complex library so we are going to need to build towards better organization.

We’re going to break this up into two parts, first we are going to reorganize the code we have already written and then we are going to set up bundling to make things a little easier to test and deploy.

### **Project Organization**

So this is the bit where we break out of writing all of our code in one file. I don’t want to either telegraph too much where we are going nor add add too much infrastructure at this point. So, we will periodically reorganize our code a bit as we go. To start with, I’m going to make two new files: `src/main/types.ts` and `src/main/elements.ts`.

In the `src/main/types.ts` file I am moving over all of our type definitions:

```
export const enum NodeType {  
    NODE,  
    TEXT,  
}export interface IAttributes {  
    [name: string]: string  
}export interface INode {  
    type: NodeType.NODE  
    tagName: string  
    attributes: IAttributes  
    children: Array<Html>  
}export interface IText {  
    type: NodeType.TEXT  
    value: string  
}export type Html =  
    INode | IText
```

Then I’m also moving all of our element-constructing functions to `src/main/elements.ts`:

```
import {  
    INode,  
    IText,  
    IAttributes,  
    Html,  
    NodeType,  
} from ‘./types’export const text =(  
    value: string  
): IText => ({  
    type: NodeType.TEXT,  
    value,  
})export const node = (  
    tagName: string,  
    attributes: IAttributes = {},  
    children: Array<Html> = [],  
): INode => ({  
    type: NodeType.NODE,  
    tagName,  
    attributes,  
    children  
})const makeNode =  
    (tagName: string) =>  
        (attributes: IAttributes = {}, children: Array<Html>): INode =>  
            node(tagName, attributes, children)export const div = makeNode(‘div’)  
// A bunch of other element constructors…
```

Our `src/main/index.ts` file now just becomes a place to export our public API:

```
export * from ‘./elements’  
export * from ‘./types’
```

### **Source Bundling and Testing**

As I’ve been writing this post I’ve gone back and forth a few times on whether or not to use bundling or just rely on native module support. I’ve decided ultimately to use bundling. I’m not really going to optimize our builds. I’m going to keep things as simple as possible. I think having a source bundle will make things a bit easier, but it also means we have to set up a bundler (groan).

```
$ npm install --save-dev webpack webpack-cli
```

Webpack means a `webpack.config.js`. Again, I am going to keep things simple.

```
const path = require('path');module.exports = {  
    mode: 'development',  
    entry: './dist/main/index.js',  
    output: {  
        path: path.resolve(__dirname, 'dist', 'bundles'),  
        filename: 'bundle.js',  
        library: 'VirtualDOM',  
    }  
}
```

In the off chance you’re not familiar with Webpack this is going to go to the entry module (`dist/main/index.js`), find all of its dependencies and bundle them all into one file (`dist/bundles/bundles.js`). The `library` option tells Webpack to expose our library on the global object with the name “VirtualDOM”. Anything that is exported from `index.ts` will become a property on this object.

For those of you who are familiar with Webpack you may be asking yourself why I’m not using `ts-loader`. I’m trying to keep set up simple. I don’t want to go to much into the options of Webpack. For our purposes it just bundles code. We’ll let `tsc` do what it does best. This all changes our `package.json` scripts to correctly call our build steps

```
{  
  "name": "virtual-dom",  
  "version": "1.0.0",  
  "description": "",  
  "main": "dist/index.js",  
  "scripts": {  
    "clean": "rm -rf dist",  
    "clean-all": "npm run clean; rm -rf node_modules",  
    "lint": "tslint --fix './src/**/*.ts'",  
    "webpack": "webpack",  
    "prebuild": "npm run clean",  
    "build": "tsc && npm run webpack",  
    "pretest": "npm run build",  
    "test": "node dist/tests/index.spec.js"  
  },  
  "author": "Kevin B. Greene",  
  "license": "Apache-2.0",  
  "devDependencies": {  
    "@types/chai": "^4.1.4",  
    "chai": "^4.1.2",  
    "ts-loader": "^4.4.2",  
    "tslint": "^5.10.0",  
    "typescript": "^2.9.2",  
    "webpack": "^4.15.1",  
    "webpack-cli": "^3.0.8"  
  }  
}
```

Let’s run a test build.

```
$ npm run build
```

If everything has been set up you should see output similar to:

```
Hash: 38db7c278ad4dcaea51c  
Version: webpack 4.15.1  
Time: 125ms  
Built at: 07/07/2018 9:26:11 PM  
    Asset      Size  Chunks             Chunk Names  
bundle.js  7.44 KiB    main  [emitted]  main  
[./dist/main/elements.js] 1020 bytes {main} [built]  
[./dist/main/index.js] 301 bytes {main} [built]  
[./dist/main/render.js] 1.07 KiB {main} [built]  
[./dist/main/types.js] 110 bytes {main} [built]
```

If you get errors I’m guessing it’s likely from import paths. The errors should guide you.

The last thing we’ll do before getting into some new stuff is to set up an example HTML file to see our work as we go. We’ll set up our test runner in a bit (We’ll use karma with puppeteer). The example HTML file for me will be `example.html` and be at the project root.

```
<!DOCTYPE html><html lang="en">  
<head>  
  <meta charset="UTF-8">  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  
  <meta http-equiv="X-UA-Compatible" content="ie=edge">  <title>Virtual DOM</title></head><body>  
  <script src="dist/bundles/bundle.js"></script>  
  <script>  
    // Experiment with VirtualDOM object  
  </script>  
</body></html>
```

Okay, let’s get going.

## **A Little Review**

When last we left we had defined a virtual DOM node as an object of more-or-less this shape:

```
export interface INode {  
    type: NodeType.NODE  
    tagName: string  
    attributes: IAttributes  
    children: Array<Html>  
}
```

Something very simple, but all that is normally required for declaring a web UI. We then wrote some functions that knew how to make objects of these types. Fairly simple stuff. These function allow us to declare UI something like this:

```
import { article, section, p, text, Html } from ‘virtual-dom’export const view: Html =  
    article({}, [  
        section({}, [  
            p({}, [  
                text(‘hello virtual dom’)  
            ])  
        ])  
    ])
```

This looks pretty similar to writing HTML. I actually like this, something like JSX is nice, but this isn’t much harder to read and doesn’t hide, through abstraction, the fact that all we’re really doing is writing JavaScript functions.

Something we are going to look at more and more is how to have our user-facing functions do more work for the users and provide abstractions around common use cases. The first thing that would be nice is that we really don’t need the user to call the text function. There’s no data associated with a text node other than the string value. We could rewrite our `node` function to allow children to be either `Html | string`. The function can then process strings to turn them into text nodes.

```
export const node = (  
    tagName: string,  
    attributes: IAttributes = {},  
    children: Array<Html | string> = [],  
): INode => ({  
    type: NodeType.NODE,  
    tagName,  
    attributes,  
    children: children.map((next: Html | string): Html => {  
        if (typeof next === ‘string’) {  
            return text(next)  
        } else {  
            return next  
        }  
    })  
})
```

Doing it this way requires an extra loop through the children for every node we create, we’ll optimize this a bit later by moving this check inside of another loop, but this is the kind of thing we will be doing. Once we are into our inner functions for diffing and rendering it makes things much easier to have our objects represented by a smaller number of reliable types, but on the public side of things its nice to give the users of our library a little more flexibility.

## **Rendering Our First Node**

For our first pass at rendering all we need is a function that takes a virtual node and returns a real node that we could insert into the page. We have two kinds of nodes to account for. I am going to start writing this in a new file `src/main/render.ts`.

```
import { Html, NodeType } from ‘./types’export function render(node: Html): Node {  
    switch (node.type) {  
        case NodeType.NODE:  
            return createElement(node)  
     
        case NodeType.TEXT:  
            return createText(node)        default:  
            const _exhaustiveCheck: never = node  
            throw new Error(  
                `Non-exhaustive match for ${_exhaustiveCheck}`  
            )  
    }  
}
```

*Note: This takes advantage of my favorite TypeScript feature* [*dicscriminated unions*](/@KevinBGreene/surviving-the-typescript-ecosystem-type-guards-and-discriminated-unions-3b833c7aff04)*. The type* `Node` *comes from the default TypeScript* `lib.es6.d.ts` *file.*

Now we just need to fill out a couple of more specialized functions. The one for rendering text is super simple.

```
function createText(node: IText): Text {  
    return document.createTextNode(node.value)  
}
```

Rendering an `Element` is a little more interesting. A tree is a recursive data structure, meaning it’s children are of the same type. Our `createElement` function then is going to need to call `render` for each of its children, which calls `render` for each of its children and so on.

The other bit of complexity is the need to apply attributes to each node. At this point attributes are just represented by key/value pairs. We’ll be revisiting this, but for now we can just loop through the attributes and apply them.

```
function applyAttrs(element: HTMLElement, attrs: IAttributes): void {  
    for (const key in attrs) {  
        element.setAttribute(key, attrs[key])  
    }  
}
```

With our `applyAttrs` function in place our `createElement` function can be complete in working order.

```
function createElement(node: INode): HTMLElement {  
    const element: HTMLElement =  
        <HTMLElement>document.createElement(node.tagName);    const children: Array<Html> = node.children;  
    const len: number = children.length;    applyAttrs(element, node.attributes);    for (let i = 0; i < len; i++) {  
        const childElement: Node = render(children[i]);  
        element.appendChild(childElement);  
    }  
      
    return element;  
}
```

In this library we will almost exclusively forgo use of the functional array methods (filter, map, reduce and forEach). I know we already used `map` in our node constructor, but we’ll remove that eventually. A big concern of virtual DOM libraries is performance. We need the library to update the DOM as quickly and efficiently as possible to maintain frame-rate. We have a lot of work to do and that doesn’t include the business logic of our host application. Loops are typically at least 10X faster than using the functional array methods ([JSPerf](https://jsperf.com/fast-array-foreach)). At the application level the number of elements we typically deal with in arrays is low enough that maximum performance can take a back seat to more concise and reliable code. In a library we need to be more aware of our performance characteristics because we are not sure what our host application needs. We want to be as invisible as possible.

Over in `src/main/index.ts` let’s export our new render method.

```
export * from './elements'  
export * from './render'  
export * from './types'
```

We can now rebuild.

```
$ npm run build
```

And finally we can go over to `example.html` and render something.

```
<script>  
    // Experiment with VirtualDOM object  
    const view = VirtualDOM.div({}, [ 'Hello World' ])  
    const node = VirtualDOM.render(view)  
    document.body.appendChild(node)  
</script>
```

If all works, you should see a rather unexciting “Hello World” printed on a web page when you load this in a browser. Yay, our first render.

### Packaging Our Render Function

Obviously we don’t want our users inserting nodes into the DOM themselves. That defeats the purpose of our library. There are a few ways to handle this and over time we’ll adjust. For now, I like to call a single virtual DOM and its subsequent changes a “scene”. I am going to make a function called `scene` that takes a virtual DOM node and a real DOM node as arguments. It will use the real DOM node as the root for our scene. Everything will be rendered into it.

I create a new file `src/main/scene.ts`.

```
import { Html } from './types'  
import { render } from './render'export function scene(  
    initialView: Html,  
    rootNode: HTMLElement  
): void {  
    const domNode: Node = render(initialView)  
    rootNode.appendChild(domNode)  
}
```

And add this to our public exports in `src/main/index.ts`.

```
export * from './elements'  
export * from './render'  
export * from './scene'  
export * from './types'
```

This is just scaffolding for now. Eventually this function will return a function that allows us to update the view.

If you want to see our new `scene` function run you can update `example.html`.

```
<script>  
    // Experiment with VirtualDOM object  
    const view = VirtualDOM.div({}, [ 'Hello World' ])  
    VirtualDOM.scene(view, document.body)  
</script>
```

Everything should still work and we are ready to move on to figuring out how to update our view.

## Finding the Difference

Finding the difference between two nodes is where most of the work is. This is the area that allows for the most room to be clever and the most opportunities to build optimization. As we go we’ll make assumptions, reassess and refactor. The goal here is to be able to find the difference between what our last view was and what our new view will be. We need to represent these differences in a way that makes them easy to apply to the actual DOM. We will call the resulting object representing these differences a `Patch`.

### A Patch By Any Other Name

Let’s sketch out some code. It is a safe assumption that we’ll want a function called `diff` that takes two objects. I’m going to start working in a new file `src/main/diff.ts`.

```
export function diff(oldNode: Html, newNode: Html): Patch {  
    // Perform magic.  
}
```

How we decide to represent a `Patch` is critical to how we will be performing diffs and how we will be applying them. Every node in our virtual DOM is possibly in need of a `Patch`. Meaning we are going to have some arbitrary number of patches to apply for each diff. Well, this isn’t necessarily true. We could represent the difference to the whole DOM as a single object, but that is unwieldy. It is conceptually much easier to think about a diff for every node instead of the entire virtual DOM. Thinking this way I’m going to update our `diff` function to return `Array<Patch>`.

```
export function diff(oldNode: Html, newNode: Html): Array<Patch> {  
    // Perform magic.  
}
```

In this situation if there are no differences between the two nodes we will return an empty array. Of course there are countless ways to solve this problem. I encourage you to get creative and try your own solutions. What I’m doing for this series of posts is actually a different solution than I’ve tried before.

For now, with what we have so far, what are some ways the nodes may be different? I think there are three somewhat broad and obvious ways nodes can be different.

1. The node has been added
2. The node has been removed
3. The node has been updated

To continue this discussion let’s go back to `src/main/types.ts` and add an `enum` for `PatchType`. We can articulate these three things as types for our patches.

```
export const enum PatchType {  
    ADDED,  
    REMOVED,  
    UPDATED,  
}
```

The most broad of these is “updated”. What does “updated” mean? With what we know, “updated” really means one of two things. If we have a text node the text value has changed. If we have an element the attributes have changed. I say that because we are going to create `Patch` objects for each of the child nodes. Each node in our tree will run through the `diff` function. That leaves attributes as the thing that will not be covered by some other `Patch`. The caveat to this is the reordering of nodes. We are not going to get to reordering of nodes in this post, it is the most complex of the changes to both diff and apply. That change will probably get its own post.

The other one of our patch types that is too broad is “added”. There are multiple ways a node may be added. What are these? It can be appended to its parent. It can be inserted at some position or it can replace an existing node. The inserting implies taking into account the order of surrounding nodes, so we’ll save that for our broader discussion of reordering.

With these things in mind I’m going to update our `PatchType` enum.

```
export const enum PatchType {  
    APPEND,  
    REPLACE,  
    REMOVE,  
    PROPS,  
    TEXT,  
}
```

We’ll go with this for now and update if needed.

### Referencing the Actual DOM

What do we need in terms of `Patch` objects? A `Patch` object needs a `type` telling us what it’s wanting to do. It probably also needs some extra data to perform that change. For example, what data would be needed for `APPEND`? We would need the new virtual DOM node to render.

```
export interface IAppendPatch {  
    type: PatchType.APPEND  
    node: Html  
}
```

However, that’s not really it. What do we append to? It would be nice to have the actual parent DOM node.

```
export interface IAppendPatch {  
    type: PatchType.APPEND  
    node: Html  
    domNode: Node  
}
```

A replace patch is almost exactly the same. What does it need? The same as append it needs the new virtual DOM node to render and a real DOM node. In this case, however, the real DOM node is the node to replace.

```
export interface IReplacePatch {  
    type: PatchType.REPLACE  
    node: Html  
    domNode: Node  
}
```

How do we get the real DOM node? There are a few ways to accomplish this. We could use the index of the node in the parent’s list of children. Another thing we could do is generate unique IDs for all of the nodes our library creates and save these IDs onto the virtual DOM nodes. Or, we could also save references to the actual DOM nodes that are rendered by our library.

Ultimately, we are going to save references to all of the nodes we create. This will greatly simplify the process of applying patches. It also avoids the problem of having to map our virtual DOM back to the real DOM. As mentioned, the real DOM is unreliable. It’s possible that other JavaScript loaded on the page is manipulating it outside of our library. This makes mapping the virtual DOM back to the real DOM an unreliable task. I also don’t like mutating the virtual DOM. These virtual DOM nodes are exposed to our users and I would like their code to appear as functionally pure as possible. I want them to unit test their view.

So, we are going to have to set up some infrastructure to support this. First off, I’m going to go over to `src/main/types.ts` and define a type for an object to cache references to DOM nodes.

```
export class NodeCache extends WeakMap<Html, Node> {  
    replace(oldKey: Html, newKey: Html): Node {  
        // If the node is not in cache something is very wrong.  
        const value: Node = this.get(oldKey)!  
        this.delete(oldKey)  
        this.set(newKey, value)  
        return value  
    }  
}
```

A `WeakMap` makes a lot of since here. We don’t need this thing to be sticky. We should be dropping references to DOM nodes if there are no longer virtual nodes to reference them. If you haven’t used WeakMaps head over to the [MDN docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WeakMap). I choose to extend `WeakMap` and add a `replace` method because this is something we are going to be doing a lot. Every time the user creates a new view we will have a new virtual node to represent the same real node. We will need to mutate the mapping so the new virtual node points to the real node we have already rendered. We’ll see this in use shortly.

Where is the point in our code where we need to be saving these references? That’s the place where we have both the virtual node and the real node it creates, the `render` function.

```
export function render(node: Html, nodeCache: NodeCache): Node {  
    switch (node.type) {  
        case NodeType.NODE:  
            const element: HTMLElement =  
                createElement(node, nodeCache)  
            nodeCache.set(node, element)  
            return element        case NodeType.TEXT:  
            const textNode: Text = createText(node)  
            nodeCache.set(node, textNode)  
            return textNode        default:  
            const _exhaustiveCheck: never = node  
            throw new Error(  
                `Non-exhaustive match for ${_exhaustiveCheck}`  
            )  
    }  
}
```

We also need to thread the `nodeCache` object through to our `createElement` function as that is where we call `render` for all of the child nodes.

```
function createElement(  
    node: INode,  
    nodeCache: NodeCache,  
): HTMLElement {  
    const element: HTMLElement =  
        <HTMLElement>document.createElement(node.tagName);  
    const children: Array<Html> = node.children;  
    const len: number = children.length;    applyAttrs(element, node.attributes);    for (let i = 0; i < len; i++) {  
        const childElement = render(children[i], nodeCache);  
        element.appendChild(childElement);  
    }    return element;  
}
```

Where is our `render` function exposed? Back over in `src/main/scene.ts`. Each scene our users create will get a new node cache. Our `scene` function will eventually return a `Scene` object that will give users some access to the underlying infrastructure, like getting references to the actual nodes that are created and scheduling updates to the view.

```
export function scene(  
    initialView: Html,  
    rootNode: HTMLElement,  
): void {  
    const nodeCache: NodeCache = new NodeCache()  
    const domNode: Node = render(initialView, nodeCache)  
    rootNode.appendChild(domNode)  
}
```

This does also complicate our `diff` function signature some since we started this with the need for `Patch` objects to have access to actual DOM nodes.

```
export function diff(  
    oldNode: Html,  
    newNode: Html,  
    nodeCache: NodeCache,  
): Patch {  
    // Perform magic.  
}
```

Now, we can return to our regularly scheduled programming.

### Defining Our Patches

Before we get into how to find the difference between nodes let’s finish defining our patch types. We are going to define a different interface for each patch type since they each need their own associated data.

```
export interface IAppendPatch {  
    type: PatchType.APPEND  
    node: Html  
    domNode: Node  
}export interface IReplacePatch {  
    type: PatchType.REPLACE  
    node: Html  
    domNode: Node  
}export interface IRemovePatch {  
    type: PatchType.REMOVE  
    domNode: Node  
}export interface IPropsPatch {  
    type: PatchType.PROPS  
    attributes: IAttributes  
    domNode: Node  
}export interface ITextPatch {  
    type: PatchType.TEXT  
    value: string  
    domNode: Node  
}
```

With these then a `Patch` is just a union of these types. Meaning a `Patch` can be any one of these.

```
export type Patch =  
    IAppendPatch | IReplacePatch | IRemovePatch |  
    IPropsPatch | ITextPatch
```

Now, we’re finally ready to a run a diff.

### Running a Diff

Let’s quickly return to our `diff` function. I’m going to keep the `diff` function very simple. The magic will be in another function.

```
export function diff(  
    oldNode: Html,  
    newNode: Html,  
    nodeCache: NodeCache,  
): Array<Patch> {  
    const patches: Array<Patch> = []  
    runDiff(oldNode, newNode, patches, nodeCache)  
    return patches  
}function runDiff(  
    oldNode: Html,  
    newNode: Html,  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    // "Actual magic is oxymoronic. It may not even be 'oxy'."  
}
```

So, yeah, a bit of cheating there. The `diff` function only exists to make a new list of patches before passing things off to `runDiff`.

What are the first ways you think of to check for differences between two nodes? We’re just comparing two objects here. Maybe `tagName`, maybe look through `attributes`. Really the first thing we need to do is check `type`. The process of diffing a text node is going to be different than an element.

```
function runDiff(  
    oldNode: Html,  
    newNode: Html,  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    if (oldNode.type !== newNode.type) {  
        // Different node types  
    } else {  
        // Same node type  
    }  
}
```

Actually, no, let’s add one more check first. We’re wanting to keep things efficient. At the top of this function we’re not doing much work. We want to short-circuit things as soon as we can.

The more similar two nodes are the harder (and more expensive) they are to diff, in the typical case. Here we are going to add our first assumption. The assumption we are going to make is that if two nodes are actually the same reference there is no difference. We expect virtual nodes to be used in an immutable manner. This will allow us to build in caching later that will make finding differences very fast. When the state of the host application changes the chances are great that really only a small portion of the DOM needs to change.

```
function runDiff(  
    oldNode: Html,  
    newNode: Html,  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    if (oldNode === newNode) {  
        // Nodes are the same, assume no changes.  
        return    } else {  
        if (oldNode.type !== newNode.type) {  
            // Different node types        } else {  
            // Same node type  
        }  
    }  
}
```

In the case of different node types what are we doing? Specifically, what is the `Patch` that accounts for this? We are replacing. We don’t need to diff props or anything else. A text node has been replaced with an element or an element has been replaced with a text node. This is also easy and fast.

The other thing you will notice is that once we know that the `oldNode` and `newNode` are not the same reference we will need to update the `nodeCache`. We need to update the `nodeCache` so that the node that was once referenced by `oldNode` is now referenced by `newNode`. We’ll use the `replace` method we added to `WeakMap`.

```
function runDiff(  
    oldNode: Html,  
    newNode: Html,  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    if (oldNode === newNode) {  
        // Nodes are the same, assume no changes.  
        return    } else {  
        const domNode: Node = nodeCache.replace(oldNode, newNode)        if (oldNode.type !== newNode.type) {  
            // Different node types  
            patches.push({  
                type: PatchType.REPLACE,  
                node: newNode,  
                domNode,  
            })        } else {  
            // Same node type  
        }  
    }  
}
```

Here we see our `NodeCache#replace` method in action. It switches out the keys and returns the real DOM node that is need for applying our patch.

From here we are going to `switch` on `oldNode.type`. It doesn’t really matter which node we choose. Once we are in our `else` block we know the nodes are of the same type.

```
// Same node type  
switch (oldNode.type) {  
    case NodeType.TEXT:  
        // Check for changes  
        return    case NodeType.NODE:  
        // Check for changes  
        return  
      
    default:  
        const _exhaustiveCheck: never = oldNode  
        throw new Error(  
            `Non-exhaustive match for ${_exhaustiveCheck}`  
        )  
}
```

Now things are getting more clear. How do we check for changes in a text node?

```
case NodeType.TEXT:  
    if (oldNode.value !== (newNode as IText).value) {  
        patches.push({  
            type: PatchType.TEXT,  
            value: (newNode as IText).value,  
            domNode,  
        })  
    }  
    return
```

We have to add casting to `IText` for `newNode` just to satisfy TypeScript. Even though we know the nodes are of the same type, and guaranteed to be `IText` in this case, TypeScript will still complain as it can only figure out the type of the node we are switching on (`oldNode`).

Anyway, that’s it for a text node. It should feel fairly obvious, at least once seeing it. There’s no real magic here, just boring JavaScript.

The more interesting case is `NodeType.NODE`. We need to find the difference in the `attributes` and in the `children`. However, there is escape hatch for us. The other property that could change is `tagName`. If the tag names don’t match we can break out the same as we did for node type. A lot has changed. It’s a clean replace.

```
case NodeType.NODE:  
    if (oldNode.tagName !== (newNode as INode).tagName) {  
        patches.push({  
            type: PatchType.REPLACE,  
            node: newNode,  
            domNode,  
        })    }  
    return
```

Diffing the `children` is essentially going to be a recursive call to `runDiff`. We’ll look at that in a minute. Finding the difference in the `attributes` is going to be a little more interesting. For a second, let’s revisit the `Patch` for attributes.

```
export interface IPropsPatch {  
    type: PatchType.PROPS  
    attributes: IAttributes  
    domNode: Node  
}
```

The attributes patch is going to keep track of the new set of attributes to apply to the node, the changed attributes. How are we going to account for removed attributes? We are going to change `IAttributes`.

```
export interface IAttributes {  
    [name: string]: string | undefined  
}
```

We will use `undefined` to represent an attribute that has been removed. That means we need to update `applyAttrs`.

```
function applyAttrs(  
    element: HTMLElement,  
    attrs: IAttributes,  
): void {  
    for (const key in attrs) {  
        const value: string | undefined = attrs[key]  
        if (value === undefined) {  
            element.removeAttribute(key)  
        } else {  
            element.setAttribute(key, value)  
        }  
    }  
}
```

Okay, now that we know how to represent and apply this patch let’s look at generating the patch. We are going to create a new function `diffAttrs` that will either return an `IAttributes` object or `undefined`, if nothing has changed.

```
case NodeType.NODE:  
    if (oldNode.tagName !== (newNode as INode).tagName) {  
        patches.push({  
            type: PatchType.REPLACE,  
            node: newNode,  
            domNode,  
        })    } else {  
        const propsDiff: IAttributes | undefined =  
            diffAttrs(  
                oldNode.attributes,  
                (newNode as INode).attributes  
            )        if (propsDiff !== undefined) {  
            patches.push({  
                type: PatchType.PROPS,  
                attributes: propsDiff,  
                domNode,  
            })  
        }  
    }  
    return
```

All we need now is our `diffAttrs` function. All this function really needs to do is loop through props and see what has changed.

```
function diffAttrs(  
    oldAttrs: IAttributes,  
    newAttrs: IAttributes  
): IAttributes | undefined {  
    let diff: IAttributes | undefined = undefined    for (const key in oldAttrs) {  
        if (oldAttrs[key] !== newAttrs[key]) {  
            diff = diff || {}  
            diff[key] = newAttrs[key]  
        }  
    }    for (const key in newAttrs) {  
        if (oldAttrs[key] === undefined) {  
            diff = diff || {}  
            diff[key] = newAttrs[key]  
        }  
    }    return diff  
}
```

We need to loop through both old and new attributes to see what has been added or removed.

That just leaves us with children.

```
case NodeType.NODE:  
    if (oldNode.tagName !== (newNode as INode).tagName) {  
        patches.push({  
            type: PatchType.REPLACE,  
            node: newNode,  
            domNode,  
        })    } else {  
        const propsDiff: IAttributes | undefined =  
            diffAttrs(  
                oldNode.attributes,  
                (newNode as INode).attributes  
            )        if (propsDiff !== undefined) {  
            patches.push({  
                type: PatchType.PROPS,  
                attributes: propsDiff,  
                domNode,  
            })  
        }  
          
        diffChildren(  
            oldNode,  
            (newNode as INode),  
            patches,  
            nodeCache,  
        )  
    }  
    return
```

What can happen when we are diffing children? We need to run the through the `runDiff` function we already have. However, we need to also check if any children have been added or removed. This means `APPEND` and `REMOVE`. For `APPEND` we need the parent DOM node to append to. We already have that. We’ll pass that through to `diffChildren` as well.

```
diffChildren(  
    oldNode,  
    (newNode as INode),  
    (domNode as HTMLElement),  
    patches,  
    nodeCache,  
)
```

I usually don’t like passing that many arguments to the function without wrapping them in an object, but this is pretty isolated. It won’t be publicly exported and won’t be used outside of `src/main/diff.ts`.

Let’s sketch out our `diffChildren` function.

```
function diffChildren<T>(  
    oldParent: INode,  
    newParent: INode,  
    parentNode: HTMLElement,  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    const oldChildren: Array<Html> = oldParent.children  
    const newChildren: Array<Html> = newParent.children  
    const len: number = Math.max(  
        oldChildren.length,  
        newChildren.length,  
    )    for (let i = 0; i < len; i++) {  
        // Check children  
    }  
}
```

We know we need to loop through all the children in the longer array. Children may have been added or removed in our new node. If something is `undefined` in the old children it has been added. If something is `undefined` in the new children it has been removed. So we just need to pick the longer length as our iteration count.

From here we can perform our checks. This function really only exists to check for children that have been added or removed, all the other work can be done by `runDiff`.

```
for (let i = 0; i < len; i++) {  
    const oldChild = oldChildren[i]  
    const newChild = newChildren[i]    // APPEND NEW  
    if (oldChild === undefined) {  
        patches.push({  
            type: PatchType.APPEND,  
            node: newChild,  
            domNode: parentNode,  
        })  
          
    // REMOVE OLD  
    } else if (newChild === undefined) {  
        patches.push({  
           type: PatchType.REMOVE,  
           domNode: nodeCache.get(oldChild)!,  
        });    // DIFF THE REST  
    } else {  
        runDiff(oldChild, newChild, patches, nodeCache)  
    }  
}
```

With that we should have our first complete iteration of how to diff two virtual DOM trees.

### Checking Our Work

I’m not patient enough at the moment to set up testing around this. That’s what we have `example.html` for. First though, let’s open up `src/main/scene.ts` again. It’s time for this to return something. What we need to return is a function to update the initial view.

I’m going to call this function a scheduler. It doesn’t schedule updates yet, but it will. I’m going to make a type for this.

```
export type Scheduler =  
    (newView: Html) => void
```

Our `scene` function will return one of these allowing us to update our view.

```
export function scene(  
    initialView: Html,  
    rootNode: HTMLElement  
): Scheduler {  
    let savedView: Html = initialView  
    const nodeCache: NodeCache = new NodeCache()  
    const domNode: Node = render(initialView, nodeCache)  
      
    rootNode.appendChild(domNode)    return (newView: Html): void => {  
        const patches = diff(savedView, newView, nodeCache)  
        savedView = newView  
        console.log('patches: ', patches)  
    }  
}
```

To check what I’m doing I throw `console.log` on the last line just to see that the patches are what I expect. The other bit of machinery I added to this is saving and updating the previous view (`savedView`). This will always be the previous view we are diffing against for updates. So after we run a diff we need to update the `savedView` so we can run a diff against the current state when the user tries to update the view again.

Now we can run this over in `example.html`.

```
<script>  
    // Experiment with VirtualDOM object  
    const view = VirtualDOM.div({}, [ 'Hello World' ])  
    const scheduler = VirtualDOM.scene(view, document.body)    scheduler(VirtualDOM.div({ id: 'foo' }, [ 'Virtual DOM' ]))  
</script>
```

So we’re doing a couple of things here. We’re adding a child and updating attributes. We should see two patches in our array of patches. That’s what I’ve got.

## Applying Our Patches

Well, the hard part is behind us, but we still don’t have a useable library. We need to apply the patches we are now creating. Anther major section of our library probably deserves another file. Let’s create a new file called `src/main/patches.ts`. This will have one public export `applyPatches`.

```
import { Patch } from './types'function applyPatch(patch: Patch): void {  
    // Execute patch  
}export function applyPatches(patches: Array<Patch>): void {  
    // Loop through patches  
    for (const patch of patches) {  
        applyPatch(patch)  
    }  
}
```

In the private `applyPatch` function we need to figure out what kind of patch we are dealing with and write the logic for that patch. But wait, we already have the logic for one of these patches, `applyAttrs`. I have been keeping `applyAttrs` in my `render` module. I’m going to move it to a new file called `src/main/ops.ts`.

```
import { IAttributes } from './types'export function applyAttrs(  
    element: HTMLElement,  
    attrs: IAttributes  
): void {  
    for (const key in attrs) {  
        const value: string | undefined = attrs[key]  
        if (value === undefined) {  
            element.removeAttribute(key)  
        } else {  
            element.setAttribute(key, value)  
        }  
    }  
}
```

Since we already have this, let’s apply this one first.

```
function applyPatch(patch: Patch): void {  
    // Execute patch  
    switch (patch.type) {  
        case PatchType.PROPS:  
            applyAttrs(  
                (patch.domNode as HTMLElement),  
                patch.attributes  
            )  
            return  
    }  
}
```

Cool, that’s all there really is to it. The only little bit of weirdness is we need to cast to `HTMLElement` to make TypeScript happy. If an element had attributes we can be certain its DOM node is an `HTMLElement` and not a text node.

What’s the next easiest one? How about `TEXT`?

```
function applyPatch(patch: Patch): void {  
    // Execute patch  
    switch (patch.type) {  
        case PatchType.PROPS:  
            applyAttrs(  
                (patch.domNode as HTMLElement),  
                patch.attributes  
            )  
            return        case PatchType.TEXT:  
            patch.domNode.textContent = patch.value  
            return  
    }  
}
```

From here we’ll move on to `REMOVE`. We’ll go back over to `src/main/ops.ts` and add a function `removeElement`.

```
export function removeElement(node: Node): void {  
    const parentNode: Node | null = node.parentNode  
    if (parentNode !== null) {  
        parentNode.removeChild(node)  
    }  
}
```

Then call it from `applyPatch`.

```
case PatchType.REMOVE:  
    removeElement(patch.domNode)  
    return
```

As we go things are going to get slightly more complex. For example. How do we perform a replace? We need to render a new element. Our `render` function requires the `nodeCache`. Hmm, okay, we’ll need to thread that through to `applyPatches`.

```
export function applyPatches(  
    patches: Array<Patch>,  
    nodeCache: NodeCache,  
): void {  
    for (const patch of patches) {  
        applyPatch(patch, nodeCache)  
    }  
}
```

We’ll also thread it through to `applyPatch` where we can use it in our `REPLACE` case.

```
case PatchType.REPLACE:  
    const toReplace: Node = patch.domNode  
    const replacement: Node = render(patch.node, nodeCache)  
    replaceElement(replacement, toReplace)  
    return
```

By doing this, `render` will handle updating the DOM node reference in our `nodeCache`. We do need to swing over to `src/main/ops.ts` and add a function for `replaceElement`.

```
export function replaceElement(  
    replacement: Node,  
    toReplace: Node  
): void {  
    const parentNode: Node | null = toReplace.parentNode;  
    if (parentNode !== null) {  
        parentNode.replaceChild(replacement, toReplace);  
    }  
}
```

The `APPEND` patch is the final case we need to account for.

```
case PatchType.APPEND:  
    const parentNode = patch.domNode  
    const toAppend = render(patch.node, nodeCache)  
    parentNode.appendChild(toAppend)  
    return
```

Now, we can go back to `src/main/scene.ts` and hook everything up into a working library. In the title I refer to the diff/render loop. It is true. Our library runs in a loop. What we need to do now is set up this loop. To get this all to work right the `Scheduler` returned from `scene` needs to diff the old view with the new view. It then needs to apply the patches. Finally it needs to save the new view as the current view for later updates, resetting to start the loop again. That looks something like this:

```
export function scene(  
    initialView: Html,  
    rootNode: HTMLElement  
): Scheduler {  
    let savedView: Html = initialView  
    const nodeCache: NodeCache = new NodeCache()  
    const domNode: Node = render(initialView, nodeCache)  
   
    rootNode.appendChild(domNode)    return (newView: Html): void => {  
        const patches = diff(savedView, newView, nodeCache)  
        applyPatches(patches, nodeCache)  
        savedView = newView  
    }  
}
```

With this done we should now have a working library. It’s time to break out `example.html` again and test this thing out. I’m going to write a little code that updates the view in a loop. You can copy this to see things working or roll something for yourself.

```
<script>  
    // Experiment with VirtualDOM object  
    const initialView = VirtualDOM.div({}, [ 'Hello World' ])  
    const schedule = VirtualDOM.scene(initialView, document.body)  
    let index = 0    function changeView() {  
        let newView  
        switch (index) {  
            case 0:  
                newView = VirtualDOM.div({ id: 'one' }, [  
                    'Hello Virtual DOM',  
                ])  
                index += 1  
                break            case 1:  
                newView = VirtualDOM.div({ id: 'two' }, [  
                    'Hello Virtual DOM',  
                    VirtualDOM.ul({}, [  
                        VirtualDOM.li({}, [ 'Item one' ])  
                    ])  
                ])  
                index += 1  
                break            case 2:  
                newView = VirtualDOM.div({ id: 'two' }, [  
                    'Hello Virtual DOM',  
                    VirtualDOM.ul({}, [  
                        VirtualDOM.li({}, [ 'Item one' ]),  
                        VirtualDOM.li({}, [ 'Item two' ])  
                    ])  
                ])  
                index = 0  
                break  
        }        schedule(newView)  
          
        setTimeout(changeView, 3000)  
    }    changeView()  
</script>
```

Let’s rebuild.

```
$ npm run build
```

And then go over to our favorite web browser and watch our view update in a loop. Cool, we have something working. Everybody grab a drink.

## Conclusion

This was a mega post. Posts in the future will be more iterative. Which makes sense. We now have a working library. We just need to refine it and build out features. I thought it was important to get all the way to something usable here as it’s pretty unfulfilling to just see a DOM node rendered, or just to see the diff between two nodes. It’s much more fun to actually have something working.

Next time we will look at building out the support structure for our scenes. This will open the door for more features and optimizations. It will also open the door for event support. Till then.