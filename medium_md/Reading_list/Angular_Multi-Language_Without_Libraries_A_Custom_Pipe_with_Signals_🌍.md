---
title: "Angular Multi-Language Without Libraries: A Custom Pipe with Signals 🌍"
url: https://medium.com/p/c1c18482fe77
---

# Angular Multi-Language Without Libraries: A Custom Pipe with Signals 🌍

[Original](https://medium.com/p/c1c18482fe77)

# Angular Multi-Language Without Libraries: A Custom Pipe with Signals 🌍

[![Ilenia Scala](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*HwXT_fYYIB1H0d2u)](https://medium.com/@ilenia.scala?source=post_page---byline--c1c18482fe77---------------------------------------)

[Ilenia Scala](https://medium.com/@ilenia.scala?source=post_page---byline--c1c18482fe77---------------------------------------)

3 min read

·

Mar 28, 2025

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

## Introduction

When developing a multi-language application in Angular, one of the crucial aspects is managing translations efficiently. In this article, I will show you how to create a **Pipe** for dynamic translation that allows seamless and reactive language switching, leveraging the power of Angular Signals.

**Everything is managed entirely on the Frontend!** We do not use external API calls to retrieve translations but store them directly in JSON files within the application. This ensures **maximum speed and independence from the backend**.

## Creating the Translation Pipe

**Pipes** in Angular are powerful tools for transforming data directly in templates. We will create a pipe called `TranslatePipe` that utilizes a **translation service** to return the translated value.

## Pipe Code

```
import { Pipe, PipeTransform } from '@angular/core';  
import { TranslationService } from '../services/languageService.service';  
  
@Pipe({  
  name: 'translate',  
  pure: false // Allows automatic recalculation when the language changes  
})  
export class TranslatePipe implements PipeTransform {  
  constructor(private translationService: TranslationService) {}  
  
  transform(value: string): string {  
    return this.translationService.translate(value);  
  }  
}
```

> **Why** `pure: false`**?** Setting this property ensures Angular re-executes the pipe whenever the language changes, preventing translation update issues in templates.

## Implementing the Translation Service

Now, let’s create a **translation service** that manages supported languages and provides the correct translation. All translations are **loaded directly from the Frontend**, with no need for API calls!

```
import { computed, Injectable, Signal, signal } from '@angular/core';  
import * as en from '../../../../src/assets/i18n/en.json';  
import * as ita from '../../../../src/assets/i18n/ita.json';  
  
@Injectable({  
  providedIn: 'root'  
})  
export class TranslationService {  
  private language = signal<'ita' | 'en'>('ita'); // Default language  
  
  private translations = computed(() => {  
    return this.language() === 'ita' ? ita : en;  
  });  
  
  setLanguage(lang: 'ita' | 'en') {  
    this.language.set(lang);  
  }  
  
  translate(key: string): string {  
    const translations = this.translations() as Record<string, string>;  
    return translations[key] || key;  
  }  
}
```

> **Using Signals:** We use `signal` and `computed` to ensure language changes automatically update translations **without ever making HTTP requests**.

## Using It in a Template

Now we can use the **pipe** directly in Angular templates.

```
<h1>{{ 'HELLO' | translate }}</h1>  
<p>{{ 'WELCOME' | translate }}</p>  
  
<!-- Buttons to change language -->  
<button (click)="changeLang('ita')">🇮🇹 Italiano</button>  
<button (click)="changeLang('en')">🇬🇧 English</button>
```

> When the user clicks a button, the application language changes, and texts update automatically **without interacting with a backend**.

## Integrating into a Component

Finally, let’s manage language switching within an Angular component.

```
import { ChangeDetectorRef, Component, OnInit, inject } from '@angular/core';  
import { TranslationService } from '../services/languageService.service';  
  
@Component({  
  selector: 'app-dashboard',  
  templateUrl: './dashboard.component.html',  
  styleUrls: ['./dashboard.component.scss']  
})  
export class DashboardComponent implements OnInit {  
  translationService = inject(TranslationService);  
  
  constructor(private cdr: ChangeDetectorRef) {  
  }  
  
  ngOnInit() {}  
  
  changeLang(lang: 'ita' | 'en') {  
    this.translationService.setLanguage(lang);  
    this.cdr.detectChanges();  
  }  
}
```

> **We force change detection (**`detectChanges`**)** to ensure Angular updates the templates with the new language.

## Conclusion

We have created a **dynamic translation pipe** that leverages Signals to enable smooth and reactive language switching. **All translations are managed entirely on the Frontend**, avoiding API calls and improving performance.

✅ **Advantages of this approach:**

* 🚀 **Zero HTTP calls:** everything is handled locally
* ⚡ **Instant language switching** with no network delay
* 📂 **Simple JSON file management** directly in the project
* 🔧 **Easy maintenance** and scalability

This approach is scalable, easy to maintain, and allows you to have a high-performance multi-language app without the need for external libraries like ngx-translate.

🔥 If you found this article useful, follow me for more insights on Angular and frontend development! 🚀

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/@InPlainEnglish) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Differ**](https://differ.blog/inplainenglish) | [**Twitch**](https://twitch.tv/inplainenglish)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)