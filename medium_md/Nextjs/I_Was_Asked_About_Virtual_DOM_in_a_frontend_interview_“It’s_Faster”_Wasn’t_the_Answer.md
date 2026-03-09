---
title: "I Was Asked About Virtual DOM in a frontend interview: “It’s Faster” Wasn’t the Answer"
url: https://medium.com/p/66656cc0dd8f
---

# I Was Asked About Virtual DOM in a frontend interview: “It’s Faster” Wasn’t the Answer

[Original](https://medium.com/p/66656cc0dd8f)

Member-only story

Featured

# I Was Asked About Virtual DOM in a frontend interview: “It’s Faster” Wasn’t the Answer

## *What the Virtual DOM actually solves, why “faster” is the wrong mental model, and how React really uses it*

[![Modern developer](https://miro.medium.com/v2/resize:fill:64:64/1*iOG3LDhndUGpP8nyvCBc1A.png)](/@moderndev?source=post_page---byline--66656cc0dd8f---------------------------------------)

[Modern developer](/@moderndev?source=post_page---byline--66656cc0dd8f---------------------------------------)

5 min read

·

Dec 20, 2025

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

In a technical interview, I confidently answered: “*React uses Virtual DOM because it’s faster than manipulating the real DOM.*”

> [**If you are not a member then read this story for free**](https://moderndev.medium.com/i-was-asked-about-virtual-dom-in-a-frontend-interview-its-faster-wasn-t-the-answer-66656cc0dd8f?sk=b930c4dede475f88706575d16a20a0e0)

The interviewer paused.

> “Is it really faster? Have you measured that? If speed was the only goal, wouldn’t we just manipulate the DOM directly?”

I was stumped. That question sent me on a journey that fundamentally changed how I understand React. The truth is: the Virtual DOM isn’t primarily about speed. It’s about something far more valuable.

## What Virtual DOM Actually Is ?

Virtual DOM is a JavaScript representation of your UI. When you write JSX, you’re creating lightweight JavaScript objects that describe what the DOM should look like:

```
<div className="container">  
  <h1>Hello World</h1>  
</div>  
  
// Becomes this JavaScript object:  
{  
  type: 'div',  
  props: {  
    className: 'container',  
    children: [{ type: 'h1', props: { children: 'Hello World' } }]  
  }  
}
```

These objects live entirely in memory. Creating and manipulating them is trivially fast : *no browser involvement, no layout calculations, just simple JavaScript.*

## What Makes Real DOM Slow

Here’s the surprise: reading and writing to the DOM isn’t inherently slow. What’s slow is what happens *after* you make changes.

Every DOM modification can trigger style recalculation, layout (reflow), and painting. This flow of operations is expensive:

```
element.style.width = '500px';   // Triggers layout  
element.style.height = '300px';  // Triggers layout again  
element.style.background = 'blue'; // Triggers paint
```

Each style change can trigger a reflow and repaint. The browser might perform three separate layout calculations for this code. This is called layout thrashing, and it’s a major performance bottleneck.

But here’s the thing: if you know exactly which DOM operations to perform and batch them efficiently, directly manipulating the DOM can be faster than using a Virtual DOM. The Virtual DOM adds an extra diffing step that takes time.

So why do we use it?

## The Real Problem Virtual DOM Solves

Virtual DOM doesn’t solve a speed problem, it solves a complexity problem.

Without Virtual DOM, you have two bad options for updating UI:

**Option 1: Rebuild everything.** Throw away DOM sections and rebuild from scratch. Simple but wasteful — you lose event listeners, form states, scroll positions.

**Option 2: Surgical updates.** Write precise logic for every state change: “If count increases, find the counter element and update its text. If a name changes, find that specific span…” This doesn’t scale. Your update logic becomes an unmaintainable mess.

The Virtual DOM provides a third option: write declarative code that describes what the UI should look like for any given state, and let React figure out the efficient DOM updates.

## How Virtual DOM Enables Declarative Programming

This is the real genius of the Virtual DOM. It lets you write UI code as if you’re rebuilding everything from scratch, while React does the surgical updates behind the scenes.

```
function TodoList({ todos }) {  
  return (  
    <ul>  
      {todos.map(todo => (  
        <li key={todo.id} className={todo.completed ? 'done' : ''}>  
          {todo.text}  
        </li>  
      ))}  
    </ul>  
  );  
}
```

This component doesn’t track what changed. It declares: “Given these todos, this is the UI.”

When `todos` changes, React creates a new Virtual DOM tree, compares it with the previous one (reconciliation), identifies differences, and performs only necessary DOM operations. You get simplicity without sacrificing efficiency.

## The Diffing Algorithm

Comparing two trees normally has O(n³) complexity. React reduces this to O(n) using heuristics:

1. **Different types = different trees.** A `<div>` changing to `<span>` means destroy and recreate, not update.
2. **Keys identify elements.** Keys tell React which items are which across renders:

```
// Without keys - inefficient, updates all items  
{todos.map(todo => <li>{todo.text}</li>)}  
  
// With keys - efficient, only updates changed items  
{todos.map(todo => <li key={todo.id}>{todo.text}</li>)}
```

**3. Level-by-level comparison.** React compares trees level by level, not across levels.

## When Virtual DOM Is Slower

For single, known updates, direct DOM manipulation is faster:

```
// Direct - faster for this specific case  
document.getElementById('counter').textContent = count;  
  
// React - slower (creates Virtual DOM, diffs, updates)  
setCount(count + 1);
```

The Virtual DOM adds overhead: creating objects, running the diffing algorithm, then updating the DOM. For simple updates, this overhead exceeds the cost of direct manipulation.

But for most apps, this difference is imperceptible, and React’s developer experience wins.

## What Virtual DOM Really Buys You

*The value isn’t performance,it’s abstraction:*

* **Declarative code:** Describe UI as a function of state. React handles updates.
* **Predictability:** Same state always produces same UI.
* **Cross-platform rendering:** Virtual DOM is just JavaScript objects. React Native renders to native components, not HTML. Server-side rendering produces strings. None of this works with direct DOM manipulation.
* **Developer tools:** Capture Virtual DOM snapshots for time-travel debugging.
* **Concurrent rendering:** React can interrupt and resume work because it’s working with objects, not actual DOM.

## The Mental Model

I have developed a new mental model for the Virtual DOM that finally made everything click.

Think of the Virtual DOM as a draft or blueprint. When your state changes, React creates a new blueprint describing what the UI should look like now. It compares this new blueprint with the previous one, identifies differences, and only then makes the actual changes to the real DOM (the physical structure).

Creating blueprints is cheap, it’s just JavaScript objects in memory. Comparing blueprints is reasonably fast because of React’s clever diffing algorithm. The expensive part, modifying the real DOM, happens only for things that actually changed.

The Virtual DOM isn’t primarily an optimization, it’s an abstraction that makes complex UI updates manageable while keeping them reasonably efficient.

## When to Optimize

Most React apps never need Virtual DOM optimization. But certain scenarios benefit:

* **Large lists:** Use virtualization (`react-window`) to render only visible items
* **Frequent updates:** Use `React.memo` for components updating many times per second
* **Expensive renders:** Memoize components with complex computation when inputs don’t change often

```
const ExpensiveList = React.memo(function ExpensiveList({ items }) {  
  return (  
    <ul>  
      {items.map(item => <ExpensiveItem key={item.id} data={item} />)}  
    </ul>  
  );  
});
```

Measure first using React DevTools Profiler before optimizing.

> Virtual DOM isn’t primarily about speed. It’s an abstraction that lets us write declarative UI code while React handles efficient DOM updates. This trades some raw performance for massive gains in code simplicity and maintainability. For most applications, that’s the right trade-off.

## Conclusion

Virtual DOM isn’t magic that makes everything fast. It’s a practical abstraction enabling declarative programming while maintaining acceptable performance.

Don’t say “it’s faster.” Say “it enables declarative UI programming by abstracting away DOM update complexity. It lets us write simple, predictable code while React handles optimization.”

Virtual DOM is brilliant not because it’s fastest, but because it’s fast enough while making code dramatically simpler to write, read, and maintain. In software development, adequate performance plus superior developer experience is often where the best solutions live.

> **All right guys this is it from this article. If you loved it, make sure to leave a comment, and follow me for more such articles.**