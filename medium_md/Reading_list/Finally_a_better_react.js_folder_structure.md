---
title: "Finally a better react.js folder structure"
url: https://medium.com/p/821a2210835
---

# Finally a better react.js folder structure

[Original](https://medium.com/p/821a2210835)

# Finally a better react.js folder structure

[![Vinoth kumar](https://miro.medium.com/v2/resize:fill:64:64/1*wJuA9aPNBo_2Rqvm-CUquw.jpeg)](/@kumarvinoth?source=post_page---byline--821a2210835---------------------------------------)

[Vinoth kumar](/@kumarvinoth?source=post_page---byline--821a2210835---------------------------------------)

4 min read

·

Nov 4, 2021

--

26

Listen

Share

More

Press enter or click to view image in full size

![]()

You might thinked “Why react.js don’t have standard folder structure?”.   
To find answer, you need to understand the difference between framework & library. Please refer the below image:-

![]()

> React.js is an library for building user interface

“**Framework are in-charge**” since it dictates the architecture of project.

When using library, “**You are in-charge**” means you can choose where and when you want to insert or use the library.

Let me explain about the react folder structure which i’m following to develop new application.

![]()

**.storybook**

* Storybook is configured via a folder, called .storybook which contains various configuration files.

**public**

* It contains static files such as index.html, javascript library files, images, and other asset.

**src**

* It contains the source code of the project.

**src/assets**

* It contain the assets like images, css & fonts

**src/components**

![]()

* It contains the reusable atomic & molecular components

![]()

* Each component folder will contain the component, test & documentation file

Button component structure explained below:-

* Button/Button.tsx  
  It contain the actual component code
* Button/Button.style.tsx  
  It contain the styles
* Button/Button.test.tsx   
  It contain the Button unit test cases using [**jest**](https://jestjs.io/)
* Button/Button.stories.tsx  
  It contain the component documentation using [**storybook**](https://storybook.js.org/docs/react/get-started/install)
* Button/index.tsx  
  index.tsx merely imports that component file and exports it.

**src/constants**

* It contain the constant file
* Eg : Regex & other application generic constant

**src/helpers**

* It contains the reusable helper functions

**src/layouts**

* It contains the layout components
* layout is the common top wrapper component usually will contain navbar , sidebar and children components

**src/pages**

* It contain the page component.
* Each component can layout component as top wrapper based on the page structure
* Each component exported as default, since lazy loading works with default export

**src/routes**

* It contain the page routes
* Dynamic configuration is best with working with routes
* Usually it have an nested array to render the routes

**src/schema**

* It contain the schema files using the yup
* It used with [formik](https://formik.org/) for field validation

**src/service**

* It contain the dynamic http request function using axios
* Axios is a promise-based HTTP Client for node.js and the browser
* Axios can be used for api request cancellation, featured with request and response interceptors.

**src/store**

![]()

* It contains the redux files like actions, reducers & actionTypes.
* **store/actions**  
  It contains the action files. It used to trigger action to update the redux state
* **store/reducers**It contains the reducers files, each file will have default export of function and will have various switch cases to update the redux state
* **store/actionTypes.tsx**It contains the actionTypes which will be used to configure reducer & actions.
* **store/selectors**It contains the selectors functions, refer R[eselect](https://github.com/reduxjs/reselect) for more details
* **store/index.tsx**It contain the create store function which returns a store object

**src/styles**

* It contain the styled components reusable breakpoints file, global styles & theme constant file

**src/App.js**

* App Component is the main component in React which acts as a container for all other components

**src/config**

* It contain the config files using the env

**src/index.js**

* It contain method to render the application into real dom

**src/test.utils.tsx**

* It contain method to render the jest component file
* This function required since we need to add top wrapper component of react-router, redux & styled-components. Without adding this wrapper component, test cases will not run.

![]()

**Github repo link** 😁: <https://github.com/vinothwino/react-boilerplate>

Press enter or click to view image in full size

![]()