---
title: "How and when (not) to use webpack for lazy loading?"
url: https://medium.com/p/bef9d37c42c1
---

# How and when (not) to use webpack for lazy loading?

[Original](https://medium.com/p/bef9d37c42c1)

# How and when (not) to use webpack for lazy loading?

[![Yonatan Kra](https://miro.medium.com/v2/resize:fill:64:64/1*EoRnAA911RNClp819vTAgg.png)](/@yonatan.kr?source=post_page---byline--bef9d37c42c1---------------------------------------)

[Yonatan Kra](/@yonatan.kr?source=post_page---byline--bef9d37c42c1---------------------------------------)

11 min read

·

Mar 26, 2018

--

3

Listen

Share

More

Load time, memory imprint and bandwidth are major considerations when building a web application. [Lazy loading](https://en.wikipedia.org/wiki/Lazy_loading) is a technique that may help reduce all of the above. However, misusing or under-planning this technique can actually harm your app and necessitate a big refactoring process later on.

Don’t get me wrong, though: Lazy loading *IS* awesome, especially since HTTP/2 came about. You can load only the files you want and improve your app’s performance. Webpack allows you to lazy load 3rd-party libraries, and, even better, it allows you to chunk your own app and lazy load parts of it on demand. Webpack has implemented the ES7 dynamic import spec ([available in Chrome and Safari](https://developers.google.com/web/updates/2017/11/dynamic-import)).

Let’s see webpack’s lazy load in action:

Press enter or click to view image in full size

![]()

Look familiar? In case you didn’t read my [no-nonsense webpack post](/@yonatan.kr/no-nonsense-webpack-project-bdfb79181737) (if not, go ahead and read it!), the above app (which can be [cloned from Github](https://github.com/YonatanKra/YOPF)), called YOPF, is what we created in that post, though we didn’t add lazy loading yet. Let’s add lazy loading to YOPF to make it lazy load like it does above.

## From Static Import to Dynamic Import

In the master branch of YOPF, we are using static imports. They look like this:

`import YOPFForm from ‘./form/form.index.js’;`

With static imports, webpack bundles the contents of *form.index.js* and its dependencies inside our main bundle. With dynamic imports, we get the effect shown in the GIF above: webpack chunks your module inside a different file, and lazy loads it on demand. Here’s what it looks like:

```
if (iWantToLoadMyModule) {  
   import('myModule').then(myModule => {  
      // do something with myModule.default   });  
}
```

Eventually, the dynamic import statement returns a promise that resolves to an object that holds our module’s exports. In this case, we have `myModule.default` (from `export.default` from the *myModule.js file*) .

It’s as simple as that. But using dynamic imports like this would create numbered bundles (e.g., *0.bundle.js*). We would like to have named bundles (e.g., *fireworks.bundle.js*). Webpack has a special syntax for that.

```
import(/* webpackChunkName: "myModuleName" */ 'myModule')
```

Now we make a small addition to the *webpack.config.js* file in the output property:

`chunkFileName: ‘[name].bundle.js’`

Here’s the full implementation:

In *app.js* we just need to move the call to the fireworks module into a condition (if) with a dynamic import and remove the references to the static call. Note the comment inside the dynamic import.

> Another thing to note is that the import itself is not a function, and you cannot use it as one! Read more [here](https://developers.google.com/web/updates/2017/11/dynamic-import).

In *webpack.config.js* we just add the`chunkFileName` property. You can play with it to see its many uses.

## Chunk file size

There are various factors that can contribute to an app’s file-size bloating.

Press enter or click to view image in full size

![]()

One factor is the app itself — but since you know how to write lean and mean, it’s not the main issue. Another factor is 3rd-party modules.

### Splitting 3rd-party code

While 3rd-party modules are time savers, they come with their own weight and dependencies. Webpack to the rescue! Webpack can automatically chunk multiple requires/imports from different bundles in order to save space and split them into their own vendor bundle files.

First — let’s add this functionality to the plugins array in the config file:

```
new webpack.optimize.CommonsChunkPlugin({  
  name: "vendor",  
  minChunks: function (module) {  
    return module.context &&  
            module.context.includes("node_modules");  
  }  
})
```

The CommonsChunkPlugin is very powerful. In the above example I just tell the plugin to create a vendors chunk from all the libraries that are imported from *node\_modules*. This is very useful with caching — you keep the vendors file cached, and change only the main file of your app.

> You could split specific node modules by specifying another entry and then chunking it:
>
> `entry: {  
>  a_very_big_module: ["a_very_big_module"],  
>  app: "./app.js"  
> },  
> plugins: [  
>  new webpack.optimize.CommonsChunkPlugin({  
>  name: "a_very_big_module",  
>  filename: "a_very_big_module.js", //optional  
>  minChunks: Infinity, //make sure no more modules enter this chunk  
>  })  
> ]`This is very useful if you have a heavy module you don’t always use or want to lazy load — or if you want to extract it and replace it piece by piece until you can discard it completely.

### Splitting your own code

Above we discussed creating multiple bundles for lazy loading. We’ve taken care of the 3rd-party modules (e.g., *node\_modules*) above. But, in your app, you might have your own code that you import in multiple places, and some of them might be in different bundles. That would cause webpack to bundle the imported code inside each bundle. We don’t (necessarily) want that.

The `CommonsChunkPlugin` has a neat feature: it can bundle every common module in our app into a single file. Just add this plugin definition:

```
     new webpack.optimize.CommonsChunkPlugin({  
       name: 'common' // Specify the common bundle's name.  
     })
```

We can even tell webpack what to consider as common (i.e., how many times we need to import a module in order for it to be considered common):

```
new webpack.optimize.CommonsChunkPlugin({  
       name: 'common',  
       minChunks: 3 //if 3 chunks import something, put it in common  
})
```

This code tells webpack to chunk only modules that are called by 3 other chunks. How awesome is that?

And you can read everything about it [here](https://webpack.js.org/plugins/commons-chunk-plugin/). [How convenient…](https://www.youtube.com/watch?v=Jm3zV1pCTQ8)

> SPOILER — a lot is going to change when we talk about browser compatibility…

### Splitting webpack’s overhead

Webpack comes with a bit of overhead: It loads its manifest data and runtime.

The manifest data is the map (hash table) between your app’s folder structure and the “virtual” structure of your app once it’s been bundled and shipped to the browser. The runtime is the actual code that uses the manifest data to load and require the various modules in your app. You can read more about it [here](https://webpack.js.org/concepts/manifest/).

By default, webpack duplicates the runtime into every file (chunk). This is not desirable for several reasons, the most obvious being file size — if code is duplicated in your app, the file size can bloat. In most cases, however, this is a minor issue.

Actually, a more concrete issue is caching. Sometimes, the manifest can change even when your app does not change, and this will bust the cache for the whole app. This might result in unneeded traffic to your server/CDN, and extra traffic can mean extra expenses.

Let’s remove the runtime and manifest data from our webpack chunks and place them in a separate file:

```
new webpack.optimize.CommonsChunkPlugin({  
  name: "manifest",  
  minChunks: Infinity  
})
```

That’s just about it. You can look at the [lazy load branch here](https://github.com/YonatanKra/YOPF/tree/lazy-load) for the final code.

> A note regarding CommonsChunkPlugin (CCP): when using it multiple times, you should remember that order matters: The next instance of CCP will receive the chunk created by the last one. More about this [here](https://github.com/webpack/webpack/issues/4638#issuecomment-292583989).

### What a mess

If you build the app using `npm run build`, you will see a small mess in the *dist* folder:

![]()

With webpack, there’s a very simple solution for this. Since we know we are going to have a few bundles, we can tell webpack to place them in a folder. This is done in the output property:

```
output: {  
    chunkFilename: 'scripts/[name].bundle.js',  
    filename: 'scripts/[name].bundle.js',   
    path: path.resolve(__dirname, 'dist')  
},
```

Note that all I did was to add the target folder’s name in the output and this is the result:

![]()

We can still see Bootstrap’s files cluttering our folder. A short reminder: we’ve used the `url-loader` to parse these files. Hence, we could also use `url-loader` in order to place them in their own folder:

```
{  
    test: /\.(woff2?|ttf|eot|svg)$/,  
    use: [  
        {  
            loader: 'url-loader',  
            options: {  
                limit: 10000,  
                name: 'fonts/[name].[ext]'  
            }  
        }  
    ]  
},
```

Just add the `name` property to the `url-loader` rule and, voila:

![]()

So now we can split our app’s code for lazy loading and even split the result into various folders to keep some sane structure to our distributed application. You can take it as a personal challenge to do the same for the CSS… ([hint](https://webpack.js.org/loaders/css-loader/#extract)).

### Caching

Now that we’ve split our app into multiple files, we would like to enjoy the browser’s powerful caching capabilities. In (very) short, the browser caches files with the same path and name in order to save time (downloading the assets is very costly performance-wise).

So, if we could add hash to our files, and only change the hash of files (modules) that actually change, we could improve user experience.

Webpack has you covered here, too! And, you guessed right: 0 code involved; it’s all in the config. Just change the output file name and add webpack’s hash convention: `chunkhash`.

```
output: {  
  chunkFilename: [name].[chunkhash].bundle.js,  
  filename: [name].[chunkhash].bundle.js,  
  path: path.resolve(__dirname, 'dist')  
}
```

Your files will look like this:

![]()

Try to rebuild and notice that the hashes remain the same after a build. Then, change the code of one of the modules, and notice that the hash *has* changed — and that the app calls the correct file (hash).

## When NOT to lazy load using webpack

Now that we’ve learned how webpack lazy loads and splits our code and the benefits of doing this, let’s consider a use case in which you might like to lazy load on your own.

### Modularizing modules

This is a far flung but valid case that we consider at 

[WalkMe](/u/909b0400e284?source=post_page---user_mention--bef9d37c42c1---------------------------------------)

. Here’s the scenario:

We have a widget that shows a menu. This menu is comprised of JavaScript (JS), HTML and CSS (well, dah…). There are several JS/HTML/CSS trios that comprise templates for use in the menu. For every customer, we can either provide a default template, or create a new one.

The way it works today is that when a customer chooses templates for the menu, the build process concatenates the selected CSS and HTML to the selected JS and serves these to the customer.

Press enter or click to view image in full size

![]()

If a customer wants a custom template (i.e., not one of the pre-made JS/HTML/CSS trios), we need to create a custom widget branch and serve the menu via a custom deployment process.

The whole build process (built between the years 2011 and 2014 and patched ever since) is a mix of Grunt tasks and browserify.

If you’re pulling out your hair by now, leave a few strands for when I get around to writing about CI/CD (…you’re spared from it in this post).

Let’s suggest some saner architectures given what we now know about webpack:

### Serve the menu as a webpack project

The most obvious would be to serve the whole project as a webpack project. This way, we can just set up the templates as dynamically imported modules. When a customer changes his templates, it will be reflected in the client’s static configuration — so all you need to change is a configuration in a static JSON file (you *could* save and query from a DB, but then you would have tons of DB queries for static data…). The application then dynamically imports the correct template:

Press enter or click to view image in full size

![]()

With this architecture, we have one *widget.common.js* file which is served to all clients. We have many template files that are lazy loaded on demand from within this one *widget.common.js* file through some static configuration. The configuration might look like this:

```
{  
    "templateUrl": "widget.template1.js"  
}
```

This seems to solve our problem, right? We reduced the complexity of the system; we now serve one file for everyone, and have one build system for everyone — even customers with a custom or semi-custom template. Custom templates are just like any other template in this system.

One caveat: in order for webpack to create our dynamic bundles, we need to specify our templates in the code (by importing the specific files) or in the config. It’s not so bad, though; we can create a class that specifies the templates, and put a switch that handles the dynamic import of the templates inside:

```
class TemplatesProvider{  
    constructor() {  
          
    }  
      
    loadTemplate(config) {  
          switch(config.templateUrl) {  
            case "template1": return import('path.to.template1')  
        }   
    }  
}
```

If we create a new template, we can just add a new switch case. There are many more ways to do it, but they all involve hard-coding the templates for an import.

### So when should we NOT use webpack’s lazy load to lazy load?

Just when you think you’ve gotten away with this approach, in comes the product manager and says: “Not so fast! Customer Support needs to be able to create and edit templates on the fly.”

Press enter or click to view image in full size

![]()

A webpack module is ultimately one distinct project. In the proposed architecture, a change in the templates (an addition or update) will require deploying a new version of the module.

It won’t hurt cache, since only the changed bundle will change its hash. It ***would*** wreakhavoc in git — and you don’t want support to start meddling with git, versions and deployment. And if you’ll remember — Support will need to fiddle with our `TemplatesProvider` class in order to add a new template (or the webpack config, if we decide to declare an entry instead of the switch).

So… how do we allow Support to create and update templates without having them messing around with the main repository? Can we think of a better way to load the templates without hard-coding everything? Let’s try another architecture.

### Serve multiple webpack projects

After meddling around with a “two webpack projects” idea — one for the templates, and one for the menu/widget — it’s time to embark on a new adventure.

We will have our main widget repository. In addition, we will have a repository per template, so each template will be a webpack project in and of itself. The widget will lazy load a template according to the data received in the configuration file.

Press enter or click to view image in full size

![]()

But wait! You can’t use import for a file outside of a given webpack project! How can we lazy load when the templates are each totally different projects?

### This is when you don’t (can’t?) use webpack’s lazy loading

Lazy loading is nothing but calling scripts. You already know how to do it!

`<script src="myScript.js"></script>`

That’s it!

Webpack does it [this way](https://github.com/webpack/webpack/blob/8b0a2ad2b3298372bf09ec22017e373625f5b06a/lib/JsonpMainTemplatePlugin.js#L50):

Because webpack does this only for files that are inside the same project during the build, it won’t work for external files.

Brace yourself, though… There is a solution! We’ll just let each project’s lazy loading be handled by webpack. We can use our lazy loading knowledge to load the external templates on demand. To do so, let’s create our own lazy loading module that loads a template according to our config file:

And there we have it…

## Summary

In this article, we’ve learned the about webpack’s lazy loading and how you can use it in your webpack project. We’ve also learned the following:

* How to chunk your application using dynamic import
* How to structure your app in folders
* That “cache” rhymes with “hash”

You can see the final YOPF project [here](https://github.com/YonatanKra/YOPF/tree/lazy-load).

We saw how there are options when using webpack and exploring these options can provide insight into new architectures in real life. We also learned of a way to design a multi-webpack-projects project with our own lazy loading solution.

As with every project, a custom solution can usually be found, but it is usually easier to find a solution by looking at the solutions of others. Why reinvent the wheel?

The webpack experience continues with:

* Browser Compatibility (coming soon)