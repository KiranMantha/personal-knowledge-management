---
title: "When to use Angular’s forRoot() method"
url: https://medium.com/p/400094a0ebb7
---

# When to use Angular’s forRoot() method

[Original](https://medium.com/p/400094a0ebb7)

# When to use Angular’s forRoot() method

[![Chris House](https://miro.medium.com/v2/resize:fill:64:64/0*LMF-x9Gw7j5PSc0z.)](/@chrishouse?source=post_page---byline--400094a0ebb7---------------------------------------)

[Chris House](/@chrishouse?source=post_page---byline--400094a0ebb7---------------------------------------)

2 min read

·

Nov 6, 2017

--

10

Listen

Share

More

**Problem**: We needed to share a singleton language service across all lazy loaded modules. For a year, I saw the forRoot() method and simply ignored its power.

**Explanation**: The `forRoot()` method returns an `NgModule` and its provider dependencies.

In this example, we are sharing a service to keep up with a counter value. Each time any component increments the value stored in the counter service, I want to share this with all components.

The issue is when you try to introduce lazy loaded modules. Notice how the Lazy loaded component does not share the same counter value. When using eager loaded components only, the below example will work if you use a shared service, but notice how the lazy loaded component behaves. The lazy component gets its own instance of the service.

```
import { NgModule } from '@angular/core';  
import { CounterService } from './counter.service';@NgModule({  
  providers: [CounterService],  
})  
export class SharedModule {}
```

See plunker: [https://stackblitz.com/edit/angular-no-for-root-72x3ht?file=app/lazy/lazy.component.ts](https://stackblitz.com/edit/angular-no-for-root-72x3ht?file=app%2Flazy%2Flazy.component.ts)

**Solution**: Call *forRoot()* in the AppModule and return a ModuleWithProviders in the sharedModule.

**shared.module.ts**

```
import { NgModule,ModuleWithProviders  } from '@angular/core';  
import { CounterService } from './counter.service';@NgModule({})  
export class SharedModule {  
  static forRoot(): ModuleWithProviders {  
    return {  
      ngModule: SharedModule,  
      providers: [ CounterService ]  
    }  
  }  
}
```

**app.module.ts**

```
import { NgModule } from '@angular/core';  
import { BrowserModule  } from '@angular/platform-browser';import { SharedModule } from './shared/shared.module';import { AppComponent } from './app.component';  
import { EagerComponent } from './eager.component';  
import { routing } from './app.routing';@NgModule({  
  imports: [  
    BrowserModule,  
    SharedModule.forRoot(),  
    routing  
  ],  
  declarations: [  
    AppComponent,  
    EagerComponent  
  ],  
  bootstrap: [AppComponent]  
})  
export class AppModule {}
```

See Plunker: <https://stackblitz.com/edit/angular-no-for-root-yfhkgz?file=app%2Fapp.module.ts>

Now the counter service is shared between eagerly loaded modules and lazy loaded modules.

Other recommended readings: <http://angularfirst.com/the-ngmodule-forroot-convention/>

* *Note: I would not recommend putting shared services and shared directives in the same module. I have written this article as a reference for myself in the future.*

Other articles:  
 [Use a Robot to upgrade your node dependencies](/@chrishouse/use-a-robot-to-upgrade-your-node-dependencies-bf679719a30e)

[Angular AsyncValidators](/slackernoon/angular-forms-and-aync-validator-functions-a663b01e9832)