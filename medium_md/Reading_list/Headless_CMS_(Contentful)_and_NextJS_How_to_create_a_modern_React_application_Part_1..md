---
title: "Headless CMS (Contentful) and NextJS: How to create a modern React application? Part 1."
url: https://medium.com/p/fdd772073a5d
---

# Headless CMS (Contentful) and NextJS: How to create a modern React application? Part 1.

[Original](https://medium.com/p/fdd772073a5d)

# Headless CMS (Contentful) and NextJS: How to create a modern React application? Part 1.

[![FocusReactive](https://miro.medium.com/v2/resize:fill:64:64/2*UeSzg0kJlGka3IxlyvgYEg.jpeg)](/@FocusReactive?source=post_page---byline--fdd772073a5d---------------------------------------)

[FocusReactive](/@FocusReactive?source=post_page---byline--fdd772073a5d---------------------------------------)

9 min read

·

Nov 20, 2019

--

Listen

Share

More

A few months ago, a client reached out to FocusReactive, asking to provide them with a convenient way of updating the content on their marketing website. At that moment their website was a **NextJS application**, and all of the information, displayed on the pages **was hardcoded into React components**. Obviously, we needed:

a) **separate** the information and implementation of the web application;

b) provide a convenient **instrument** for storing and editing content.

It was necessary to choose an appropriate tool for working with content, which would be easy for **people without development experience**. It was also important to separate the processes of app development and content update since different departments were responsible for these. As a result of a discussion with the client, it was decided to transfer the content to Headless CMS, to be specific **we chose Contentful as the most stable and popular system** at that moment.

![]()

Contentful — Modern headless CMS promoting API-first and cloud-native approaches

![]()

NextJS — Modern React-based framework with Server Side Rendering and file system based router out of the box.

We want to share and discuss ideas for organizing the structure of a React application using Headless CMS. Additionally to this post we have created the minimalistic [complementary NextJS application](https://github.com/UsulPro/contentful-post-demo-app) which demonstrate approaches we have developed at FocusReactive.

Let`s outline what we are going to discuss in this and the following parts.

* Creating of **scalable Content Model** and connecting it with your application
* How to develop and scale your application within the **limitation of the chosen Contentful payment plan**
* Empower Contentful with **Next.js Dynamic Routing** introduced in the v9.0 of the framework.
* Full pages management with an external server for **creating arbitrary URLs** only via Contentful
* Setup advanced DX with **mocking content** locally
* **Testing** Contentful connected React components and Next.js pages with Jest
* Advanced DX: **Using Storybook** for creating Contentful Content Types in isolation
* Advanced UX: Custom **component editor**

## What is Headless CMS?

Among various Backend as a Service solution, Headless CMS occupies a special market niche and it has gained a lot of popularity among developers. In comparison to “traditional” CMS, such as Wordpress or Joomla, they focus exclusively on content hosting, tools for convenient content editing and providing an API for accessing content from the application. This empowers developers and designers with complete freedom of implementation of a business logic and application appearance.

## The specifics of Contentful pricing plans

The content model in Contentful, which describes your application data, includes entries, assets, and references. Entries should belong to one of Content Types. While creating Content Model you’re adding new Content Types that describes what fields your entries should have. Later, when creating a specific element, you will have to choose which exact type you want to create.Your main task as a developer when working with Contentful is to add a new Content Type while you are developing the application.

> Regardless of what payment plan you’ve chosen, you will be limited in the number of available Content Types.

When choosing a payment plan you can see the number of available content types. For example, the first free plan has 24 content types.

Press enter or click to view image in full size

![]()

*Choosing a payment plan to create your space*

I would like to draw your attention to the following detail. Regardless of what payment plan you’ve chosen, **you will be limited in the number of available Content Types**. Cheaper payment plans offer Content Types, while the most expansive plans can double that number.

This plays an important role in all of the subsequent conclusions. Creating a Content Model we will have to stay within that limitation. If your application is not very large or generally contains uniform pages (for example, if you are creating a blog), then you are lucky and you can feel free to use up the types, creating your model. But what should you do, if you assume that **you might need more types**?

We, at Focus Reactive, found a solution that allows **developing scalable content models, avoiding the limitation** on available types. Further in this article, we will assume that the application we develop can contain a considerably greater number of pages, component types, and templates in comparison to what was set by the limitations of the payment plan.

## Building a hierarchical content model

In order to describe the structure of our application, we have to build the content model. Note that Contentful does not provide any sort of hierarchy for the created Content Types. All the types are organized as a flat list and they are represented in the Content Model tab. This gives us a lot of **flexibility in building our model**. We can implement whatever organization structure of content types. The connections between content types are assigned with the help of fields that have a reference type, allowing to refer to one or a few Entries. You can assign as many fields as possible for an element of a specific type. Taking into consideration the described content type limitations, let’s establish a **hierarchical structure of the application content model** that has the following three levels of components:

- page

- template

- component

We’ll also be using components like config in order to modify the behavior of the available types and to store general information about the application. The references to files stored in CMS will be added to our components. These files can be considered as an additional hierarchical level of a lower rank.

Press enter or click to view image in full size

![]()

*Levels and components of the content model*

The following flowchart shows the **hierarchical levels** in the form of big colored blocks, and there are also examples of Content Types, which can be located at these levels. There is only one type, located at the highest level, which describes the page. The arrows are the references, which are possible between components. In fact, the components of the higher level can refer to any levels that are located below. For example, a page component may have a `background` field for an explicit reference to a file with an image. Component types, outlined in the flowchart, are given as an example and for an understanding of the structure. Some of them are specific types, and others imply a whole category of types. As we progress, we will become more familiar with the types of components and their role.

It is convenient to set aside one **universal data type for page description** and place all the general settings here. Even if you are planning to have pages of different types and purposes, think about what they might have in common and keep it here. This will simplify the support of this type in application. It is better to identify things that are different from each other in the types of the next hierarchical level. Suppose all pages controlled through CMS will have a header with a heading and a background picture. Besides, we need to set the page URL and meta-tags for search engines. Then, Page might contain the following fields:

A convenient feature of Contentful is field validation. Let’s take advantage of it in order to set some important limitations, which will save us some time later. It’s useful to assign **unique** and **required** to url, and also to agree on whether or not you will have slashes at the beginning and at the end of a line.

Press enter or click to view image in full size

![]()

*URL Validation*

We will insert a link to the page template in the Template field. This field is required and can only take on certain types.

Press enter or click to view image in full size

![]()

*Template Configuration*

Why do **we need templates** and why are there a few different types of them? Technically, it depends on the scale of your project, your abilities to group different pages according to their appearance and function, and it also depends on how much of your data you would like to control through CMS. All these parameters may vary widely depending on your needs; however, we always have the limitation on the number of types (24 or 48 Content Types), and we have to look for solutions to combine a wide range of data into common patterns. I would like to discuss the **main ideas that can help** you with this.

The templates are grouped into a separate hierarchical level in our structure because they define the page appearance as a whole. If **components represent separate fragments of user interface**, then a **template defines where the components are located** on the page, how they interact with each other, and which components can be present. You can use templates that are composed entirely of components, defined by us in the Content Model, but there might be situations when template implementation will contain a large amount of custom code, and we will **store it as JSON**. In the worst-case scenario, a template might not contain any data at all that we would like to see and edit in CMS. However, even this option makes sense only when we want to manage the pages dynamically through CMS. In this article, we will take a look at how to create templates that combine standard CMS components and custom code.

## Organizing page layout via standard template

Let’s start from the simplest case when a page can be easily decomposed into separate independent components. For these cases, we will use the Standard template and the main Content field, which will simply contain a list of the used components.

Press enter or click to view image in full size

![]()

*The first template type — standard template*

Suppose, we want to create a page whose UI consists of alternating blocks with motivating text and quotes from happy product users. A template of Standard type is what we need for a page like this. Besides the template itself, we will also need two types of components: Description and Quote. Each component can have a wide range of options. Depending on the needs, we can change the background color, use various text styles, add buttons. Contentful even lets you insert images into Rich Text and display them in our applications. For example, our page should have approximately the following layout.

Press enter or click to view image in full size

![]()

*An example of a template layout*

Such template can cover needs of a lot of pages and give us flexibility of combining various types of components. How to implement this in the app code? We will consider it in the [second part](/@FocusReactive/headless-cms-contentful-and-nextjs-how-to-create-a-modern-react-application-part-2-3c51fb238064) of this series.

## 4 tips that will make creating NextJS + Contentful App easier

* Collaborate with a designer while creating your content model. Together, you will quickly figure out the right approach for building pages from components and you will be able to highlight the properties that have to be transferred to CMS. Collaborating with a designer will help you to develop a design system that you will implement in your content model.
* Tell the people who will be working with content about the limitations set by any CMS. For example, if your content manager or designer is used to controlling every element on the page, then here, they will need to think in terms of composing larger blocks.
* Do not trust the data that comes from CMS. Especially, if you are using JSON fields. Wrap the code that works with content into `try - catch` and use `error boundaries` in React components.
* Do not mix content and markup. If you need to store the formatted text, it’s better to switch to markdown right away.

This was the first part in a series of “How to create a modern React application?”. In the [second part](/@FocusReactive/headless-cms-contentful-and-nextjs-how-to-create-a-modern-react-application-part-2-3c51fb238064) we will dive deeper into the code and implement templates and components in our [NextJs Application](https://github.com/UsulPro/contentful-post-demo-app)

Written by [**Oleg Proskurin**](https://twitter.com/UsulPro)

Senior Software Engineer @ [FocusReactive](https://focusreactive.com/)