---
title: "Top 30 Most Complicated Interview Questions on React"
url: https://medium.com/p/5715830f0c7e
---

# Top 30 Most Complicated Interview Questions on React

[Original](https://medium.com/p/5715830f0c7e)

# Top 30 Most Complicated Interview Questions on React

[![Coding Guy](https://miro.medium.com/v2/resize:fill:64:64/1*3XynojYxXKRvCO4a2NdpRg.jpeg)](/@codingguy?source=post_page---byline--5715830f0c7e---------------------------------------)

[Coding Guy](/@codingguy?source=post_page---byline--5715830f0c7e---------------------------------------)

10 min read

·

Aug 19, 2024

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

React is a popular JavaScript library for building user interfaces, especially single-page applications. Mastering React can be challenging, especially when faced with complex interview questions that test both fundamental concepts and advanced techniques. This article presents 30 of the most complicated and innovative React interview questions, complete with code examples and explanations.

*Disclaimer: gpt4 helped me in writing this article*

## 1. Understanding Virtual DOM

**Question**: What is the Virtual DOM, and how does it improve performance in React?

**Answer**: The Virtual DOM is an in-memory representation of the real DOM elements. React updates the Virtual DOM first, calculates the difference (diffing), and then updates the real DOM with minimal changes, improving performance.

```
// Example of a Virtual DOM diffing process  
function render(element, container) {  
    const prevVirtualDOM = container.__virtualDOM;  
    const nextVirtualDOM = element;  
if (prevVirtualDOM) {  
        // Perform diffing and update the real DOM  
        updateDOM(container, prevVirtualDOM, nextVirtualDOM);  
    } else {  
        // Initial render  
        mountElement(nextVirtualDOM, container);  
    }  
    container.__virtualDOM = nextVirtualDOM;  
}
```

## 2. Hooks: useState and useEffect

**Question**: How do `useState` and `useEffect` hooks work? Provide an example of a component that fetches data from an API.

**Answer**: `useState` allows you to add state to functional components, and `useEffect` performs side effects like data fetching, subscriptions, or manually changing the DOM.

```
import React, { useState, useEffect } from 'react';  
function DataFetchingComponent() {  
    const [data, setData] = useState(null);  
    useEffect(() => {  
        fetch('https://api.example.com/data')  
            .then(response => response.json())  
            .then(data => setData(data));  
    }, []); // Empty dependency array means this effect runs once on mount  
    if (!data) return <div>Loading...</div>;  
    return <div>{JSON.stringify(data)}</div>;  
}
```

## 3. Context API for State Management

**Question**: Explain how the Context API works in React and provide an example of sharing state across multiple components.

**Answer**: The Context API allows you to pass data through the component tree without having to pass props down manually at every level.

```
import React, { createContext, useState, useContext } from 'react';  
const MyContext = createContext();  
function ParentComponent() {  
    const [value, setValue] = useState('Hello, World!');  
    return (  
        <MyContext.Provider value={{ value, setValue }}>  
            <ChildComponent />  
        </MyContext.Provider>  
    );  
}  
function ChildComponent() {  
    const { value } = useContext(MyContext);  
    return <div>{value}</div>;  
}
```

## 4. Custom Hooks

**Question**: What are custom hooks in React? Create a custom hook to handle form inputs.

**Answer**: Custom hooks are JavaScript functions that start with “use” and can call other hooks. They encapsulate logic that can be reused across components.

```
import { useState } from 'react';  
function useFormInput(initialValue) {  
    const [value, setValue] = useState(initialValue);  
    function handleChange(event) {  
        setValue(event.target.value);  
    }  
    return {  
        value,  
        onChange: handleChange,  
    };  
}  
// Usage in a component  
function MyForm() {  
    const name = useFormInput('');  
    return (  
        <form>  
            <input type="text" {...name} />  
        </form>  
    );  
}
```

## 5. React Fiber

**Question**: What is React Fiber, and how does it enhance React’s rendering process?

**Answer**: React Fiber is a re-implementation of the React core algorithm for reconciliation, improving the ability to split rendering work into units and manage work prioritization for smooth user interactions.

## 6. Handling Performance with `React.memo`

**Question**: How does `React.memo` help in optimizing performance? Provide an example.

**Answer**: `React.memo` is a higher-order component that memoizes the result of a component render. It only re-renders the component if its props change.

```
const MyComponent = React.memo(function({ name }) {  
    console.log('Rendering MyComponent');  
    return <div>Hello, {name}</div>;  
});
```

## 7. Error Boundaries

**Question**: What are Error Boundaries in React, and how do you use them?

**Answer**: Error boundaries are components that catch JavaScript errors in their child component tree, log them, and display a fallback UI.

```
class ErrorBoundary extends React.Component {  
    constructor(props) {  
        super(props);  
        this.state = { hasError: false };  
    }  
static getDerivedStateFromError() {  
        return { hasError: true };  
    }  
    componentDidCatch(error, errorInfo) {  
        console.log(error, errorInfo);  
    }  
    render() {  
        if (this.state.hasError) {  
            return <h1>Something went wrong.</h1>;  
        }  
        return this.props.children;  
    }  
}  
function MyComponent() {  
    throw new Error('Test Error');  
}  
function App() {  
    return (  
        <ErrorBoundary>  
            <MyComponent />  
        </ErrorBoundary>  
    );  
}
```

## 8. Server-Side Rendering (SSR) with React

**Question**: How does server-side rendering (SSR) work in React? Provide an example using `Next.js`.

**Answer**: SSR in React involves rendering components on the server and sending the HTML to the client. This improves performance and SEO.

```
// In a Next.js page component  
export async function getServerSideProps() {  
    // Fetch data here  
    return { props: { data: 'Hello from SSR' } };  
}  
function MyPage({ data }) {  
    return <div>{data}</div>;  
}  
export default MyPage;
```

## 9. React Portals

**Question**: What are React Portals and how do you use them?

**Answer**: React Portals allow you to render components outside the current component hierarchy, useful for modals and tooltips.

```
import ReactDOM from 'react-dom';  
function Modal({ children }) {  
    return ReactDOM.createPortal(  
        <div className="modal">{children}</div>,  
        document.getElementById('modal-root')  
    );  
}  
function App() {  
    return (  
        <div>  
            <Modal>  
                <h1>Hello from Modal</h1>  
            </Modal>  
        </div>  
    );  
}
```

## 10. Higher-Order Components (HOC)

**Question**: What is a Higher-Order Component in React? Provide an example of an HOC that adds logging functionality.

**Answer**: A Higher-Order Component is a function that takes a component and returns a new component with additional props or logic.

```
function withLogging(WrappedComponent) {  
    return function(props) {  
        console.log('Rendering component:', WrappedComponent.name);  
        return <WrappedComponent {...props} />;  
    };  
}  
const MyComponent = withLogging(function({ name }) {  
    return <div>Hello, {name}</div>;  
});
```

## 11. Understanding Refs and `useRef`

**Question**: How do you use `refs` and the `useRef` hook in React? Provide an example.

**Answer**: Refs allow you to directly access and manipulate DOM elements or React components.

```
import React, { useRef } from 'react';  
function FocusInput() {  
    const inputRef = useRef(null);  
    function focusInput() {  
        inputRef.current.focus();  
    }  
    return (  
        <div>  
            <input ref={inputRef} type="text" />  
            <button onClick={focusInput}>Focus Input</button>  
        </div>  
    );  
}
```

## 12. Lazy Loading with `React.lazy` and `Suspense`

**Question**: How do you implement lazy loading in React using `React.lazy` and `Suspense`?

**Answer**: `React.lazy` and `Suspense` allow components to be loaded lazily, improving performance by splitting the bundle.

```
import React, { Suspense } from 'react';  
const LazyComponent = React.lazy(() => import('./LazyComponent'));  
function App() {  
    return (  
        <div>  
            <Suspense fallback={<div>Loading...</div>}>  
                <LazyComponent />  
            </Suspense>  
        </div>  
    );  
}
```

## 13. Optimizing React Apps with `useCallback` and `useMemo`

**Question**: How do `useCallback` and `useMemo` hooks optimize React apps? Provide examples.

**Answer**: `useCallback` memoizes functions, and `useMemo` memoizes computed values to prevent unnecessary re-renders.

```
import React, { useCallback, useMemo, useState } from 'react';  
function ExpensiveCalculation({ num }) {  
    const result = useMemo(() => {  
        console.log('Calculating...');  
        return num * 2;  
    }, [num]);  
    return <div>Result: {result}</div>;  
}  
function App() {  
    const [count, setCount] = useState(0);  
    const increment = useCallback(() => {  
        setCount(prevCount => prevCount + 1);  
    }, []);  
    return (  
        <div>  
            <ExpensiveCalculation num={count} />  
            <button onClick={increment}>Increment</button>  
        </div>  
    );  
}
```

## 14. React Router for Navigation

**Question**: How do you handle navigation in a React application using `React Router`?

**Answer**: `React Router` is a library that provides declarative routing for React applications.

```
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';  
function Home() {  
    return <h1>Home</h1>;  
}  
function About() {  
    return <h1>About</h1>;  
}  
function App() {  
    return (  
        <Router>  
            <nav>  
                <Link to="/">Home</Link>  
                <Link to="/about">About</Link>  
            </nav>  
            <Switch>  
                <Route exact path="/" component={Home} />  
                <Route path="/about" component={About} />  
            </Switch>  
        </Router>  
    );  
}
```

## 15. Component Lifecycle Methods

**Question**: What are the lifecycle methods in class components, and how do they map to hooks in functional components?

**Answer**: Lifecycle methods in class components include `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount`. These map to `useEffect` in functional components.

```
class MyComponent extends React.Component {  
    componentDidMount() {  
        console.log('Component mounted');  
    }  
componentDidUpdate() {  
        console.log('Component updated');  
    }  
    componentWillUnmount() {  
        console.log('Component will unmount');  
    }  
    render() {  
        return <div>Hello</div>;  
    }  
}  
// Equivalent in a functional component  
import React, { useEffect } from 'react';  
function MyComponent() {  
    useEffect(() => {  
        console.log('Component mounted');  
        return () => {  
            console.log('Component will unmount');  
        };  
    }, []);  
    return <div>Hello</div>;  
}
```

## 16. Implementing Controlled and Uncontrolled Components

**Question**: What are controlled and uncontrolled components in React? Provide examples of each.

**Answer**: Controlled components have their state controlled by React, while uncontrolled components manage their own state via the DOM.

```
function ControlledComponent() {  
    const [value, setValue] = useState('');  
return (  
        <input  
            type="text"  
            value={value}  
            onChange={(e) => setValue(e.target.value)}  
        />  
    );  
}  
function UncontrolledComponent() {  
    const inputRef = useRef(null);  
    function handleSubmit() {  
        alert(inputRef.current.value);  
    }  
    return (  
        <div>  
            <input type="text" ref={inputRef} />  
            <button onClick={handleSubmit}>Submit</button>  
        </div>  
    );  
}
```

## 17. React with TypeScript

**Question**: How do you integrate TypeScript with React, and what are the benefits?

**Answer**: TypeScript adds static typing to JavaScript, providing better tooling and reducing runtime errors in React applications.

```
import React, { FC } from 'react';  
interface MyComponentProps {  
    name: string;  
}  
const MyComponent: FC<MyComponentProps> = ({ name }) => {  
    return <div>Hello, {name}</div>;  
};  
export default MyComponent;
```

## 18. Using Redux for State Management

**Question**: How does Redux manage state in a React application? Provide an example of a simple counter.

**Answer**: Redux is a state management library that centralizes application state, making it predictable and easier to debug.

```
import { createStore } from 'redux';  
import { Provider, useDispatch, useSelector } from 'react-redux';  
function counterReducer(state = 0, action) {  
    switch (action.type) {  
        case 'increment':  
            return state + 1;  
        case 'decrement':  
            return state - 1;  
        default:  
            return state;  
    }  
}  
const store = createStore(counterReducer);  
function Counter() {  
    const dispatch = useDispatch();  
    const count = useSelector(state => state);  
    return (  
        <div>  
            <button onClick={() => dispatch({ type: 'decrement' })}>-</button>  
            <span>{count}</span>  
            <button onClick={() => dispatch({ type: 'increment' })}>+</button>  
        </div>  
    );  
}  
function App() {  
    return (  
        <Provider store={store}>  
            <Counter />  
        </Provider>  
    );  
}
```

## 19. React and GraphQL

**Question**: How do you integrate GraphQL with React? Provide an example using `Apollo Client`.

**Answer**: Apollo Client is a popular library for integrating GraphQL with React, allowing you to query data in a declarative way.

```
import React from 'react';  
import { ApolloProvider, ApolloClient, InMemoryCache, useQuery, gql } from '@apollo/client';  
const client = new ApolloClient({  
    uri: 'https://api.spacex.land/graphql/',  
    cache: new InMemoryCache(),  
});  
const GET_LAUNCHES = gql`  
    query GetLaunches {  
        launchesPast(limit: 5) {  
            mission_name  
        }  
    }  
`;  
function Launches() {  
    const { loading, error, data } = useQuery(GET_LAUNCHES);  
    if (loading) return <p>Loading...</p>;  
    if (error) return <p>Error :(</p>;  
    return data.launchesPast.map(({ mission_name }) => <div key={mission_name}>{mission_name}</div>);  
}  
function App() {  
    return (  
        <ApolloProvider client={client}>  
            <Launches />  
        </ApolloProvider>  
    );  
}
```

## 20. React Testing with Jest and React Testing Library

**Question**: How do you test React components using Jest and React Testing Library?

**Answer**: Jest is a testing framework, and React Testing Library provides utilities for testing React components by interacting with the DOM.

```
import { render, screen } from '@testing-library/react';  
import '@testing-library/jest-dom/extend-expect';  
import MyComponent from './MyComponent';  
test('renders hello world text', () => {  
    render(<MyComponent />);  
    expect(screen.getByText(/hello world/i)).toBeInTheDocument();  
});
```

## 21. Component Composition

**Question**: What is component composition in React, and how does it differ from inheritance?

**Answer**: Component composition is the process of combining simple components to build complex UIs. It leverages props and children to pass data and elements between components.

```
function Card({ title, children }) {  
    return (  
        <div className="card">  
            <h1>{title}</h1>  
            <div>{children}</div>  
        </div>  
    );  
}  
function App() {  
    return (  
        <Card title="My Card">  
            <p>This is the card content.</p>  
        </Card>  
    );  
}
```

## 22. Handling Forms in React

**Question**: How do you handle forms in React, including validation?

**Answer**: Forms in React are typically handled using controlled components. Validation can be added using functions or third-party libraries like Formik or React Hook Form.

```
import React, { useState } from 'react';  
function MyForm() {  
    const [name, setName] = useState('');  
    const [error, setError] = useState('');  
    const handleSubmit = (e) => {  
        e.preventDefault();  
        if (name.trim() === '') {  
            setError('Name is required');  
        } else {  
            setError('');  
            alert(`Hello, ${name}`);  
        }  
    };  
    return (  
        <form onSubmit={handleSubmit}>  
            <input  
                type="text"  
                value={name}  
                onChange={(e) => setName(e.target.value)}  
            />  
            {error && <p>{error}</p>}  
            <button type="submit">Submit</button>  
        </form>  
    );  
}
```

## 23. React with Web Components

**Question**: How do you integrate Web Components with React?

**Answer**: React can render Web Components just like any other component. However, you may need to handle custom events manually.

```
function MyWebComponentWrapper() {  
    const ref = useRef(null);  
useEffect(() => {  
        const handleCustomEvent = (e) => console.log(e.detail);  
        ref.current.addEventListener('custom-event', handleCustomEvent);  
        return () => ref.current.removeEventListener('custom-event', handleCustomEvent);  
    }, []);  
    return <my-web-component ref={ref}></my-web-component>;  
}
```

## 24. React and CSS-in-JS

**Question**: How do you use CSS-in-JS libraries like `styled-components` or `emotion` with React?

**Answer**: CSS-in-JS allows you to write CSS directly in your JavaScript, enabling scoped and dynamic styling.

```
import styled from 'styled-components';  
const Button = styled.button`  
    background: palevioletred;  
    color: white;  
    font-size: 1em;  
    padding: 0.25em 1em;  
    border: 2px solid palevioletred;  
    border-radius: 3px;  
`;  
function App() {  
    return <Button>Click me</Button>;  
}
```

## 25. Managing Side Effects with Redux Middleware

**Question**: How do you handle side effects like asynchronous actions in Redux using middleware?

**Answer**: Redux middleware like `redux-thunk` or `redux-saga` allows you to handle side effects and asynchronous actions.

```
import { createStore, applyMiddleware } from 'redux';  
import thunk from 'redux-thunk';  
function counterReducer(state = 0, action) {  
    switch (action.type) {  
        case 'increment':  
            return state + 1;  
        default:  
            return state;  
    }  
}  
function incrementAsync() {  
    return (dispatch) => {  
        setTimeout(() => {  
            dispatch({ type: 'increment' });  
        }, 1000);  
    };  
}  
const store = createStore(counterReducer, applyMiddleware(thunk));  
store.dispatch(incrementAsync());
```

## 26. React with Progressive Web Apps (PWAs)

**Question**: How do you create a Progressive Web App (PWA) with React?

**Answer**: A PWA can be created with React by ensuring it is fast, reliable, and installable. `create-react-app` provides built-in support for PWAs.

```
// In service-worker.js  
self.addEventListener('install', (event) => {  
    console.log('Service worker installed');  
});  
self.addEventListener('fetch', (event) => {  
    event.respondWith(  
        caches.match(event.request).then((response) => {  
            return response || fetch(event.request);  
        })  
    );  
});
```

## 27. SSR vs CSR

**Question**: Compare Server-Side Rendering (SSR) and Client-Side Rendering (CSR) in React.

**Answer**: SSR renders pages on the server before sending them to the client, improving load times and SEO. CSR renders pages entirely in the browser, offering a more dynamic user experience.

## 28. State Management with Recoil

**Question**: What is Recoil, and how does it differ from other state management solutions in React?

**Answer**: Recoil is a state management library that provides a more granular and scalable approach, allowing for atoms (pieces of state) and selectors (derived state) to be used.

```
import { atom, selector, useRecoilState, useRecoilValue } from 'recoil';  
const textState = atom({  
    key: 'textState',  
    default: '',  
});  
const charCountState = selector({  
    key: 'charCountState',  
    get: ({ get }) => {  
        const text = get(textState);  
        return text.length;  
    },  
});  
function CharacterCounter() {  
    const [text, setText] = useRecoilState(textState);  
    const count = useRecoilValue(charCountState);  
    return (  
        <div>  
            <input type="text" value={text} onChange={(e) => setText(e.target.value)} />  
            <p>Character Count: {count}</p>  
        </div>  
    );  
}
```

## 29. React and Micro-Frontends

**Question**: How do you implement micro-frontends with React?

**Answer**: Micro-frontends allow you to build a large application by composing multiple smaller apps. Each can be developed independently and then integrated into a single UI.

## 30. Accessibility in React

**Question**: How do you ensure accessibility (a11y) in React applications?

**Answer**: Ensuring accessibility involves using semantic HTML, ARIA attributes, and following best practices for keyboard navigation and screen reader compatibility.

```
function AccessibleButton({ label }) {  
    return (  
        <button aria-label={label}>  
            <span aria-hidden="true">🔍</span>  
            {label}  
        </button>  
    );  
}
```

## Conclusion

These 30 React interview questions cover a wide range of topics, from fundamental concepts like the Virtual DOM and state management to advanced topics like server-side rendering, error boundaries, and performance optimization. Mastering these questions will prepare you for React interviews and deepen your understanding of this powerful JavaScript library, making you a more effective React developer.

*disclaimer- gpt4 helped me writing this article*

Thanks for reading  
cheers 🥃🥃