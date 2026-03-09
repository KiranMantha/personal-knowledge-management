---
title: "A Guide to inject variable into your code using webpack"
url: https://medium.com/p/36c49fcc1dcd
---

# A Guide to inject variable into your code using webpack

[Original](https://medium.com/p/36c49fcc1dcd)

# A Guide to inject variable into your code using webpack

[![Gagan Sharma](https://miro.medium.com/v2/resize:fill:64:64/1*_WmUwDeSWP_5hrJqMPrF8g.jpeg)](/@gagan.sharma61?source=post_page---byline--36c49fcc1dcd---------------------------------------)

[Gagan Sharma](/@gagan.sharma61?source=post_page---byline--36c49fcc1dcd---------------------------------------)

3 min read

·

Mar 28, 2018

--

5

Listen

Share

More

**Webpack** is modular bundler. Webpack can take care of bundling alongside a separate task runner. When you bundle a project using Webpack, it traverses through imports, constructing a dependency graph of the project and then generating the output based on the configuration. It allows you to build your whole project — including CSS, preprocessed CSS, images, font and many more.

***This guide assumes that you are familiar with the Webpack and how to setup.***

We are going to use DefinePlugin, included with Webpack to define the global variable and inject them into our code. Using the NPM scripts we can pass the environment variable for specific URL and configuration.

Here is a simple constant file with the backend APIs

Press enter or click to view image in full size

![]()

We have defined our REST API and this can later be used in other function for making the calls. This is set to localhost but we have different environments such as staging, beta, and production that require setting this to different backend url. The problem is we have hardcoded this but we need to make builds for different backend URL for deploying code on production, staging, and beta.

We can use Webpack to help us solve this problem. With DefinePlugin, we can set the API URL as a global constant and inject it into our code.

Let’s start by creating some build commands with NPM. You should have a package.json similar to this already:

Press enter or click to view image in full size

![]()

In the scripts section, we have created a general build command for the Webpack build process. *These flags will output a progress meter and use colored text while running in the terminal*.

**Now for each environment create a new command:**

Press enter or click to view image in full size

![]()

Each of these will call the regular build command, but also set the NODE\_ENV variable to the specific environment we are building. This will allow the variable to be accessed in the Webpack configs.

This is our standard production Webpack config file:

![]()

In the plugins section, we are going to use the DefinePlugin and pass in a config object. Everywhere in our code where \_\_API\_\_ appears will be replaced with the value of apiHost:

![]()

Now, we need to write a function to define apiHost. Inside setupAPI function, we have access to the NODE\_ENV variable we passed in with the NPM command. Using a switch statement, we can set apiHost to the URL of our backend servers depending on the NODE\_ENV. We should also set the default to our production server. **setupAPI function should be inside the webpack.config.js file**

Press enter or click to view image in full size

![]()

Back to our constant file. We will change the hardcoded URL with \_\_API\_\_

Press enter or click to view image in full size

![]()

Now, each of our build commands will inject the correct server URL for deployment.

All done Cheers 😃.