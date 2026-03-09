---
title: "Micro-Frontend using Web Components"
url: https://medium.com/p/e9faacfc101b
---

# Micro-Frontend using Web Components

[Original](https://medium.com/p/e9faacfc101b)

# Micro-Frontend using Web Components

[![Anjali Verma](https://miro.medium.com/v2/resize:fill:64:64/1*ZQbIeJamTa822ZNe4z0HNw.jpeg)](/@anjaliverma471?source=post_page---byline--e9faacfc101b---------------------------------------)

[Anjali Verma](/@anjaliverma471?source=post_page---byline--e9faacfc101b---------------------------------------)

7 min read

·

Jun 28, 2020

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

> *Good frontend architecture is hard. Scaling frontend development so that many teams can work simultaneously on a large and complex product is even harder. In this article, we’ll talk about a recent trend of breaking up frontend monoliths into many smaller, more manageable components using* ***Web Components.***

### First of all, what is Micro Frontend?

**Micro Frontend** is a micro service approach to front end web development. The concept of **Micro Frontend** is to think about a web application as a **composition of features** owned by different **independent teams**. Each team has a **distinct area of business** or **mission** it cares about and specialises in. A team is **cross functional** and develops its features **end-to-end.**

Press enter or click to view image in full size

![]()

We’ve established a good micro service architecture for our backends. It’s time to apply the same principles to our front ends. A lot of firms are moving towards micro frontend from classic monolith architecture like Google, Amazon, Salesforce, Zalando, ThoughtWorks etc.

Press enter or click to view image in full size

![]()

There are various implementations for micro frontend approach. But, in this article, we’d be talking about micro frontend implementation using Web Components only.

### What are Web Components?

In modern web development, everyone is using components to encapsulate UI functionalities. Web components are low-level browser API that helps us to extend the browser with new components, they provide us a standard interface for defining new components. Web components have a standard way of creating components that use HTML and DOM API that every other front end framework uses and a common way of receiving and sending data using props and events.

> Web component simply tells the browser WHEN and WHERE to create a component, not HOW to create a component.

Web Components comprises of 3 concepts:

1. **Custom Elements:** Set of JavaScript APIs that allow you to create your own HTML elements and define the way they behave.
2. **Shadow DOM: A p**rivate DOM that is scoped to your component only and capable of isolating CSS and JavaScript.
3. **HTML templates.** New HTML tags that allows us to create templates for your components.

In simpler terms, you can create your own HTML selector, like <select>, <h1> etc.

Press enter or click to view image in full size

![]()

*EVERYONE is using Web components, according to Google, 5% of page loads today, use Web components.*

### What’s driving this adoption?

As a developer, we have full freedom to use the stack to create our own components and still maintain interoperability. That’s the key difference between web components and proprietary component libraries.

Once you have invested your time in creating a web component, they can be used widely in a more diverse range of applications because they work anywhere the web works.

### Custom Elements

The Custom Elements specification lays the foundation for designing and using new types of DOM elements. Autonomous custom elements are new HTML tags, defined entirely by you. They have none of the semantics of existing HTML elements, so all the behaviour needs to be defined by you.

You can define your own custom element by using:

Custom Elements follow a lifecycle to mount and unmount the component on the DOM. To learn more about custom elements and shadow DOM in depth, refer [*WebComponents*.](https://www.webcomponents.org/introduction)

Till here, I hope you got a basic understanding of micro frontends and web components. Let’s dive into the implementation part, and build something cool using *Web Components* and *Custom HTML Elements.*

## Implementation

For demonstrating the use of web components and its compatibility with different frameworks I have built an application that fetches Github statistics of a user.

Press enter or click to view image in full size

![]()

This Application has one parent component developed in Angular which includes the search bar and the two child components, the profile section and statistics section are developed using Angular and React respectively.

*All the components follow material design pattern thus ensuring consistent styling*. For communication between the parent component, we need to pass Github username typed in the search bar and maintain the global state of the entire application. Child components have their own isolated states.

**Steps to create React Web Component:**

1. We will start by creating the custom element class and by defining it in the [CustomElementRegistry](/@gilfink/understanding-the-customelementregistry-object-74408a25a3d4), here we’ve registered our component having ‘react-el’ selector. The customElements global is used for defining a custom element and teaching the browser about a new tag. Use *CustomElements.define()* with the tag name you want to create and a JavaScript class that extends the base HTMLElement.
2. To establish the communication between child component and parent component, we will observe the attributes passed to our React component so that we can re-render our component once the attributes change.
3. In the connectedCallBack function, we will mount and render our React component. It is invoked each time the custom element is appended into the DOM. In our case, we’ll be rendering the Graphs component that we’ve created in React by passing the global attributes while calling *React.render()* method. Graph component has its own isolated state, no relation with other components.
4. Last step is to unmount the React component and unsubscribe the observer. The disconnectedCallback() callback logs simple messages to the console to inform us when the element is either removed from the DOM, or moved to a different page.

**Now you can just include *<react-el>* selector to your parent apps.**

### Building Angular Web Component

Unlike the defined way of extending to HTMLElement in any JavaScript library, Angular provides the support to create custom elements using *Angular* *Elements*.

> **Angular Elements** are Angular components packaged as custom elements (also called Web Components), a web standard for defining new HTML elements in a framework-agnostic way.

**Steps to create Angular Web Component:**

1. To convert and existing app to custom element we need to import *createCustomElement()* function from ‘@angular/elements’

*npm i @angular/elements — save*

2. Change package.json to build Angular project and serve the project as custom elements:

3. Instead of loading AppComponent on bootstrap, we are going to wrap into a custom element. Move it to the *entryPoint* list for dynamic loading of the component. Although this step can be skipped if root micro component is the AppComponent. You can read more about entry component vs bootstrap here: <https://angular.io/guide/entry-components>

Angular provides the createCustomElement() function for converting an Angular component, together with its dependencies, to a custom element. The function collects the component’s observable properties, along with the Angular functionality the browser needs to create and destroy instances, and to detect and respond to changes.

The conversion process implements the NgElementConstructor interface, and creates a constructor class that is configured to produce a self-bootstrapping instance of your component.

Use a JavaScript function, customElements.define(), to register the configured constructor and its associated custom-element tag with the browser’s CustomElementRegistry. When the browser encounters the tag for the registered element, it uses the constructor to create a custom element instance.

**Now you can just include *<ng-profile>* selector to your parent apps.**

### Building the Parent App and integrating the Micro components

1. In the parent Angular app to use the web components defined, we need to add CUSTOM\_ELEMENTS\_SCHEMA to the module.
2. We now just need to import the built .js served by the micro components into the parent app and create the elements in parent app with the tag name defined. We include the url for served .js file in parent app’s index.html. In addition to these zone.js and custom-element-es5-adapter.js needs to be included for the web components to work
3. The parent app will add the child component to the DOM when username is entered by the user. Then child component will check for attribute change by the parent app which is used as communication mechanism.
4. The Angular component will fetch data and update the component once username attribute is set. Similarly React component uses mutation observer api to handle fetch data and update the micro component.

## Deployment

Now let’s talk about how to deploy these separate web components to efficiently utilise the concept of micro frontends.

I used *AWS Elastic Beanstalk* service to deploy graphs component and used *S3* to deploy my profile component statically on AWS using Github Actions to have a separate CI/CD pipeline for each component. I did this just to ensure and prove the point that I’m trying to make in this article is that we can have isolated teams working on different components irrespective of their deployment architecture.

Github workflow files and Elastic Beanstalk config files can be found in the repository.

*Having said all of the above things, I strongly believe that micro frontend is the approach for large teams only, and this approach is still under consideration by a lot of companies. Try and figure out if this is the architecture your team needs.*

Finally, we come to an end of this article, hope you got a bit inspired to move your monolith architecture to micro frontend.

[Demo of the application](http://microgithubdashboard-env.eba-x5bzpamu.ap-south-1.elasticbeanstalk.com/)

The complete code for this sample can be found here:

[## anjy-07/micro-frontend

### Contribute to anjy-07/micro-frontend development by creating an account on GitHub.

github.com](https://github.com/anjy-07/micro-frontend?source=post_page-----e9faacfc101b---------------------------------------)