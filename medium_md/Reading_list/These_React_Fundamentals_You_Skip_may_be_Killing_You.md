---
title: "These React Fundamentals You Skip may be Killing You"
url: https://medium.com/p/7629fb87dd4a
---

# These React Fundamentals You Skip may be Killing You

[Original](https://medium.com/p/7629fb87dd4a)

# These React Fundamentals You Skip may be Killing You

[![Ohans Emmanuel](https://miro.medium.com/v2/resize:fill:64:64/1*FDK9_hITBY8rgHaUopgpNQ@2x.jpeg)](/@ohansemmanuel?source=post_page---byline--7629fb87dd4a---------------------------------------)

[Ohans Emmanuel](/@ohansemmanuel?source=post_page---byline--7629fb87dd4a---------------------------------------)

6 min read

·

Oct 5, 2018

--

13

Listen

Share

More

![]()

Often times, the inability to debug a certain error stems from not understanding some foundational concept.

You can say the same thing if you don’t understand some more advanced concepts because you lack the knowledge of certain fundamentals.

In this article, I hope to explain what I consider some of the most important foundational React concepts you need to understand.

These concepts aren’t particularly technical. There are lots of other articles that cover those — things like `props`, `state`, `context`, `setState` , and so on.

However, in this article I’ll focus on some more conceptual knowledge that forms the basis of most technical things you’ll do in React.

Ready?

## How React works under the hood

One of the first things everyone learns in React is how to build components. I’m pretty sure you learned that too.

For example:

```
// functional component   
function MyComponent() {  
  return <div> My Functional Component </div>   
}  
  
// class based component   
class MyComponent extends React.Component {  
  render() {  
     return <div> My Class Component </div>   
  }  
}
```

Most components you write will return some elements:

```
function MyComponent() {  
  return <span> My Functional Component </span> //span element  
}  
  
class MyComponent extends React.Component {  
  render() {  
     return <div> My Class Component </div> //div element  
  }  
}
```

Under the hood, most components return a tree of elements.

![]()

Now, you must also remember that components are like functions that return values based on their `props` and `state` values.

Press enter or click to view image in full size

![]()

Consequently, whenever the `props` or `state` values of a component change, a new tree of elements is rendered.

Press enter or click to view image in full size

![]()

If the component is a class-based component, the `render` function is invoked to return the tree of elements.

```
class MyComponent extends React.Component {  
    
  render() {  
    //this function is invoked to return the tree of elements  
  }  
}
```

If the component is a functional component, its return value yields the tree of elements.

```
function MyComponent() {  
    
   // the return value yields the tree of elements  
   return <div>   </div>  
}
```

Why is this important?

Consider a component, `<MyComponent />` which takes in a `prop` as shown below:

```
<MyComponent name='Ohans'/>
```

When this component is rendered, a tree of elements is returned.

![]()

What happens when the value of `name` changes?

```
<MyComponent name='Quincy'/>
```

Well, a new tree of elements is returned!

![]()

Okay.

Now, React has in its custody two different trees — the former and the current element tree.

At this point, React then compares both trees to find what exactly has changed.

![]()

Most times the entire tree hasn’t changed. Just some updates here and there.

Upon comparing these two trees of elements, the actual DOM is then updated with the change in the new element tree.

Easy, huh?

This process of comparing two trees for changes is called “reconciliation”. It’s a [technical process](https://reactjs.org/docs/reconciliation.html#motivation), but this conceptual overview is just great for understanding what goes on under the hood.

## React Only Updates What’s Necessary. True?

When you get started with React, everyone’s told how awesome React is — particularly how it just updates the essential part of the DOM being updated.

![]()

Is this completely true?

Yes it is.

However, before React gets to updating the DOM, remember that under the hood — it had first constructed the element tree for the various components and did the essential “diffing” before updating the DOM. In other words, it had compared the changes between the previous and current element trees.

The reason I re-iterate this is, if you’re new to React you may be blind to the performance ditches dug in your app because you think React just updates the DOM with what’s necessary.

While that is true, the performance concerns in most React apps begin with the process before the DOM is updated!

## Wasted Renders vs. Visual Updates

No matter how small, rendering a component element tree takes some time (no matter how minute). The time for rendering gets larger as the component element tree increases.

The implication of this is that in your app you do not want React re-rendering your component element tree if it is NOT important.

Let me show you a quick example.

Consider an app with a component structure as shown below:

![]()

The overall container component, `A` receives a certain prop. However, the sole reason for this is to pass the props down to component `D`.

![]()

Now, whenever the prop value in `A` changes, the entire children elements of `A` are re-rendered to compute a new element tree.

Press enter or click to view image in full size![]()

Press enter or click to view image in full size![]()

By implication, the components `B` and `C` are also re-rendered even though they haven’t changed at all! They have not received any new props!

This needless re-rendering is what is termed a “wasted” render.

In this example, `B` and `C` need not re-render, but React doesn’t know this.

There are many ways to deal with such issue, and I cover that in my recent article, [How to Eliminate React Performance Issues](/@ohansemmanuel/how-to-eliminate-react-performance-issues-a16a250c0f27).

Moving forward, consider the application below:

Press enter or click to view image in full size

![]()

I call this app [Cardey](http://cardie-performace.surge.sh/).

When I click the button to change the user’s profession, I can choose to highlight updates to the DOM as shown below:

Press enter or click to view image in full size

![]()

And now I see what’s been updated in the DOM.

This is a representation of the visual updates to the DOM. Note the green flash around the “I am a Librarian” text.

This is great, but I am concerned about React’s initial rendering of the component element tree.

So, I could choose the check that as well.

Press enter or click to view image in full size

![]()

Upon doing this, I see what components are actually re-rendered when I hit that button.

Press enter or click to view image in full size

![]()

Do you see how the visual updates to the DOM and react’s render updates are different?

The large user card was re-rendered but just the small text region was updated.

This is important.

## Conclusion

I believe you now have a more intuitive understanding how what happens under the hood in your React components.

Actually, a lot more happens than I have discussed here. However, this is a good start.

Go build great apps!

Are you learning React/Redux at the moment? If yes, I have a really great [book series on Redux](https://thereduxjsbooks.com). Some say it’s [one of the best](https://twitter.com/Kaafu4u/status/1041495744803491840) tech books they [ever read](https://twitter.com/LedZeck/status/1044888661664378880)!