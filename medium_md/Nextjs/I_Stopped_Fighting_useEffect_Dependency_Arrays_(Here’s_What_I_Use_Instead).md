---
title: "I Stopped Fighting useEffect Dependency Arrays (Here’s What I Use Instead)"
url: https://medium.com/p/4d8c1b0cfe7d
---

# I Stopped Fighting useEffect Dependency Arrays (Here’s What I Use Instead)

[Original](https://medium.com/p/4d8c1b0cfe7d)

Member-only story

# I Stopped Fighting useEffect Dependency Arrays (Here’s What I Use Instead)

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](https://medium.com/@Iggy01?source=post_page---byline--4d8c1b0cfe7d---------------------------------------)

[Ignatius Sani](https://medium.com/@Iggy01?source=post_page---byline--4d8c1b0cfe7d---------------------------------------)

6 min read

·

Feb 8, 2026

--

1

Listen

Share

More

Three years of useCallback hell taught me that React’s reactivity model has a fundamental limitation — and signals solve it with 50 lines of code

Press enter or click to view image in full size

![]()

## The useEffect That Broke Me

Last month, I spent three hours debugging an infinite render loop. The culprit? This innocuous useEffect:

```
function UserProfile({ userId }) {  
  const [user, setUser] = useState(null);  
    
  const fetchUser = async () => {  
    const data = await api.getUser(userId);  
    setUser(data);  
  };  
    
  useEffect(() => {  
    fetchUser();  
  }, [fetchUser]); // ESLint: All dependencies included  
    
  return <div>{user?.name}</div>;  
}
```

**The problem:** `fetchUser` is recreated on every render, which triggers the effect, which triggers a render, which recreates `fetchUser`, which...

**The “fix”:**

```
const fetchUser = useCallback(async () => {  
  const data = await api.getUser(userId);  
  setUser(data);  
}, [userId]); // Now wrap in useCallback  
  
useEffect(() => {  
  fetchUser();  
}, [fetchUser]); // ESLint: Still happy
```

**But wait, there’s more:**

```
// Six months later, you add another dependency  
const fetchUser = useCallback(async () => {  
  const data = await api.getUser(userId, options); // New param  
  setUser(data);  
}, [userId]); // Oops, forgot to add options  
  
// Stale closure bug. Users see outdated data.  
// No error. No warning. Just silent failure.
```

This isn’t React being difficult. This is a fundamental mismatch between what we’re trying to express (“fetch user when ID changes”) and how React’s reactivity model works (“re-run the component, figure out what changed”).

After three years of wrapping functions in `useCallback`, adding dependencies to satisfy ESLint, and debugging stale closures, I started wondering: Is there a better way?

## The Real Problem: Components Are Too Coarse

React’s unit of reactivity is the component, not the variable.

When `userId` changes, React re-renders the entire component, all hooks re-run, dependencies are compared, and effects decide whether to run.

This works beautifully for UI composition. But for state management, it’s overkill.

**What we actually want to say:**

“When userId changes, fetch the user.”

**What React forces us to say:**

“When the component renders, check if the userId changed. If it did, and if the effect dependencies haven’t changed, and if the function reference is stable, then fetch the user. Oh, and make sure you’ve wrapped everything correctly.”

The bookkeeping overwhelms the intent.

## Enter Signals: Fine-Grained Reactivity

Signals flip the model. Instead of asking “did something change?” they notify you when it does.

Here’s the same user fetch logic with signals:

```
function UserProfile({ userId }) {  
  const [user, setUser] = createSignal(null);  
    
  createEffect(() => {  
    const data = await api.getUser(userId());  
    setUser(data);  
  });  
    
  return <div>{user()?.name}</div>;  
}
```

No dependency array. No useCallback. No stale closures.

The effect automatically tracks that it reads `userId()`, and re-runs when — and only when — `userId` changes.

## How Signals Work (50 Lines of Code)

The magic is simpler than you think. Here’s a complete signal implementation:

```
let currentListener = null;  
  
export function createSignal(initialValue) {  
  let value = initialValue;  
  const subscribers = new Set();  
    
  const read = () => {  
    // Automatic dependency tracking  
    if (currentListener) {  
      subscribers.add(currentListener);  
    }  
    return value;  
  };  
    
  const write = (newValue) => {  
    if (Object.is(value, newValue)) return;  
    value = newValue;  
    // Notify only subscribers  
    subscribers.forEach((fn) => fn());  
  };  
    
  return [read, write];  
}  
  
export function createEffect(callback) {  
  const execute = () => {  
    currentListener = execute;  
    callback();  
    currentListener = null;  
  };  
    
  execute(); // Run immediately to discover dependencies  
}
```

That’s it. 50 lines. No framework. No magic.

**How it works:** When you read a signal (`userId()`), it checks if an effect is currently running. If yes, it adds that effect to its subscriber list. When you write a signal (`setUserId(5)`), it notifies all subscribers. Subscribers re-run, discover new dependencies, repeat.

The key insight: Dependencies are discovered at runtime by observing what the effect actually reads, not by manually listing them.

## Example 1: Derived State

**React (useEffect + useMemo):**

```
function CartTotal({ items }) {  
  const [discount, setDiscount] = useState(0);  
    
  const subtotal = useMemo(() => {  
    return items.reduce((sum, item) => sum + item.price, 0);  
  }, [items]);  
    
  const total = useMemo(() => {  
    return subtotal - discount;  
  }, [subtotal, discount]);  
    
  return (  
    <div>  
      <p>Subtotal: ${subtotal}</p>  
      <p>Discount: ${discount}</p>  
      <p>Total: ${total}</p>  
      <button onClick={() => setDiscount(10)}>Apply Discount</button>  
    </div>  
  );  
}
```

**Signals:**

```
function CartTotal({ items }) {  
  const [discount, setDiscount] = createSignal(0);  
    
  const subtotal = () => items().reduce((sum, item) => sum + item.price, 0);  
  const total = () => subtotal() - discount();  
    
  return (  
    <div>  
      <p>Subtotal: ${subtotal()}</p>  
      <p>Discount: ${discount()}</p>  
      <p>Total: ${total()}</p>  
      <button onClick={() => setDiscount(10)}>Apply Discount</button>  
    </div>  
  );  
}
```

No useMemo. No dependency arrays. Derived values are just functions.

## Example 2: Multiple Effects

**React:**

```
function Dashboard({ userId }) {  
  const [user, setUser] = useState(null);  
  const [posts, setPosts] = useState([]);  
  const [comments, setComments] = useState([]);  
    
  // Effect 1: Fetch user  
  useEffect(() => {  
    fetchUser(userId).then(setUser);  
  }, [userId]);  
    
  // Effect 2: Fetch posts (depends on user)  
  useEffect(() => {  
    if (user) {  
      fetchPosts(user.id).then(setPosts);  
    }  
  }, [user]);  
    
  // Effect 3: Fetch comments (depends on posts)  
  useEffect(() => {  
    if (posts.length > 0) {  
      const postIds = posts.map(p => p.id);  
      fetchComments(postIds).then(setComments);  
    }  
  }, [posts]);  
}
```

Same logic. No dependency arrays. Effects automatically coordinate.

When `userId` changes → `user` updates → `posts` update → `comments` update. The data flow is explicit in the code.

## Example 3: The Timer Problem

**React (the infamous setInterval issue):**

```
function Timer() {  
  const [count, setCount] = useState(0);  
    
  useEffect(() => {  
    const id = setInterval(() => {  
      setCount(count + 1); // Stale closure!  
    }, 1000);  
      
    return () => clearInterval(id);  
  }, []); // Empty deps = stale count  
    
  return <div>{count}</div>;  
}
```

The fix requires either adding count to deps (creates new interval every second), using `setCount(c => c + 1)` (functional update), or using useRef.

**Signals:**

```
function Timer() {  
  const [count, setCount] = createSignal(0);  
    
  setInterval(() => {  
    setCount(count() + 1);  
  }, 1000);  
    
  return <div>{count()}</div>;  
}
```

No useEffect. No stale closure. It just works.

## When NOT to Use Signals

Signals are not a silver bullet. Here’s when React’s model is better.

**Simple, Local UI State**

```
function Toggle() {  
  const [open, setOpen] = useState(false);  
  return <button onClick={() => setOpen(!open)}>{open ? 'Close' : 'Open'}</button>;  
}
```

No dependencies, no effects, no problem. Don’t overcomplicate.

**Component-Heavy UIs**

If your app is mostly composition (forms, layouts, static content), React’s component model is a natural fit. Signals shine when you have interconnected state, not just UI structure.

**Server-Side Rendering**

React’s SSR story is mature. Signals in frameworks like SolidJS support SSR, but the ecosystem is smaller. If SSR is critical, React is safer.

**Large Teams with Established React Patterns**

Retraining a team on a new mental model has cost. If your React patterns work well, the migration overhead may not be worth it.

## The Practical Path Forward

You don’t have to rewrite your entire app.

**Use Signals for State, React for UI**

Use a signal library like `@preact/signals-react`:

```
import { signal } from '@preact/signals-react';  
  
const count = signal(0);  
  
function Counter() {  
  return (  
    <div>  
      <p>Count: {count.value}</p>  
      <button onClick={() => count.value++}>Increment</button>  
    </div>  
  );  
}
```

React components automatically re-render when signals they read change. No hooks required.

**Migrate Gradually to SolidJS**

SolidJS uses signals natively and has a React-like API:

```
import { createSignal } from 'solid-js';  
  
function Counter() {  
  const [count, setCount] = createSignal(0);  
    
  return (  
    <div>  
      <p>Count: {count()}</p>  
      <button onClick={() => setCount(count() + 1)}>Increment</button>  
    </div>  
  );  
}
```

You can run SolidJS components alongside React in the same app.

**Use the Pattern, Not the Library**

Even if you stick with React, understanding signals changes how you think: minimize effects, centralize interconnected state, and think in data flow rather than render cycles.

## Why This Matters Now

Signals are not new. MobX, Knockout, and Vue’s reactivity have used similar patterns for years.

What’s changed: The TC39 Signals proposal suggests this may become a native JavaScript primitive, like Promises or async/await.

If that happens, signals won’t be a “framework choice” — they’ll be a language feature. Understanding them now prepares you for that future.

## The Uncomfortable Truth

React’s `useEffect` isn't hard because developers don't understand it. It's hard because the abstraction doesn't match the problem.

**The problem:** Run this code when these specific values change.

**React’s abstraction:** Re-render the component and figure out if this effect should run based on referential equality of its dependencies.

That mismatch creates friction. useCallback, useMemo, and dependency arrays are duct tape over a model that’s too coarse for fine-grained state updates.

Signals eliminate the mismatch. The abstraction matches the intent.

After three years of dependency array gymnastics, I’ve realized: This isn’t my fault. It’s the model.

React’s component-based reactivity is brilliant for UI composition. But for state management? It’s overkill.

Signals offer a simpler mental model: no dependency arrays, no stale closures, no useCallback. Just data that knows when it changes.

You don’t have to adopt them today. But understanding how they work clarifies why certain React patterns feel harder than they should.

The next time you’re debugging a useEffect, ask yourself: Am I fighting the tool, or is the tool fighting me?

Maybe it’s time to stop fighting.