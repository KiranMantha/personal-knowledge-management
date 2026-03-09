---
title: "Simple React Server Components Implementation Without Next.js"
url: https://medium.com/p/28182584450a
---

# Simple React Server Components Implementation Without Next.js

[Original](https://medium.com/p/28182584450a)

# Simple React Server Components Implementation Without Next.js

[![Mohi Bagherani](https://miro.medium.com/v2/resize:fill:64:64/1*w7Ot0unDLFOnm1POHw4WUw.jpeg)](/@bagherani?source=post_page---byline--28182584450a---------------------------------------)

[Mohi Bagherani](/@bagherani?source=post_page---byline--28182584450a---------------------------------------)

5 min read

·

Sep 11, 2023

--

3

Listen

Share

More

Press enter or click to view image in full size

![server side components in react]()

This article will explain how to use the React server component API without using any extra library like Next.js to achieve Server Side Rendering and Server Components by running a simple node server to handle the client requests.

So,let’s start…

## Initialising the App

Create an empty directory, open a terminal in it and run the following commands:

```
npm init --y  
  
# installing react and react-dom libraries  
npm i react react-dom
```

Now for *transpiling* the `JSX` syntax that we usually use in React applications into Javascript that can be run on the browser, we need to install `babel` and `webpack` as the development dependency as follows:

```
npm i -D webpack webpack-cli webpack-node-externals  
npm i -D @babel/cli @babel/core @babel/preset-env @babel/preset-react babel-loader
```

It’s good to know that the `webpack-node-externals` library creates some `externals` that ignores `node_modules` when bundling with Webpack.

## Create a Simple React Application

Make a subdirectory called `client` then create an `App.jsx` file in it and paste these codes into it:

```
// /client/App.jsx  
  
import React, { useState } from "react";  
  
export default function App() {  
  const [counter, setCounter] = useState(0);  
  
  return (  
    <button onClick={() => { setCounter(counter + 1) }}>Counter: {counter}</button>  
  )  
}
```

As you can see it’s a very simple component that creates a `button` and uses the `useState` to keep some value inside itself.

## Creating the Server

Next create a `server.js` file in the root of the app’s directory and put the following codes in it:

```
// /server.js  
  
import http from 'http';  
import fs from 'fs';  
import React from 'react';  
import { renderToString } from 'react-dom/server';  
  
import App from './client/App.jsx'; // transpiling with babel is required  
  
http.createServer((req, res) => {  
  // this is not the best code, I'm just trying to keep things simple  
  if (req.url.endsWith('/client.js')) {  
    res.writeHead(200, { 'Content-Type': 'text/javascript' });  
    res.end(fs.readFileSync('./dist/client.js'), 'utf8');  
    return;  
  }  
  
  res.writeHead(200, { 'Content-Type': 'text/html' });  
  
  res.end(`  
    <html>  
      <head></head>  
      <body>  
        <div id="root">${renderToString(React.createElement(App))}</div>  
        <script src="/client.js"></script>  
      </body>  
    </html>  
    `);  
}).listen(3000);
```

Let’s talk about the above code a little bit:

First, I’ve imported some required modules to handle the `http` requests and also using the `fs` module, I try to read a static file(`dist/client.js`) from the server and send it to the client.

Next, using `http.createServer` I’m creating the server and listening to the port number`3000`

> As you can see this code **only** handles if the client is asking for the main page or asks for the `/client.js` file because I didn’t want to go deeper and cover the routing and etc which is not related to this article.

```
res.end(`  
  <html>  
    <head></head>  
    <body>  
      <div id="root">${renderToString(React.createElement(App))}</div>  
      <script src="/client.js"></script>  
    </body>  
  </html>  
`);
```

This code sends back an HTML to the client’s request and as you can see within the `body` tag, it has a `<div id="root">…</div>` and inside this `div` I’m putting the React app render’s output using the `renderToString` function.

> Although based on the [React documentation](https://react.dev/reference/react-dom/server/renderToString) there are better alternatives for this function that supports streaming, but for now, let’s move on with this function.

Basically, the `renderToString` function renders a React tree to an HTML string.

So, as the result of sending the page request, we should expect the following HTML response:

```
<!-- expected html response -->  
  
<html>  
 <head></head>  
 <body>  
   <div id="root">  
    <!-- This is the React app generated HTML -->  
    <button>Counter: 0</button>   
   </div>  
   <script src="/client.js"></script>  
 </body>  
</html>
```

The `<script src="/client.js">` will send a request to our server to get this file, so we should provide it somehow to the clients that will be covered later in the building phase.

## The Hydration Phase

The output of the server has our React application HTML result which in this case is `<button>Counter: 0</button>`

Create an `index.jsx` file in the `client` folder and put the following codes in it:

```
// /client/index.jsx  
  
import React from "react";  
import { hydrateRoot } from "react-dom/client";  
import App from './App.jsx';  
  
hydrateRoot(document.getElementById("root"), <App />);
```

This code calls the `hydrateRoot` function from the React APIs and mixes the React`App` with the content of the `root` element on the client browser.

It means that we are sure that at the moment of calling this function the client has the exact HTML of the React application in the `div id="root"`

Now, let’s give it a try by running the server.

## Compiling the App

But before that we need to do one more step:

Since we have imported a `jsx` file in the `server.js`, we have to compile the React app as well as the server into something runnable on the NodeJs and Browsers.

Put these into the `scripts` section of the `package.json` file:

```
// package.json  
  
"scripts": {  
  "start": "node ./dist/server.js",  
  "build:client": "webpack --config webpack.config.js --env client",  
  "build:server": "webpack --config webpack.config.js --env server",  
  "build": "yarn build:client && yarn build:server"  
},
```

It needs a `webpack.config.js` file, so create it and put these codes in that file too:

```
// webpack.config.js  
  
const nodeExternals = require('webpack-node-externals');  
  
const sharedModuleRules = {  
  rules: [  
    {  
      test: /\.?jsx$/,  
      exclude: /node_modules/,  
      use: {  
        loader: "babel-loader",  
        options: {  
          presets: ['@babel/preset-env', '@babel/preset-react']  
        }  
      }  
    },  
  ]  
}  
  
module.exports = (env) => {  
  if (env.client) {  
    return {  
      entry: './client/index.jsx',  
      output: {  
        filename: './client.js',  
      },  
      module: sharedModuleRules  
    }  
  }  
  
  return {  
    target: 'node',  
    entry: './server.js',  
    output: {  
      filename: './server.js',  
    },  
    externals: nodeExternals(),  
    module: sharedModuleRules  
  }  
}
```

By running the `build` command on your terminal(`npm run build`), Webpack goes through this file and read the configurations we’ve written, so it will compile the client and the server apps because they are using `jsx` and they have to be compiled using the`babel` plugin.

As the result of building the app, next you can run the app by running `npm run start` that will execute the `node ./dist/server.js` command.

Also the build command will compile the `index.jsx` file and will put the compiled client app into the `/dist/client.js` file. So later, when the client asks for the `client.js` file, it will serve this file that has a version of the runnable App in the browser as well as the `hydration` logic.

Open your browser and head to `localhost:3000` , you should see this:

![]()

![]()

As soon as we receive the response, the browser will download the `client.js` file too. So first, it will render the application HTML and then it will run the content of the `client.js` file which has the React app and `hydrate` function. So, everything would be synced at this moment and our React application will go alive and by clicking on the `button` we should expect the Javascript of our application work well and increases the counter.

## Conclusion:

By calling the `renderToString` function we can get the string/HTML output of a React component or application on the server and sent that HTML to the client. It means that we achieve Server Side Rendering(SSR) in our stack. Next by calling the `hydrateRoot` function on the client, we can attach the React app to the received HTML and make our application alive and give the control to React.