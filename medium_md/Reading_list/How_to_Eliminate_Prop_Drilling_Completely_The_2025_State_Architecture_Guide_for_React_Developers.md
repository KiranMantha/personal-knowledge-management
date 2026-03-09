---
title: "How to Eliminate Prop Drilling Completely: The 2025 State Architecture Guide for React Developers"
url: https://medium.com/p/54460d9f3683
---

# How to Eliminate Prop Drilling Completely: The 2025 State Architecture Guide for React Developers

[Original](https://medium.com/p/54460d9f3683)

Member-only story

# **How to Eliminate Prop Drilling Completely: The 2025 State Architecture Guide for React Developers**

## *A complete breakdown of modern state management patterns, React 19 features, and architecture principles that help you write cleaner, scalable apps — without passing props down endless component chains.*

[![Tejasvi Navale](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*OiSMcOu6KWz-vl7z)](/@tejasvinavale1599?source=post_page---byline--54460d9f3683---------------------------------------)

[Tejasvi Navale](/@tejasvinavale1599?source=post_page---byline--54460d9f3683---------------------------------------)

6 min read

·

Nov 13, 2025

--

6

Listen

Share

More

Press enter or click to view image in full size

![]()

> [***If Not a Member READ FROM HERE***](/@tejasvinavale1599/how-to-eliminate-prop-drilling-completely-the-2025-state-architecture-guide-for-react-developers-54460d9f3683?sk=fd04f3151908c4c6695b5ebdbd713705)

If you’ve ever passed data down four or five levels of components just to update a button, you’ve experienced the pain of **prop drilling**. It’s one of those problems every React developer faces early — and often continues to battle as apps grow more complex.

But in 2025, React development has matured dramatically. With **React 19**, **Server Components**, and tools like **Zustand**, **Jotai**, **React Query**, and the **Context Selector API**, we now have the power to eliminate prop drilling entirely — without adding unnecessary complexity or performance costs.

This guide breaks down how to structure your state and components in a way that’s **scalable, maintainable, and completely prop-drilling free**.

## What Is Prop Drilling?

Prop drilling happens when data or functions need to be passed from a parent component down through multiple intermediate components that don’t use the data themselves.

For example:

```
function App() {  
  const [theme, setTheme] = useState("light");  
  return <Layout theme={theme} setTheme={setTheme} />;  
}  
  
function Layout({ theme, setTheme }) {  
  return <Sidebar theme={theme} setTheme={setTheme} />;  
  
function Sidebar({ theme, setTheme }) {  
  return <ThemeToggle theme={theme} setTheme={setTheme} />;  
}
```

Only the `ThemeToggle` component needs the `theme`, but every component in between has to pass it down. This pattern quickly becomes unmanageable in large applications.

## Why Prop Drilling Is a Problem

Prop drilling may seem harmless in small components, but at scale, it introduces serious issues:

* **Tight coupling**: Changing one prop can require editing multiple unrelated components.
* **Reduced reusability**: Components become dependent on specific prop chains.
* **Performance issues**: Even components that don’t use a value will re-render when a parent prop changes.
* **Developer fatigue**: Onboarding new developers becomes harder as the app grows in depth and complexity.

The goal isn’t just to *reduce* prop drilling, but to **design a state architecture that makes it impossible**.

## The 2025 State Architecture Philosophy

Modern React encourages **layered state architecture** — a clear separation of where data lives and how it flows through the app.

Here’s the high-level principle:

> *“Keep state close to where it’s used, but globalize it only when necessary.”*

We can think of state in three scopes:

Scope Purpose Tool/Pattern **Local State** Used by one component `useState`, `useReducer` **Feature State** Shared within a feature Zustand, Jotai, Context Selector **Global State** Shared across the app Zustand store, Redux Toolkit **Server State** Synced with backend React Query (TanStack Query)

By placing state in the correct layer, you can almost always avoid prop drilling.

## Step 1: Use Context Properly (With Care)

React’s built-in Context API is powerful — but can easily cause over-rendering if used carelessly. The trick is to **create context slices** that expose only what each consumer needs.

Example: Theme management using a context.

```
// ThemeContext.tsx  
import { createContext, useContext, useState } from "react";  
  
const ThemeContext = createContext(null);  
  
export const ThemeProvider = ({ children }) => {  
  const [theme, setTheme] = useState("light");  
  return (  
    <ThemeContext.Provider value={{ theme, setTheme }}>  
      {children}  
    </ThemeContext.Provider>  
  );  
};  
  
export const useTheme = () => useContext(ThemeContext);
```

Now you can use it anywhere without passing props:

```
import { useTheme } from "@/shared/context/ThemeContext";  
  
function ThemeToggle() {  
  const { theme, setTheme } = useTheme();  
  return (  
    <button onClick={() => setTheme(theme === "light" ? "dark" : "light")}>  
      Switch Theme  
    </button>  
  );  
}
```

But in large apps, **too many contexts** can create unnecessary re-renders. This is where modern tools shine.

## Step 2: Use Modern State Libraries (Zustand, Jotai, or Signals)

In 2025, libraries like **Zustand** and **Jotai** have become the enterprise standard for managing state with minimal boilerplate and maximum performance.

## Example: Using Zustand for Feature State

```
import { create } from "zustand";  
  
export const useUserStore = create((set) => ({  
  user: null,  
  setUser: (data) => set({ user: data }),  
}));
```

Now, any component can access or update user data directly:

```
function Profile() {  
  const { user } = useUserStore();  
  return <h2>Welcome, {user?.name}</h2>;  
}
```

No prop drilling, no unnecessary re-renders, and no complicated setup.

**Why it works:** Zustand stores subscribe components only to the pieces of state they use, ensuring performance and isolation.

## Step 3: Handle Async and Server State Separately

A common mistake is mixing **server-fetched data** with local state.  
 With **React Query (TanStack Query)**, you can treat server state as a separate concern — cached, synchronized, and available anywhere.

Example:

```
import { useQuery } from "@tanstack/react-query";  
import { getUser } from "@/infrastructure/api/user";  
  
function UserProfile() {  
  const { data: user, isLoading } = useQuery(["user"], getUser);  
  if (isLoading) return <p>Loading...</p>;  
  return <div>{user.name}</div>;  
}
```

Now, there’s no need to pass fetched data around — any component can access it through query caching.

**Benefit:** Each feature manages its own async lifecycle without relying on props or parent states.

## Step 4: Combine State Layers with a Clean Folder Structure

To maintain this architecture, organize your code in a **feature-driven structure** that separates global and feature-level states clearly:

```
src/  
│  
├── app/  
│   ├── providers.tsx       # ThemeProvider, QueryClientProvider, etc.  
│   └── layout.tsx  
│  
├── features/  
│   ├── auth/  
│   │   ├── store/           # useAuthStore.ts  
│   │   ├── hooks/           # useLogin.ts  
│   │   └── components/  
│   ├── users/  
│   │   ├── store/           # useUserStore.ts  
│   │   └── components/  
│  
├── shared/  
│   ├── context/  
│   ├── hooks/  
│   ├── lib/  
│   ├── types/  
│   └── components/
```

Each **feature** owns its state, hooks, and logic. This keeps data flow consistent and predictable.

## Step 5: Introduce Context Selectors (React 19+)

React 19 introduces **context selectors**, allowing components to subscribe only to the specific values they need from a context — finally solving the over-render problem.

Example:

```
import { createContext, useContextSelector } from "use-context-selector";  
  
const ThemeContext = createContext(null);  
  
export const ThemeProvider = ({ children }) => {  
  const [theme, setTheme] = useState("light");  
  return (  
    <ThemeContext.Provider value={{ theme, setTheme }}>  
      {children}  
    </ThemeContext.Provider>  
  );  
};  
  
export const useThemeValue = () => useContextSelector(ThemeContext, v => v.theme);  
export const useSetTheme = () => useContextSelector(ThemeContext, v => v.setTheme);
```

This fine-grained subscription eliminates unnecessary re-renders and gives you React-level precision.

## Step 6: Avoid Common Anti-Patterns

Here are a few pitfalls to watch for:

* **Avoid global everything** — not all state needs to be global.
* **Don’t store derived data** — compute it with selectors or memoized hooks.
* **Don’t overload contexts** — keep each context focused on one domain (e.g., AuthContext, ThemeContext).
* **Avoid mixing local and server state** — keep them independent.

## Step 7: Build a Unified State Layer

For enterprise-scale applications, it’s best to have a unified **state layer** that coordinates global contexts, stores, and queries in one central place.

Example:

```
app/providers.tsx
```

```
import { ThemeProvider } from "@/shared/context/ThemeContext";  
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";  
import { StoreProvider } from "@/shared/store/Provider";  
  
const queryClient = new QueryClient();  
  
export function Providers({ children }) {  
  return (  
    <QueryClientProvider client={queryClient}>  
      <StoreProvider>  
        <ThemeProvider>{children}</ThemeProvider>  
      </StoreProvider>  
    </QueryClientProvider>  
  );  
}
```

This structure makes your app’s state architecture **predictable and pluggable** — you can add or remove features without touching unrelated code.

## Conclusion

Prop drilling is no longer a necessary evil. With the tools and architecture available in 2025 — **React 19 Context Selectors**, **Zustand**, **React Query**, and a **feature-driven structure** — you can build applications where **state lives exactly where it should**, and data flows cleanly without manual prop passing.

The secret lies in thinking in **layers of state**, not just hooks or contexts. When each layer has a clear purpose — local, feature, global, or server — you’ll find that prop drilling simply disappears.

React has grown up, and with the right architecture, your state management can too.

## Stay tuned in upcoming …

## follow me for more information:

* [**GitHub**](https://github.com/TejasviNaval): Code hosting & collaboration
* [**LinkedIn**](https://www.linkedin.com/in/tejasvi-navale-942067270/): Professional networking platform
* [**Instagram**:](https://www.instagram.com/tejasvi1n/?igsh=MWM5M3RrMnZvZTk4cQ%3D%3D#) Photo & video sharing
* [**Facebook**](https://www.facebook.com/tejasvi.navale): Social media & connections