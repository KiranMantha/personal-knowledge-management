---
title: "Decoupling UI and Logic in React: A Clean Code Approach with Headless Components"
url: https://medium.com/p/82e46b5820c
---

# Decoupling UI and Logic in React: A Clean Code Approach with Headless Components

[Original](https://medium.com/p/82e46b5820c)

# Decoupling UI and Logic in React: A Clean Code Approach with Headless Components

[![Juntao Qiu](https://miro.medium.com/v2/resize:fill:64:64/1*kLYYTxfVSAYAXxyfMrqYKA.png)](https://juntao-qiu.medium.com/?source=post_page---byline--82e46b5820c---------------------------------------)

[Juntao Qiu](https://juntao-qiu.medium.com/?source=post_page---byline--82e46b5820c---------------------------------------)

8 min read

·

Jul 6, 2023

--

11

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D82e46b5820c&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fdecoupling-ui-and-logic-in-react-a-clean-code-approach-with-headless-components-82e46b5820c&source=---header_actions--82e46b5820c---------------------post_audio_button------------------)

Share

In the realm of front-end development, terms and paradigms can sometimes be mystifying, and ‘headless UI’ or ‘headless components’ may very well belong to this category. If you’re scratching your head wondering what these mean, you’re not alone. In fact, despite the confusing moniker, these concepts are compelling strategies that can significantly simplify the management of complex user interfaces.

*Update 10 Nov 2023: I’ve published a long-form article on Martin Fowler’s blog (*[*https://martinfowler.com/articles/headless-component.html*](https://martinfowler.com/articles/headless-component.html)*). If you enjoy the more extended version, that article should be a good fit.*

Headless components may seem esoteric, but their true power lies in their flexibility, reusability potential, and ability to improve your codebase’s organization and cleanliness. In this article, we will demystify this pattern, shedding light on what exactly it is, why it’s beneficial, and how it can revolutionize your approach to interface design.

To illustrate, we will begin by exploring a simple yet effective application of headless components: extracting a ‘useToggle’ hook from two similar components to reduce code duplication. While this example may seem trivial, it paves the way for understanding the core principles of headless components. By recognizing common patterns and extracting them into reusable parts, we can streamline our codebase and pave the way for a more efficient development process.

But that’s only the tip of the iceberg! As we delve deeper, we will encounter a more complex instance of this principle in action: leveraging Downshift, a powerful library for creating enhanced input components.

By the end of this article, I hope to offer you not just an understanding of headless components but also the confidence to integrate this powerful pattern into your own projects. So, let’s shed the confusion and embrace the transformative potential of headless components.

## A Toggle component

Toggles form an integral part of numerous applications. They’re the silent workers behind functions like “remember me on this device”, “activate notifications”, or the ever-popular “dark mode”.

Press enter or click to view image in full size

![]()

Creating such a toggle in React is a surprisingly straightforward process. Let’s delve into how we can build one.

```
const ToggleButton = () => {  
  const [isToggled, setIsToggled] = useState(false);  
  
  const toggle = useCallback(() => {  
    setIsToggled((prevState) => !prevState);  
  }, []);  
  
  return (  
    <div className="toggleContainer">  
      <p>Do not disturb</p>  
      <button onClick={toggle} className={isToggled ? "on" : "off"}>  
        {isToggled ? "ON" : "OFF"}  
      </button>  
    </div>  
  );  
};
```

The `useState` hook sets up a state variable `isToggled` with initial value `false`. The function `toggle`, created with `useCallback`, toggles the `isToggled` value between `true` and `false` each time it's called (on button click). The button's appearance and text ("ON" or "OFF") dynamically reflect the `isToggled` state.

Let’s say now we need to build another, totally different component ExpandableSection, it will show or hide the detailed information of a Section. There is a button aside of the heading, and you can click to expand or collapse the details.

Press enter or click to view image in full size

![]()

The implementation is not too hard either, you can easily do that like so:

```
const ExpandableSection = ({ title, children }: ExpandableSectionType) => {  
  const [isOpen, setIsOpen] = useState(false);  
  
  const toggleOpen = useCallback(() => {  
    setIsOpen((prevState) => !prevState);  
  }, []);  
  
  return (  
    <div>  
      <h2 onClick={toggleOpen}>{title}</h2>  
      {isOpen && <div>{children}</div>}  
    </div>  
  );  
};
```

There’s an evident similarity here — the ‘on’ and ‘off’ states in `ToggleButton` bear resemblance to the 'expand' and 'collapse' actions in `ExpandableSection`. Recognizing this commonality, we can abstract this shared functionality into a separate function. In the React ecosystem, we do this through the creation of a custom hook.

```
const useToggle = (init = false) => {  
  const [state, setState] = useState(init);  
    
  const toggle = useCallback(() => {  
    setState((prevState) => !prevState);  
  }, []);  
  
  return [state, toggle];  
};
```

The refactor might seem fairly simple, but it highlights an important concept: separating behaviour from presentation. In this scenario, our custom hook serves as a state machine independent of JSX. Both `ToggleButton` and `ExpandableSection` leverage this same underlying logic.

Anyone who’s spent a reasonable amount of time on mid-scale frontend projects would recognize that the majority of updates or bugs aren’t related to the UI visuals but rather to managing the UI’s state — in essence, its logic. Hooks offer a potent tool for centralizing these logical aspects, making them easier to scrutinize, optimize, and maintain.

## The headless component

There are actually many great libraries already using this pattern to separate behaviour (or state management) and presentation. And among these component libraries, the most famous one should be [Downshift](https://www.downshift-js.com/).

Downshift applies the concept of headless components, which are components that manage behaviour and state without rendering any UI. They provide a state and a set of actions in their render prop function, allowing you to connect it to your UI. This way, Downshift allows you to control your UI while it takes care of the complex state and accessibility management.

For instance, I want to build a dropdown list, obviously I need list data, a trigger and a few customisations around how I like to highlight a selected item, how many lines should be rendered. But I don’t want to build the accessibility all from scratch because there are many edge cases to consider, including cross-browser and cross-device adoptions.

Press enter or click to view image in full size

![]()

So with a few lines of JSX, I can easily make a fully accessible select with Downshift:

```
const StateSelect = () => {  
  const {  
    isOpen,  
    selectedItem,  
    getToggleButtonProps,  
    getLabelProps,  
    getMenuProps,  
    highlightedIndex,  
    getItemProps,  
  } = useSelect({items: states});  
  
  return (  
    <div>  
      <label {...getLabelProps()}>Issued State:</label>  
      <div {...getToggleButtonProps()} className="trigger" >  
        {selectedItem ?? 'Select a state'}  
      </div>  
      <ul {...getMenuProps()} className="menu">  
        {isOpen &&  
          states.map((item, index) => (  
            <li  
              style={  
                highlightedIndex === index ? {backgroundColor: '#bde4ff'} : {}  
              }  
              key={`${item}${index}`}  
              {...getItemProps({item, index})}  
            >  
              {item}  
            </li>  
          ))}  
      </ul>  
    </div>  
  )  
}
```

This component is a state selector using Downshift’s `useSelect` hook. It allows users to select a state from a dropdown menu.

* `useSelect` manages the state and interactions for a select input.
* `isOpen`, `selectedItem`, and `highlightedIndex` are state variables controlled by `useSelect`.
* `getToggleButtonProps`, `getLabelProps`, `getMenuProps`, and `getItemProps` are functions to provide necessary props to the corresponding elements.
* `isOpen` determines if the dropdown is open.
* `selectedItem` holds the value of the currently selected state.
* `highlightedIndex` indicates which list item is currently highlighted.
* If the dropdown is open, `states.map` generates an unordered list of selectable states.
* The spread (`...`) operator is used to pass props from Downshift's hooks to the components. This includes things like click handlers, keyboard navigation, and ARIA properties.
* If a state is selected, it will display as the button content. Otherwise, it displays ‘Select a state’.

This approach gives you complete control over the rendering, so you can style your components to fit your application’s look and feel, and apply custom behavior if necessary. It’s also great for sharing behaviour logic across different components or projects.

There are a few more headless component libraries already following this pattern:

* [Reakit](https://reakit.io/): It provides a set of headless components for building accessible high-level UI libraries, toolkits, design systems, etc.
* [React Table](https://tanstack.com/table/v8): It’s a headless utility meant to be composed. It’s Hooks-based and allows you to build all sorts of tables.
* [react-use](https://github.com/streamich/react-use): It’s a collection of Hooks that includes several headless components.

**To learn more about writing maintainable React code, I’ve created** [**a book for it**](https://leanpub.com/react-clean-code) **on leanpub. You can get a copy with** [**this link for 30% off**](https://leanpub.com/react-clean-code/c/mYXp686cMFw1)**.**

## Dive a bit deep

When we continue to separate logic from the UI in a deliberate manner, we gradually create a layered structure. This structure is not a traditional layered architecture that spans the entire application, but rather it’s specific to the UI part of an application.

Press enter or click to view image in full size

![]()

In this arrangement, JSX (or most tags) is defined at the highest layer, which is solely responsible for displaying the properties that have been passed in. Right below it, there’s what we call a ‘headless component’. This component maintains all behaviours, manages states, and provides an interface for JSX to interact with. At the base of this structure, we have data models that encapsulate domain-specific logic. These models aren’t concerned with the UI or states. Instead, they focus on data management and business logic. This layered approach offers a neat separation of concerns, enhancing our code's clarity and maintainability.

## A balanced view

Like any other type of technique, Headless UI has pros and cons you should be aware of before adopting it. Let’s discuss the benefits of Headless UI first:

1. **Reusability**: The primary advantage of headless components is their reusability. By encapsulating logic into standalone components, you can reuse these components across multiple UI elements. This not only reduces code duplication but also fosters consistency across your application.
2. **Separation of Concerns**: Headless components clearly separate logic and presentation. This makes your codebase more manageable and easier to understand, particularly for larger teams with split duties.
3. **Flexibility**: Since headless components do not dictate the presentation, they allow for greater flexibility in design. You can customize the UI as much as you want without affecting the underlying logic.
4. **Testability**: Because logic is separate from presentation, writing unit tests for your business logic is easier.

And on the other hand, it’s typically a bit more complicated than an all-in-one component, so use it wisely with the following considerations:

1. **Initial Overhead**: For simpler applications or components, creating headless components might seem like overengineering, leading to unnecessary complexity.
2. **Learning Curve**: Developers unfamiliar with the concept might find it challenging to understand at first, leading to a steeper learning curve.
3. **Possibility of Overuse**: It’s easy to get carried away and try to make every component headless, even when unnecessary, leading to an overcomplicated codebase.
4. **Potential Performance Issues**: Although generally not a significant concern, if not handled carefully, re-rendering multiple components using shared logic could lead to performance issues.

Remember, headless UI isn’t a one-size-fits-all solution like any architectural pattern. The decision to use it should be based on your project's specific needs and complexity.

## Further readings

* [Headless User Interface Components](https://www.merrickchristensen.com/articles/headless-user-interface-components/)
* [Headless UI](https://tanstack.com/table/v8/docs/guide/introduction)
* [Modularizing React Applications with Established UI Patterns](https://martinfowler.com/articles/modularizing-react-apps.html)

## Summary

In this article, we delved into the world of Headless User Interfaces, an empowering approach to tackling complex UI tasks. We explored how separating behaviour from rendering allows us to create more maintainable and reusable code, reducing redundancy and potential bugs. We first illustrated this through a simple example by creating a custom React hook, `useToggle`, and showing its application in two separate components. Then, we extended this concept to a more complex scenario with Downshift, an excellent library that facilitates building enhanced input components. By gaining a deeper understanding of the 'headless' approach, we hope you can leverage this pattern to create more scalable and maintainable UIs in your future projects.

**If you like the reading, please** [**Sign up for my mailing list**](https://juntao.substack.com/)**. I share Clean Code and Refactoring techniques weekly via** [**blogs**](https://juntao-qiu.medium.com/)**,** [**books**](https://leanpub.com/u/juntao) **and** [**videos**](https://www.youtube.com/@icodeit.juntao)**.**

[## The Pragmatic Developer | Juntao Qiu | Substack

### "The Pragmatic Developer" is a bi-weekly newsletter dedicated to helping developers write clean, maintainable code…

juntao.substack.com](https://juntao.substack.com/?source=post_page-----82e46b5820c---------------------------------------)