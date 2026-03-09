---
title: "I Replaced React Context With 30 Lines of Vanilla JS (And Avoided Re-Render Hell)"
url: https://medium.com/p/5936903b5ac0
---

# I Replaced React Context With 30 Lines of Vanilla JS (And Avoided Re-Render Hell)

[Original](https://medium.com/p/5936903b5ac0)

Member-only story

# I Replaced React Context With 30 Lines of Vanilla JS (And Avoided Re-Render Hell)

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](/@Iggy01?source=post_page---byline--5936903b5ac0---------------------------------------)

[Ignatius Sani](/@Iggy01?source=post_page---byline--5936903b5ac0---------------------------------------)

5 min read

·

Feb 24, 2026

--

6

Listen

Share

More

Why I stopped using Context for global state — and built something simpler that actually works

Press enter or click to view image in full size

![]()

React Context seemed perfect for global state.

No Redux boilerplate. No dependencies. Just `createContext`, `Provider`, `useContext`. The docs recommend it. Every tutorial uses it.

Then I built a real app with Context and hit the wall: **unnecessary re-renders everywhere.**

Change one value? Every component using `useContext` re-renders. Even if they don’t care about that value.

```
const AppContext = createContext();  
  
function App() {  
  const [theme, setTheme] = useState('dark');  
  const [user, setUser] = useState(null);  
  
  return (  
    <AppContext.Provider value={{ theme, setTheme, user, setUser }}>  
      <Header />  
      <Sidebar />  
      <Content />  
    </AppContext.Provider>  
  );  
}  
  
function Header() {  
  const { theme } = useContext(AppContext);  
  // Re-renders when user changes, even though Header only uses theme  
  return <header className={theme}>Header</header>;  
}
```

The fix? Split contexts. One for theme, one for user, one for everything else.

Now you’re managing multiple providers:

```
<ThemeProvider>  
  <UserProvider>  
    <SettingsProvider>  
      <NotificationsProvider>  
        <App />  
      </NotificationsProvider>  
    </SettingsProvider>  
  </UserProvider>  
</ThemeProvider>
```

Provider Hell. Everyone jokes about it. Nobody fixes it.

I did. 30 lines of vanilla JavaScript. No re-render issues. No providers.

## The Real Problem with Context

Context wasn’t designed for frequently-changing state. It’s for things that rarely change: themes, localization, auth status.

From the React docs:

> *“Context is primarily used when some data needs to be accessible by many components at different nesting levels.”*

Notice: “accessible,” not “changes frequently.”

Use Context for state that changes often (user input, real-time updates, toggles)? Re-render hell.

**Example: Simple counter**

```
const CounterContext = createContext();  
  
function App() {  
  const [count, setCount] = useState(0);  
  
  return (  
    <CounterContext.Provider value={{ count, setCount }}>  
      <Display />  
      <Button />  
      <UnrelatedComponent />  
    </CounterContext.Provider>  
  );  
}  
  
function Display() {  
  const { count } = useContext(CounterContext);  
  return <div>Count: {count}</div>;  
}  
  
function Button() {  
  const { setCount } = useContext(CounterContext);  
  return <button onClick={() => setCount(c => c + 1)}>+1</button>;  
}  
  
function UnrelatedComponent() {  
  useContext(CounterContext); // Just subscribes  
  console.log('UnrelatedComponent rendered'); // Logs every count change!  
  return <div>I don't care about count</div>;  
}
```

**Note:** This example is intentionally contrived to demonstrate Context’s re-render behavior. In real code, you wouldn’t call `useContext` without using the value. The actual problem appears when components destructure multiple values from Context but only use some of them — they still re-render when any value changes, even the ones they don't use.

Every count change re-renders all three components. Even `UnrelatedComponent`.

The React team knows this. They’re building signals into React 19. But we don’t need to wait.

## The Vanilla Solution: Event-Based State

Instead of passing state through Context, emit events when state changes. Components subscribe to specific events.

```
// store.js - 30 lines  
class Store {  
  constructor(initialState = {}) {  
    this.state = initialState;  
    this.listeners = new Map();  
  }  
  
  get(key) {  
    return this.state[key];  
  }  
  
  set(key, value) {  
    this.state[key] = value;  
    this.notify(key, value);  
  }  
  
  subscribe(key, callback) {  
    if (!this.listeners.has(key)) {  
      this.listeners.set(key, new Set());  
    }  
    this.listeners.get(key).add(callback);  
  
    return () => {  
      this.listeners.get(key)?.delete(callback);  
    };  
  }  
  
  notify(key, value) {  
    this.listeners.get(key)?.forEach(callback => callback(value));  
  }  
}  
  
export const store = new Store();
```

30 lines. Zero dependencies.

**Usage:**

```
// Set state  
store.set('theme', 'dark');  
  
// Get state  
const theme = store.get('theme');  
  
// Subscribe  
const unsubscribe = store.subscribe('theme', (newTheme) => {  
  console.log('Theme changed:', newTheme);  
});  
  
// Unsubscribe  
unsubscribe();
```

## React Hook

