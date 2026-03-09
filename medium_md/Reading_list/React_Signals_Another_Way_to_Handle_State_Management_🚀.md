---
title: "React Signals: Another Way to Handle State Management 🚀"
url: https://medium.com/p/a5fc39bd97b5
---

# React Signals: Another Way to Handle State Management 🚀

[Original](https://medium.com/p/a5fc39bd97b5)

# React Signals: Another Way to Handle State Management 🚀

[![Frontend Highlights](https://miro.medium.com/v2/resize:fill:64:64/1*ISIQMnQqz3UzRTGB0_d4jw.jpeg)](/@ignatovich.dm?source=post_page---byline--a5fc39bd97b5---------------------------------------)

[Frontend Highlights](/@ignatovich.dm?source=post_page---byline--a5fc39bd97b5---------------------------------------)

7 min read

·

Nov 26, 2024

--

12

Listen

Share

More

React Signals are a relatively new concept designed to simplify and optimize state management in React applications. Borrowing ideas from reactive programming and frameworks like SolidJS or Angular, signals offer a performant, fine-grained reactivity mechanism that focuses on reducing unnecessary re-renders and improving developer experience.

## What Are Signals?

A **signal** is a reactive primitive used to track and propagate state changes efficiently. Unlike React’s `useState` or `useReducer`, signals:

* Are not tied to React’s component lifecycle.
* Automatically trigger updates for components or computations that depend on their value.
* Avoid the need for wrapping components in hooks like `useMemo` or `useCallback` for optimization.

**Key Features:**

1. **Fine-Grained Reactivity**: Only components or functions that directly depend on a signal are updated.
2. **Lifecycle Independence**: Signals exist independently of React components, making them reusable across different contexts.
3. **Predictable Behaviour**: They simplify state handling by eliminating dependency arrays and minimizing bugs.

## Why Use Signals in React?

**Performance Optimization**:

* React Signals allow updates at a granular level, avoiding unnecessary re-renders.
* Ideal for applications with frequent or complex state changes, such as dashboards or collaborative tools.

Press enter or click to view image in full size

![]()

**Improved Code Simplicity**:

* Signals reduce boilerplate compared to useState or useEffect
* Dependency arrays and cleanup logic in effects are no longer a concern
* State management becomes more declarative

**Reactive Ecosystem**:

* Similar to reactivity models in Angular or SolidJS
* Allows React to handle state like a “reactive system,” enabling modern development paradigms
* Bridges the gap between React’s component model and fine-grained reactivity

## How to Use Signals in React

### 1. Installation

While React Signals are not natively available in React as of now, several libraries provide this functionality. For React applications, use `@preact/signals-react`:

```
npm install @preact/signals-react
```

> **Note**: The original Preact Signals library (`@preact/signals`) works with Preact, while `@preact/signals-react` is specifically adapted for React applications.

### 2. Basic Example: Counter

```
import { signal } from '@preact/signals-react';  
  
const Counter = () => {  
  const count = signal(0); // Create a signal  
  
  return (  
    <div>  
      <h1>Count: {count.value}</h1>  
      <button onClick={() => count.value++}>Increment</button>  
      <button onClick={() => count.value--}>Decrement</button>  
    </div>  
  );  
};  
  
export default Counter;
```

**Explanation**:

* `signal(0)` creates a reactive state container with an initial value of 0
* `count.value` provides the current value of the signal and is automatically updated when the signal changes
* Unlike with useState, we don’t need a separate setter function

### 3. Signal Lifecycle

Signals have their own lifecycle independent of React components:

1. **Creation**: Signals can be created inside or outside components
2. **Subscription**: Components or computed values subscribe to signals when rendering
3. **Update**: Signal updates trigger re-renders in subscribed components only
4. **Disposal**: Signals persist until their last reference is removed

For signals defined inside components, create them conditionally:

```
import React, { useRef } from 'react';  
import { signal } from '@preact/signals-react';  
  
const Component = () => {  
  // Use useRef to ensure the signal is only created once  
  const countSignal = useRef(signal(0)).current;  
    
  return (  
    <div>  
      <p>Count: {countSignal.value}</p>  
      <button onClick={() => countSignal.value++}>Increment</button>  
    </div>  
  );  
};
```

### 4. Reactive Computations

Reactive computations allow derived state to automatically update based on dependencies.

```
import { signal, computed } from '@preact/signals-react';  
  
const App = () => {  
  const count = signal(0);  
  const double = computed(() => count.value * 2); // Reactive computation  
  const isEven = computed(() => count.value % 2 === 0);  
  
  return (  
    <div>  
      <h1>Count: {count.value}</h1>  
      <h2>Double: {double.value}</h2>  
      <p>The number is {isEven.value ? 'even' : 'odd'}</p>  
      <button onClick={() => count.value++}>Increment</button>  
    </div>  
  );  
};  
  
export default App;
```

**Key Points**:

* `computed` creates a reactive value derived from `count.value`
* `double.value` and `isEven.value` automatically update whenever `count.value` changes
* Computed values are cached and only recalculated when dependencies change

### 5. TypeScript Integration

Signals work well with TypeScript, providing type safety for your state:

```
import React from 'react';  
import { signal, computed } from '@preact/signals-react';  
  
interface User {  
  id: number;  
  name: string;  
  email: string;  
}  
  
// Typed signal  
const currentUser = signal<User | null>(null);  
  
// Type inference works with computed values  
const userDisplayName = computed(() => {  
  return currentUser.value ? currentUser.value.name : 'Guest';  
});  
  
// Generic types for arrays  
const userList = signal<User[]>([]);  
  
const UserProfile: React.FC = () => {  
  return (  
    <div>  
      <h1>Welcome, {userDisplayName.value}!</h1>  
      {currentUser.value && (  
        <div>  
          <p>Email: {currentUser.value.email}</p>  
        </div>  
      )}  
      <button onClick={() => {  
        currentUser.value = {  
          id: 1,  
          name: 'John Doe',  
          email: 'john@example.com'  
        };  
      }}>  
        Login  
      </button>  
    </div>  
  );  
};  
  
export default UserProfile;
```

## Global State Management with Signals

### 1. Signals Outside Components

One of the most powerful features of signals is their ability to exist outside of components:

```
// store/userStore.ts  
import { signal, computed } from '@preact/signals-react';  
  
export interface User {  
  id: number;  
  name: string;  
  email: string;  
  role: 'admin' | 'user';  
}  
  
// Global state  
export const currentUser = signal<User | null>(null);  
export const isLoggedIn = computed(() => currentUser.value !== null);  
export const isAdmin = computed(() =>   
  currentUser.value?.role === 'admin'  
);  
  
// Actions  
export const login = (user: User) => {  
  currentUser.value = user;  
  // You could also save to localStorage here  
};  
  
export const logout = () => {  
  currentUser.value = null;  
  // Clear localStorage, etc.  
};
```

Then use it in any component:

```
// components/Header.tsx  
import React from 'react';  
import { currentUser, isLoggedIn, logout } from '../store/userStore';  
  
const Header: React.FC = () => {  
  return (  
    <header>  
      <h1>My App</h1>  
      {isLoggedIn.value ? (  
        <>  
          <span>Welcome, {currentUser.value?.name}</span>  
          <button onClick={logout}>Logout</button>  
        </>  
      ) : (  
        <button onClick={() => { /* open login modal */ }}>  
          Login  
        </button>  
      )}  
    </header>  
  );  
};  
  
export default Header;
```

### 2. Signals with Context API

For cases where you want to provide signals through React’s component tree:

```
// contexts/ThemeContext.tsx  
import React, { createContext, useContext, ReactNode } from 'react';  
import { signal } from '@preact/signals-react';  
  
type Theme = 'light' | 'dark';  
  
const ThemeSignal = signal<Theme>('light');  
  
const ThemeContext = createContext(ThemeSignal);  
  
export const ThemeProvider: React.FC<{ children: ReactNode }> = ({ children }) => {  
  return (  
    <ThemeContext.Provider value={ThemeSignal}>  
      {children}  
    </ThemeContext.Provider>  
  );  
};  
  
// Custom hook for better developer experience  
export const useTheme = () => {  
  const themeSignal = useContext(ThemeContext);  
    
  const toggleTheme = () => {  
    themeSignal.value = themeSignal.value === 'light' ? 'dark' : 'light';  
  };  
    
  return {   
    theme: themeSignal.value,   
    themeSignal, // For direct access if needed  
    toggleTheme   
  };  
};
```

Usage:

```
// components/ThemeToggle.tsx  
import React from 'react';  
import { useTheme } from '../contexts/ThemeContext';  
  
const ThemeToggle: React.FC = () => {  
  const { theme, toggleTheme } = useTheme();  
  
  return (  
    <button onClick={toggleTheme}>  
      Switch to {theme === 'light' ? 'Dark' : 'Light'} Mode  
    </button>  
  );  
};  
  
// App.tsx  
import React from 'react';  
import { ThemeProvider } from './contexts/ThemeContext';  
import ThemeToggle from './components/ThemeToggle';  
  
const App: React.FC = () => (  
  <ThemeProvider>  
    <div>  
      <h1>My App</h1>  
      <ThemeToggle />  
    </div>  
  </ThemeProvider>  
);  
  
export default App;
```

### Advanced Example: Error Handling with Signals

Signals can be used with error boundaries or try-catch blocks for error handling:

```
import React from 'react';  
import { signal, computed } from '@preact/signals-react';  
  
// Error state signal  
const errorSignal = signal<Error | null>(null);  
  
// Async data fetching with error handling  
const userDataSignal = signal<any>(null);  
const isLoadingSignal = signal(false);  
  
const fetchUserData = async (userId: string) => {  
  try {  
    isLoadingSignal.value = true;  
    errorSignal.value = null;  
      
    const response = await fetch(`/api/users/${userId}`);  
      
    if (!response.ok) {  
      throw new Error(`Failed to fetch user: ${response.statusText}`);  
    }  
      
    const data = await response.json();  
    userDataSignal.value = data;  
  } catch (error) {  
    errorSignal.value = error instanceof Error   
      ? error   
      : new Error('Unknown error occurred');  
    userDataSignal.value = null;  
  } finally {  
    isLoadingSignal.value = false;  
  }  
};  
  
// Component using the error signal  
const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {  
  // Trigger fetch on mount or userId change  
  React.useEffect(() => {  
    fetchUserData(userId);  
  }, [userId]);  
    
  if (errorSignal.value) {  
    return (  
      <div className="error-container">  
        <h2>Error Loading User</h2>  
        <p>{errorSignal.value.message}</p>  
        <button onClick={() => fetchUserData(userId)}>Retry</button>  
      </div>  
    );  
  }  
    
  if (isLoadingSignal.value) {  
    return <div>Loading...</div>;  
  }  
    
  if (!userDataSignal.value) {  
    return <div>No user data available</div>;  
  }  
    
  return (  
    <div>  
      <h1>{userDataSignal.value.name}</h1>  
      <p>Email: {userDataSignal.value.email}</p>  
    </div>  
  );  
};
```

## Signal Batching & Optimization

### Understanding Signal Updates

Unlike React’s state updates which are automatically batched, signals update synchronously by default. To optimize performance, you can batch multiple signal updates:

```
import { batch } from '@preact/signals-react';  
  
// Without batching - causes two renders  
const updateUser = (name, email) => {  
  user.value.name = name;  
  user.value.email = email;  
};  
  
// With batching - causes only one render  
const updateUserBatched = (name, email) => {  
  batch(() => {  
    user.value.name = name;  
    user.value.email = email;  
  });  
};
```

## Optimizing Signal Usage

For optimal performance:

1. Keep signal values immutable:

```
// Correct way to update objects and arrays  
tasks.value = [...tasks.value, newTask];  
user.value = { ...user.value, name: 'New Name' };
```

2. Use computed for expensive calculations:

```
// Expensive calculation only runs when dependencies change  
const filteredSortedUsers = computed(() => {  
  console.log('Recomputing filtered and sorted users');  
  return users.value  
    .filter(user => user.name.includes(searchQuery.value))  
    .sort((a, b) => a.name.localeCompare(b.name));  
});
```

## When to Use React Signals 🤔

### Best Use Cases:

1. **Highly Interactive UIs**: Dashboards, real-time applications, or collaborative tools
2. **Granular Updates**: Scenarios where frequent state changes affect only parts of the UI
3. **Global State Without Boilerplate**: Replacing Redux or Context API in simpler scenarios
4. **When Performance is Critical**: Applications that need to minimize render cycles
5. **Derived Values**: When you need computed values based on other state

### When to Avoid:

1. **Small Applications**: Where useState or useReducer are sufficient
2. **Legacy Codebases**: Where integration might be complex
3. **When Ecosystem Support is Critical**: Signals are still evolving in the React ecosystem
4. **Teams New to Reactive Programming**: The learning curve might slow development initially

## Under the Hood

Signals work by leveraging dependency tracking:

1. **Dependency Tracking**: A signal keeps track of every function or component that accesses its value
2. **Subscription Model**: When a component reads a signal’s value, it subscribes to updates
3. **Selective Updates**: When the signal changes, only those dependencies are re-executed or re-rendered
4. **Efficient Updates**: Bypasses React’s virtual DOM diffing in favor of direct updates

This approach differs from React’s reconciliation process, where:

* State updates trigger re-renders of components
* React creates a new virtual DOM tree
* React compares the new and old trees (diffing)
* React updates only the changed DOM nodes

The signal approach is more granular and can be more efficient for many types of applications.

## Conclusion 🎙️

React Signals represent a significant evolution in React state management, bringing fine-grained reactivity to the React ecosystem. While signals may not be the right choice for every application, they offer compelling advantages for complex, interactive UIs where performance and code simplicity are priorities.

> [Buy me a coffee](https://buymeacoffee.com/guestdm)