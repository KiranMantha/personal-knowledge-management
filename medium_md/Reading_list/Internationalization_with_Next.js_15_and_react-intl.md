---
title: "Internationalization with Next.js 15 and react-intl"
url: https://medium.com/p/6b67b5a2d28d
---

# Internationalization with Next.js 15 and react-intl

[Original](https://medium.com/p/6b67b5a2d28d)

# Internationalization with Next.js 15 and react-intl

[![F3S Software](https://miro.medium.com/v2/resize:fill:64:64/1*I1h7ayMkTWqTA6c6zFgKWw.png)](/@f3ssoftware?source=post_page---byline--6b67b5a2d28d---------------------------------------)

[F3S Software](/@f3ssoftware?source=post_page---byline--6b67b5a2d28d---------------------------------------)

3 min read

·

Nov 6, 2024

--

6

Listen

Share

More

There is two approaches that can be used with Next.js 15 and the library next-intl

With I18n Routing: Translate texts based on prefix-bases or domainbased routes

Without i18n Routing: Translate based on a single language based on user configurations

In this tutorial we're going to implement only the "With i18n Routing" because it's so much more dynamic. If you need to implement a translate solution more static you can check the [official docs from next-intl](https://next-intl-docs.vercel.app/docs/getting-started/app-router/without-i18n-routing).

## Routing with i18n

**Step 1: Install library next-intl with the command**

```
# Yarn   
yarn add next-intl  
# NPM  
npm install next-intl
```

**Step 2: Configure next.config.ts**

Your's next.config.ts have to be update from it's initial state like below

```
import type { NextConfig } from 'next'  
   
const nextConfig: NextConfig = {  
  /* config options here */  
}  
   
export default nextConfig
```

to this new one, where your configuration is being passed as parameter to a withNextIntl() function

```
import type { NextConfig } from "next";  
import createNextIntlPlugin from "next-intl/plugin";  
  
const withNextIntl = createNextIntlPlugin();  
  
const nextConfig: NextConfig = {};  
  
export default withNextIntl(nextConfig);
```

Step 3: Create a routing file

Into the src of your project, create a folder named i18n and inside of it create a new file named routing.ts

```
import { defineRouting } from "next-intl/routing";  
import { createNavigation } from "next-intl/navigation";  
  
export const routing = defineRouting({  
  locales: ["en", "pt"], // Define in this line the possible languages for translation  
  defaultLocale: "en", // Define in this line the default language to be shown  
});  
  
export const { Link, redirect, usePathname, useRouter } =  
  createNavigation(routing);
```

Step 4: Setup a middleware

Now create a file named middleware.ts in the src of your project

```
import createMiddleware from "next-intl/middleware";  
import { routing } from "./i18n/routing";  
  
export default createMiddleware(routing);  
  
export const config = {  
  matcher: ["/", "/(pt|en)/:path*"], // At this line, define into the matcher all the availables language you have defined into routing.ts  
};
```

**Step 5: Define a central module for Server Components**

Define a file named request.ts into your i18n folder. Based on next-intl docs this is needed for using the features of next-intl into Server Components.

```
import { getRequestConfig } from "next-intl/server";  
import { routing } from "./routing";  
  
export default getRequestConfig(async ({ requestLocale }) => {  
  let locale = await requestLocale;  
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any  
  if (!locale || !routing.locales.includes(locale as any)) {  
    locale = routing.defaultLocale;  
  }  
  
  return {  
    locale,  
    messages: (await import(`../../messages/${locale}.json`)).default,  
  };  
});
```

Step 6: Move all your project structure inside a [locale] directory into the src/app directory. Your project structure should follow this

```
├── messages  
│   ├── en.json  
│   └── pt.json  
├── next.config.ts  
└── src  
    ├── i18n  
    │   ├── routing.ts  
    │   └── request.ts  
    ├── middleware.ts  
    └── app  
        └── [locale]  
            └──... // Here comes your subfolders into routing structure
```

**Step. 7: Setup the translations dictionaries**

Now you have to define the dictionaries for each language you have configured into your routing.ts. I suggest you to divide it into contexts based on your components name for a better organization, like the example below:

```
{  
  "Home": {  
    "title": "NextJS i18n Tutorial",  
    "description": "Tutorial of how to manipulate i18n based on route path or domain with  Nextjs v15"  
  },  
  "Step1": {  
    "title": "Step 1 Title",  
    "EXPLANATION_PARAGRAPH1": "lorem ipsum"  
  },  
  "Step2": {  
    "title": "Step 2 Title",  
    "EXPLANATION_PARAGRAPH1": "lorem ipsum",  
    "EXPLANATION_PARAGRAPH2": "lorem ipsum",  
    "EXPLANATION_PARAGRAPH3": "lorem ipsum"  
  }  
}
```

**Step. 8: Use the useTranslations hook into your's component**

Now everything was ended setup you can declare into your component the useTranslations hook using the following code:

```
import { useTranslations } from 'next-intl'; // declare this import  
  
export default function HomePage() {  
    const t = useTranslations('Home'); // declare the hook passing into parameter a context name  
    return (  
        <div>  
            <h1>{t('title')}</h1> // Call the hook by passing as parameter the dictionary key you want  
        </div>  
    );  
}
```

**Conclusion**

In this tutorial, we’ve successfully walked through the essential steps for implementing internationalization (i18n) in Next.js 15 using the next-intl library with i18n routing. By setting up language-specific routes and creating a centralized configuration, we’ve enabled our application to dynamically switch between languages based on route prefixes. This approach not only enhances the user experience by providing a seamless, multilingual interface but also streamlines the localization process for developers.

With the flexibility provided by next-intl, you can easily scale this setup as your application grows, adding more languages or tailoring content to specific audiences. For those looking for a simpler, static translation solution, next-intl offers alternative configurations. Remember to explore and expand your dictionaries as your project evolves. Now you’re ready to deliver a multilingual experience that resonates with global users — good luck!