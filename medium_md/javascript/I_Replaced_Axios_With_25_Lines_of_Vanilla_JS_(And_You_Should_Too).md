---
title: "I Replaced Axios With 25 Lines of Vanilla JS (And You Should Too)"
url: https://medium.com/p/328fda24244f
---

# I Replaced Axios With 25 Lines of Vanilla JS (And You Should Too)

[Original](https://medium.com/p/328fda24244f)

Member-only story

# I Replaced Axios With 25 Lines of Vanilla JS (And You Should Too)

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](https://medium.com/@Iggy01?source=post_page---byline--328fda24244f---------------------------------------)

[Ignatius Sani](https://medium.com/@Iggy01?source=post_page---byline--328fda24244f---------------------------------------)

5 min read

·

Nov 25, 2025

--

10

Listen

Share

More

Press enter or click to view image in full size

![]()

I used to install Axios in every project.

It felt professional. “Real developers use Axios,” I thought.

Then I actually read Axios’s source code.

Turns out, I was importing 13KB to wrap `fetch()` with features JavaScript already provides.

Here’s what changed my mind.

## What Axios Actually Does

Before we replace it, let’s be honest about what Axios gives you:

**Automatic JSON transformation** — Axios auto-parses JSON responses

**Better error handling** — Axios rejects on HTTP error status codes

**Request/response interceptors** — Middleware for requests

**Request cancellation** — AbortController wrapper

**Timeout support** — Race condition with setTimeout

That’s it. Five features.

And here’s the thing: **JavaScript’s Fetch API can do all of this.**

You just need to know how.

## The 25-Line Axios Alternative

Here’s a drop-in replacement that does everything Axios does:

```
class HTTP {  
  constructor(baseURL = '', timeout = 5000) {  
    this.baseURL = baseURL;  
    this.timeout = timeout;  
    this.interceptors = { request: [], response: [] };  
  }  
  
  async request(url, options = {}) {  
    // Apply request interceptors  
    let config = { ...options };  
    for (let interceptor of this.interceptors.request) {  
      config = await interceptor(config);  
    }  
  
    // Create abort controller for timeout  
    const controller = new AbortController();  
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);  
  
    try {  
      const response = await fetch(this.baseURL + url, {  
        ...config,  
        signal: controller.signal  
      });  
  
      clearTimeout(timeoutId);  
  
      // Axios-style error handling (throw on bad status)  
      if (!response.ok) {  
        throw new Error(`HTTP Error: ${response.status}`);  
      }  
  
      // Auto-parse JSON (like Axios does)  
      const data = await response.json();  
  
      // Apply response interceptors  
      let result = { data, status: response.status, headers: response.headers };  
      for (let interceptor of this.interceptors.response) {  
        result = await interceptor(result);  
      }  
  
      return result;  
  
    } catch (error) {  
      if (error.name === 'AbortError') {  
        throw new Error('Request timeout');  
      }  
      throw error;  
    }  
  }  
  
  // Convenience methods  
  get(url, options) {   
    return this.request(url, { ...options, method: 'GET' });   
  }  
    
  post(url, data, options) {   
    return this.request(url, {   
      ...options,   
      method: 'POST',   
      headers: { 'Content-Type': 'application/json', ...options?.headers },  
      body: JSON.stringify(data)   
    });   
  }  
    
  put(url, data, options) {   
    return this.request(url, {   
      ...options,   
      method: 'PUT',   
      headers: { 'Content-Type': 'application/json', ...options?.headers },  
      body: JSON.stringify(data)   
    });   
  }  
    
  delete(url, options) {   
    return this.request(url, { ...options, method: 'DELETE' });   
  }  
  
  // Interceptor support  
  addRequestInterceptor(fn) {   
    this.interceptors.request.push(fn);   
  }  
    
  addResponseInterceptor(fn) {   
    this.interceptors.response.push(fn);   
  }  
}  
  
export default HTTP;
```

**That’s it.** 25 lines. Does everything Axios does.

## How to Use It

**Basic Usage (Just Like Axios)**

```
const http = new HTTP('https://api.example.com');  
  
// GET request  
const { data } = await http.get('/users');  
  
// POST request  
const { data } = await http.post('/users', {   
  name: 'John',   
  email: 'john@example.com'   
});  
  
// With timeout (5 seconds default)  
const http = new HTTP('https://api.example.com', 5000);
```

**Request Interceptors (Add Auth Tokens)**

```
http.addRequestInterceptor((config) => {  
  const token = localStorage.getItem('token');  
  if (token) {  
    config.headers = {  
      ...config.headers,  
      'Authorization': `Bearer ${token}`  
    };  
  }  
  return config;  
});  
  
// Now every request includes the token  
await http.get('/protected-route');
```

**Response Interceptors (Handle Errors Globally)**

```
http.addResponseInterceptor((response) => {  
  console.log('Response received:', response.status);  
  return response;  
});  
  
// Or handle errors globally  
http.addResponseInterceptor((response) => {  
  if (response.status === 401) {  
    // Redirect to login  
    window.location.href = '/login';  
  }  
  return response;  
});
```

**Request Cancellation (Built-in Timeout)**

```
// Automatically cancels after timeout  
const http = new HTTP('https://slow-api.com', 3000);  
  
try {  
  await http.get('/slow-endpoint');  
} catch (error) {  
  console.log(error.message); // "Request timeout"  
}
```

## Works Perfectly With React (and Every Framework)

One question I always get: “Can I use this in React?”

**Absolutely.** This isn’t a library replacement. It’s a pattern you can use anywhere.

**React Example — Custom Hook**

```
import { useState, useEffect } from 'react';  
import HTTP from './http';  
  
const http = new HTTP('https://api.example.com');  
  
function useAPI(url) {  
  const [data, setData] = useState(null);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  
  
  useEffect(() => {  
    http.get(url)  
      .then(response => {  
        setData(response.data);  
        setLoading(false);  
      })  
      .catch(err => {  
        setError(err.message);  
        setLoading(false);  
      });  
  }, [url]);  
  
  return { data, loading, error };  
}  
  
// Usage in component  
function Users() {  
  const { data, loading, error } = useAPI('/users');  
  
  if (loading) return <div>Loading...</div>;  
  if (error) return <div>Error: {error}</div>;  
  
  return (  
    <ul>  
      {data.map(user => <li key={user.id}>{user.name}</li>)}  
    </ul>  
  );  
}
```

**Vue Example**

```
import { ref } from 'vue';  
import HTTP from './http';  
  
const http = new HTTP('https://api.example.com');  
  
export function useAPI(url) {  
  const data = ref(null);  
  const loading = ref(true);  
  const error = ref(null);  
  
  http.get(url)  
    .then(response => {  
      data.value = response.data;  
      loading.value = false;  
    })  
    .catch(err => {  
      error.value = err.message;  
      loading.value = false;  
    });  
  
  return { data, loading, error };  
}
```

**Next.js Server Actions**

```
'use server'  
import HTTP from './http';  
  
const http = new HTTP('https://api.example.com');  
  
export async function getUsers() {  
  const { data } = await http.get('/users');  
  return data;  
}  
  
export async function createUser(formData) {  
  const userData = {  
    name: formData.get('name'),  
    email: formData.get('email')  
  };  
    
  const { data } = await http.post('/users', userData);  
  return data;  
}
```

**Node.js Backend**

```
import express from 'express';  
import HTTP from './http';  
  
const app = express();  
const http = new HTTP('https://external-api.com');  
  
app.get('/api/users', async (req, res) => {  
  try {  
    const { data } = await http.get('/users');  
    res.json(data);  
  } catch (error) {  
    res.status(500).json({ error: error.message });  
  }  
});
```

### The Point:

It’s just JavaScript. It works everywhere Axios works because i**t performs the same function as Axios**. React, Vue, Angular, Svelte, vanilla JavaScript, Node.js backends — doesn’t matter. If you can use `fetch()`, you can use this.

## What You Gain

**Smaller Bundle Size**

Axios: **13KB** minified + gzipped

This: **~1KB** (you write it yourself)

**Savings: 12KB** (92% reduction)

**No Dependencies**

Axios has dependencies that have dependencies.

This: Zero dependencies.

**No supply chain attacks, no version conflicts.**

**Complete Control**

Want to add retry logic? Add it.

Want custom error handling? Change it.

Want to log all requests? One line.

**You own the code.**

**Learning**

This is the big one.

When you write it yourself, you understand how HTTP actually works. You learn fetch, AbortController, and Promises. You see how interceptors are just arrays of functions.

**You become a better developer.**

## When to Use Axios Instead

Let me be fair: Axios still has legitimate use cases.

**Use Axios if:**

You need to support Internet Explorer (fetch isn’t available)

You’re working in a large team and want consistent patterns

You need advanced features like upload progress tracking

Your project already uses it (don’t refactor for no reason)

**But 90% of projects?** You don’t need it.

## The Bigger Lesson

Here’s what this really taught me:

**Most libraries are just wrappers around language features.**

Axios wraps `fetch()`

Lodash wraps array methods

Moment.js wraps `Date` (use `Intl.DateTimeFormat` instead)

UUID wraps `crypto.randomUUID()`

That doesn’t make them bad. But it means: **If you understand the underlying JavaScript, you don’t need most libraries.**

## Try It Yourself

Copy the code above.

Replace one Axios call in your project.

See if you miss anything.

I bet you won’t.

And when you’re comfortable, replace another. Then another.

Eventually, you’ll realize: **You never needed Axios.**

You just needed to understand `fetch()`.

## Final Thought

I’m not against libraries. I use plenty of them.

But I’m against **unnecessary dependencies.**

Every `npm install` is a potential security vulnerability, a maintenance burden, a piece of code you don't control, and a learning opportunity you just skipped.

So before you install Axios (or any library), ask:

**“Can I build this in 25 lines?”**

If yes, build it.

You’ll write better code. And you’ll become a better developer.

**What You’ll Build Next:**

Now that you understand HTTP clients, try building a caching layer (memoize responses), retry logic with exponential backoff, request deduplication (prevent duplicate calls), or progress tracking for uploads.

Once you see how simple it is, you’ll never look at libraries the same way.