---
title: "Work with Vite and NX"
url: https://medium.com/p/af2e5a7558cb
---

# Work with Vite and NX

[Original](https://medium.com/p/af2e5a7558cb)

# Work with Vite and NX

[![David Meir-Levy](https://miro.medium.com/v2/resize:fill:64:64/0*DQzQU0-6TD9gA6J3.)](/@davidmeirlevy?source=post_page---byline--af2e5a7558cb---------------------------------------)

[David Meir-Levy](/@davidmeirlevy?source=post_page---byline--af2e5a7558cb---------------------------------------)

4 min read

·

Sep 21, 2022

--

2

Listen

Share

More

This practical post will help you combine Vite with the NX monorepo tool.

Press enter or click to view image in full size

![]()

Follow those steps and you’ll see it working as expected.  
Note: I’m not a yarn fan, so I’ll use the npm commands, but you can switch to yarn if you like.

## I recommend using @nxext/vite

I checked several generators and this package was the better one (I can’t say “best”, but better).

**Note**: replace the word “vite” with “react” / “preact” / “svelte” / “solid” if you’re using one of them, for both install and “generate” operations.  
If you’re using vanilla JS or Vue (like me, copy the commands as mentioned).

run to install:

```
npm install @nxext/vite --save-dev
```

then to generate your app:

```
nx g @nxext/vite:app my-app
```

## Upgrade Vite version

I always prefer to use the latest stable version of vite, because it has many upgrades and speed improvements each version, and also — don’t trust the updates of custom NX generators to do it for you.

At the time I’m writing this post, the latest version is 3.1.0, and I used it in my code, but feel free to get a newer version

run:

```
npm i --save-dev vite
```

## Override Vite version

the generator and several other internal libraries are using different versions of vite in their own dependencies.   
In order to avoid it, and to make sure your package.json is the one that sets the rules, and also to avoid npm install errors — make sure your package.json file includes an override for the vite version, such as:

```
{  
  "name": "my-nx-monorepo",  
  "dependencies": {...},  
  "overrides": {  
    "vite": "^3.1.0"  
  }  
}
```

## Vitest is also necessary

unless you’re coding a PHP website for your uncle’s pet shop, you probably want and need to write tests for your app.

Install the vitest executor:

```
npm install @nxext/vitest -D
```

then init the generator:

```
nx g @nxext/vitest:init
```

It will create a **vitest.config.ts** file in your repository root folder.  
It can be reused for all applications in the monorepo.

## Let’s run the vite application

The `@nxext/vite` executor is coming with a built-in default `vite.config.ts` file under the hood. if you’ll use the react / solid/ svelte / preact executor, they will contain a default configuration for those frameworks, but even then I recommend overriding it with your own config file.

Create a `vite.config.ts` file inside your vite app, and put the vite configurations you like.

As a Vue developer, for me it looks like this:

```
import { defineConfig } from 'vite'  
import vue from '@vitejs/plugin-vue'export default defineConfig({  
     plugins: [vue()]  
 })
```

**Note**: if you’re also a Vue developer, don’t forget to install the necessary packages from npm:

```
npm i -D @vitejs/plugin-vue vue
```

## Don’t forget vitest.config.ts !

In most of the time, it’s a file that imports the actual `vite.config.ts` and then overrides several parts. e.g.:

```
import { defineConfig } from 'vitest/config'  
import config from './vite.config'export default defineConfig({  
  ...config,  
  test: { // you need those configs. thank me later:  
    globals: true,  
    environment: 'jsdom'  
  }  
})
```

## Here are some missing TS configs

go to `tsconfig.spec.json` (the TS config of the tests!) and make sure `compilerOptions.types` includes `vitest/globals` .  
It should look like this:

```
{  
  "extends: "./tsconfig.json",  
  "compilerOptions": {  
    ...  
    "types": ["vitest/globals", "node"]  
  }  
  ...  
}
```

Without this change, your IDE will not recognize the global ***vitest*** functions and test utils (such as `describe` , `it` , `expect` , etc).

## Every app has a *project.json* to modify

The `project.json` file includes the description of each executor that binds to a folder (your app).  
Because we’ve added `vite.config.ts` and `vitest.config.ts` , we must now mention those files inside our `project.json` configuration.

go to **build** and **serve** targets, and make sure everyone's `options` contains a `configFile` that specify the config path.

It might look like this:

```
{  
  "$schema": "../../node_modules/nx/schemas/project-schema.json",  
  ...  
  "targets": {  
    "build": {  
      ..  
      "options": {  
        ..  
        "configFile": "libs/my-app/vite.config.ts"  
      }  
      "configurations": { ... }  
    },  
    "serve": {  
      ..  
      "options": {  
        ..  
        "configFile": "libs/my-app/vite.config.ts"  
      }  
      "configurations": { ... }  
    }  
    ...  
  }
```

On the same file, also find the `test` target, and copy it.  
I prefer to add a target called `test-watch` , so the original will be used for a “regular” single run, and the “watch” will be used by developers (with filesystem watch obviously).

Those tests targets should look like this:

```
{  
  "$schema": "../../node_modules/nx/schemas/project-schema.json",  
  ...  
  "targets": {  
    "test": {  
      ..  
      "options": {  
        "command": "run",  
        "vitestConfig": "libs/my-app/vitest.config.ts",   
        "passWithNoTests": true  
      }  
    },  
    "test-watch": {  
      ..  
      "options": {  
        "command": "watch",  
        "vitestConfig": "libs/my-app/vitest.config.ts",   
        "passWithNoTests": true  
      }  
    }  
    ...  
  }
```

Notice the “**command**” property, it will be added the `vitest` cli as the second argument. `run` means a one-time run, and `watch` will run and wait for changes in files.

## Edit: Additional changes for Vue + Vitest

When you write Vue components using the `<script setup>` feature, the unit tests work as expected, but if you don’t use the `setup` attribute, the TS IntelliSense doesn’t recognize the interface of the file.

The first solution is to return the component object wrapped with `defineComponent({ .. })` , but it’s weird to add it just for the unit tests when it’s not actually necessary in “real code”.

**The solution:**

Create `vite-env.d.ts` and `vitest-env.d.ts`files inside the project’s `src` folder.

`src/vite-env.d.ts` :

```
/// <reference types="vite/client" />  
  
declare module '*.vue' {  
  import type { DefineComponent } from 'vue';  
  const component: DefineComponent<{}, {}, any>;  
  export default component;  
}
```

`src/vitest-env.d.ts` :

```
/// <reference types="vitest" />
```

Now, inside your project, look for the `tsconfig.spec.json` file, and add the bolded line into the `include` array:

```
{  
  "extends": "./tsconfig.json",  
  ...  
  "include: [  
    ...  
    "**/*.d.ts" // <<-- add this line  
  ]
```

## Good luck!

Share your successes or failures in the comments so we can all learn.

## Who am I?

**David Meir-Levy**, a coffee-to-code converter.