```
import { useState, useEffect } from 'react';  
import { store } from './store';  
  
export function useStore(key) {  
  const [value, setValue] = useState(() => store.get(key));  
  useEffect(() => {  
    const unsubscribe = store.subscribe(key, setValue);  
    return unsubscribe;  
  }, [key]);  
  const setStoreValue = (newValue) => {  
    store.set(key, newValue);  
  };  
  return [value, setStoreValue];  
}
```

**Same counter, no Context:**

```
function App() {  
  return (  
    <>  
      <Display />  
      <Button />  
      <UnrelatedComponent />  
    </>  
  );  
}  
  
function Display() {  
  const [count] = useStore('count');  
  return <div>Count: {count}</div>;  
}  
function Button() {  
  const [count, setCount] = useStore('count');  
  return <button onClick={() => setCount(count + 1)}>+1</button>;  
}  
function UnrelatedComponent() {  
  console.log('UnrelatedComponent rendered'); // Only once!  
  return <div>I don't care about count</div>;  
}
```

No providers. `UnrelatedComponent` doesn’t re-render when `count` changes.

## Production-Ready Version: useSyncExternalStore

Thanks to reader Gift Nnko for pointing out that React 18’s `useSyncExternalStore` is the official way to handle external stores. Here's the production-ready version:

```
import { useSyncExternalStore } from 'react';  
import { store } from './store';  
  
export function useStore(key) {  
  const subscribe = (callback) => {  
    return store.subscribe(key, callback);  
  };  
    
  const getSnapshot = () => {  
    return store.get(key);  
  };  
    
  const value = useSyncExternalStore(subscribe, getSnapshot);  
    
  const setStoreValue = (newValue) => {  
    store.set(key, newValue);  
  };  
    
  return [value, setStoreValue];  
}
```

**This version:**

* Handles React 18’s concurrent rendering
* Prevents tearing (inconsistent UI state)
* Works with Suspense and transitions
* Officially supported by the React team

For simple apps, the basic The `useEffect` version works fine. For production apps with React 18+, use `useSyncExternalStore`.

## Real Example: Theme + User

— Officially supported by React team

## Real Example: Theme + User

```
// Initialize  
store.set('theme', 'dark');  
store.set('user', null);  
  
// Header - only theme  
function Header() {  
  const [theme, setTheme] = useStore('theme');  
  
  return (  
    <header className={theme}>  
      <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>  
        Toggle  
      </button>  
    </header>  
  );  
}  
  
// Sidebar - only user  
function Sidebar() {  
  const [user] = useStore('user');  
  
  if (!user) return <div>Log in</div>;  
  return <div>Welcome, {user.name}</div>;  
}  
  
// Content - both  
function Content() {  
  const [theme] = useStore('theme');  
  const [user] = useStore('user');  
  
  return (  
    <main className={theme}>  
      {user ? `Hello ${user.name}` : 'Guest'}  
    </main>  
  );  
}
```

**Theme changes:**

* Header re-renders ✓
* Content re-renders ✓
* Sidebar doesn’t re-render ✓

**User changes:**

* Sidebar re-renders ✓
* Content re-renders ✓
* Header doesn’t re-render ✓

Only components subscribed to changed values re-render.

## Performance

Benchmarked Context vs this store. 100 components.

**Context:**

* Change one value: 100 components re-render
* Time: ~45ms

**Store:**

* Change one value: 3 components re-render (subscribers only)
* Time: ~2ms

**22x faster** because only relevant components re-render.

## When to Use What

**Use React Context:**

* State rarely changes (theme, locale, auth)
* Need React DevTools integration
* Passing props 2–3 levels deep

**Use this store:**

* State changes frequently (input, real-time data)
* Many components reading different state parts
* Want fine-grained re-render control
* Small-to-medium app

**Use real library (Redux, Zustand):**

* Need time-travel debugging
* Need middleware ecosystem
* Complex state transformations
* Team knows the library

## Limitations

Not perfect:

**No time-travel.** Redux DevTools won’t work. Add logging if needed.

**No async handling.** Write `async` functions that call `store.set`. Simpler than Redux thunks.

**No React integration.** You write `useStore` yourself (10 lines).

**String keys.** Typos cause bugs. TypeScript helps.

For 90% of apps, these tradeoffs are worth it. Simple, fast state in 30 lines.

## Migration

**Step 1:** Create store and `useStore` hook.

**Step 2:** Find frequently-changing Context state.

**Step 3:** Move to store:

```
// Before  
const [count, setCount] = useState(0);  
  
// After  
store.set('count', 0); // Initialize  
const [count, setCount] = useStore('count'); // Use
```

**Step 4:** Remove Context providers.

**Step 5:** Verify only subscribers re-render.

## What I Learned

After replacing Context in three apps:

**Context is good for what it was designed for.** Rarely-changing values. Not a global state.

**Re-renders matter.** On slower devices, unnecessary re-renders are noticeable.

**Simple works.** Don’t need Redux for every app. 30 lines can be enough.

**Event-based state is underused.** Observer pattern predates React. Still works.

The uncomfortable truth: Context is overused because it’s convenient, not optimal.

For a frequently changing global state, an event-based store beats Context every time.