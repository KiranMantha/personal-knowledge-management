---
title: "5 React Component Patterns That Make Your Code Reusable"
url: https://medium.com/p/8e23374eff20
---

# 5 React Component Patterns That Make Your Code Reusable

[Original](https://medium.com/p/8e23374eff20)

Member-only story

# 5 React Component Patterns That Make Your Code Reusable

## Stop copying components. Start composing systems. These 5 patterns changed how I write React.

[![Loshan Paul](https://miro.medium.com/v2/resize:fill:64:64/1*elwrf9MQs8jneV4_B10lGA.png)](https://medium.com/@thanuyanloshan?source=post_page---byline--8e23374eff20---------------------------------------)

[Loshan Paul](https://medium.com/@thanuyanloshan?source=post_page---byline--8e23374eff20---------------------------------------)

4 min read

·

Jan 17, 2026

--

Listen

Share

More

Press enter or click to view image in full size

![]()

I still remember the moment I realized my React codebase was lying to me.

Everything *worked*.

The UI shipped.

The sprint closed.

But opening a file felt like déjà vu.

Same props.

Same logic.

Same components… slightly renamed.

`UserCard`, `ProfileCard`, `AuthorCard` all cousins.

All fragile.

All screaming the same thing:

> *“You don’t actually understand reuse yet.”*

That realization hurt.

But it also fixed how I write React forever.

This article isn’t theory.

It’s the five component patterns I actually use after building, breaking, and refactoring real React apps.

Patterns that reduce duplication, improve readability, and make your components feel intentional instead of accidental.

Let’s get into it.

### 1. The Container / Presentational Pattern (Yes, It Still Matters)

People love to say this pattern is “old.”

That’s usually said by people who’ve never maintained a large app.

The idea is simple:

* **Container** → owns data, state, side effects
* **Presentational** → pure UI, zero business logic

### Why it works in the real world

Because logic changes more often than layout.

Because designers tweak UI while APIs stay the same.

Because tests become trivial.

### Example

```
// UserContainer.jsx  
function UserContainer() {  
const { data, isLoading } = useUser();  
  
  
if (isLoading) return <Spinner />;  
  
  
return <UserView user={data} />;  
}  
  
  
// UserView.jsx  
function UserView({ user }) {  
return (  
<div>  
<h2>{user.name}</h2>  
<p>{user.email}</p>  
</div>  
);  
}
```

### Reality check

If your UI component has `useEffect`, API calls, and conditional fetching logic it’s not reusable.

It’s married.

This pattern gives you a clean divorce.

### 2. The Compound Components Pattern (Your API Should Feel Like HTML)

If you’ve ever used `<select>` with `<option>`, you’ve already felt this pattern.

Compound components let consumers control structure *without* prop drilling hell.

### Example

```
<Tabs>  
<Tabs.List>  
<Tabs.Trigger>Profile</Tabs.Trigger>  
<Tabs.Trigger>Settings</Tabs.Trigger>  
</Tabs.List>  
  
  
<Tabs.Panel>Profile content</Tabs.Panel>  
<Tabs.Panel>Settings content</Tabs.Panel>  
</Tabs>
```

### Why this is powerful

* No giant prop APIs
* No boolean soup (`isActive`, `isOpen`, `isSelected`)
* Components feel *designed*, not hacked together

Under the hood, this uses React context.

Simple.

Effective.

### Reality

If your component has more than **8–10 props**, stop.

You’re designing a configuration file, not a component.

Compound components fix that.

### 3. The Controlled vs Uncontrolled Pattern (Give Control, Don’t Steal It)

Reusable components must work in *both* modes.

* Controlled → parent owns the state
* Uncontrolled → component manages itself

If your component only supports one, it’s selfish.

### Example

```
function Toggle({ value, defaultValue = false, onChange }) {  
const [internal, setInternal] = useState(defaultValue);  
const isControlled = value !== undefined;  
  
  
const state = isControlled ? value : internal;  
  
  
const toggle = () => {  
const next = !state;  
if (!isControlled) setInternal(next);  
onChange?.(next);  
};  
  
  
return <button onClick={toggle}>{state ? 'ON' : 'OFF'}</button>;  
}
```

### Why this matters

Because *you* don’t know how this component will be used six months from now.

Libraries like Radix and React Aria rely heavily on this pattern for a reason.

### Reality check

If your component forces state ownership on the parent *or* hides it completely, it’s not reusable it’s opinionated in the wrong way.

### 4. The Render Props Pattern (When Composition Beats Abstraction)

Hooks replaced a lot of render props.

Not all of them.

Render props still shine when you want **maximum flexibility** with **shared logic**.

### Example

```
<DataFetcher url="/users">  
{({ data, isLoading, error }) => {  
if (isLoading) return <Spinner />;  
if (error) return <Error />;  
  
  
return <UserList users={data} />;  
}}  
</DataFetcher>
```

### Why it still works

* Consumers control rendering
* Logic stays centralized
* Zero assumptions about UI

### Reality check

If your abstraction starts dictating markup, you’ve gone too far.

Render props pull you back.

### 5. The Slot / Children as API Pattern (The Most Underrated One)

This is the pattern I reach for the most and see used the least.

Instead of props like `headerText`, `footerButton`, `iconLeft`…

Just accept **children**.

### Example

```
<Card>  
<Card.Header>  
<h3>Invoice</h3>  
</Card.Header>  
  
  
<Card.Body>  
<p>$1,200 due</p>  
</Card.Body>  
  
  
<Card.Footer>  
<Button>Pay now</Button>  
</Card.Footer>  
</Card>
```

### Why this scales

* No prop explosion
* Natural composition
* UI stays flexible

### Reality check

If you keep adding props because “someone might need it later”… you’re already late.

Slots let consumers decide without bloating your API.

### Final Thoughts (The Hard Truth)

Reusable components are **designed**, not extracted.

Copy paste reuse is a code smell.

If your components:

* Know too much
* Do too much
* Accept too many props

They’re not reusable.

They’re just lucky.

The patterns above forced me to think like a system designer, not a JSX typist.

And once that clicked, my React codebases got smaller, calmer, and easier to reason about.

> If this made you rethink how you write components clap.
>
> If you disagree with one of these patterns comment.

I want the debate.

And if you know a teammate who keeps copying components instead of composing them… share this with them (lovingly).

Save it. You’ll need it during your next refactor.