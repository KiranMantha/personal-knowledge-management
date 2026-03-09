---
title: "Tailwind in React Native? Here’s the Truth!"
url: https://medium.com/p/55c48e1725a3
---

# Tailwind in React Native? Here’s the Truth!

[Original](https://medium.com/p/55c48e1725a3)

Member-only story

# Tailwind in React Native? Here’s the Truth!

[![Sunny Prakash](https://miro.medium.com/v2/resize:fill:64:64/1*uEXMlwNl9bqblzPzwkZpZA.jpeg)](https://sunny-prakash.medium.com/?source=post_page---byline--55c48e1725a3---------------------------------------)

[Sunny Prakash](https://sunny-prakash.medium.com/?source=post_page---byline--55c48e1725a3---------------------------------------)

5 min read

·

Mar 7, 2025

--

Listen

Share

More

If you’re a mobile developer working with React Native, chances are you’ve had at least one “Why is managing StyleSheet objects and inline styles such a nightmare?” moment. Meanwhile, over in the “Web Development world”, developers are happily using something called **Tailwind**, which makes styling feel less like a chore and more like a breeze. I mean take a look at the benefits you get -

* **Responsive Design**: Utility classes to create adaptive layouts easily
* **Theming support**: Works well with dark mode and dynamic styles
* **Productivity Boost**: Faster styling without writing long StyleSheet object
* **No Context Switching:** Avoid switching between JSX and stylesheets, keeping your workflow streamlined.

So, can you just slap Tailwind into your React Native app and call it a day? The answer is… ***NO****.* At least, not directly. But don’t lose hope just yet! Let’s take a look at why Tailwind doesn’t play nice with React Native out of the box — and then, I’ll let you in on a secret that might just save the day.

* **Tailwind CSS is Designed for the Web**: Tailwind CSS generates utility classes that are meant to be used in HTML and CSS for web applications. React Native, on the other hand, uses a completely different styling system that doesn’t rely on CSS or HTML. Instead, React Native uses a JavaScript-based StyleSheet objects.
* **No CSS in React Native**: React Native doesn’t support CSS or class names. Styles in React Native are applied using JavaScript objects, and there’s no concept of CSS selectors, classes, or global styles.
* **Different Syntax and Units**: Tailwind uses web-specific units (e.g. px, rem, %) and properties (e.g. display: flex, grid, hover:). React Native uses a subset of CSS-like properties with different syntax and units (e.g. flexDirection, paddingHorizontal, no hover states).
* **Dynamic Styling Needs JavaScript** — Tailwind generates styles via a PostCSS plugin that outputs static CSS classes, while React Native requires inline styles or a JavaScript-based styling system.

Alright… so if Tailwind doesn’t work with React Native, why does this post even exist? *To introduce you to* ***NativeWind****!* 😎

Wait, what the… who? Another library? Yep! But hold on — this isn’t *just* another library. NativeWind lets you style React Native apps using Tailwind CSS, bringing all the goodness of utility-first styling to mobile development.

Remember all those Tailwind benefits I explained earlier? Well, NativeWind delivers the same experience — just for React Native. If you’re still with me and curious to see if this thing actually lives up to the hype, let’s dive into some hands-on coding and find out! 🚀

## Setting up NativeWind

Lets go step by step to setup NativeWind into an Expo project. And yes I am using expo because it is way better than using Bare React Native.

If you are starting from the scratch then best way to setup everything would be to use recommended boilerplate template by running below command -

```
npx create-expo-stack@latest --nativewind
```

But if you already have a project then follow along -

### 1. Install NativeWind and required packages

```
npx expo install nativewind tailwindcss@^3.4.17 react-native-reanimated@3.16.2 react-native-safe-area-context
```

### 2. Setup Tailwind CSS

Run `npx tailwindcss init` to create a `tailwind.config.js` file. Add the paths to all of your component files in your tailwind.config.js file.

```
/** @type {import('tailwindcss').Config} */  
module.exports = {  
  // NOTE: Update this to include the paths to all of your component files.  
  content: ["./app/**/*.{js,jsx,ts,tsx}"],  
  presets: [require("nativewind/preset")],  
  theme: {  
    extend: {},  
  },  
  plugins: [],  
}
```

### 3. Import global CSS file

Create a `global.css` in your app directory and add below directives.

```
@tailwind base;  
@tailwind components;  
@tailwind utilities;
```

> Don’t forget to import global.css file at the very top of your base `_layout.tsx`

### 4. Adjust metro.config.js

```
metro.config.js  
  
const { getDefaultConfig } = require("expo/metro-config");  
const { withNativeWind } = require('nativewind/metro');  
  
const config = getDefaultConfig(__dirname)  
  
module.exports = withNativeWind(config, { input: './global.css' })
```

### 5. Add the babel preset

```
module.exports = function (api) {  
  api.cache(true);  
  return {  
    presets: [  
      ["babel-preset-expo", { jsxImportSource: "nativewind" }],   
      "nativewind/babel"  
    ],  
    plugins: ["react-native-reanimated/plugin"],  
  };  
};
```

### 6. Switch to Metro bundler

Adjust your `app.json` to use bundler as Metro bundler.

```
{  
  "expo": {  
    "web": {  
      "bundler": "metro"  
    }  
  }  
}
```

### 7. Usage with TypeScript

If you would like to import types then simply create a `nativewind-env.d.ts` at the root of your directory and add below reference to it

```
/// <reference types="nativewind/types" />
```

After following these steps, you’re all set to use Tailwind — *ahem* — I mean, NativeWind in your React Native app.

Oh, and here’s a little bonus for you! If you’re using Visual Studio Code, do yourself a favor and grab the [***Tailwind CSS extension***](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss). It’ll give you code snippet IntelliSense, so you can write styles faster and with fewer typos Because let’s be real, nobody enjoys debugging class names 😜.

Press enter or click to view image in full size

![]()

## When should you not use NativeWind?

Alright, enough of the *everything’s amazing* talk — let’s get real for a second. NativeWind might not be the perfect solution if…

* You prefer writing styles using React Native’s `StyleSheet` or a different styling solution (e.g., Styled Components).
* You’re working on a small project where the overhead of setting up NativeWind isn’t justified.
* You need highly customized styles that don’t align with Tailwind’s utility-first approach.

## Conclusion

While you can’t use Tailwind CSS directly with React Native/Expo, **NativeWind** provides a seamless way to bring Tailwind’s utility-first styling to your React Native projects. It simplifies the styling process, improves code readability, and maintains consistency across platforms. If you’re a fan of Tailwind CSS and want to use it in your Expo projects, NativeWind is the way to go.

However, if you’re comfortable with React Native’s built-in styling system or prefer a different approach, you might not need NativeWind. Ultimately, the choice depends on your workflow, project requirements, and familiarity with Tailwind CSS.

And that’s a wrap folks! Stay healthy and *keep reading*. 📖

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Differ**](https://differ.blog/inplainenglish)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)