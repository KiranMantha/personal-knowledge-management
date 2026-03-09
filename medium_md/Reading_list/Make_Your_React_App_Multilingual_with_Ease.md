---
title: "Make Your React App Multilingual with Ease"
url: https://medium.com/p/c4611c4369f9
---

# Make Your React App Multilingual with Ease

[Original](https://medium.com/p/c4611c4369f9)

Member-only story

# Make Your React App Multilingual with Ease

[![PRADIP KAITY](https://miro.medium.com/v2/resize:fill:64:64/1*tD8eoRJBnyfvqXto-bXvBg.png)](https://pradipkaity.medium.com/?source=post_page---byline--c4611c4369f9---------------------------------------)

[PRADIP KAITY](https://pradipkaity.medium.com/?source=post_page---byline--c4611c4369f9---------------------------------------)

4 min read

·

Feb 9, 2025

--

2

Listen

Share

More

Press enter or click to view image in full size

![Make Your React App Multilingual with Ease — Internationalization in React with React-Intl]()

If you’re building a web application that serves users from different parts of the world, you need to think about **internationalization (i18n)**.

Manually implementing translations for multiple languages can be complex and time-consuming.

> Enjoy free access to this article with [**my Friend’s Link**](https://pradipkaity.medium.com/make-your-react-app-multilingual-with-ease-c4611c4369f9?sk=5e51d0dafff9d2202f883c9326d09a9a)— feel free to share it with others!

Fortunately, there are libraries like **React-Intl**, which simplify the process and help you integrate translations seamlessly into your React applications.

In this guide, you’ll learn how to use **React-Intl**, a powerful library from the **FormatJS** ecosystem, to translate text, format numbers and dates, and create a localized user experience.

By the end of this tutorial, you’ll be able to implement internationalization in your React app with just a few lines of code.

### Setting Up React-Intl in Your Project

Before diving into implementation, let’s set up a new React project and install **React-Intl**.

### Step 1: Create a New React App

If you haven’t already, create a new React project using Create React App:

```
npx create-react-app my-i18n-app  
cd my-i18n-app
```

### Step 2: Install React-Intl

Now, add the **react-intl** package to your project:

```
npm install react-intl
```

or if you’re using Yarn:

```
yarn add react-intl
```

### Adding Translations to Your React App

To begin translating content, define message objects containing the text for each supported language.

### Step 1: Define Translations

Inside your `src` folder, create a new file called `messages.js` and add the following code:

```
const messages = {  
  en: {  
    greeting: "Hello {name}, welcome to our website!",  
    current_time: "Current time: {time, time, short}",  
    current_date: "Today's date: {date, date, long}"  
  },  
  es: {  
    greeting: "¡Hola {name}, bienvenido a nuestro sitio web!",  
    current_time: "Hora actual: {time, time, short}",  
    current_date: "Fecha de hoy: {date, date, long}"  
  },  
  fr: {  
    greeting: "Bonjour {name}, bienvenue sur notre site web!",  
    current_time: "Heure actuelle: {time, time, short}",  
    current_date: "Date d'aujourd'hui: {date, date, long}"  
  }  
};
```

```
export default messages;
```

The curly braces `{}` inside messages allow you to pass dynamic values like a user's name or formatted date/time.

### Implementing React-Intl in Your App

Now, integrate **React-Intl** into your React component.

### Step 1: Import Dependencies

Modify `src/App.js` as follows:

```
import React, { useState } from "react";  
import { IntlProvider, FormattedMessage } from "react-intl";  
import messages from "./messages";
```

```
function App() {  
  const [locale, setLocale] = useState("en");  
  const [name, setName] = useState("User");  
  return (  
    <IntlProvider locale={locale} messages={messages[locale]}>  
      <div style={{ padding: 20 }}>  
        <h2>React-Intl Example</h2>  
          
        <label>  
          Select Language:  
          <select value={locale} onChange={(e) => setLocale(e.target.value)}>  
            <option value="en">English</option>  
            <option value="es">Español</option>  
            <option value="fr">Français</option>  
          </select>  
        </label>  
        <br /><br />  
        <label>  
          Enter Your Name:  
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />  
        </label>  
        <p>  
          <FormattedMessage id="greeting" values={{ name }} />  
        </p>  
        <p>  
          <FormattedMessage id="current_time" values={{ time: new Date() }} />  
        </p>  
        <p>  
          <FormattedMessage id="current_date" values={{ date: new Date() }} />  
        </p>  
      </div>  
    </IntlProvider>  
  );  
}  
export default App;
```

### Step 2: Understanding the Code

* **IntlProvider**: This component wraps your app and provides locale and message translations.
* **FormattedMessage**: Used to display localized text with dynamic placeholders.
* **useState**: Stores the selected language and user input.
* **Dynamic Locale Switching**: Users can change the language dynamically using a dropdown.

### Handling Pluralization and Numbers

You can also handle pluralization and number formatting with React-Intl.

### Example: Pluralization

Modify `messages.js` to add pluralization support:

```
const messages = {  
  en: {  
    item_count: "You have {count, plural, one {# item} other {# items}} in your cart."  
  },  
  es: {  
    item_count: "Tienes {count, plural, one {# artículo} other {# artículos}} en tu carrito."  
  }  
};
```

Then, update `App.js` to use **FormattedMessage** for pluralization:

```
<p>  
  <FormattedMessage id="item_count" values={{ count: 3 }} />  
</p>
```

If `count` is 1, it will say **"You have 1 item in your cart."** If `count` is 3, it will say **"You have 3 items in your cart."**

### Next Steps

* Explore the **React-Intl** [official documentation](https://formatjs.io/docs/react-intl/) for advanced features.
* Implement localization for more UI elements.
* Consider storing user preferences for locale selection.

By internationalizing your React app, you’re opening the door to a **global audience**, making your application accessible and user-friendly for people worldwide.

Thanks for Reading.

Follow me on [**Linkedin**](https://www.linkedin.com/in/pradipkaity/)&[**Medium**](https://pradipkaity.medium.com/)

[## How to Use Viewing Patterns in Your Website Designs

### Viewing patterns refer to the natural ways in which users scan and process visual information on a page.

medium.com](https://medium.com/design-bootcamp/how-to-use-viewing-patterns-in-your-website-designs-75a2de7fec36?source=post_page-----c4611c4369f9---------------------------------------)

[## No BS Topics for Frontend Developers to Master in 2025

### Modular programming with tools like Webpack and Vite.

medium.com](https://medium.com/front-end-weekly/no-bs-topics-for-frontend-developers-to-master-in-2025-17d85b200406?source=post_page-----c4611c4369f9---------------------------------------)

[## Skip the Frameworks, Learn CSS First

### True frontend mastery begins with understanding CSS deeply.

medium.com](https://medium.com/design-bootcamp/skip-the-frameworks-learn-css-first-35d36c1f83df?source=post_page-----c4611c4369f9---------------------------------------)

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)