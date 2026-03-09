---
title: "5 Vanilla JS Patterns That Replace Entire Libraries"
url: https://medium.com/p/3d22445bfbc0
---

# 5 Vanilla JS Patterns That Replace Entire Libraries

[Original](https://medium.com/p/3d22445bfbc0)

Member-only story

# 5 Vanilla JS Patterns That Replace Entire Libraries

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](https://medium.com/@Iggy01?source=post_page---byline--3d22445bfbc0---------------------------------------)

[Ignatius Sani](https://medium.com/@Iggy01?source=post_page---byline--3d22445bfbc0---------------------------------------)

11 min read

·

Nov 1, 2025

--

20

Listen

Share

More

Press enter or click to view image in full size

![]()

Your node\_modules folder is 300MB.

Your bundle size is 2MB.

Your app takes 8 seconds to load.

And 80% of what you installed, you could have built in 50 lines of vanilla JavaScript.

Here are 5 patterns that prove it.

## Before You Reach for npm Install

I’m not saying libraries are evil. I’m not advocating for reinventing every wheel.

But before you npm install another package, ask yourself: “Could I build this in 50 lines?”

Often, the answer is yes.

Here are 5 patterns I use to keep my projects lean, my bundles small, and my understanding deep.

Each one replaces a popular library. Each one is production-ready. And each one teaches you more than installing ever could.

## 1. State Management (Replace Redux/Zustand)

**The Library Way:**

```
// Redux: ~40KB  
// Complex setup, actions, reducers, middleware  
npm install redux react-redux
```

**The Vanilla Way:**

```
// Simple observer pattern: ~30 lines  
class Store {  
  constructor(initialState = {}) {  
    this.state = initialState;  
    this.listeners = [];  
  }  
    
  getState() {  
    return this.state;  
  }  
    
  setState(updates) {  
    this.state = { ...this.state, ...updates };  
    this.listeners.forEach(listener => listener(this.state));  
  }  
    
  subscribe(listener) {  
    this.listeners.push(listener);  
    return () => {  
      this.listeners = this.listeners.filter(l => l !== listener);  
    };  
  }  
}  
  
// Usage  
const store = new Store({ count: 0, user: null });  
  
store.subscribe(state => {  
  console.log('State changed:', state);  
});  
  
store.setState({ count: 1 }); // Triggers all subscribers
```

**Using it with React:**

```
import { useState, useEffect } from 'react';  
  
function useStore(store) {  
  const [state, setState] = useState(store.getState());  
    
  useEffect(() => {  
    const unsubscribe = store.subscribe(newState => {  
      setState(newState);  
    });  
    return unsubscribe; // Cleanup on unmount  
  }, [store]);  
    
  return state;  
}  
  
// In your component  
function Counter() {  
  const state = useStore(store);  
    
  return (  
    <div>  
      <p>Count: {state.count}</p>  
      <button onClick={() => store.setState({ count: state.count + 1 })}>  
        Increment  
      </button>  
    </div>  
  );  
}
```

**When to use vanilla:**

* Single-page apps with simple state
* Projects with < 10 state variables
* When you need full control over state updates

**When to use a library:**

* Large apps with complex state relationships
* Time-travel debugging needed
* Team familiar with Redux patterns

**What you learn:** The observer pattern. How subscriptions work. Why React’s useState needs a re-render mechanism. This is the foundation of every state management library.

## 2. Event Bus (Replace EventEmitter/Mitt)

**The Library Way:**

```
// mitt: ~200 bytes (minimal, but still a dependency)  
// eventemitter3: ~7KB  
npm install mitt
```

**The Vanilla Way:**

```
// Custom event bus: ~20 lines  
  
class EventBus {  
  constructor() {  
    this.events = {};  
  }  
  
  on(event, callback) {  
    if (!this.events[event]) {  
      this.events[event] = [];  
    }  
    this.events[event].push(callback);  
  }  
  
  off(event, callback) {  
    if (!this.events[event]) return;  
    this.events[event] = this.events[event].filter(cb => cb !== callback);  
  }  
  
  emit(event, data) {  
    if (!this.events[event]) return;  
  
    // Copy to prevent issues if listeners mutate the list  
    [...this.events[event]].forEach(callback => {  
      callback(data);  
    });  
  }  
  
  once(event, callback) {  
    const wrapper = (data) => {  
      // Unsubscribe first to guarantee "once"  
      this.off(event, wrapper);  
      callback(data);  
    };  
  
    this.on(event, wrapper);  
  }  
}
```

**Using it with React:**

```
import { useEffect } from 'react';  
  
// Create global event bus  
export const eventBus = new EventBus();  
  
// Custom hook for events  
function useEvent(event, callback) {  
  useEffect(() => {  
    eventBus.on(event, callback);  
    return () => eventBus.off(event, callback);  
  }, [event, callback]);  
}  
  
// In your components  
function Notification() {  
  useEvent('notification:show', (message) => {  
    alert(message);  
  });  
    
  return <div>Notifications enabled</div>;  
}  
  
function LoginButton() {  
  const handleLogin = () => {  
    // Login logic...  
    eventBus.emit('user:login', { id: 1, name: 'John' });  
    eventBus.emit('notification:show', 'Welcome back!');  
  };  
    
  return <button onClick={handleLogin}>Login</button>;  
}
```

**When to use vanilla:**

* Component-to-component communication without prop drilling
* Decoupled modules that need to talk
* Simple pub/sub patterns
* Analytics tracking

**When to use a library:**

* Need wildcard events (\*.click)
* Require event priority/ordering
* Need advanced debugging tools

**What you learn:** The pub/sub pattern. Event-driven architecture. How frameworks handle cross-component communication. This pattern is everywhere in modern apps.

## 3. DOM Manipulation (Replace jQuery)

**The Library Way:**

```
// jQuery: ~90KB minified  
// Used to be essential. Now it's just habit.  
npm install jquery
```

**The Vanilla Way:**

```
// Modern DOM methods are just as easy  
  
// jQuery: $('.class').hide()  
document.querySelectorAll('.class').forEach(el => el.style.display = 'none');  
  
// jQuery: $('#id').addClass('active')  
document.getElementById('id').classList.add('active');  
  
// jQuery: $('.item').on('click', handler)  
document.querySelectorAll('.item').forEach(el => {  
  el.addEventListener('click', handler);  
});  
  
// jQuery: $.ajax()  
fetch('/api/data')  
  .then(res => res.json())  
  .then(data => console.log(data));  
  
// Helper function for common operations  
const $ = {  
  select: (selector) => document.querySelector(selector),  
  selectAll: (selector) => [...document.querySelectorAll(selector)],  
    
  create: (tag, props = {}) => {  
    const el = document.createElement(tag);  
    Object.assign(el, props);  
    return el;  
  },  
    
  on: (selector, event, handler) => {  
    document.querySelectorAll(selector).forEach(el => {  
      el.addEventListener(event, handler);  
    });  
  },  
    
  addClass: (selector, className) => {  
    document.querySelectorAll(selector).forEach(el => {  
      el.classList.add(className);  
    });  
  },  
    
  removeClass: (selector, className) => {  
    document.querySelectorAll(selector).forEach(el => {  
      el.classList.remove(className);  
    });  
  }  
};  
  
// Usage (jQuery-like syntax)  
$.addClass('.button', 'active');  
$.on('.button', 'click', () => console.log('clicked'));  
  
const newDiv = $.create('div', {   
  className: 'card',   
  textContent: 'Hello'   
});
```

**Real-world example:**

```
// Building a simple tabs system without jQuery  
  
function Tabs(containerSelector) {  
  const container = document.querySelector(containerSelector);  
  const tabs = [...container.querySelectorAll('[data-tab]')];  
  const panels = [...container.querySelectorAll('[data-panel]')];  
    
  tabs.forEach(tab => {  
    tab.addEventListener('click', () => {  
      // Remove active from all  
      tabs.forEach(t => t.classList.remove('active'));  
      panels.forEach(p => p.classList.remove('active'));  
        
      // Add active to clicked  
      tab.classList.add('active');  
      const panelId = tab.dataset.tab;  
      const panel = container.querySelector(`[data-panel="${panelId}"]`);  
      panel.classList.add('active');  
    });  
  });  
}  
  
// Usage  
Tabs('#my-tabs');
```

**When to use vanilla:**

* Modern browsers (95%+ support)
* Small to medium projects
* When bundle size matters
* Learning fundamental DOM APIs

**When to use jQuery:**

* Legacy browser support (IE < 11)
* Massive existing jQuery codebase
* Team very familiar with jQuery
* Honestly? Almost never anymore.

**What you learn:** How the DOM actually works. What querySelector does. How events propagate. Native APIs are powerful — jQuery just made them easier before browsers standardized.

## 4. Client-Side Routing (Replace React Router)

**The Library Way:**

```
// react-router-dom: ~70KB  
// Powerful, but overkill for simple apps  
npm install react-router-dom
```

**The Vanilla Way:**

```
// Simple router using History API: ~40 lines  
class Router {  
  constructor(routes) {  
    this.routes = routes;  
    this.currentPath = window.location.pathname;  
      
    // Handle browser back/forward  
    window.addEventListener('popstate', () => {  
      this.navigate(window.location.pathname, false);  
    });  
      
    // Handle link clicks  
    document.addEventListener('click', (e) => {  
      if (e.target.matches('[data-link]')) {  
        e.preventDefault();  
        this.navigate(e.target.getAttribute('href'));  
      }  
    });  
      
    // Initial render  
    this.navigate(this.currentPath, false);  
  }  
    
  navigate(path, pushState = true) {  
    this.currentPath = path;  
      
    if (pushState) {  
      window.history.pushState({}, '', path);  
    }  
      
    this.render();  
  }  
    
  render() {  
    const route = this.routes[this.currentPath] || this.routes['/404'];  
    const container = document.getElementById('app');  
      
    if (route) {  
      container.innerHTML = route();  
    }  
  }  
}  
  
// Define routes  
const routes = {  
  '/': () => `  
    <h1>Home</h1>  
    <a href="/about" data-link>About</a>  
  `,  
    
  '/about': () => `  
    <h1>About</h1>  
    <a href="/" data-link>Home</a>  
  `,  
    
  '/404': () => `<h1>404 - Not Found</h1>`  
};  
  
// Initialize  
const router = new Router(routes);
```

**Using it with React:**

```
import { useState, useEffect } from 'react';  
  
class ReactRouter {  
  constructor() {  
    this.routes = {};  
    this.listeners = [];  
    this.currentPath = window.location.pathname;  
      
    window.addEventListener('popstate', () => {  
      this.navigate(window.location.pathname, false);  
    });  
  }  
    
  addRoute(path, component) {  
    this.routes[path] = component;  
  }  
    
  navigate(path, pushState = true) {  
    this.currentPath = path;  
    if (pushState) {  
      window.history.pushState({}, '', path);  
    }  
    this.listeners.forEach(listener => listener(path));  
  }  
    
  subscribe(listener) {  
    this.listeners.push(listener);  
    return () => {  
      this.listeners = this.listeners.filter(l => l !== listener);  
    };  
  }  
    
  getComponent() {  
    return this.routes[this.currentPath] || this.routes['/404'];  
  }  
}  
  
// Create router instance  
export const router = new ReactRouter();  
  
// Custom hooks  
export function useRouter() {  
  const [path, setPath] = useState(router.currentPath);  
    
  useEffect(() => {  
    return router.subscribe(setPath);  
  }, []);  
    
  return { path, navigate: router.navigate.bind(router) };  
}  
  
export function Link({ to, children }) {  
  const handleClick = (e) => {  
    e.preventDefault();  
    router.navigate(to);  
  };  
    
  return <a href={to} onClick={handleClick}>{children}</a>;  
}  
  
// Usage in App  
function App() {  
  const { path } = useRouter();  
    
  // Define routes  
  router.addRoute('/', HomePage);  
  router.addRoute('/about', AboutPage);  
  router.addRoute('/404', NotFoundPage);  
    
  const Component = router.getComponent();  
    
  return (  
    <div>  
      <nav>  
        <Link to="/">Home</Link>  
        <Link to="/about">About</Link>  
      </nav>  
      <Component />  
    </div>  
  );  
}
```

**Adding dynamic routes:**

```
class Router {  
  // ... previous code ...  
    
  matchRoute(path) {  
    // Check exact matches first  
    if (this.routes[path]) {  
      return { handler: this.routes[path], params: {} };  
    }  
      
    // Check dynamic routes like /user/:id  
    for (let route in this.routes) {  
      const pattern = route.replace(/:[^/]+/g, '([^/]+)');  
      const regex = new RegExp(`^${pattern}$`);  
      const match = path.match(regex);  
        
      if (match) {  
        const keys = route.match(/:[^/]+/g) || [];  
        const params = {};  
        keys.forEach((key, i) => {  
          params[key.slice(1)] = match[i + 1];  
        });  
        return { handler: this.routes[route], params };  
      }  
    }  
      
    return { handler: this.routes['/404'], params: {} };  
  }  
    
  render() {  
    const { handler, params } = this.matchRoute(this.currentPath);  
    const container = document.getElementById('app');  
    container.innerHTML = handler(params);  
  }  
}  
  
// Usage with params  
const routes = {  
  '/': () => `<h1>Home</h1>`,  
  '/user/:id': (params) => `<h1>User ${params.id}</h1>`,  
  '/post/:slug': (params) => `<h1>Post: ${params.slug}</h1>`  
};
```

**When to use vanilla:**

* Simple SPAs with < 10 routes
* Static sites with light interactivity
* Learning how routing works
* Bundle size is critical

**When to use React Router:**

* Complex nested routes
* Route guards/authentication
* Code splitting per route
* Large team familiar with it

**What you learn:** The History API. How SPAs handle navigation. Why routes need to be matched. How frameworks prevent full page reloads. This is the foundation of every client-side router.

## 5. HTTP Requests (Replace Axios)

**The Library Way:**

```
// axios: ~13KB  
// Nice API, but fetch can do 90% of what you need  
npm install axios
```

**The Vanilla Way:**

```
// Fetch wrapper with common patterns: ~30 lines  
class HTTP {  
  constructor(baseURL = '', defaultHeaders = {}) {  
    this.baseURL = baseURL;  
    this.defaultHeaders = {  
      'Content-Type': 'application/json',  
      ...defaultHeaders  
    };  
  }  
    
  async request(endpoint, options = {}) {  
    const url = `${this.baseURL}${endpoint}`;  
    const config = {  
      ...options,  
      headers: {  
        ...this.defaultHeaders,  
        ...options.headers  
      }  
    };  
      
    try {  
      const response = await fetch(url, config);  
        
      // Handle non-2xx responses  
      if (!response.ok) {  
        throw new Error(`HTTP Error: ${response.status}`);  
      }  
        
      // Parse JSON if response has content  
      const contentType = response.headers.get('content-type');  
      if (contentType && contentType.includes('application/json')) {  
        return await response.json();  
      }  
        
      return await response.text();  
    } catch (error) {  
      console.error('Request failed:', error);  
      throw error;  
    }  
  }  
    
  get(endpoint, options = {}) {  
    return this.request(endpoint, { ...options, method: 'GET' });  
  }  
    
  post(endpoint, data, options = {}) {  
    return this.request(endpoint, {  
      ...options,  
      method: 'POST',  
      body: JSON.stringify(data)  
    });  
  }  
    
  put(endpoint, data, options = {}) {  
    return this.request(endpoint, {  
      ...options,  
      method: 'PUT',  
      body: JSON.stringify(data)  
    });  
  }  
    
  delete(endpoint, options = {}) {  
    return this.request(endpoint, { ...options, method: 'DELETE' });  
  }  
}  
  
// Usage  
const api = new HTTP('https://api.example.com');  
  
// GET request  
const users = await api.get('/users');  
  
// POST request  
const newUser = await api.post('/users', {  
  name: 'John',  
  email: 'john@example.com'  
});  
  
// With custom headers  
const data = await api.get('/protected', {  
  headers: { Authorization: 'Bearer token123' }  
});
```

**Adding interceptors (like Axios):**

```
class HTTP {  
  constructor(baseURL = '', defaultHeaders = {}) {  
    this.baseURL = baseURL;  
    this.defaultHeaders = {  
      'Content-Type': 'application/json',  
      ...defaultHeaders  
    };  
    this.interceptors = {  
      request: [],  
      response: []  
    };  
  }  
    
  addRequestInterceptor(fn) {  
    this.interceptors.request.push(fn);  
  }  
    
  addResponseInterceptor(fn) {  
    this.interceptors.response.push(fn);  
  }  
    
  async request(endpoint, options = {}) {  
    const url = `${this.baseURL}${endpoint}`;  
    let config = {  
      ...options,  
      headers: {  
        ...this.defaultHeaders,  
        ...options.headers  
      }  
    };  
      
    // Run request interceptors  
    for (let interceptor of this.interceptors.request) {  
      config = await interceptor(config);  
    }  
      
    try {  
      let response = await fetch(url, config);  
        
      // Run response interceptors  
      for (let interceptor of this.interceptors.response) {  
        response = await interceptor(response);  
      }  
        
      if (!response.ok) {  
        throw new Error(`HTTP Error: ${response.status}`);  
      }  
        
      const contentType = response.headers.get('content-type');  
      if (contentType && contentType.includes('application/json')) {  
        return await response.json();  
      }  
        
      return await response.text();  
    } catch (error) {  
      console.error('Request failed:', error);  
      throw error;  
    }  
  }  
    
  // ... get, post, put, delete methods same as before  
}  
  
// Usage with interceptors  
const api = new HTTP('https://api.example.com');  
  
// Add auth token to all requests  
api.addRequestInterceptor(async (config) => {  
  const token = localStorage.getItem('token');  
  if (token) {  
    config.headers.Authorization = `Bearer ${token}`;  
  }  
  return config;  
});  
  
// Log all responses  
api.addResponseInterceptor(async (response) => {  
  console.log('Response received:', response.status);  
  return response;  
});
```

**Using it with React:**

```
import { useState, useEffect } from 'react';  
  
// Custom hook for data fetching  
function useFetch(endpoint, options = {}) {  
  const [data, setData] = useState(null);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  
    
  useEffect(() => {  
    const controller = new AbortController();  
      
    async function fetchData() {  
      try {  
        setLoading(true);  
        const result = await api.get(endpoint, {  
          ...options,  
          signal: controller.signal  
        });  
        setData(result);  
        setError(null);  
      } catch (err) {  
        if (err.name !== 'AbortError') {  
          setError(err.message);  
        }  
      } finally {  
        setLoading(false);  
      }  
    }  
      
    fetchData();  
      
    return () => controller.abort(); // Cleanup  
  }, [endpoint]);  
    
  return { data, loading, error };  
}  
  
// Usage in component  
function UserList() {  
  const { data: users, loading, error } = useFetch('/users');  
    
  if (loading) return <div>Loading...</div>;  
  if (error) return <div>Error: {error}</div>;  
    
  return (  
    <ul>  
      {users.map(user => (  
        <li key={user.id}>{user.name}</li>  
      ))}  
    </ul>  
  );  
}  
  
// For mutations  
function CreateUser() {  
  const [loading, setLoading] = useState(false);  
    
  const handleSubmit = async (e) => {  
    e.preventDefault();  
    setLoading(true);  
      
    try {  
      await api.post('/users', {  
        name: e.target.name.value,  
        email: e.target.email.value  
      });  
      alert('User created!');  
    } catch (error) {  
      alert('Error: ' + error.message);  
    } finally {  
      setLoading(false);  
    }  
  };  
    
  return (  
    <form onSubmit={handleSubmit}>  
      <input name="name" placeholder="Name" />  
      <input name="email" placeholder="Email" />  
      <button disabled={loading}>Create</button>  
    </form>  
  );  
}
```

**When to use vanilla:**

* Simple REST APIs
* Modern browsers (fetch is supported)
* Small to medium projects
* When you control the API

**When to use Axios:**

* Need automatic request cancellation
* Complex interceptor logic
* Progress tracking for uploads
* Legacy browser support (fetch polyfill)
* Team very familiar with Axios patterns

**What you learn:** The Fetch API. How HTTP works. Request/response cycles. Error handling. AbortController for cleanup. This is fundamental to every web application.

## The Real Cost of Dependencies

Here’s what nobody tells you about npm install:

**Bundle Size**

Those five libraries? They just added 500KB to your bundle. Your users now wait 3 extra seconds for your app to load. On mobile, that’s the difference between engagement and bounce.

**Maintenance Burden**

Every dependency is a commitment. Security updates. Breaking changes. Deprecated APIs. You didn’t just install code — you installed ongoing maintenance work.

**Understanding Gap**

When something breaks, you can’t fix it. You search GitHub issues. You wait for maintainers. You try workarounds. Because you never learned how it works underneath.

But when you build it yourself?

You understand every line. You fix bugs in minutes. You add features without waiting for PRs. You control your destiny.

## When to Use Libraries (Yes, Really)

I’m not advocating for zero dependencies. I’m advocating for intentional dependencies.

Use a library when:

* The problem is genuinely complex (date manipulation, i18n)
* Edge cases are critical (security, accessibility)
* The library is battle-tested (React, not random-state-lib)
* Your time is more valuable than bundle size
* The alternative is reinventing a very complicated wheel

Don’t use a library when:

* You can build it in < 50 lines
* You only need 10% of its features
* It’s not actively maintained
* You’re doing it “because everyone else does”
* Learning how it works would make you better

## The Pattern Behind the Patterns

Notice something? All five patterns share common traits:

**Observer Pattern** — State management and event bus both use subscriptions

**Encapsulation** — Each pattern hides complexity behind a simple API

**Functional Core** — Pure functions at the heart, side effects at the edges

**Composability** — Small pieces that work together

These aren’t “vanilla JS tricks.” These are fundamental programming patterns. Learning them makes you better at using libraries, not just replacing them.

When you understand the pattern, every library using that pattern becomes obvious.

## Start Small

You don’t need to rewrite your entire codebase tomorrow.

Next time you reach for npm install, pause. Ask yourself:

* Could I build this in 50 lines?
* Would building it teach me something?
* Do I really need all its features?

Start with one pattern. Build a simple event bus. Create a tiny router. Write a fetch wrapper.

See how it feels. Notice what you learn. Appreciate how much lighter your bundle becomes.

Then decide: library or vanilla?

Either way, you’re making an informed choice. Not a default one.

And that’s the difference between a developer who uses tools and a developer who understands tools.

**Want more patterns like these?**

I write about deep JavaScript concepts without the fluff — no metaphors, no follow-along tutorials, just practical patterns and strong opinions about building better with less.

Follow me here on Medium for more.

**Previous articles:**

* [You Don’t Hate Coding — You Hate Following Tutorials](https://medium.com/@Iggy01/maybe-you-dont-like-project-based-tutorials-and-that-s-perfectly-okay-43063101b771)
* [JavaScript Event Loop Explained (Without the Coffee Shop Analogy)](https://medium.com/javascript-in-plain-english/javascript-event-loop-explained-without-the-coffee-shop-analogy-9120cce50c46)
* [I Rebuilt React’s useState in 20 Lines of Vanilla JS](https://medium.com/codex/i-rebuilt-reacts-usestate-in-20-lines-of-vanilla-js-28edf6b78f55)
* [Your Framework Knowledge Is Worthless (But Your JS Fundamentals Aren’t)](https://medium.com/javascript-in-plain-english/your-framework-knowledge-is-worthless-but-your-js-fundamentals-arent-a33efd202430)

**Next up:** Deep dive into JavaScript closures — the pattern that powers 80% of modern JavaScript.

Which pattern will you try first? Drop a comment and let me know. Or share your own vanilla JS patterns that replaced libraries.

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!