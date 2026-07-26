---
title: "I Copy These 10 Code Snippets Into Every Single Project"
url: https://medium.com/p/38d8874be673
---

# I Copy These 10 Code Snippets Into Every Single Project

[Original](https://medium.com/p/38d8874be673)

# **I Copy These 10 Code Snippets Into Every Single Project**

[![Shayan Khan](https://miro.medium.com/v2/resize:fill:64:64/1*fksE1Ta5fRdQmK32xKaZTw.jpeg)](/@shynkhn17?source=post_page---byline--38d8874be673---------------------------------------)

[Shayan Khan](/@shynkhn17?source=post_page---byline--38d8874be673---------------------------------------)

5 min read

·

Jul 8, 2026

--

2

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D38d8874be673&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fskillstuff%2Fi-copy-these-10-code-snippets-into-every-single-project-38d8874be673&source=---header_actions--38d8874be673---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

**After shipping dozens of React, Node, and full-stack apps, these are the utilities I paste first. They’re simple, battle-tested, and save me hours of reinventing the wheel.**

You know that moment. You run npx create-vite or open a fresh repo, and within ten minutes you’re writing the same debounce function for the third time this year. Or wrestling with a date formatter because toLocaleDateString never quite does what you want on the first try.

I got tired of it. So I started keeping a private utils.ts file that travels with me from project to project. Over the years it evolved into a small but lethal set of helpers I literally copy-paste into every new codebase on day one.

These aren’t fancy libraries. They’re not framework-specific magic. They’re the boring, reliable pieces that make everything else less painful. Here are the ten I use most, with real TypeScript versions and the exact scenarios where they pay for themselves.

## 1. Debounce Stop Wasting API Calls on Every Keystroke

Live search, window resize handlers, scroll listeners — anything that fires too often needs debouncing.

TypeScript

```
export function debounce<T extends (...args: any[]) => void>(  
  func: T,  
  delay = 300  
) {  
  let timeout: NodeJS.Timeout;  
  return (...args: Parameters<T>) => {  
    clearTimeout(timeout);  
    timeout = setTimeout(() => func(...args), delay);  
  };  
}
```

**Real use case** in a React search component:

tsx

```
const [query, setQuery] = useState('');  
const debouncedSearch = useCallback(  
  debounce((q: string) => fetchUsers(q), 350),  
  []  
);
```

```
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {  
  const val = e.target.value;  
  setQuery(val);  
  debouncedSearch(val);  
};
```

Saves backend load and prevents janky UI. I’ve used variations of this in every dashboard I’ve built.

## 2. Format Date Consistent, Readable, No Surprises

Never Google date formatting again.

TypeScript

```
export function formatDate(  
  date: Date | string,  
  options: Intl.DateTimeFormatOptions = {  
    year: 'numeric',  
    month: 'short',  
    day: 'numeric',  
  },  
  locale = 'en-US'  
): string {  
  return new Date(date).toLocaleDateString(locale, options);  
}
```

**Use it everywhere**: table columns, activity logs, invoice dates. Pair it with a relative time helper when needed.

## 3. classNames — Clean Conditional Classes

Tailwind or plain CSS, this one belongs in every project.

TypeScript

```
export function classNames(...classes: (string | boolean | null | undefined)[]): string {  
  return classes.filter(Boolean).join(' ');  
}
```

**Example**:

tsx

```
<button  
  className={classNames(  
    'px-4 py-2 rounded-lg font-medium transition-colors',  
    isActive && 'bg-blue-600 text-white',  
    !isActive && 'bg-gray-100 hover:bg-gray-200',  
    disabled && 'opacity-50 cursor-not-allowed'  
  )}  
>
```

No more ugly template literals or giant ternary chains.

## 4. Safe JSON Parse — Protect Against Bad localStorage or API Data

TypeScript

```
export function safeJsonParse<T>(  
  str: string | null | undefined,  
  fallback: T = {} as T  
): T {  
  if (!str) return fallback;  
  try {  
    return JSON.parse(str) as T;  
  } catch {  
    console.warn('Failed to parse JSON:', str);  
    return fallback;  
  }  
}
```

I use this constantly with localStorage.getItem(‘userPreferences’). One malformed value won’t crash the entire app.

## 5. Throttle — For Scroll, Resize, and Mouse Events

When debounce isn’t the right tool.

TypeScript

```
export function throttle<T extends (...args: any[]) => void>(  
  func: T,  
  limit = 100  
) {  
  let inThrottle = false;  
  return (...args: Parameters<T>) => {  
    if (!inThrottle) {  
      func(...args);  
      inThrottle = true;  
      setTimeout(() => (inThrottle = false), limit);  
    }  
  };  
}
```

Perfect for infinite scroll position tracking or analytics events.

## 6. Deep Merge For Configs and State Updates

TypeScript

```
export function deepMerge<T>(target: T, ...sources: Partial<T>[]): T {  
  const result = { ...target };  
  for (const source of sources) {  
    if (source && typeof source === 'object') {  
      for (const key in source) {  
        if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {  
          result[key] = deepMerge(result[key] || {}, source[key]);  
        } else {  
          result[key] = source[key] as any;  
        }  
      }  
    }  
  }  
  return result;  
}
```

I use this when merging default theme configs with user overrides.

## 7. Local Storage Wrapper with Type Safety

TypeScript

```
export const storage = {  
  get: <T>(key: string, fallback: T): T => {  
    const item = localStorage.getItem(key);  
    return safeJsonParse(item, fallback);  
  },  
  set: <T>(key: string, value: T) => {  
    localStorage.setItem(key, JSON.stringify(value));  
  },  
  remove: (key: string) => localStorage.removeItem(key),  
};
```

TypeScript makes this delightful. No more any everywhere.

## 8. Fetch Wrapper with Timeout and Error Handling

TypeScript

```
export async function apiFetch<T>(  
  url: string,  
  options: RequestInit = {}  
): Promise<T> {  
  const controller = new AbortController();  
  const timeout = setTimeout(() => controller.abort(), 10000);
```

```
  try {  
    const response = await fetch(url, {  
      ...options,  
      signal: controller.signal,  
    });
```

```
    if (!response.ok) {  
      throw new Error(`HTTP ${response.status}`);  
    }
```

```
    return await response.json();  
  } finally {  
    clearTimeout(timeout);  
  }  
}
```

Add auth headers in a higher wrapper and you have a solid base for every API call.

## 9. Type Guard for Common Patterns

TypeScript

```
export function isDefined<T>(value: T | null | undefined): value is T {  
  return value !== null && value !== undefined;  
}
```

```
// Usage  
const validUsers = users.filter(isDefined);
```

Saves endless !== null && !== undefined checks, especially with strict mode.

## 10. Event Emitter (Lightweight Pub/Sub)

For components that need loose coupling without full state management.

TypeScript

```
type Listener = (...args: any[]) => void;
```

```
class EventEmitter {  
  private events = new Map<string, Listener[]>();
```

```
  on(event: string, listener: Listener) {  
    if (!this.events.has(event)) this.events.set(event, []);  
    this.events.get(event)!.push(listener);  
  }
```

```
  emit(event: string, ...args: any[]) {  
    this.events.get(event)?.forEach(listener => listener(...args));  
  }
```

```
  off(event: string, listener: Listener) {  
    const listeners = this.events.get(event);  
    if (listeners) {  
      this.events.set(  
        event,  
        listeners.filter(l => l !== listener)  
      );  
    }  
  }  
}
```

```
export const emitter = new EventEmitter();
```

I use this for cross-tab communication or global notifications in complex dashboards.

## How I Organize Them in Every Project

I create a src/lib/utils.ts (or utils/index.ts) and re-export everything from a barrel file. In larger apps I split into lib/utils, lib/api, lib/formatters, etc.

I also add JSDoc comments and tests for the critical ones. Consistency beats brilliance every time.

## Why This Approach Works So Well

Copying these snippets gives me:

* Immediate productivity on day one of a new project
* Fewer runtime surprises (especially with strict TypeScript)
* Consistent patterns across codebases, which helps when jumping between client work
* A foundation I can build higher-level abstractions on top of

They’re not sexy. But they’re the reason I can go from zero to functional prototype faster than most teams.

I’ve shipped production React apps, Node services, and full-stack tools using variations of this exact toolbox. The code isn’t perfect, but it’s good enough that I rarely have to think about these problems again.

What are the snippets you copy into every new project? Share your favorites in the comments — I’m always looking to improve the list.

The best tools are the ones you stop noticing because they just work