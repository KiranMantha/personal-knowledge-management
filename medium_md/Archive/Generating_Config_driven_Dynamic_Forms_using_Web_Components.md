---
title: "Generating Config driven Dynamic Forms using Web Components"
url: https://medium.com/p/7c8d400f7f2e
---

# Generating Config driven Dynamic Forms using Web Components

[Original](https://medium.com/p/7c8d400f7f2e)

# Generating Config driven Dynamic Forms using Web Components

[![Param Singh](https://miro.medium.com/v2/resize:fill:64:64/0*d3ML_mBrORTXjhUK.jpg)](https://medium.com/@paramsingh_66174?source=post_page---byline--7c8d400f7f2e---------------------------------------)

[Param Singh](https://medium.com/@paramsingh_66174?source=post_page---byline--7c8d400f7f2e---------------------------------------)

12 min read

·

Mar 8, 2019

--

2

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7c8d400f7f2e&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Fgenerating-config-driven-dynamic-forms-using-web-components-7c8d400f7f2e&source=---header_actions--7c8d400f7f2e---------------------post_audio_button------------------)

Share

![]()

Over the years, we as UI Developers have become so habitual of using the already available UI Frameworks and Libraries like React, Angular, Vue etc due to the increasing demand of shipping things quickly. And the main selling point of these frameworks is that they not only solve this problem efficiently but also provide us with a sophisticated interface and apis while hiding the lower level details. The details are so hidden that over the years, we’ve sort of become complacent accepting the “magic” that happens behind the scenes that renders our Angular or React component we just created in typescript.

## Agenda

The purpose of this post is not into exploring how the internals mechanisms of these frameworks work. Rather, I’d be discussing about a scenario wherein let’s assume that these frameworks don’t exist in the market and if you were to write components today using plain VanillaJS and Web Standards, how you’d do that along with some complexity of introducing dynamic config driven and reactive components. Throughout the article, we’ll observe the cost we pay for not using a sophisticated framework and how you have to think of workarounds to get the job done by yourself. Here’s the repo link <https://github.com/paramsinghvc/dynamic-form-web-components>. Feel free to fork and extend it’s functionality.

## Web Components

Press enter or click to view image in full size

![]()

> Web Components is a suite of different technologies allowing you to create reusable custom elements — with their functionality encapsulated away from the rest of your code — and utilize them in your web apps.

In other words, the web components standard implemented by the browsers help us create custom html elements by extending the existing elements or base elements while keeping them well encapsulated or independent and hence suitable for reusability throughout our applications.

The web components specification is based on the following three pillars:

1. **Custom Elements**: We can now create our own html tags like `<my-element>` with the set of api provided for the same. Just like we create a React or Angular component to isolate a piece of functionality and to perform some desired behaviour on some event, we can use the custom elements api to do the same without using any third party framework.
2. **Shadow DOM**: Shadow DOM is a great way to encapsulate the DOM and CSSOM of our web component so that it doesn’t mess around or get messed around by it’s surrounding or ancestor elements. In other words, it doesn’t allow leaking of styles from the parent to children sub-dom trees and vice versa. The use case fits best when you want to create a pluggable component like a chat support window inside the application such that it’s theming and styles are not influenced by the host application (Remember using iframes for the same thing?)

Press enter or click to view image in full size

![]()

And, did you know that the already existing html elements also have shadow dom built inside them, you can enable them to be seen inside the devtools by going to settings → elements→ show user agent shadow dom

Press enter or click to view image in full size

![]()

![]()

3. **Template Tag**: The `<template>` and `<slot>` tags can be used to create markup that can be loaded into the existing DOM on demand, pretty much like we create handlebars but sadly `<template>` doesn’t support interpolation ( `{{title}}` ) of dynamic variables.

Press enter or click to view image in full size

![]()

Anything inside the template tag isn’t loaded or honoured unless its activated dynamically by using JavaScript. Hence, all the scripts, images and markup is dormant till we add it to a host element explicitly.

Press enter or click to view image in full size

![]()

The content property of a template tag returns the [document fragment](https://developer.mozilla.org/en-US/docs/Web/API/DocumentFragment) of what’s present inside the tag. Document Fragment is a collection of dom nodes to which if any change is made like appending, removing, it won’t cause a paint or layout reflow unless it’s added to the dom. Hence, we can define the markup of our custom element using it so that it’ll be re used across all our component instances.

## Config Driven Development (CDD)

A config driven development involves maintaining a config in say JSON format, which can be used to do all the mundane and repetitive tasks of rendering. Maintaining a config has a lot of benefits

* First, it provides a generic interface to develop things which help your project scale well.
* It saves a lot of development time and effort. Instead of developing new pages or modules in a imperative way by writing the code for each module yourself, you can just configure the module or page.
* The config can be decoupled from the frontend code base and hence any modification required in the future won’t require a deployment on UI.
* Since the config is maintained in the backend as JSON, experimentation by product teams can be done easily by just changing the configuration but yeah incorporation of a new element or widget would require writing code for it on the UI of course.
* Centralised code for taking and rendering the config would be more robust since any errors would be centralised to that code only. Contrary to a scenario where we had different codebases for different modules.

![]()

Let me explain with an example, suppose you have an application which has a lot of forms to be rendered. So instead of writing form code multiple times which involves, writing html markup, styling, initialising, binding event handlers, validations, what we can do is that we can maintain a configuration file wherein we need to write about the form elements and their behaviours in response to events like keypress, click, change and how to handle validations etc. And this configuration framework can now be used to create any sort of form. So, it’s like a one time investment which gives a lot of benefits in the long run.

Here’s how the config looks like

### Config Parser

The above config needs to be read and translated into Web Components to be rendered as

Press enter or click to view image in full size

![]()

The config passed is looped over and for each entry in the config, we determine it’s component to be rendered based on the type passed. There’s a `COMPONENTS_MAPPING` that we need to maintain to map the component type to the actual web component tag name. Once, we get that we create that element in JS using `document.createElement` etc which is hidden behind the helper method `createNode(nodeName, options)` in the above snippet.

Besides this, there’s a `formValidations` map that is to be kept which is nothing but a map of elementId vs it’s current form validation state. For eg: An age form element at any point could hold validations of required, out of range, not a number etc. All of it could be maintained inside this map.

Along with this, we need to maintain a `formElementsMap` which would be used for triggering changes imperatively on a component in response to an event. We’ll see that later.

## Reactive Components

Now, the way we want our components to be dynamic and reactive enough to respond to any changes in the so called “props” that we pass to them.

Before jumping on to how we’d implement them with web components, lets reflect upon how it works with the UI frameworks we have today. In React, we pass props to a component, when any of the prop changes, a reconciliation process is triggered internally by react which traverses the whole component hierarchy to mark any changes required in the given component at a time.

![]()

Same goes for Angular, where we specify `@Input()` decorator for all the input props of given components. By doing this, all the frameworks maintain a separate space in the memory for internal housekeeping like maintaining a registry of the props of a given component and checking the previous props and next props and then responding to any changes if found by re-rendering the part to be rendered. Hence, they always make sure that the component view is always in the sync with the component state or model. That’s the main selling point of these sophisticated frameworks out there. Because, natively it has not been possible in vanilla JS to determine the changes in response to the component props.

## Get Param Singh’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

But today, there are two ways you can listen to any prop changes happening on a web component

* Using [Mutation Observer](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver) API
* Web Components Api `attributeChangedCallback(attrName, oldValue, newValue)`

## Building Custom Components

Let’s extend HTML with our own form elements.

Press enter or click to view image in full size

![]()

Here’s how it would look like to implement your own custom web component without using any third party library or framework. But it comes with a cost which I’ll be discussing soon. We can register the given component class onto the current window by doing

Press enter or click to view image in full size

![]()

Since, we’ve been using libs like React and Angular for over years now, we expect our web components as well to behave the same way as the ones created with React. But here we won’t be investing time in building an elegant layer of our own compilation, data binding, reconciliation (change detection). Rather, my purpose here is to use the existing web apis out of the box.

So, for detecting changes based on the props, `attributeChangedCallback` seems a good (and only :P) fit. Hence, we produce all the dynamic properties on the components as attributes and we need to inform out web component about which properties it should observe by defining a static getter property on it as

Press enter or click to view image in full size

![]()

It means that if any of these attributes change on a given component, we will be able to tap into the process by writing logic in the `attributeChangedCallback`

So far, we discussed about inputs to our component, what about outputs? If any internal state of our component changes, we need to tell the outer world or the parent component about it by dispatch a custom event.

Press enter or click to view image in full size

![]()

If you observe the component we defined carefully here, we’re basically treating it as a black block, it could have it’s internal state, animations, data at any given point of time. All we’re interested in is giving it an input and expecting an output to keep the input too in sync. Just like how unidirectional data flow concept of React works.

![]()

Here, view is our component, state is the input attribute accessed via getter `this.value` and action is the change event we’re triggering when the value changes through user input in the text box. Hence, in this example, we’re just relaying input and output to and from our input box inside it so far.

## Validations

But now, let’s say we want to incorporate support for validations for our form components. Since an element could have multiple validation error, a map would be a good data structure to hold it against every component id.

Press enter or click to view image in full size

![]()

It looks like this in the form of map.

Press enter or click to view image in full size

![]()

Please note that, it’ll be better to use an ES6 Map here to avoid unnecessary load of object proto on it. But I haven’t used because of JSON stringification.

We’ll store the element validity status inside a sort of global map as `formValidations` . The idea is to update this map by listening to the valueChange event and checking that value based on the validation configuration passed for that element and appending an error key in the map if the validation criteria fails. Here’s a small example for Range validation.

Press enter or click to view image in full size

![]()

Now that we’ve updated the formValidations map, we need to pass it as an attribute to our custom component but wait a second till you see this

Press enter or click to view image in full size

![]()

Whoops! HTML attributes get stringified, hence we can’t pass objects or array into it. Hence, an extra step of wrapping and unwrapping to and from JSON needs to be done here. This is one thing that I found a little disappointing working with web components because we’re so used to passing non-primitive data structures in and out our components that we found it to be instinctive here as well.

Press enter or click to view image in full size

![]()

Big deal! We can do it by identifying whether the attribute value being passed is of non primitive type. (Please mind that typeof array is also an object). Although this is not a very fool proof way for identifying since creating a string using `new String('')` would give typeof as true.

Now the next step is to tap into the `attributeChangedCallback` hook provided in the web components lifecycle api and listen for the changes happening for a given attribute and react accordingly by re-rendering the desired piece of dom. Here, in case of validations we’d like to render the `<ul>` that we have created as a sibling to our input component. We need to parse the stringified json attribute values and shallow compare them as then trigger changes or else there would be a lot of re-renders.

Press enter or click to view image in full size

![]()

We’re reacting to the validations attribute by checking whether it’s an empty object or not. If it’s empty, it means there are no validation errors and we need to remove the previously rendered errors ui or else re-render the errors div and apply styling on the input element accordingly like a red border.

Press enter or click to view image in full size

![]()

The renderErrors function look like this. I’m using documentFragment to append all the dom nodes first and then add it to the original dom at once in the end.

So, overall this is the basic approach I’ve found to make the custom components analogous to the way we create them using any framework.

## Lessons Learnt

Following are some lessons learnt in my wishful pursuit of using vanilla JS completely for creating dynamic and reactive applications that we create today:

* It’s hard to pass the data into the components due to an extra json stringification and de-stringification layer.
* You have to rely on setAttribute and getAttribute for “props” to a component since attributeChangedCallback is the only way to detect changes.
* If I reminisce about angular or vue data bindings and how they work actually. These frameworks have compilers or dom parsers which look for these bindings and update the UI in response to any change in the bound properties(model). But here, we have to explicitly, write updation logic for handling every prop/attribute change, just how we did for `validations` key by calling renderErrors every time which is far beyond an optimised approach compared to React or Vue keys or angular’s `trackBy`.

It’s due to these limitations and poor browser support and incompatibilities that these frameworks exists because they didn’t wanted to wait for browsers to implement all this. Hence, these frameworks have come up with their own individual ways of dom creation and manipulation with a splendid work for years now.

## Conclusion

We explored a twisted way of creating web components with a vow of not using any third party thing and we ran through some obstacles and discussed how we could solve them while keeping the problem statement non-trivial. Relying on Web components to create production ready app would a strong statement to say because I still find it to be in an immature state. I’ve been just wondering about the future days wherein the web apis would be mature enough to let us create what we do using third party frameworks today. A utopia for web that I can envision would have rich component creation and manipulation capabilities in built as a part of spec and browsers implementing them. Hence, we won’t have to include any of the heavy third party libraries which will give faster load times to the users by saving the download costs by a huge amounts.

That said, here’s a reason to cheer. The web components are platform neutral and if you’re thinking of creating framework agnostic components with all the lux and ease of apis at par with the frameworks we have today, we can use [Polymer](https://www.polymer-project.org) or [Stencil](https://stenciljs.com) for the same.

## References

* <https://alligator.io/web-components/attributes-properties/>
* <https://dev.to/thepassle/web-components-from-zero-to-hero-4n4m>
* <https://developer.mozilla.org/en-US/docs/Web/Web_Components>
* <https://github.com/paramsinghvc/dynamic-form-web-components>