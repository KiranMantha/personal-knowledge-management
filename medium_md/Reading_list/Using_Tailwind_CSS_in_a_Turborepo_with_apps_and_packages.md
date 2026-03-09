---
title: "Using Tailwind CSS in a Turborepo with apps and packages"
url: https://medium.com/p/5a05d2076caf
---

# Using Tailwind CSS in a Turborepo with apps and packages

[Original](https://medium.com/p/5a05d2076caf)

# Using Tailwind CSS in a Turborepo with apps and packages

[![Philipp Trentmann](https://miro.medium.com/v2/resize:fill:64:64/1*NjHkqY0ksQy0mRFYNh2lsQ@2x.jpeg)](/@philippbtrentmann?source=post_page---byline--5a05d2076caf---------------------------------------)

[Philipp Trentmann](/@philippbtrentmann?source=post_page---byline--5a05d2076caf---------------------------------------)

6 min read

·

Jul 17, 2024

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

This is a quick guide how to set up a Turbo monorepo with Tailwind CSS used in both Apps and Packages. It can be used for fresh projects as well as for existing ones.

### For Tailwind CSS version 4 check out this article!

[## Setting up Tailwind CSS v4 in a Turbo Monorepo

### A guide to set up or upgrade a monorepo with Turbo using Tailwind CSS for styling. This article includes an example…

medium.com](/@philippbtrentmann/setting-up-tailwind-css-v4-in-a-turbo-monorepo-7688f3193039?source=post_page-----5a05d2076caf---------------------------------------)

### For Tailwind version 3 stay here

First of all, if you are creating a new project the easiest way to set up a Turbo monorepo with Tailwind CSS is by using Turbo’s example with Tailwind (you can find it [here](https://github.com/vercel/turbo/tree/main/examples/with-tailwind)). ([Turbo Documentation here](https://turbo.build/repo/docs/getting-started/installation#start-with-an-example))

```
pnpm dlx create-turbo@latest --example with-tailwind
```

However, if you - like me - want to **add Tailwind CSS to an existing Turbo repo or want to include additional apps and/or packages** using Tailwind, this might still be helpful.

The project structure I am using looks like this (not including any other config packages):

```
root  
├── apps  
│   └── web  
└── packages  
    ├── tailwind-config  
    ├── design-system  
    └── ui
```

The web app is based on [Next.js](https://nextjs.org/) and for this example I use [pnpm](https://pnpm.io/), any other package manager will of course work as well.

## Adding the Tailwind Config

First we add a new package “config-tailwind”, and inside we add a `package.json` and a `tsconfig.json`

```
// tsconfig.json  
{  
  "extends": "@turbo-with-tailwind/typescript-config/react-library.json",  
  "compilerOptions": {  
    "outDir": "dist"  
  },  
  "include": ["tailwind.config.ts"],  
  "exclude": ["node_modules", "dist"]  
}
```

```
// package.json  
{  
  "name": "@turbo-with-tailwind/tailwind-config",  
  "version": "0.0.0",  
  "private": true,  
  "exports": {  
    ".": "./tailwind.config.ts"  
  },  
  "devDependencies": {  
    "@turbo-with-tailwind/typescript-config": "workspace:*",  
    "tailwindcss": "^3.4.1"  
  }  
}
```

Make sure to **use your repo name** instead of `@turbo-with-tailwind` . Finally we add a `tailwind.config.ts` file to the package. This is where all your customizations will go into (more info in the [Tailwind CSS documentation](https://tailwindcss.com/docs/configuration)).

```
import type { Config } from "tailwindcss"  
  
const config: Omit<Config, "content"> = {  
  theme: {  
    extend: {  
      colors: {  
        primary: {  
          DEFAULT: "#c094f6",  
          dark: "#522281",  
          50: "#faf6fe",  
          100: "#f2e9fe",  
          200: "#e7d7fd",  
          300: "#d5b8fa",  
          400: "#c094f6",  
          500: "#a15eee",  
          600: "#8a3de0",  
          700: "#752cc4",  
          800: "#6429a0",  
          900: "#522281",  
          950: "#360c5f",  
        },  
      },  
    },  
    plugins: [],  
  },  
}  
  
export default config
```

Note that `content` is excluded from this configuration file — we will add this in the individual config files for each app and package later.

## Get the web app ready for Tailwind CSS

Lets start and add Tailwind CSS to the app “web”. First we need to install the dependencies.

```
cd apps/web  
  
pnpm install -D tailwindcss postcss autoprefixer  
  
cd ../../
```

Now we add the `postcss.config.js` and `tailwind.config.ts` to the app ‘web’.

Press enter or click to view image in full size

![File structure after adding post css and tailwind css configuration files in app ‘web’]()

```
// postcss.config.js  
module.exports = {  
  plugins: {  
    tailwindcss: {},  
    autoprefixer: {},  
  },  
};
```

```
// tailwind.config.ts  
import type { Config } from "tailwindcss"  
import sharedConfig from "@turbo-with-tailwind/tailwind-config"  
  
const config: Pick<Config, "content" | "presets"> = {  
  content: ["./src/app/**/*.tsx"],  
  presets: [sharedConfig],  
}  
  
export default config
```

In the Tailwind config file you can see that we use the config from the ‘tailwind-config’ package as our preset and add the before mentioned `content` .   
Make sure you have the `globals.css` file in `apps/web/src/app` with at least these entries:

```
@tailwind base;  
@tailwind components;  
@tailwind utilities;
```

And it’s imported in your `layout.tsx`

```
import "./globals.css"  
  
...
```

After making sure that all dependencies have been installed, your web app should now have tailwind enabled including the customizations from our tailwind-config.

## Time for the packages to be ‘tailwinded’

Since these steps will be valid for most packages, they will only be demonstrated for the `ui` package.  
Assuming you already have this or any package we just need to (again) add the `postcss.config.js` and `tailwind.config.ts` files.

Press enter or click to view image in full size

![File structure after adding post css and tailwind css configuration files in package ‘ui’]()

Make sure to add the correct `devDependencies` **plus** the tailwind-config package in the `package.json` as well as `exports` , `sideEffects` and `files` !

```
cd packages/ui  
  
pnpm install -D tailwindcss postcss autoprefixer  
  
cd ../../
```

```
{  
  "name": "@turbo-with-tailwind/ui",  
  "version": "0.0.0",  
  "sideEffects": [  
    "**/*.css"  
  ],  
  "files": [  
    "dist"  
  ],  
  "exports": {  
    "./styles.css": "./dist/index.css",  
    "./card": "./src/card.tsx"  
  },  
  "license": "MIT",  
  "scripts": {  
    "build": "tailwindcss -i ./src/styles.css -o ./dist/index.css",  
    "lint": "eslint src/",  
    "dev": "tailwindcss -i ./src/styles.css -o ./dist/index.css --watch",  
    "type-check": "tsc --noEmit"  
  },  
  "peerDependencies": {  
    "react": "^18.2.0"  
  },  
  "devDependencies": {  
    "@turbo-with-tailwind/eslint-config": "workspace:*",  
    "@turbo-with-tailwind/tailwind-config": "workspace:*",  
    "@turbo-with-tailwind/typescript-config": "workspace:*",  
    "@types/react": "^18.2.61",  
    "autoprefixer": "^10.4.18",  
    "postcss": "^8.4.35",  
    "tailwindcss": "^3.4.1",  
    "typescript": "^5.3.3"  
  }  
}
```

Now we can fill the config files, similar to the ones in the app.

```
// postcss.config.js  
module.exports = {  
  plugins: {  
    tailwindcss: {},  
    autoprefixer: {},  
  },  
};
```

```
// tailwind.config.ts  
import type { Config } from "tailwindcss"  
import sharedConfig from "@turbo-with-tailwind/tailwind-config"  
  
const config: Pick<Config, "prefix" | "presets" | "content"> = {  
  content: ["./src/**/*.tsx"],  
  prefix: "ui-",  
  presets: [sharedConfig],  
}  
  
export default config
```

In the `tailwind.config.ts` file it’s important that the `content` **points to the correct folder with your components**. I added a prefix `ui-` for CSS classes, which is also recommended by Tailwind. This helps in general to prevent colliding class names in generated utility classes, but in my use case, it makes debugging easier. Seeing prefixed class names with `ui-` and `ds-` immediately shows the origin of the component. It comes with the cost of having to manually prefix all Tailwind class names in the different packages. If you don’t need/want prefixing you can just delete that line.

Finally we add a `styles.css` file to the `src` folder which should again at least include these lines

```
@tailwind base;  
@tailwind components;  
@tailwind utilities;
```

As you can see from the `build` script in the `package.json` the `index.css` file will be compiled into the `dist` folder from where it will be exported.

```
"build": "tailwindcss -i ./src/styles.css -o ./dist/index.css",
```

```
"exports": {  
    "./styles.css": "./dist/index.css",  
  },
```

## Making sure Next.js transpiles the packages

The final steps are necessary to make sure the Next.js app transpiles the packages ( `ui` and `design-system` ) and that the CSS of the packages is imported.

In the `next.config.js` file you need to add the following line (or add new packages)

```
transpilePackages: [  
  "@turbo-with-tailwind/design-system",   
  "@turbo-with-tailwind/ui"  
],
```

```
/** @type {import('next').NextConfig} */  
module.exports = {  
  reactStrictMode: true,  
  transpilePackages: [  
    "@turbo-with-tailwind/design-system",  
    "@turbo-with-tailwind/ui",  
  ],  
}
```

**Make sure the UI package dependencies were added** to your `package.json` in the web app.

```
  "dependencies": {  
    "@turbo-with-tailwind/design-system": "workspace:*",  
    "@turbo-with-tailwind/ui": "workspace:*",  
    "next": "^14.2.3",  
    "react": "^18.2.0",  
    "react-dom": "^18.2.0"  
  },
```

Last step is to include the compiled and exported CSS from each package in the web app.

```
import "./globals.css"  
import "@turbo-with-tailwind/design-system/styles.css"  
import "@turbo-with-tailwind/ui/styles.css"  
  
...
```

## Debugging

* **Make sure you ran** `pnpm install` **in the root directory**
* **Make sure all packages are imported correctly**
* **Double check the folder/path the** `content` **points to in all** `tailwind.config.ts` **files**
* **Are all CSS files imported in your** `layout.tsx` **?**
* **Did you add the transpiler option in the** `next.config.js` **?**
* **In case you use prefixed class names, did YOU use the prefix in the components’ className?**

## Find the example repo here

[## GitHub - philipptpunkt/turbo-with-tailwind: Based on Turbo's example, this is an extention of the…

### Based on Turbo's example, this is an extention of the "with-tailwind" example - philipptpunkt/turbo-with-tailwind

github.com](https://github.com/philipptpunkt/turbo-with-tailwind?source=post_page-----5a05d2076caf---------------------------------------)