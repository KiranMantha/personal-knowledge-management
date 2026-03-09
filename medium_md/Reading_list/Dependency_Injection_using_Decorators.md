---
title: "Dependency Injection using Decorators"
url: https://medium.com/p/77dd4c89968e
---

# Dependency Injection using Decorators

[Original](https://medium.com/p/77dd4c89968e)

Member-only story

# Dependency Injection using Decorators

[![Chidume Nnamdi](https://miro.medium.com/v2/resize:fill:64:64/1*pXClPxHH6zeWUrFWPJSmCw.png)](https://kurtwanger40.medium.com/?source=post_page---byline--77dd4c89968e---------------------------------------)

[Chidume Nnamdi](https://kurtwanger40.medium.com/?source=post_page---byline--77dd4c89968e---------------------------------------)

13 min read

·

Aug 16, 2018

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

## Tip: Share and reuse Angular Components

Use [**Bit**](https://bit.dev/?utm_medium=content&utm_source=bitsandpieces&utm_content=9&utm_campaign=aug19) to encapsulate Angular components with all their dependencies and setup. Share them in [Bit’s cloud](https://bit.dev/?utm_medium=content&utm_source=bitsandpieces&utm_content=9&utm_campaign=aug19), collaborate with your team and use them anywhere.

[![]()](https://bit.dev)

## Dependency Injection: Whatever It Is

First, let’s start by knowing what **dependency** actually mean.

A **dependency** is a piece of code (either a library, class, object or any other data type) required by another piece of code to work.

> Put simply, if **module A** requires **module B** to run, then, **module B** is a dependency of **module A**. — Asim Hussain

For example, let’s say we have this:

```
class Http {}class FoodService {  
    constructor() {  
        this.http = new Http()  
    }  
    getFoods() {  
        return this.http.get(`localhost:3000/foods`)  
    }  
}
```

Looking at the above code, `FoodService` constructs an object of the class `Http`, in order to fetch the list of foods in `getFoods` method. You see here, FoodService needs the help/services of `Http` to work perfectly. So, `Http` is a dependency of `FoodService`. It can't do without `Http`.

The above implementation is quite bad, no worries, we will come to it later.

Next, what is **dependency injection**?

This is a technique where the piece of code (dependency) needed by another code to run is supplied by an external module. This external module/code is called the **Injector**.

> ***Dependency Injection*** *is a technique whereby one object( or static method) supplies the dependencies of another object. —* [***Wikipedia***](https://wikipedia.org/wiki/Dependency_Injection)
>
> ***Injection*** *is the passing of a dependency to a dependent object. —* [***Wikipedia***](https://wikipedia.org/wiki/Dependency_Injection)

Coming back to our dependency example we did earlier:

```
class Http {}class FoodService {  
    constructor() {  
        this.http = new Http()  
    }  
    getFoods() {  
        return this.http.get(`localhost:3000/foods`)  
    }  
}
```

This implementation is very **bad**. Why?

* Hard to re-use
* Hard to test
* Hard to maintain
* Tightly-coupled

We can actually re-write the code so that FoodService doesn’t have to create `Http` instance by itself. The object should be supplied by an external code:

```
class Http {}class FoodService {  
    constructor(private http: Http()) {  
    }  
    getFoods() {  
        return this.http.get(`localhost:3000/foods`)  
    }  
}
```

The `Http` class is now supplied via the constructor. Now, `FoodService` is now de-coupled from `Http`. `Http`, hence, is now supplied by an external factor. How the `Http` class is instantiated or how it is to be constructed is of no concern to `FoodService`.

This implementation is **better**, why?

* Decoupled
* Easier to test
* Easy maintainability

We have seen in a little detail how DI works and the importance of it. In the later sections, we will implement our own DI framework to better demonstrate the mechanics.

*Credit/Further Reading:* [*Angular: From Theory To Practice*](https://www.amazon.com/Angular-Practice-applications-tomorrow-framework-ebook/dp/B01N9S0CZN)

Angular is famous for its heavy use of DI to resolve and create dependencies for its classes. In the next section, we will look into the Angular DI framework.

## Angular DI framework

Angular uses the concept of `providers` to configure injectors:

```
@NgModule({  
  ...  
➥providers: [MailService, HttpService],  
})  
export class AppModule { }
```

During bootstrapping of an Angular app, it feeds the Injector class with classes to resolve and create their instances:

```
i0.ɵmod([  
        i0.ɵmpd(512, i0.ComponentFactoryResolver, i0.ɵCodegenComponentFactoryResolver, [  
            [8, [i3.AppComponentNgFactory]],  
            [3, i0.ComponentFactoryResolver], i0.NgModuleRef  
        ]),   
➥      i0.ɵmpd(4608, i3.MailService, i3.MailService, []),  
➥      i0.ɵmpd(4608, i3.HttpService, i3.HttpService, []),  
        ...  
        i0.ɵmpd(5120, i0.LOCALE_ID, i0.ɵm, [  
            [3, i0.LOCALE_ID]  
        ])  
])
```

The ɵ-suffixed methods are from the Angular core library. They are written as so by the Angular compiler to reduce file size during minification and bundling. The ɵmpd refers to `moduleProvideDef` and ɵmod => moduleDef. All functions reside in `@angular/core/src/view/ng_module.ts`. The moduleProvideDef takes in NodeFlags, ctor, and deps. NodeFlags denotes how the class is to be instantiated.

```
export const enum NodeFlags {  
...  
  TypeValueProvider = 1 << 8,  
  TypeClassProvider = 1 << 9,  
  TypeFactoryProvider = 1 << 10,  
  TypeUseExistingProvider = 1 << 11,  
...  
}
```

Either from a class `useClass` or from a value `useValue` or from a factory `useFactory`. The mpd returns an object that contains the token and deps of the provider. The mod function aggregates all the providers' array into a provider object. This provider object is parsed during bootstrapping of an Angular app in the initNgModule function and the instances are created and stored in the \_providers property of the NgModuleDef created from the NgModuleFactory. So when an instance is needed from the NgModule, the injector property of the NgModuleRef is accessed and the get method called, which parse through the instances in the \_properties using the token provided as the key to retrieve the corresponding instance.

```
const mailService = ngModuleRef.injector.get(MailService)  
const appRef = moduleRef.injector.get(ApplicationRef) as ApplicationRef;
```

Let’s say we have our AppComponent class dependent on the MailService class to send emails to clients.

```
@Component({  
...  
})  
export class AppComponent {  
➥  constructor(private mailService: MailService){}  
    sendMail(){  
        this.mailService.sendMail_()  
    }  
}
```

During the creation of the AppComponent instance following createViewNodes call in createDirectiveInstance function. The MailService dependency is resolved from the component’s NgModule \_providers array.

```
// @angular/core/src/view/provider.tsexport function createDirectiveInstance(view: ViewData, def: NodeDef): any {  
  // components can see other private services, other directives can't.  
  const allowPrivateServices = (def.flags & NodeFlags.Component) > 0;  
  // directives are always eager and classes!  
➥const instance = createClass(  
      view, def.parent !, allowPrivateServices, def.provider !.value, def.provider !.deps);  
'''  
}function createClass(  
    view: ViewData, elDef: NodeDef, allowPrivateServices: boolean, ctor: any, deps: DepDef[]): any {  
  const len = deps.length;  
  switch (len) {  
    case 0:  
      return new ctor();  
➥  case 1:  
      return new ctor(resolveDep(view, elDef, allowPrivateServices, deps[0]));  
...  
}  
export function resolveDep(  
    view: ViewData, elDef: NodeDef, allowPrivateServices: boolean, depDef: DepDef,  
    notFoundValue: any = Injector.THROW_IF_NOT_FOUND): any {  
...  
➥return startView.root.ngModule.injector.get(depDef.token, notFoundValue);  
}
```

DI mechanism in Angular is very complex. The DI injectors are hierarchical: The PlatformInjector, NgZoneInjector, AppModule Injector and the Element Injector.

```
PlatformInjector  
    |  
    v  
NgZoneInjector  
    |  
    V  
AppModuleInjector  
    |  
    v  
ElementInjector
```

The NgModule injector was used to resolve the MailService instance because it was defined in AppModule which is a parent to AppComponent. If the MailService was provided only in the AppComponent’s provider property. The root view element injector will be used instead.

```
export function resolveDep(  
    view: ViewData, elDef: NodeDef, allowPrivateServices: boolean, depDef: DepDef,  
    notFoundValue: any = Injector.THROW_IF_NOT_FOUND): any {  
...  
  const value = startView.root.injector.get(depDef.token, NOT_FOUND_CHECK_ONLY_ELEMENT_INJECTOR);  
}
```

We won’t go into their details here.

To go in-depth on the mechanics of Angular-Dependency Injection system, I’d recommend:

* [What you have always wanted to know about Angular Dependency Injection Tree](https://blog.angularindepth.com/angular-dependency-injection-and-tree-shakeable-tokens-4588a8f70d5d) by 

  [Alexey Zuev](https://medium.com/u/d59a9e801370?source=post_page---user_mention--77dd4c89968e---------------------------------------)

Angular exports two injection classes: *ReflectiveInjector* and *StaticInjector*.

The **ReflectiveInjector** class creates and stores the instances of classes, and also retrieve an instance using the reflection capabilities of Reflect metadata. It uses the class name as the key to retrieve the class instance.

The ReflectiveInjector could be used like this:

```
import { ReflectiveInjector } from '@angular/core';class Http {  
    constructor() {}  
    get(url: string) {  
        return ['rice', 'beans']  
    }  
}class FoodService {  
    constructor(private http: Http) {}  
    getFoods() {  
        return this.http.get('foods')  
    }  
}const injector = ReflectiveInjector.resolveAndCreate([  
    Http,  
    FoodService  
]);const foodService = injector.get(FoodService);  
console.log(foodService.getFoods()) // ['rice', 'beans']
```

We import our injector `ReflectiveInjector` from `@angular/core`. We construct two classes of Http and FoodService. Http returns an array of food in its get method, FoodService takes an instance of Http in its constructor, it uses the instance in its getFoods methods to get the array of food from Http. Next, we configure our injector by calling the static method `resolveAndCreate` in ReflectiveInjector. It takes an array of classes as parameters, these classes are stored in a key-value store with their class name as key and their instances as the value.

That is the reason we have to supply the class name to get its instance:

```
const foodService = injector.get(FoodService);  
// foodService instance of FoodService
```

The Injector uses `FoodService` as the key to resolving its instance.

When we run the above example, it will fail.

`Cannot resolve all parameters for FoodService(?). Make sure they all have valid type or annotations.`

Why? Well, we will know in a while.

Looking at the error message, it says something about type or annotations, so we know its kinda related to decorator and metadata. In order to solve this issue, we can either decorate our classes with the @Injectable decorator or decorate the `private http: Http` in the FoodService constructor with @Inject.

We now see that when ReflectiveInjector creates instances it uses the metadata to deduce class dependencies. If we don’t annotate our classes or params with @Injectable or @Inject, the error message above is thrown.

To solve the problem using **@Injectable**, our code will be written to this:

```
import { ReflectiveInjector, Injectable } from '@angular/core';class Http {  
    constructor() {}  
    get(url: string) {  
        return ['rice', 'beans']  
    }  
}➥@Injectable()  
class FoodService {  
    constructor(private http: Http) {}  
    getFoods() {  
        return this.http.get('foods')  
    }  
}  
...
```

Using **@Inject**:

```
import { ReflectiveInjector, Inject } from '@angular/core';class Http {  
    constructor() {}  
    get(url: string) {  
        return ['rice', 'beans']  
    }  
}class FoodService {  
➥  constructor(@Inject(Http) http) {}  
    getFoods() {  
        return this.http.get('foods')  
    }  
}  
...
```

These decorator functions (@Inject, @Injectable) uses the Reflect library to add metadata to classes or parameters. **Reflect** library is dedicated to adding and retrieving metadata added to our code (class, function, parameters) using `defineMetadata`, `getOwnMetadata` functions.

We will talk more on the Reflect library and its functions in the next section when we implement our own DI framework using decorators.

The **StaticInjector** is used internally by Angular. It doesn’t use reflection to resolve dependencies like ReflectiveInjector. The developer specifies the dependencies in a `deps` array, like this:

```
const staticInjector = StaticInjector.resolveAndCreate([  
    Http,  
    {  
        provide: FoodService,   
➥      deps: [Http]  
    }  
]);
```

We have seen how ReflectiveInjector uses metadata generated by decorators to resolve dependencies of a class. In the next section, we will create our own DI. We will also implement our own custom `@Injectable` decorator to demonstrate how to use metadata and decorators in DI.

## Implementing DI using decorators

Decorators are an experimental feature in ES6 that is designed to modify class, methods, parameters at runtime. It provides a way of adding additional information to class declarations and members.

Decorators are available in TypeScript as an experimental feature.

To use decorators, we must enable `experimentalDecorators` compiler option in our `tsconfig.json` file.

It can be done manually, first create tsconfig.json:

```
tsc --init
```

Then, add the experimentalDecorators property:

```
"compilerOptions": {  
    "target": "ES5",  
    "experimentalDecorators": true  
}
```

We can easily do everything from the command-line:

```
tsc --target ES5 --experimentalDecorators
```

Decorators use `@decoratorFn` form, where `decoratorFn` must be a function.

```
function decoratorFn(target) {  
    //code here  
}@decoratorFn()  
class Animal {}
```

The decoratorFn has a target parameter. This is the code to which the decorator is applied. In our example, we applied the decorator to a class `Animal`. The class Animal is fed to the decoratorFn when called at runtime.

Here, the decorator can apply any metadata it wishes to the class.

We have had a basic theory about how Decorator is implemented and used.

To explore more about Decorators, go through these links:

* [Decorators. TypeScript](https://typescriptlang.org/docs/handbook/decorators.html)
* [Typescript decorators](https://www.sparkbit.pl/typescript-decorators)

Let’s create a very basic injection class. We will emulate Angular’s `ReflectiveInjection` system. We will have our own `@Injectable` function which will mark a class as available for creation. Also, we will create a `ReflectiveInjector` class with the same methods as Angular's, `resolveAndCreate` and `get`.

Let’s get started. We create a new project:

```
mkdir di-ts  
cd di-ts  
npm init -y  
tsc --target ES5 --experimentalDecorators  
npm i typescript -S latest && npm i @types/node -D
```

As we are creating an injector with reflective capabilities we will need the reflect-metadata library.

```
npm i reflect-metadata -S
```

We create our main file:

```
touch index.ts
```

Our setup is complete, we begin implementation.

First, we import the `reflect-metadata` library and declare the `ANNOTATIONS` constant.

```
import 'reflect-metadata'  
const ANNOTATIONS = '__annotations__'
```

Yes, if you have read the Angular sources esp where they implemented the *makeDecorator* function(@angular/core/src/util/decorators.ts). You will see that the `ANNOTATIONS` constant is used to add metadata to a class.

We will kinda mimick Angular’s Injectable function in a way. I’ll just pick the relevant parts.

Implementing our Injectable function, we have this:

```
function Injectable() {  
    function DecoratorFactory(cls: any, objOrType?: any) {  
        const annotationInstance = (<any>DecoratorFactory)objOrType          
        const annotations = cls.hasOwnProperty(ANNOTATIONS) ?  
            (cls as any)[ANNOTATIONS] :  
            Object.defineProperty(cls, ANNOTATIONS, {value: []})[ANNOTATIONS];  
        annotations.push(annotationInstance);  
        return cls;  
    }  
  return DecoratorFactory  
}
```

This code is similiar to Injectable in Angular. The Injectable is a Decorator Factory. Know this, a Decorator Factory is a function that returns the expression that will be called by the decorator at runtime.

Example:

```
function log(name) { // the decorator factory  
    return function(target) { // the decorator  
        // do work with `target` and `name`  
    }  
}
```

So in our case:

```
function Injectable() { // the decorator factory  
    function DecoratorFactory(cls: any, objOrType?: any) {...}// the decorator    return DecoratorFactory  
}
```

Looking at the *DecoratorFactory*, we see that it takes *cls* and an optional *objOrType*. The *cls* is the class which is decorated by the Injectable function, *objOrType* is the additional properties to be added to the class, *cls*.

Moving into its implementation, *objOrType* is assigned to the annotationInstance variable. Then, the cls is checked to see if it has already **annotations** defined in its constructor using the hasOwnProperty method from the Object class. If it already, it is accessed `(cls as any)[ANNOTATIONS]`, if not it is defined using Object.defineProperty method and accessed on the fly `Object.defineProperty(cls, ANNOTATIONS, {value: []})[ANNOTATIONS]`. The result is assigned to the annotations variable which holds the reference to the cls' **annotations** property. Next, the annotationInstance defined earlier is pushed on the **annotations** array and the modified cls is returned.

What really happened here? To put it simply, our class cls was modified to add a **annotations** property to it.

Why do we have to do all that? Our injection method is reflective. Like we said earlier, the dependencies of a class is going to be derived from the annotations to the class. So we could use the reflect-metatdata getOwnMetatdata function to get the class parameters.

getOwnMetadata returns the information stored on a target from its key.

To see how we could retrieve the parameters from the class, let’s implement the ReflectiveInjector class:

```
class ReflectiveInjector {  
    private static records: { token:any, deps:any }[] = []    static resolveAndCreate(tokens: Array<any>) {  
        tokens.forEach((token:any)=> {  
            ReflectiveInjector.records.push({  
                token,  
                deps: Reflect.getOwnMetadata('design:paramtypes', token)  
            })  
        })  
        return this  
    }  
    static get(_token: any) {  
        // get the `token` from the record set  
        const [record] = ReflectiveInjector.records.filter((record)=>{  
            return record.token == _token  
        })  
        let {token, deps} = record        // resolve dependencies into instances  
        deps = deps.map((dep: any)=>{ return new dep() })        // create the instance of the token with the resolved dependencies  
        return new token(...deps)  
    }  
}
```

Here, the ReflectiveInjector two methods resolveAndCreate and get. It also has a records property, which stores all the classes in a `{token, deps}` format. So we could retrieve a class with reference from the token provided.

resolveAndCreate method aggregates and stores all the tokens in the records store. We see here that it uses the getOwnMetadata function to get the parameters of each class token.

Mind you, this works if the class has been decorated with the @Injectable function.

`Reflect.getOwnMetadata('design:paramtypes', target)` returns the parameters of a decorated class. This will help us when the instance of the class is to be instantiated and returned to the user.

The `get` method, retrieves a class token from the records store with \_token param passed to it. It destructures the token and deps from the retrieved record. Then, proceeds to resolve its deps into instances utilizing the map method of the Array class. Finally, the class instance is created passing in the deps with the help of the spread operator.

Let’s run a simple example to test our custom DI framework:

```
class Http {  
    getFoodGet() {  
        return ['rice', 'beans']  
    }  
}@Injectable()  
class FoodS {  
    constructor(private http: Http) {}  
    getFood(){  
        return this.http.getFoodGet()  
    }  
}const injector = ReflectiveInjector.resolveAndCreate([Http, FoodS])  
const foodS = injector.get(FoodS)  
console.log(foodS.getFood())
```

We have a Http class with a getFoodGet method which returns an array of `food` :-)

Then we have an Injectable-decorated FoodS class which has an Http dependency in its constructor. Its getFood method gets a list of food from the Http class using its getFoodGet method.

In a way Http instance must be injected into FoodS when its instance is being craeted, like this:

```
const foodS = new FoodS(new Http())
```

We use our ReflectiveInjector class, passing in an array of our classes: Http and FoodS, as its resolveAndCreate method is called. Like we stated earlier, its retrieves their parameters with the help of Reflect’s getOwnMetadata function.

Then, FoodS gets an array of dependencies, like this:

```
[[function Http]]
```

Http gets undefined because it wasn’t decorated. If it was but with no parameters in its constructor. It will return an empty array.

So we see to get the dependencies of a class it needs to be decorated. That’s why we implemented Injectable.

So when we can retrieve an instance of FoodS:

```
const foodS = injector.get(FoodS)
```

The injector parses through its deps store and creates its instance passing in the deps array, just like this:

```
// array of dependencies  
const deps = [Http]// instances of dependencies created  
deps = [new Http()]// dependencies passed into the class instance  
new FoodS(...deps) => new foodS(new Http())
```

Now, we can call the getFood method on our resolved FoodS instance, foodS.

```
console.log(foodS.getFood())
```

And BOOM!, we get

```
$ ts-node index  
[ 'rice', 'beans' ]
```

on our terminal.

## Conclusion

That was a heavy one. Decorators are such an important concept in the JavaScript world. It helps with a lot of things.

We just demonstrated how Angular uses it to implement a powerful DI framework and also, we kinda simulated the Angular ReflectiveInjection method to see how it works its nuts and bolts using the @Injectable decorator.

Decorators can be used in a lot of ways aside DI. Ehhhmmm, I don’t know of any other usage, but I have a hunch it has other uses.

I almost forget we saw how to use metadata reflection API from the reflect-metadata library and its highly useful method: getOwnMetadata.

I think with this, the vague concept of DI in Angular and general will become clearer.

If you have any question regarding this or the little demo on reflective injection, feel free to comment, email or DM me

Thanks !!!

## Helpful links:

* [Difference between Annotations and Decorators](https://blog.thoughtram.io/angular/2015/05/03/the-difference-between-annotations-and-decorators.html)
* [Resolve Dependencies in Angular 2](https://blog.thoughtram.io/angular/2015/09/17/resolve-service-dependencies-in-angular-2.html)

## Shared with ❤️ in Bit’s Blog

Bit helps you build applications faster by turning components into building blocks which can be shared, used and developed from any project. It’s open source, so feel free to give it a try and collaborate with your team.

[## Component Discovery and Collaboration · Bit

### Bit is where developers share components and collaborate to build amazing software together. Discover components shared…

bit.dev](https://bit.dev/?source=post_page-----77dd4c89968e---------------------------------------)

## Learn more

[## How To “Publish” Multiple Packages From Any Repository In 5 Minutes

### How to make any part of any repo available as a package with NPM in 5 minutes without splitting or restructuring your…

blog.bitsrc.io](/how-to-publish-multiple-packages-from-any-repository-in-5-minutes-9aafd31d85b7?source=post_page-----77dd4c89968e---------------------------------------)

[## 6 Ways to Unsubscribe from Observables in Angular

### A review of the different ways you can unsubscribe from Observables in Angular

blog.bitsrc.io](/6-ways-to-unsubscribe-from-observables-in-angular-ab912819a78f?source=post_page-----77dd4c89968e---------------------------------------)

[## Component Inheritance in Angular

### Respect the DRY rule! Learn how to write code efficiently using component inheritance

blog.bitsrc.io](/component-inheritance-in-angular-acd1215d5dd8?source=post_page-----77dd4c89968e---------------------------------------)

[## One-way property binding mechanism in Angular

### In-depth dive of how Angular updates properties on directives/elements and runs a DOM re-render to reflect changes.

blog.bitsrc.io](/one-way-property-binding-mechanism-in-angular-f1b25cf00de7?source=post_page-----77dd4c89968e---------------------------------------)

[## Creating Modals in Angular

### Different methods and tools for building modals in Angular

blog.bitsrc.io](/creating-modals-in-angular-cb32b126a88e?source=post_page-----77dd4c89968e---------------------------------------)

[## Using Google Analytics with Angular

### by Chidume Nnamdi

codeburst.io](https://codeburst.io/using-google-analytics-with-angular-25c93bffaa18?source=post_page-----77dd4c89968e---------------------------------------)

[## Boost Angular’s Performance by Lazy Loading your Modules

### Get better performance for your NG apps in just a few minutes

blog.bitsrc.io](/boost-angulars-performance-by-lazy-loading-your-modules-ca7abd1e2304?source=post_page-----77dd4c89968e---------------------------------------)

[## 10 Ways to Optimize Your React App’s Performance

### How to optimize performance to deliver an awesome user experience.

blog.bitsrc.io](/10-ways-to-optimize-your-react-apps-performance-e5e437c9abce?source=post_page-----77dd4c89968e---------------------------------------)

## Reference/Credits

* [Angular: From Theory To Practice — Asim Hussain](https://www.amazon.com/Angular-Practice-applications-tomorrow-framework-ebook/dp/B01N9S0CZN)