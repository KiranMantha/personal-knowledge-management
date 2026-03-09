---
title: "Mapping content types to React components: How to create a modern React application? Part 2."
url: https://medium.com/p/3c51fb238064
---

# Mapping content types to React components: How to create a modern React application? Part 2.

[Original](https://medium.com/p/3c51fb238064)

# Mapping content types to React components: How to create a modern React application? Part 2.

[![FocusReactive](https://miro.medium.com/v2/resize:fill:64:64/2*UeSzg0kJlGka3IxlyvgYEg.jpeg)](/@FocusReactive?source=post_page---byline--3c51fb238064---------------------------------------)

[FocusReactive](/@FocusReactive?source=post_page---byline--3c51fb238064---------------------------------------)

9 min read

·

Nov 21, 2019

--

2

Listen

Share

More

This is the second part in series of “How to create a modern React application?”. In the [first part](/@FocusReactive/headless-cms-contentful-and-nextjs-how-to-create-a-modern-react-application-part-1-fdd772073a5d) we have discussed problems of Contenful Content Types limitation and general questions of component hierarchy. We have finished on introducing simple standard template and now we’re ready to implement it in our React Application. All examples of code shown in this post are taken from [complementary NextJS application](https://github.com/UsulPro/contentful-post-demo-app) which you can inspect to see all things altogether.

Press enter or click to view image in full size

![]()

*An example of a template layout*

In order to display this page in our application, let’s add Contentful support. We will be using Javascript SDK. Suppose that we have already created a NextJS application. Let’s install the necessary packages:

Let’s set up data upload from Contentful into our application:

Don’t pay attention to the lines that are commented out for now, we will need them later. The reason why we we wrote the import in CommonJS style is that we are going to use this file not only in the browser but also for the application server, which we will write on our own using NodeJS when we need to add dynamic routing. You can find the values for `SPACE`, `DELIVERY_TOKEN` и `PREVIEW_TOKEN` you can find in the menu `Settings` > `API Keys`.

Press enter or click to view image in full size

![]()

Note that all the changes made inside content editor will be accessible with `PREVIEW_TOKEN`, and only after the publication you will be able to access them with the help of `DELIVERY_TOKEN`, which we will utilize for showing the changes to the real users.

So, let’s assume that we will have a page called `/leaders`, and for a start we will create a corresponding file in `pages` folder. By now, we have already created a page in our CMS that has a standard template and a few components with the following types: " `Component: Description`" and " `Component: Quote`". The code of our page will look as follows.

To simplify, let’s assume that the `Layout` component contains all of our general UI. It may contain components for displaying the navigational menu, the footer and the customizable page header. In order for the page data to display we will need to upload it from CMS. To do this, we will place the code inside `getInitialProps`, which will allow us to use NextJS ability to generate pages both for the client and the server. All of the code, connected to receiving data will be encapsulated inside the `getPage` function, taking on the page `id` as a parameter. For rendering template content we will create a function called `renderTemplate`.

Let’s take a look at the `getPage` function.

Here, we are just uploading the data with the help of `getEntry` and organizing them in a way that is convenient for further usage. The values that we are inputting in content editor while filling a page with data in Contentful will be accessible to us as fields of `customPage.fields` object. Naturally, this function is asynchronous as it sends a request to Contentful server. Here, you can also see two helper functions: `selectImages` и `selectTemplate`. It is convenient for us to keep such selectors in a separate file, since we'll have to access these functions permanently. We will take a look at their code later, but for now it's enough to know that these functions retrieve the necessary data from the nested fields. The `selectImages` function returns an array of objects, containing `url` and the name of the image file. Of course, in out case we only have one image, that's why we retrieve the first element of the array. Likewise, `selectTemplate` returns an object, containing Content Type of the template in the `templateType` field, and the data stored inside of it is returned in the `data` field.

Now, let’s take a look at `renderTemplate`. Right now, we only have one type of a template, but we plan to add more in the future. Our standard template has `title`, `content` and `config` fields, but at this moment the only field that matters is the `content` field, which has a " `References, many`" type and a limitation on the type of used entries. This is exactly where our CMS users will be forming a list of components to display on the page.

Standard template display is rather trivial. We are just returning the specified components one by one. If necessary, we can add other template types here, thus adding more functionality to our application.

## Component implementation

The key idea for solving out problem is mapping React components to objects stored inside CMS. Our cross-functional building block is a component. It must have certain properties, so that we could use it for creating pages. First of all, it must be an isolated module in terms of design. If you are using atomic design methodology, which sets up the hierarchical levels like atoms, molecules, organisms and templates, then organism are suitable candidates for implementing them as components. In Contentful, we describe a component as an entry that has a certain data set. Then, we send this data as props to a React component of our application. This might be some data that will be immediately visualized, like text or a picture. We can also assign some properties that change a component’s behavior or some of its internal characteristics. Some components might not have any properties at all if their appearance does not depend on user data. Besides, it is possible to have a list of other child components acting as component properties. For example, a text item, apart from a heading and the text itself, may have a set of links, tags, social buttons, etc. How can you implement a nested list like this in the content model? I think it’s clear — we do it the same way as with a template by adding a field with references to other components.

Press enter or click to view image in full size

![]()

*An example of Component Description in Contentful*

How can we align CMS entry and React components? The first obvious reason is to take the component’s Content Type and use it for displaying a specific component, assigned in our code. For example, for Content Type “ `Component: Description`" we will be using a component that is defined in the file `components/App/Description.js`, and for " `Component: Quote`" - `components/App/Quote.js`.

But what should you do if the number of components is much greater than the number of available Content Types, defined by our tariff plan? In this case, we can use one universal data type, giving the reference for the corresponding React component in the `type` field of the given component. With this approach we lose the ability to assign each property of the component using a separate field in Contentful source editor, since this property set can vary. We will need to use one `JSON` type field and store all the data there in a format that is familiar for developers. Clearly, users will not be happy with such interface, especially if they have to input large information blocks. Let me list the problems that appeared right after implementing such components.

1. It is uncomfortable to input and edit a large amount of data. Users who are unfamiliar with JSON format may get lost or completely break the entry by entering a wrong character. And if you haven’t set up error catching, then an extra comma will easily break the whole page. Take this into consideration and do not trust the data coming from CMS.
2. JSON is not a good fit for formatted text. You can insert end of line characters (\n) or even use markdown, but working with this in JSON format is not very convenient.
3. You cannot refer to files that you store inside CMS. Certainly, you can manually copy the file url and insert it in the right field in JSON. But along with this you lose Contentful features regarding content organization. You will not be able to choose files from a gallery, as it happens with fields like `Media`. Worse still, you will not be able to see which files are used in components and pages.
4. The same goes for nested components — it’s impossible to insert a reference to another entry in JSON.

However, further we will take a look at some ways to make the lives of your users easier and how to solve the mentioned problems. The first idea will be implemented right now, and then we will gradually implement the other ideas as our app grows.

Suppose we have a significant number of components which have a text field among their properites that needs formatting. We can set aside a separate Content Type for such components, where, besides JSON formatted data, there will be a usual text field for entering text into Rich Format. Thus, the component will look as follows.

Press enter or click to view image in full size

![]()

*Component Custom Properties*

Now we are ready to return to our code and implement the `renderComponents` function, which allows to display components of any type universally.

Here, we simply take the list of entries, transferred from the template, and with the help of `map`, we transform it into an array of React components. The result of this function will be rendered on our page in the place that was assigned by us. Let's draw our attention to a few points. For substituting the right component, we should use the `componentsMap` object, whose keys are the types that come from CMS, and the values of these keys are the React components of our application.

We are adding the `renderComponents` function into the `options` property. Thus, we can use it again for displaying the nested components, which allows us to have an unlimited number of nested levels.

Here, we also have a few selectors, extracting nested data from the `component` structure which describes the entry of this component in Contentful. Let's take a look at the implementation of `selectComponentReference`.

Here, it’s important that no matter how you assign the component type (whether you do it through Content Type or through the `type` field), we transfer this value into the function. `selectComponentProps` is done in the same manner.

Here, we proceed from the agreement that all components, which have a JSON object, also have a field with the name `componentData` for storing this data. Note how the fields from `componentData` are transferred to props along with other component properties in the form of a flat object. Thus, a React component must not even know which Contet Type it corresponds with. If necessary, these components may be used in the application in a usual way, without CMS. It's as convenient as if you had to change the Content Type of a specific component, like making it a separate type.

For example, in an overly simplified way, the `Description` component can be described as follows.

Note that we defined the `description` property as `Rich Text`, and in order to display it we are using the `documentToReactComponents` function, which is provided by Contentful developers. This function creates a nested pattern of html tags that displays your text. If necessary, with the help of second argument you can transfer a configuration into the function, allowing to predetermine how exactly the text elements will be displayed. For example, you can transfer your own React components into that function, but it has nothing to do with this article.

For returning the nested components, we use `options.renderComponents`. Obviously, when implementing a component, we have to identify where the child components will be displayed. If necessary, a component may have a few lists of child components and display them in different places.

This was the second part in a series of “How to create a modern React application?”. In the third part we will add dynamic pages to our [NextJs Application](https://github.com/UsulPro/contentful-post-demo-app)

Written by [**Oleg Proskurin**](https://twitter.com/UsulPro)

Senior Software Engineer @ [FocusReactive](https://focusreactive.com/)