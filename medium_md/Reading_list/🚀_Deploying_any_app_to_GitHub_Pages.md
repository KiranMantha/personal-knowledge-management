---
title: "🚀 Deploying any app to GitHub Pages"
url: https://medium.com/p/1e8e946bf890
---

# 🚀 Deploying any app to GitHub Pages

[Original](https://medium.com/p/1e8e946bf890)

Member-only story

# 🚀 Deploying any app to GitHub Pages

[![Chetan Raj](https://miro.medium.com/v2/resize:fill:64:64/1*iD7glZR-CwR-H_CwfKYg-A.png)](https://chtn.medium.com/?source=post_page---byline--1e8e946bf890---------------------------------------)

[Chetan Raj](https://chtn.medium.com/?source=post_page---byline--1e8e946bf890---------------------------------------)

3 min read

·

Aug 22, 2020

--

Listen

Share

More

Press enter or click to view image in full size

![]()

[GitHub Pages](https://pages.github.com/) is a website holder for you & your projects. You can host your code directly from your GitHub repo. This article will help you how to manage your app in the `master` branch and deploy the code in the `gh-pages` branch easily.

You can choose any front-end framework like [React](https://reactjs.org/), [Vue](https://vuejs.org/), [Gatsby](http://gatsbyjs.com/), [Next](https://nextjs.org/), [Nuxt](https://nuxtjs.org/), [Gridsome](https://gridsome.org/), and build the app in the master branch and build the code using the `npm run build` command and host directly using the `gh-pages` branch.

The quickest way to put your app to GitHub Pages is by using a package — [gh-pages](https://github.com/tschaub/gh-pages).

[## tschaub/gh-pages

### Publish files to a gh-pages branch on GitHub (or any other branch anywhere else). npm install gh-pages — save-dev This…

github.com](https://github.com/tschaub/gh-pages?source=post_page-----1e8e946bf890---------------------------------------)

```
npm i gh-pages -D
```

Or you can install the package globally:

```
npm i gh-pages -g
```

Add this simple script to your **package.json**:

```
{  
  "scripts": {  
    "deploy": "npm run build && gh-pages -d dist"  
  }  
}
```

**Note**: Assuming the build folder to be `dist`.

When you run `npm run deploy` all the contents of the build folder will be pushed to your repository’s gh-pages branch.

## If you are creating a User page in GitHub

Create a repository with your username like `username.github.io`, Create a branch called `code` or you can name the branch anything. Build the app in this branch and when it comes to deploying the app use the `gh-pages`command to push the build folder contents to the gh-pages branch

***Note****: In this case, you need to push your build directory to* `master` *branch, use the following command*

```
{  
  "scripts": {  
     "deploy": "npm run build && gh-pages -d dist -b master",  
  }  
}
```

After running `npm run deploy` you should see your website at `http://username.github.io`.

Run **gh-pages — help** to list all the supported options of the gh-pages package.

## Useful npm scripts of gh-pages

If your source code of the app is in a private repository, create a public repository named about, the source code will reside in the private repository and the static content generated from the build will go into the public repository

```
{  
  "scripts": {  
    "deploy": "npm run build && gh-pages -d dist --repo <url>",  
  }  
}
```

Deploy to another branch [which is not gh-pages]:

```
{  
  "scripts": {  
    "deploy": "gridsome build && gh-pages -d dist -b master",  
  }  
}
```

To include dotfiles while pushing the changes to the branch:

```
{  
  "scripts": {  
    "deploy": "npm run build && gh-pages -d dist -t"  
  }  
}
```

To change the commit message when publishing the change:

```
{  
  "scripts": {  
    "deploy": "npm run build && gh-pages -d dist -m Build v1"  
  }  
}
```

### JavaScript In Plain English

Did you know that we have three publications and a YouTube channel? Find links to everything at [**plainenglish.io**](https://plainenglish.io/)!