---
title: "Implementing Micro Frontends with Next.js: A Real-World Experience"
url: https://medium.com/p/6a83bfcd1dbc
---

# Implementing Micro Frontends with Next.js: A Real-World Experience

[Original](https://medium.com/p/6a83bfcd1dbc)

# Implementing Micro Frontends with Next.js: A Real-World Experience

[![Mindfire Solutions](https://miro.medium.com/v2/resize:fill:64:64/1*g7P1YOYp4q1ozuimdznvhw.jpeg)](/@mindfiresolutions.software?source=post_page---byline--6a83bfcd1dbc---------------------------------------)

[Mindfire Solutions](/@mindfiresolutions.software?source=post_page---byline--6a83bfcd1dbc---------------------------------------)

4 min read

·

Jan 14, 2025

--

4

Listen

Share

More

Micro Frontends are increasingly being adopted to enable scalable and flexible frontend development in large applications. Recently, our team integrated Micro Frontends into a project using Next.js and **next-module-federation-mf**. With over 18 developers working on the UI, breaking down our application into Micro Frontends made collaboration easier, but we encountered some unique challenges along the way.

This post will walk you through the challenges, solutions, and the advantages we found in adopting this architecture with Next.js, along with example code to demonstrate key setup steps.

## Our Setup: Next.js and Module Federation

We used Next.js as our main framework with **@module-federation/nextjs-mf** to handle Module Federation. Our application was split into **13 Micro Frontends**, with each section represented by an isolated Next.js project.

Each micro frontend was exposed as a federated module and imported dynamically where needed. Here’s how we set up imports, exposes, and shared modules in our configuration.

## Setting Up Module Federation in Next.js

To get started, you need to configure module federation in your next.config.js file.

## 1. Installing Dependencies

First, install the required module federation plugin:

**npm install @module-federation/nextjs-mf**

## 2. Setting Up the next.config.js File

In each micro frontend, configure the next.config.js with @module-federation/nextjs-mf as follows:

Here’s what each option means:

Press enter or click to view image in full size

![]()

* **name**: The unique identifier for each Micro Frontend. For example, app1 in this case.
* **exposes**: Specifies which modules in this project will be exposed. For example, ComponentA is exposed and can be used in other applications.
* **remotes**: Defines other federated modules (Micro Frontends) that this application can import. For instance, app2 is available at http://localhost:3001.
* **shared**: Specifies shared dependencies between micro frontends, ensuring only a single instance of react and react-dom is used across applications.

## 3. Importing Federated Modules Dynamically

In the host app or another micro frontend, you can use next/dynamic to import and render the exposed modules dynamically. Here’s an example:

Press enter or click to view image in full size

![]()

In this example, ComponentA from app1 is dynamically imported in the host application. Setting ssr: false prevents server-side rendering, ensuring the federated component loads only on the client side.

## 4. Sharing Common Modules (Like Axios)

In our case, certain libraries like Axios and custom hooks didn’t work seamlessly with shared modules, so we had to isolate them in each micro frontend or manage versioning closely. Here’s how you can configure shared modules:

Press enter or click to view image in full size

![]()

Using **singleton** ensures only one instance of the library is loaded, but in some cases, isolated instances might work better to avoid version conflicts.

## Challenges We Faced

## 1. Plugin Limitations with Next.js:

Micro Frontends are new, especially for server-rendered frameworks like Next.js. We had to forcefully use the **page router** as @module-federation/nextjs-mf does not support the **app router**. This impacted our project structure, and we had to adjust routing patterns accordingly.

## 2. Increased Build Size and Memory Usage:

Having 13 Micro Frontends increased our total build size, causing memory issues during builds. We tackled the **“Node max space exceeded”** error by configuring Node’s memory limit:

**NODE\_OPTIONS=”–max-old-space-size=2048″**

## 3. Deployment Complexity

Each micro frontend was hosted on a separate VM, adding significant infrastructure costs. For large applications, this separation can quickly become expensive.

## Advantages of Micro Frontends in Our Project

Despite the challenges, adopting Micro Frontends provided significant benefits:

* **Reduced Merge Conflicts**:  
  With 18 developers, Micro Frontends allowed teams to work on isolated parts, reducing merge conflicts.
* **Increased Development Speed**:  
  Each team could work independently, making development faster and more efficient.
* **Simplified Deployments**:  
  We could deploy updates for individual micro frontends rather than redeploying the entire application.

## Which Tool is Best for Micro Frontends with Next.js?

Each bundler has its strengths:

* **Webpack**: Recommended for Next.js Micro Frontends. Webpack’s Module Federation is currently the most reliable solution for federated modules in Next.js.
* **Vite**: Best suited for purely client-rendered Micro Frontends with frameworks like React, Vue, and Angular. Vite’s faster builds make it ideal, though it lacks server-rendered support for Next.js.
* **Parcel**: Offers a simpler setup, though it’s limited in flexibility and advanced configurations compared to Webpack.

## Conclusion

Using Micro Frontends with Next.js helped us scale development and reduce conflicts, but the journey came with hurdles, especially around plugins, build sizes, and deployment costs. For large, complex applications where team autonomy and modularity are key, Micro Frontends can be a powerful architecture choice, though it’s essential to be prepared for its unique challenges, especially with server-rendered frameworks like Next.js.

Looking to build dynamic, scalable, and high-performance applications? Mindfire Solutions offers top-notch [JavaScript development services](https://www.mindfiresolutions.com/custom-software-development/javascript/) tailored to your unique business needs. Whether it’s implementing cutting-edge frameworks like Next.js or adopting innovative architectures like Micro Frontends, our team delivers seamless, future-ready solutions to help you stay ahead in the digital landscape.

Originally Posted on: <https://www.mindfiresolutions.com/blog/2024/12/implementing-micro-frontends-with-next-js/>