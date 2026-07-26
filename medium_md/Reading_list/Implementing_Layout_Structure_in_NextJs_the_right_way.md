---
title: "Implementing Layout Structure   in NextJs the right way"
url: https://medium.com/p/746d7e08f2a5
---

# Implementing Layout Structure   in NextJs the right way

[Original](https://medium.com/p/746d7e08f2a5)

# Implementing Layout Structure in NextJs the right way

[![Azhar Zaman](https://miro.medium.com/v2/resize:fill:64:64/1*gR4iNbAJopZC0JZUKiCH4g.png)](/@idrazhar?source=post_page---byline--746d7e08f2a5---------------------------------------)

[Azhar Zaman](/@idrazhar?source=post_page---byline--746d7e08f2a5---------------------------------------)

6 min read

·

Mar 10, 2022

--

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D746d7e08f2a5&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40idrazhar%2Fimplementing-layout-structure-in-nextjs-the-right-way-746d7e08f2a5&source=---header_actions--746d7e08f2a5---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

## Intro & Why Layouts?

React allows us to build a UI into a series of components and subcomponents. Many of these components are often reused between pages. For example, you might have the same *Header and Footer* on every page. One of the main reasons, React.js was adopted like the wind is reusability and components-based architecture. The same thing applies to the Next.js, except for its different implementation to handle pages. When I started coding in NextJs, I really struggled while implementing **Layout based architecture**.

Layouts let you build consistent UI throughout your application, and along with that, you can share generic components like the **Header** component, or the **Footer** component which are often the same on each page.

I read some articles and came to a proper solution for Layout based architecture in simple or even complex Next.js applications.

### Tutorial Outcomes

At the end of the tutorial you will be able to;

* Create a global layout for NextJs pages
* Create multiple dedicated layouts for pages like **GlobalLayout** and **DashboardLayout**.
* You will learn how to fix remount and state persistence issues while implementing Layouts.

## Setting up the NextJs project

Let's create a **new NextJs project** by running CNA(create-next-app) command with the default template, in the terminal(personally prefer **Git Bash**),

```
npx create-next-app <app-name>  
# or  
yarn create next-app
```

Navigate to the project directory,

`cd <app-name>`

Run newly created NextJs application in a development environment,

```
npm run dev  
//or  
npm start
```

You should get directories like this,

```
/<app-name>  
   /pages  
        /_app.js  
        /index.js  
   /public  
   /styles
```

## Adding Necessary Components

Create another file inside the pages directory, named `about.js`, which will be mapped to `/about.js` as About page.

Create another directory inside the root directory as components;

Inside the Components directory create directories named, ***Layout****,* ***Header****, and* ***Footer****,* each with `index.js` file inside it.

The project directory should look like this;

```
/<app-name>  
   /pages  
      /_app.js  
      /index.js  
      /about.js  
   /public  
   /styles  
   /components  
      /Layout  
          /index.js  
      /Header  
          /index.js  
      /Footer  
          /index.js
```

## Adding Content

Now open index.js inside the `/pages` directory, and clean up the mockup code initially created by running the `create-next-app` command. Add the following code instead;

![]()

And inside the about.js page,

Press enter or click to view image in full size

![]()

## Implementing Layout

Now you can see, that Components like the Header, Footer are being shared between both pages. We are going to separate these shared components inside the Layout component, so we do not need to import them on every single page.

Open the `index.js` file inside `Layout` directory and add this code;

Press enter or click to view image in full size

![]()

What are we doing here exactly? Nothing special. We are using the `children` prop provided by reacting, which will let us wrap pages inside Layout. Anything wrapped inside this Layout component will be added to react render tree between `<main>`tag at,

`<main>{children}</main>`

Now let's implement this layout inside our pages, and make the following changes to `index.js` and `about.js`;

Press enter or click to view image in full size

![]()

and,

![]()

Hurrah!, Isn’t it simple. We have successfully implemented Layout architecture inside our NextJs app. But hold on, there is a major drawback in this implementation. **Unnecessary rerender and Remount at every Navigation😒**. Let me explain.

## **Fixing the Remounting and Rerendering issue**

First of all, let me demonstrate what I mean by **unnecessary re-renders and remounting issues.** Let's start a development server, by running

`npm run dev` or `npm start`

If everything was right, you must see this basic page when visiting `localhost:3000`

![]()

Isn’t it ugly 😊, I guessed your answer. Let's give it a bit of shape with Tailwind CSS(really awesome, if haven’t tried it, you should give it a shot).

I have added some styles, and a **useEffect** hook inside the **Header** component to demonstrate to you, what is actually going on. Have a look;

![]()

`useEffect` hook is provided by ReactJs, which pretty much replaces the 3 life cycle methods `(componentDidMount, componentWillUpdate, componentWillUnmout )` of react class-based implementation.

Now our Header component should look like this;

Press enter or click to view image in full size

![]()

### **Testing**

Setup is done, now let's test this out. Open a terminal, and refresh your page. You must see in the terminal;

`Header mounted`

Press enter or click to view image in full size

![]()

Now it's time to navigate to the About page, by clicking About in the Header, you will see that header first unmounts and then re-mounts again.

![]()

Is this okay? You guessed it right. When navigating between pages, we want to ***persist* page state** (input values, scroll position, etc.) for a **Single-Page Application (SPA) experience**. But in our case, this is doing nothing, just separating the shared components.

## **Okay! Fix time**

NextJs comes with the solution itself, by providing us with getLayout method. We need to refactor this code a bit, and we are good to go.

When using Next.js we often need to override the global `App` component to get access to some features like *persisting state*, or *global layouts*. This can be done by creating a file`_app.js` directly in the `/pages/` folder. If this file exists, then Next.js will use this instead of the default App.

Time to mess with `_app.js` file;

Press enter or click to view image in full size

![]()

What are we exactly doing here, we are telling NextJs to use Layout as specified at the page level, while preserving the memory(state, scroll position, etc.). When navigating between pages, we want to *persist* page state (input values, scroll position, etc.) for a Single-Page Application (SPA) experience.

This layout pattern enables state persistence because the React component tree is maintained between page transitions. With the component tree, React can understand which elements have changed to preserve the state.

## Refactoring Page Layouts

Let's refactor code inside pages, `index.js` and `about.js.`

Move the Layout from the component return state to `Component.getLayout` method as;

Press enter or click to view image in full size

![]()

and,

![]()

### Testing

Let's test it again. clear console and refresh again. You must see a message `Header mounted` in the console, now try to navigate to the About page, and Boom 😍.

You see that no more remounting, state loss. We together have just implemented a proper Layout architecture in NextJs.

## Conclusion

You can easily add **multiple layouts inside your NextJs** app, like **Dashboard Layout**, etc. You just need to create a Layout, and add common components, like a *Sidebar, Dashboard Header, and Dashboard Footer* in case of Dashboard Layout. And the next step would be to wrap `pages` inside this layout.

**Simple isn’t it.**

Hopefully, you got some value from this article, in case you have any queries please let me know in the comment section.

**Thanks a lot. I am** [**Azhar Zaman**](https://www.azharzaman.com) **and I will see you in another amazing tutorial like this.**

**Till then be safe and try to keep others safe.**