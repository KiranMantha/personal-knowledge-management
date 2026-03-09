---
title: "Things only senior React engineers know"
url: https://medium.com/p/618d81154cb6
---

# Things only senior React engineers know

[Original](https://medium.com/p/618d81154cb6)

Member-only story

# Things only senior React engineers know

[![Emmanuel Meric de Bellefon](https://miro.medium.com/v2/resize:fill:64:64/1*DK59Qt7UJWuZBb-5-06GDg.png)](/@meric.emmanuel?source=post_page---byline--618d81154cb6---------------------------------------)

[Emmanuel Meric de Bellefon](/@meric.emmanuel?source=post_page---byline--618d81154cb6---------------------------------------)

3 min read

·

Nov 15, 2024

--

21

Listen

Share

More

Press enter or click to view image in full size

![]()

React can be tricky for beginners. However, understanding a few underlying principles or tricks can make becoming a senior React engineer easier.

### **1. The useEffect clean-up callback executes on every render**

Most people think it executes only when the component unmounts, but that’s not true.

On every render, **the clean-up callback from the previous render executes just before the next effect execution**.

Let’s see an example:

```
function SomeComponent() {  
  const [count, setCount] = useState(0)  
  
  useEffect(() => {  
    console.log('The current count is ', count)  
    return () => {  
      console.log('The previous count is ', count)  
    }  
  })  
  
  return <button onClick={() => setCount(count + 1)}>Click me</button>  
}
```

This logs the following:

```
// Component mounts  
The current count is 0  
  
// Click  
The previous count is 0  
The current count is 1  
  
// Click  
The previous count is 1  
The current count is 2  
  
// Component unmounts  
The previous count is 2
```

This is useful for creating “unsubscribe then immediately subscribe” patterns, which is the only thing useEffect should be used for.

Of course, if we add a dependency array these things are called only when a dependency changes.

### 2. useEffect is a low-level utility that should be used only in library-like code

It’s common for junior React developers to use useEffect when they don’t need to. This can make code more complex, create flickers, or subtle bugs.

The most common case is to synchronize different useStates, where you actually need one single useState:

```
function MyComponent() {  
  const [text, setText] = useState("Lorem ipsum dolor sit amet")  
  
  // You don't need to do this !!!  
  const [trimmedText, setTrimmedText] = useState("Lorem ip...")  
  
  useEffect(() => {  
    setTrimmedText(text.slice(0, 8) + '...')  
  }, [text])  
}  
  
  
function MyBetterComponent() {  
  const [text, setText] = useState("Lorem ipsum dolor sit amet")  
  
  // Do this instead:  
  // (each time text changes, the component will re-render so trimmedText  
  //  will be up-to-date)  
  const trimmedText = text.slice(0, 8) + '...'  
}
```

### 3. Use the key prop to reset internal state

When the `key` prop changes on an element, the render of this element is not interpreted as an update, but as an unmount plus a mount of a brand new component instance with a fresh state.

```
function Layout({ currentItem }) {  
  /* When currentItem changes, we want any useState inside <EditForm/>  
     to be reset to a new initial value corresponding to the new item */  
  return (  
    <EditForm  
      item={currentItem}  
      key={currentItem.id}  
    />  
  )  
}
```

### **4. Don’t put server state inside a useState**

Server state is more or less a snapshot of your database that lives in-memory in your front end while the page is loaded.

Typically it is managed by a server state manager, like react-query or Apollo.

If you put any of it inside a useState, when the query is refreshed, or there is a mutation, the content of your useState won’t be updated.

### 5. ReactElement vs ReactNode

`ReactElement` represents only a **piece of markup** while `ReactNode` can be **anything that React can render** like `ReactElement` but also `string`, `number`, `boolean`, `array`, `null`, `undefined`, etc.

```
// this is a ReactElement  
const a = <div/>  
  
// these are ReactNodes  
1  
"hello"  
<div/>  
[2, <span/>]  
null
```

Always type the `children` prop as `ReactNode` is you don’t want to constrain what children can be put for that component.

`JSX.Element` is an internal Typescript feature (not defined by the React library) that targets only library developers. Other than that it’s equivalent to `ReactElement`.