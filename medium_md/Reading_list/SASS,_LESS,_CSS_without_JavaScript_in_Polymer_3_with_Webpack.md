---
title: "SASS, LESS, CSS without JavaScript in Polymer 3 with Webpack"
url: https://medium.com/p/f6a3c032ea75
---

# SASS, LESS, CSS without JavaScript in Polymer 3 with Webpack

[Original](https://medium.com/p/f6a3c032ea75)

# SASS, LESS, CSS without JavaScript in Polymer 3 with Webpack

[![Jose Javi Asilis](https://miro.medium.com/v2/resize:fill:64:64/1*8iLuGqZNHWdrw_F71CZ0rw.jpeg)](/@javiasilis?source=post_page---byline--f6a3c032ea75---------------------------------------)

[Jose Javi Asilis](/@javiasilis?source=post_page---byline--f6a3c032ea75---------------------------------------)

3 min read

·

Jul 6, 2018

--

Listen

Share

More

Ever since the beginning, you’d had to write or inject your CSS into [HTML](https://hackernoon.com/tagged/html), in order to style Polymer Components. At a time, Polymer did include the ability to import [external stylesheets](https://www.polymer-project.org/2.0/docs/devguide/style-shadow-dom#external-stylesheets), although it was an experimental feature, and was deprecated in favor of style modules. With the recent version of Polymer 3, we ditch HTML (finally, no more silent errors 🎉!) in favor of good ol… er, I mean, good and new [JavaScript](https://hackernoon.com/tagged/javascript) (ES2015 classes).

Nonetheless, there’s a problem. Within HTML, we could get CSS support with our IDE or Text Editors. Writing them in a JavaScript makes it more difficult to static analyze and autocomplete our code.

Fortunately, since it’s JavaScript, this means that we can tap into its powerful ecosystem, and use the tooling available to us.

`polymer-css-loader` [is a Webpack Loader](https://github.com/superjose/polymer-css-loader) that creates the JavaScript styling for you, and “makes CSS great again” by just importing the CSS to the Polymer Component JavaScript file.

## How to use

Install the loader:

```
npm install save-dev polymer-css-loader extract-loader css
```

Or

```
yarn add save-dev polymer-css-loader extract-loader css-loader -D
```

Add it to your Webpack.config file:

```
module.exports = {  
  entry: './src/index.js',  
  module: {  
    rules: [  
     {  
        test: /\.css|\.s(c|a)ss$/,  
        use: [{  
          loader: 'polymer-css-loader',  
          options: {  
            minify: true, // defaults to false  
          },  
        }, 'extract-loader', 'css-loader', 'sass-loader'],  
      },  
    ],  
  },  
};
```

Note: You can use either sass-loader or less-loader. Leave polymer-css-loader for last.

And import your css in your JavaScript Component file

```
import { html, PolymerElement } from '@polymer/polymer/polymer-element';  
  
import './style-1.scss';  
// The ?name will specify the name to be used in the include.  
import './style-2.css?name=maria';  
class PolymerTestComponent extends PolymerElement {  
  static get template() {  
    return html`  
      <style include="style-1 maria">      
      </style>  
      <p>This is the test component</p>  
      <p>This is the propertie's value: {{prop1}} </p>  
      <div>This font size should be bigger</div>  
    `;  
  }  
  
  static get properties() {  
    return {  
      prop1: {  
        type: String,  
        value: 'polymer3-app',  
      },  
    };  
  }  
}  
  
window.customElements.define('polymer-test-component', PolymerTestComponent);
```

That’s it! The name of the file will be used for the `<style include=””>`

## Other Features

### Add a custom name for <style include=””>

Add a custom name by adding `?name=` at the end of the import **(Don’t use quotes “” for the value)**.

```
import './style-1.scss?name=my-custom-style';// Then:  
// Code omitted:  
static get template() {  
    return html`  
      <style include="my-custom-style">      </style>// Code omitted:
```

### Skip a css file

You can skip a css file by adding `?skip` at the end of the import. This **will include** the CSS into your Webpack Bundle, but it will not be parsed as a Polymer JavaScript styling file.

```
import './style-1.scss?skip';
```

### Skip all the files and explicitly include the ones you need

Useful when you’re combining multiple libraries. This **will include** the CSS into your Webpack Bundle, but it will not be parsed as a Polymer JavaScript styling file.

```
entry: './src/index.js',  
  module: {  
    rules: [  
     {  
        test: /\.css|\.s(c|a)ss$/,  
        use: [{  
          loader: 'polymer-css-loader',  
          options: {  
            minify: true, // defaults to false  
            defaultSkip: true // will skip all the files          },  
        }, 'extract-loader', 'css-loader', 'sass-loader'],  
      },  
    ],  
  },  
};
```

Then, you’d use `?include` for the ones that you’d like to be parsed by the loader.

```
import './style-1.scss?include&name=my-custom-style';// Will still be included, but not in the JavaScript  
// Polymer-Web Components fashion  
import './style-2.scss' // Then:  
// Code omitted:  
static get template() {  
    return html`  
      <style include="my-custom-style"></style>// Code omitted:
```