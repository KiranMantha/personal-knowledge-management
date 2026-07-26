---
title: "7 React Patterns Senior Devs Use That Juniors Have Never Heard Of"
url: https://medium.com/p/d1c65ea09a48
---

# 7 React Patterns Senior Devs Use That Juniors Have Never Heard Of

[Original](https://medium.com/p/d1c65ea09a48)

Press enter or click to view image in full size

![]()

# **7 React Patterns Senior Devs Use That Juniors Have Never Heard Of**

## *After 4 years of React in production, these are the patterns that separate the developers who write maintainable code from the ones who create technical debt.*

[![Ajay singh Bisht](https://miro.medium.com/v2/resize:fill:64:64/1*Ibslxg_J9KWd35FMTSqaoA@2x.jpeg)](/@ajaybisht-dev?source=post_page---byline--d1c65ea09a48---------------------------------------)

[Ajay singh Bisht](/@ajaybisht-dev?source=post_page---byline--d1c65ea09a48---------------------------------------)

5 min read

·

Apr 28, 2026

--

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd1c65ea09a48&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fworks-on-my-machine%2F7-react-patterns-senior-devs-use-that-juniors-have-never-heard-of-d1c65ea09a48&source=---header_actions--d1c65ea09a48---------------------post_audio_button------------------)

Share

I have reviewed hundreds of React pull requests over the past four years. Junior developers write code that works. Senior developers write code that works, scales, and is easy to delete. The difference usually comes down to a handful of patterns that are never taught in tutorials but are used constantly in production codebases.

Here are the seven patterns I use every day — and why they matter.

**Pattern 1: The Compound Component Pattern**

Most developers build components with a long list of props to control every aspect of behavior. Senior devs instead use compound components — a parent that shares state with its children through React Context, letting the consumer control the layout themselves.

Instead of this:

```
<Select options={items} onSelect={fn} placeholder="Choose" searchable={true} />  
Seniors build this:  
<Select onSelect={fn}>  
<Select.Trigger placeholder="Choose" />  
<Select.SearchBox />  
<Select.Options items={items} />  
</Select>
```

**WHY THIS MATTERS** This pattern gives consumers full control over layout and composition without adding dozens of props to one component. Libraries like Headless UI and Radix UI are built entirely on this principle.

**Pattern 2: Custom Hooks as Service Layers**

Juniors call APIs directly inside components with useEffect. This mixes data fetching, error handling, and UI rendering all in one place — a nightmare to test or reuse.

Seniors extract all data logic into custom hooks that return a clean interface:

```
function useTasks() {  
const [tasks, setTasks] = useState([]);  
const [loading, setLoading] = useState(true);  
const [error, setError] = useState(null);  
const addTask = async (task) => { /* … */ };  
const deleteTask = async (id) => { /* … */ };  
return { tasks, loading, error, addTask, deleteTask };  
}
```

Now the component only cares about display. The hook handles everything else. Swapping the API for a mock in tests takes one line.

**WHY THIS MATTERS** A component that imports a custom hook is easy to test. A component with raw fetch calls in useEffect is not.

**Pattern 3: State Colocation**

Beginners lift all state to the top of the component tree — Redux or a root useState for everything. This causes unnecessary re-renders across the entire app.

Seniors keep state as close to where it is used as possible. If only a modal component needs a piece of state, that state lives inside the modal. It never goes into a global store unless multiple unrelated components need it.

The rule: start local, only promote state when you actually need to share it. Most state in real apps never needs to leave its component.

**WHY THIS MATTERS** Global state is a convenience that becomes a performance problem at scale. Colocated state is a discipline that prevents 90% of re-render issues before they start.

**Pattern 4: The Render Props Pattern for Logic Sharing**

When you need to share stateful logic while giving the consumer full control over what gets rendered, render props are more powerful than hooks alone.

```
function MouseTracker({ render }) {  
const [position, setPosition] = useState({ x: 0, y: 0 });  
return (  
<div onMouseMove={e => setPosition({ x: e.clientX, y: e.clientY })}>  
{render(position)}  
</div>  
);  
}
```

The consumer decides what to show — a tooltip, a canvas cursor, a debug overlay. The tracking logic is shared without imposing any UI.

**Pattern 5: Controlled vs Uncontrolled — Knowing When to Choose**

Most junior devs default to controlled components (value + onChange for everything). Most senior devs know that uncontrolled components with useRef are significantly faster for forms that do not need real-time validation.

Use controlled inputs when: you need real-time feedback, dependent fields, or instant validation. Use uncontrolled inputs when: you just need the values on submit and do not care what happens between keystrokes. The difference in re-render count in a large form is enormous.

**WHY THIS MATTERS** React Hook Form is built on uncontrolled inputs. That is why it is dramatically faster than Formik for large forms.

**Pattern 6: Error Boundaries as First-Class Citizens**

Most developers treat error boundaries as an afterthought — one catch-all at the root of the app. Senior developers place error boundaries strategically around every major feature boundary so that one broken widget does not crash the entire page.

```
class TaskListErrorBoundary extends React.Component {  
state = { hasError: false };  
static getDerivedStateFromError() { return { hasError: true }; }  
render() {  
if (this.state.hasError) return <TaskListFallback />;  
return this.props.children;  
}  
}
```

Wrap your TaskList, your Chart, your PaymentForm — each gets its own boundary with a meaningful fallback. Users see a degraded experience instead of a blank screen.

**WHY THIS MATTERS** In production, a React app with proper error boundaries feels ten times more reliable than one without, even if the underlying bug rate is identical.

**Pattern 7: Memoization — But Only Where It Costs**

Juniors either never memoize (everything re-renders) or memoize everything (React.memo, useMemo, useCallback on every function). Both are wrong.

Seniors measure first, then memoize. The React DevTools Profiler shows you exactly which components are re-rendering and why. The real rule:

• Use React.memo only on components that render often with the same props

• Use useMemo only for genuinely expensive calculations (think: filtering thousands of items)

• Use useCallback only when passing callbacks to memoized child components

Wrapping a simple string operation in useMemo is not optimization — it is overhead. Profile before you optimize.

**WHY THIS MATTERS** Premature memoization adds complexity without benefit. Measure your render times in the Profiler, find the actual bottleneck, then apply the right tool.

## Summary

These seven patterns are not advanced theory. They are practical decisions senior developers make every day to keep codebases maintainable, performant, and testable. The gap between junior and senior React work is usually not about knowing more APIs — it is about knowing when and why to apply patterns like these.

Start with compound components and custom hooks. They will change how you think about component design immediately.

**Follow ajaybisht-dev on Medium**

I publish React, .NET, and AI content for developers twice a week. If this helped you, clap up to 50 times — it genuinely helps more developers find this article.