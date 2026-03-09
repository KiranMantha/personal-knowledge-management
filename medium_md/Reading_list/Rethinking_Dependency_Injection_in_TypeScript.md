---
title: "Rethinking Dependency Injection in TypeScript"
url: https://medium.com/p/6f47aa27e891
---

# Rethinking Dependency Injection in TypeScript

[Original](https://medium.com/p/6f47aa27e891)

# Rethinking Dependency Injection in TypeScript

## Comparing named-injection, constructor-injection, and property-injection

[![Garrett Mills](https://miro.medium.com/v2/resize:fill:64:64/1*VT3-P00uiSQ8cpC--vVq7g.jpeg)](/@glmdev?source=post_page---byline--6f47aa27e891---------------------------------------)

[Garrett Mills](/@glmdev?source=post_page---byline--6f47aa27e891---------------------------------------)

9 min read

·

Mar 30, 2021

--

1

Listen

Share

More

> This post originally appeared on my blog, [here](https://garrettmills.dev/blog/2021/03/30/Rethinking-Dependency-Injection-in-TypeScript/).

![]()

Anyone who has read this blog before knows that I have a particular interest in dependency injection and inversion-of-control paradigms.

Over the last few years, I’ve implemented DI in JavaScript for various projects, and I’m currently in the process of rewriting my framework and its DI implementation, so I wanted to share some observations about different JavaScript/TypeScript DI strategies.

In particular, we’ll explore named-injection, constructor-injection, and property-injection.

## Named Injection

My [first foray into DI in JavaScript](https://garrettmills.dev/blog/2019/11/16/Dependency-Injection-in-Less-Than-100-Lines-of-Pure-JavaScript/) relied on purely-runtime code and allowed injecting services from a container by name:

```
const Injectable = require('./Injectable')class SomeInjectableClass extends Injectable {  
    static services = ['logging']	myMethod() {  
        this.logging.info('myMethod called!')  
    }  
}
```

This was a fairly efficient and scalable paradigm, and defining the services as a property on the class itself made it easy to account for the services required by parent classes:

```
// ...  
class AnotherInjectableClass extends SomeInjectableClass {  
    static get services() {  
        return [...super.services, 'another_service']  
    }  
      
    myMethod() {  
        this.another_service.something()  
        super.myMethod()  
    }  
}
```

In fact, this mechanism was reliable enough that it became the basis of the injector used in my [Flitter framework](https://code.garrettmills.dev/Flitter/di).

## Drawbacks

This method is not without its downsides, however. For one, all classes must extend a common `Injectable` base class. If your class extends from, say, a base class from a library, then it can’t be injected directly.

Likewise, relying on service names makes it hard to know exactly what’s being injected into your class. Especially as I am transitioning more projects and my framework over to TypeScript, relying on named-injection just wasn’t going to cut it. This would require referencing properties with the `any` type annotation:

```
class SomeInjectableClass extends Injectable {  
    static get services(): string[] {  
        return [...super.services, 'another_service']  
    }  
      
    myMethod(): void {  
        (this as any).another_service.something()  // NOT type safe  
    }  
}
```

Relying on named services also makes the injectable classes inflexible, as the services have to be injected into properties with the same name. Say, for example, I have a service called `models`, and a class that uses it. If that class wants to keep an array called `models`, it will conflict with the injected service:

```
class SomethingThatUsesModels extends Injectable {  
    static get services() {  
        return [...super.services, 'models']  
    }  
      
    // CONFLICT with the injected 'models' service  
    protected models: Model[] = []  
}
```

Because a named-injector would have to bypass type-safety, this could lead to a situation where the TypeScript compiler types `models` as `Model[]`, but the injector overrides it to be the injected `models` service, which would cause runtime errors.

## Constructor Injection

Since we’re working in TypeScript, we want to do away with named-injection entirely. The TypeScript compiler has a flag which, when enabled, emits the type metadata for classes and properties, making it available via the Reflection API.

This is useful because it effectively enables “naming” a dependency based on its type, rather than an arbitrary string. So, when defining typed injectable classes, each property contains *two* pieces of information, rather than just one.

Likewise, we can enable the experimental “decorators” functionality, which can allow us inject any arbitrary class rather than requiring it to extend a base `Injectable` class. For example:

```
@Injectable()  
class SomethingThatUsesModels {  
    protected models: Model[] = []    constructor(  
    	protected readonly modelsService: ModelsService,  
    ) { }  
}
```

Anyone who has used the Angular framework is familiar with this format. The Angular DI historically worked this way, using type reflection to handle injection. Nowadays, it uses its custom compiler to handle injection at compile time, but that’s beyond the scope of this writeup.

## How does this work?

Okay, so we have a decorator and some type annotations. But, how do we actually do the injection from that?

The key is that `Injectable` decorator. In essence, this decorator is a function that accepts the class it decorates. Then, this function uses the `reflect-metadata` package to get a list of type annotations for the constructor’s parameters, then stores that information as additional metadata.

Here’s a (simplified) example from the [Extollo DI](https://code.garrettmills.dev/extollo/di/src/branch/master/src/decorator/injection.ts) (Flitter’s TypeScript successor):

```
/**  
 * Get a collection of dependency requirements for  
 * the given target object.  
 * @param {Object} target  
 * @return Collection<DependencyRequirement>  
 */  
function initDependencyMetadata(target: Object): Collection<DependencyRequirement> {  
    const paramTypes = Reflect.getMetadata('design:paramtypes', target)  
    return collect<DependencyKey>(paramTypes).map<DependencyRequirement>((type, idx) => {  
        return {  
            paramIndex: idx,  
            key: type,  
            overridden: false,  
        }  
    })  
}/**  
 * Class decorator that marks a class as injectable.  
 * When this is applied, dependency metadata for the constructors   
 * params is resolved and stored in metadata.  
 * @constructor  
 */  
export const Injectable = (): ClassDecorator => {  
    return (target) => {  
        const meta = initDependencyMetadata(target)  
        Reflect.defineMetadata(DEPENDENCY_KEYS_METADATA_KEY, meta, target)  
    }  
}
```

In essence, all this decorator does is read the type annotations from the class’ meta-data and store them in a nicer format in its own meta-data key (`DEPENDENCY_KEYS_METADATA_KEY`).

### Instantiating the Class

Okay, so we have the type annotations stored in meta-data, but how do we actually inject them into the class? This is where the container comes in.

In our old paradigm, the container was a class that mapped service names (`another_service`) to factories that created the service with that name. (e.g. `another_service` to `instanceof AnotherService`). In the type-based system, the container is a class that maps *types* to factories that create the service with that type.

This result is very strong as it enables type-safe injection. In the example above, the “token”, `ModelsService` is mapped to an instance of the `ModelsService` by the container.

So, when we ask the container to inject and create an instance of our `SomethingThatUsesModels` class, the container goes through all the items in the `DEPENDENCY_KEYS_METADATA_KEY` meta-data key and resolves them. Then, it passes those instances into the new class to instantiate it. For a (simplified) example:

```
class Container {  
    resolveAndCreate<T>(token: Instantiable<T>): T {  
        const dependencies = Reflect.getMetadata(DEPENDENCY_KEYS_METADATA_KEY)  
        const params = dependencies.orderByAsc('paramIndex')  
        	.map(dependency => this.resolveAndCreate(dependency.key))        return new token(...params)  
    }  
}
```

So, we can instantiate our `SomethingThatUsesModels` class like so:

```
const inst = <SomethingThatUsesModels> container.resolveAndCreate(SomethingThatUsesModels)
```

## Drawbacks

The constructor-injection paradigm works well and addresses many of the features we cared about between named-injection. In particular:

* Provides type-hinted injection
* Separates class property names from injection tokens

However, one way this falls behind named-injection is in the sense that the child classes must know and provide the dependencies of their parents.

For example, assume I have a class:

```
@Injectable()  
class ParentClass {  
    constructor(  
    	protected logging: LoggingService  
    ) { }  
}
```

Now, I want to define a child of this class that has its own dependencies:

```
@Injectable()  
class ChildClass extends ParentClass {  
    constructor(  
    	protected another: AnotherService,  
    ) { super() }  // ERROR!  
}
```

This will immediately fail to compile, since the `ChildClass` doesn’t pass the required dependencies into the parent. In reality, the child class must *also* specify the dependencies of the parent as parameters in its constructor:

```
@Injectable()  
class ChildClass extends ParentClass {  
    constructor(  
    	protected another: AnotherService,  
        logging: LoggingService,  
    ) { super(logging) }  
}
```

The issue with this becomes immediately obvious. All of the dependencies and imports of the parent must also be specified in *all* of the children. As the classes become larger and the inheritance chain becomes longer, you can quickly run into ridiculously long constructor signatures:

```
@Injectable()  
class LargerControllerClass extends ParentControllerClass {  
    constructor(  
    	protected logging: LoggingService,  
        protected config: ConfigService,  
        protected models: ModelsService,  
        socket: SocketService,  
        renderer: ViewRenderer,  
        other: OtherService,  
		another: AnotherService,  
        more: MoreService,  
    ) { super(socket, renderer, other, another, more) }  
}
```

Here, not only does the child need to be aware of the dependencies of the parent, it needs to take into account the order of the constructor parameters, which might be irrelevant in practice, but could break between versions.

## Property Injection

To improve upon this, we want to divorce the injected dependencies from the constructor while still maintaining the type-hinted and property-name benefits we gained from constructor-injection

This has the additional benefit of keeping the constructor signatures smaller, and keeping the non-injected constructor parameters distinct from the injected ones.

Luckily, in TypeScript, properties of a class also emit type annotations, and can be decorated. So, we can change our

`ParentClass` and `ChildClass` definitions to look as follows:

```
@Injectable()  
class ParentClass {  
    @Inject()  
    protected readonly logging!: LoggingService  
}@Injectable()  
class ChildClass extends ParentClass {  
    @Inject()  
    protected readonly another!: AnotherService  
}
```

## How does this work?

The “magic” bit here is the `@Inject()` decorator, which looks at the type annotation of the property it decorates and stores that property and its token value as meta-data on the class. Here’s a simplified example of Extollo’s [implementation](https://code.garrettmills.dev/extollo/di/src/branch/master/src/decorator/injection.ts#L69):

```
/**  
 * Mark the given class property to be injected by the container.  
 * @constructor  
 */  
export const Inject = (): PropertyDecorator => {  
    return (target, property) => {  
        const propertyMetadata = new Collection<PropertyDependency>()  
        Reflect.defineMetadata(DEPENDENCY_KEYS_PROPERTY_METADATA_KEY, propertyMetadata, target)        const type = Reflect.getMetadata('design:type', target, property)  
        if ( type ) {  
            const existing = propertyMetadata.firstWhere('property', '=', property)  
            if ( existing ) {  
                existing.key = key  
            } else {  
                propertyMetadata.push({ property, key })  
            }  
        }        Reflect.defineMetadata(DEPENDENCY_KEYS_PROPERTY_METADATA_KEY, propertyMetadata, target)  
    }  
}
```

Now, when the container creates an instance of a class, instead of passing in the dependencies as parameters to the constructor, it instantiates the class, then sets the properties on the class that have `@Inject()` decorators. For example:

```
class Container {  
    resolveAndCreate<T>(token: Instantiable<T>): T {  
        const inst = new token()  
        const dependencies = Reflect.getMetadata(DEPENDENCY_KEYS_PROPERTY_METADATA_KEY, token)  
        const instances = dependencies.map(x => {  
            inst[x.property] = this.resolveAndCreate(x.key)  
        })  
          
        return inst  
    }  
}
```

There’s a problem here, though. Say we were to `resolveAndCreate<ChildClass>(ChildClass)`. Because of the way JavaScript works, the instance returned by this call would ONLY have the properties defined in the child class, not the parent (i.e. `another`, but not `logging`).

To understand why, we need a bit of background.

### The Prototype Chain

In JavaScript, inheritance is prototypical. Say we have the following:

```
const parent = new ParentClass(...)  
const child = new ChildClass(...)
```

The object created as `parent` has a “chain” of prototypes that comprise it. So, if I try to access a method or property on `parent`, JavaScript will first check if the property exists on `parent` itself. If not, it will check if the property exists on `ParentClass.prototype`, then `ParentClass.prototype.prototype`, and so on.

If you follow the prototype chain long enough, every item in JavaScript eventually extends from `Object.prototype` or `Function.prototype`. (For classes, it’s the latter.) From any of these prototypes, we can access the constructor they are associated with using `Class.prototype.constructor`.

So, to get the `ParentClass` constructor from its prototype, we could do `ParentClass.prototype.constructor`.

### The Issue

When our `@Inject()` decorator saves the meta-data about the property type annotations, it does so by defining a new meta-data property on the prototype of the class where the property was defined.

Since the `logging` property was first defined and decorated in the `ParentClass`, the meta-data property with the information we need is actually defined on `ParentClass.prototype`.

However, when `@Inject()` is called for the `another` property in the `ChildClass`, it *defines* a new meta-data key with `ChildClass`‘s defined properties on the `ChildClass.prototype`.

Thus, in order to get all the properties we need to inject, we must check the meta-data defined for *all* prototypes in the inheritance chain of the constructor being instantiated. So, the container implementation might look something like:

```
class Container {  
    resolveAndCreate<T>(token: Instantiable<T>): T {  
        const inst = new token()  
        const meta = new Collection<PropertyDependency>()  
        let currentToken = token        do {  
            const loadedMeta = Reflect.getMetadata(DEPENDENCY_KEYS_PROPERTY_METADATA_KEY, currentToken)  
            if ( loadedMeta ) meta.concat(loadedMeta)  
            currentToken = Object.getPrototypeOf(currentToken)  
        } while (  
            Object.getPrototypeOf(currentToken) !== Function.prototype  
            && Object.getPrototypeOf(currentToken) !== Object.prototype  
        )        meta.map(x => {  
            inst[x.property] = this.resolveAndCreate(x.key)  
        })  
          
        return inst  
    }  
}
```

Now, `inst` will have all properties defined as injected for all parent classes in the inheritance chain.

## Best of Both Worlds

This approach combines the benefits of named-injection with the type-safety of constructor-injection:

* Child classes don’t need to account for the dependencies of their parents
* Injected dependencies can be type-hinted
* Property names of dependencies are independent of their types
* Parent dependencies are automatically accounted for

After using it for a while, I really like this paradigm. It provides a type-safe way to do dependency injection reliably, while still keeping the class definitions clean and parent-agnostic.

## Drawbacks

While its still my preferred solution, property-injection in TypeScript still isn’t without its drawbacks. Namely, it requires use of the [non-null assertion operator](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-0.html#non-null-assertion-operator) since the properties are being filled in by the container.

Because of this, if you were to instantiate a class manually outside the container and not fill in all the properties, the compiler wouldn’t catch it. Accessing properties on that instance would lead to runtime errors. However, assuming you always instantiate `Injectable` classes with the container, this problem is largely mute.

Another downside that I didn’t explore much in this article is the container code. Generalizing the container (for either constructor- or property-injection) requires use of the `any` operator *at some point* since factories are matched by key. At least in my implementation. I’d be interested to see alternatives.

## Conclusion

There will, undoubtedly, be another iteration of this article wherein I discover a new paradigm I want to try. But for the foreseeable future, I’ll be implementing and running with property-injection in my projects. As I mentioned in the article, constructor-injection and property-injection support form the basis of the dependency injector for the [Extollo framework](https://extollo.garrettmills.dev), my new project.

I tried not to dive too deep into the actual code required to implement the various strategies in this article, so if you’re interested in seeing how I’ve implemented them for my projects, here are some links:

* [The Flitter DI](https://code.garrettmills.dev/flitter/di) (named-injection)
* [The Extollo DI](https://code.garrettmills.dev/extollo/di) (constructor- and property-injection, WIP)

As always, I’d love to hear any other strategies or ways people have implemented this, so feel free to leave a comment or [get in touch](https://garrettmills.dev/#contact).