---
title: "Event Binding Mechanism in Angular"
url: https://medium.com/p/b38f0e46d2ed
---

# Event Binding Mechanism in Angular

[Original](https://medium.com/p/b38f0e46d2ed)

Member-only story

# Event Binding Mechanism in Angular

## How Angular’s event binding mechanics works — in depth.

[![Chidume Nnamdi](https://miro.medium.com/v2/resize:fill:64:64/1*pXClPxHH6zeWUrFWPJSmCw.png)](https://kurtwanger40.medium.com/?source=post_page---byline--b38f0e46d2ed---------------------------------------)

[Chidume Nnamdi](https://kurtwanger40.medium.com/?source=post_page---byline--b38f0e46d2ed---------------------------------------)

12 min read

·

Aug 29, 2018

--

2

Listen

Share

More

![]()

This tutorial provides you with the information required to understand how an event is attached to the host element and the check for performance optimization. Also, what you will learn from this post will enable you to come up with various scenarios for event binding on your own.

**NB:** This article is based on the Renderer2 API of Angular. It is assumed that you know how Angular represents Directives and Components internally. If you don’t, then go ahead and get familiar with the topic by going through the following links:

* [Here is why you will not find components inside Angular](https://blog.angularindepth.com/here-is-why-you-will-not-find-components-inside-angular-bdaf204d955c) by 

  [Max NgWizard K](https://medium.com/u/bd29063a4857?source=post_page---user_mention--b38f0e46d2ed---------------------------------------)

**Tip**: Use [**Bit**](https://github.com/teambit/bit)to build apps faster with components. Easily share and reuse components with your team, using them to build new apps! Give it a try.

[## Component Discovery and Collaboration · Bit

### Bit is where developers share components and collaborate to build amazing software together. Discover components shared…

bit.dev](https://bit.dev/?source=post_page-----b38f0e46d2ed---------------------------------------)

[![]()](https://bit.dev/)

## Introduction

Events are used to register callbacks for an event so when the particular event is fired the callback is run.

We register/add event listeners to our elements using the addEventListener API in the HTMLElement class.

```
<html>  
<button>Click Me</button><script>  
    const button = document.querySelector('button')[0]  
    button.addEventListener('click',()=>{  
        console.log('Im clicked')  
    })  
</script>  
</html>
```

We see here, that a click event has been bound to the button element. When we click on the element in our browser, the callback function is executed.

We have seen how event binding mechanics work in a basic HTML/JS app. The question is how does Angular attach event listeners to its elements and call their associated callback functions whenever the event is fired?

## Events through `()`

In Angular, we can register and capture an event from an element by wrapping the event in a `()` parenthesis.

We can bind most of the common events in the DOM:

```
(focus)="focusCallback()"    
(blur)="blurCallback()"(submit)="submitCallback()" (scroll)="scrollCallback()"(cut)="cutCallback()"  
(copy)="copyCallback()"  
(paste)="pasteCallback()"(keydown)="keydownCallback()"  
(keypress)="keypressCallback()"  
(keyup)="keyupCallback()"(mouseenter)="mouseenterCallback()"  
(mousedown)="mousedownCallback()"  
(mouseup)="mouseupCallback()"(click)="clickCallback()"  
(dblclick)="dblclickCallback()"(drag)="dragCallback()"  
(dragover)="dragoverCallback()"  
(drop)="dropCallback()"
```

When we use the () brackets symbol. We are attaching an event to the element. The target inside the () is an event we want to listen for.

Using `()` in Angular is synonymous with calling addEventListener`()`.

Let’s see this example:

```
@Component({  
    selector: 'app-root',  
    template: `<button (click)="clickEvent()">Click Me</button>`  
})  
export class AppComponent{  
    clickEvent() {  
        console.log('You clicked me')  
    }  
}
```

`click` event is attached to the `Click Me` button element using (). The right-hand side `="expression"` specifies the callback function that will be run when the registered event is fired by the element. In our case, we have the clickEvent function attached.

Let’s look at the component factory generated for the `AppComponent`:

```
export function View_AppComponent_0(_l) {  
    return i1.ɵvid(0, [  
        (_l()(), i1.ɵeld(0, 0, null, null, 1, "button", [], null,   
1.➥      [  
        [null, "click"]  
    ],   
2.➥  function(_v, en, $event) {  
        var ad = true;  
        var _co = _v.component;  
        if (("click" === en)) {  
            var pd_0 = (_co.clickEvent() !== false);  
            ad = (pd_0 && ad);  
        }  
        return ad;  
    }, null, null)),   
    (_l()(), i1.ɵted(-1, null, ["Click Me"]))], null, null);  
}
```

All these will be quite familiar if you have went through the links above thoroughly. The two functions ɵeld and ɵted are element and text definition nodes that constitutes our AppComponent view.

Looking at the ɵeld function, we see that it has information on how to create our button element. The `1.` param corresponds to `outputs` arg in the elementDef implementation and 2. param is the `handleEvent` arg:

```
export function elementDef(  
    checkIndex: number, flags: NodeFlags,  
    matchedQueriesDsl: null | [string | number, QueryValueType][], ngContentIndex: null | number,  
    childCount: number, namespaceAndName: string | null, fixedAttrs: null | [string, string][] = [],  
    bindings?: null | [BindingFlags, string, string | SecurityContext | null][],  
    1.➥ outputs?: null | ([string, string])[], 2.➥ handleEvent?: null | ElementHandleEventFn,  
    componentView?: null | ViewDefinitionFactory,  
    componentRendererType?: RendererType2 | null): NodeDef {  
...}
```

The outputs and handleEvents args are used for event propagation. The outputs array holds the event name to be registered against the element and the handleEvent holds the callback function to be triggered when the event is fired.

Looking at the handleEvent function:

```
function(_v, en, $event) {  
    var ad = true;  
    var _co = _v.component;  
    if (("click" === en)) {  
        var pd_0 = (_co.clickEvent() !== false);  
        ad = (pd_0 && ad);  
    }  
    return ad;  
}
```

It takes three parameters: \_v is the view definition of the component, en is the type of event fired and $event holds the event object. This function is the callback function for any event attached to a element. click, mouseneter, dblclick etc events calls this function. That’s why it uses the `if` statement to call each event callback function defined in the template.

During the creation of view nodes via createViewNodes function.

```
function createViewNodes(view: ViewData) {  
...  
    switch (nodeDef.flags & NodeFlags.Types) {  
      case NodeFlags.TypeElement:  
        const el = createElement(view, renderHost, nodeDef) as any;  
        let componentView: ViewData = undefined !;  
        if (nodeDef.flags & NodeFlags.ComponentView) {  
          const compViewDef = resolveDefinition(nodeDef.element !.componentView !);  
          componentView = Services.createComponentView(view, nodeDef, compViewDef, el);  
        }  
➥      listenToElementOutputs(view, componentView, nodeDef, el);  
    ...  
}
```

The listenToElementOutputs function is called to loop over the events in the outputs array and attach each one to the button element:

```
export function listenToElementOutputs(view: ViewData, compView: ViewData, def: NodeDef, el: any) {  
  for (let i = 0; i < def.outputs.length; i++) {  
    const output = def.outputs[i];  
    const handleEventClosure = renderEventHandlerClosure(  
        view, def.nodeIndex, elementEventFullName(output.target, output.eventName));  
    let listenTarget: 'window'|'document'|'body'|'component'|null = output.target;  
    let listenerView = view;  
    if (output.target === 'component') {  
      listenTarget = null;  
      listenerView = compView;  
    }  
    const disposable =  
        <any>listenerView.renderer.listen(listenTarget || el, output.eventName, handleEventClosure);  
    view.disposables ![def.outputIndex + i] = disposable;  
  }  
}
```

We see the for-loop statement iterating through the outputs array. The renderer listen function is called to attach each event `output.eventName` to the button element `el` and the function handleEventClosure is passed as the callback function.

What happened to handleEvent param? Remember the handleEvent function takes three params a view definition object, an event name, and a $event object. But callbacks attached to listeners in browser DOM only have one param to receive the $event object but our callback receives three params.

```
buttonElement.addEventListener('click',(➥$event) => {...})
```

To make it work Angular uses closure.

The renderEventHandlerClosure function returns the callback that is actually registered to the events in the DOM:

```
function renderEventHandlerClosure(view: ViewData, index: number, eventName: string) {  
➥return (event: any) => dispatchEvent(view, index, eventName, event);  
}
```

The function it returns has one param `event` which will receive the $event passed by thebroser when the callback is run on an event emission.

Looking back at listenToElementOutputs function:

```
export function listenToElementOutputs(view: ViewData, compView: ViewData, def: NodeDef, el: any) {  
  for (let i = 0; i < def.outputs.length; i++) {  
    const output = def.outputs[i];  
    const handleEventClosure = renderEventHandlerClosure(  
        view, def.nodeIndex, elementEventFullName(output.target, output.eventName));  
    ...
```

It calls the renderEventHandlerClosure with the params needed by the handleEvent function, the renderEventHandlerClosure returns the callback function we saw above and is assigned to handleEventClosure. The handleEventClosure with reference to the returned function is registered as the callback function for the event. The params passed into the renderEventHAndlerClosure function will be visible to the callback function when it is called by the browser (when any event registered on it is fired) and subsequently calls the dispatchEvent function.

The dispatchEvent function will call the handleEvent param:

```
export function dispatchEvent(  
    view: ViewData, nodeIndex: number, eventName: string, event: any): boolean|undefined {  
  try {  
    const nodeDef = view.def.nodes[nodeIndex];  
    const startView = nodeDef.flags & NodeFlags.ComponentView ?  
        asElementData(view, nodeIndex).componentView :  
        view;  
    markParentViewsForCheck(startView);  
➥  return Services.handleEvent(view, nodeIndex, eventName, event);  
  } catch (e) {  
    // Attention: Don't rethrow, as it would cancel Observable subscriptions!  
    view.root.errorHandler.handleError(e);  
  }  
}
```

Looking into the renderer listen function:

```
...  
    const disposable =  
        <any>listenerView.renderer.listen(listenTarget || el, output.eventName, handleEventClosure);  
...
```

We will see that it uses the addEventListener API of HTMLElement to attach the event to the button element.

```
class DefaultDomRenderer2 implements Renderer2 {  
...  
  listen(target: 'window'|'document'|'body'|any, event: string, callback: (event: any) => boolean):  
      () => void {  
    checkNoSyntheticProp(event, 'listener');  
    if (typeof target === 'string') {  
      return <() => void>this.eventManager.addGlobalEventListener(  
          target, event, decoratePreventDefault(callback));  
    }  
➥  return <() => void>this.eventManager.addEventListener(  
               target, event, decoratePreventDefault(callback)) as() => void;  
  }  
}
```

With these the click event is attached to our button element.

Let’s demonstrate what we have learned so far in a basic HTML/JS app

```
<!doctype html>  
<html lang="en"><head>  
    <meta charset="utf-8">  
    <title>Event Binding</title>    <meta name="viewport" content="width=device-width, initial-scale=1">  
    <link rel="icon" type="image/x-icon" href="favicon.ico">  
</head><body>  
1.➥<button id="button">Click Me</button>    <script>  
2.➥    class AppComponent {  
            clickEvent() {  
                console.log('Clicked!!!')  
            }  
        }  
3.➥   class DOMRenderer {  
            listen(target, event, callback) {  
                target.addEventListener(event, callback)  
            }  
        }4.➥    const button = document.getElementById("button")  
5.➥    let outputs = ["click"]  
6.➥    let renderer = new DOMRenderer()7.➥    let handleEvent = function(_v, en, $event) {  
            if (("click" === en)) {  
                _v.clickEvent();  
            }  
        }8.➥    function listenToElementOutputs(target, outputs, _v) {  
            for (var index = 0; index < outputs.length; index++) {  
                const event = outputs[index]  
                const handleEventClosure = renderEventHandlerClosure(_v, event)  
                renderer.listen(target, event, handleEventClosure)  
            }  
        }9.➥    function renderEventHandlerClosure(_v, eventName) {  
            return (event) => dispatchEvent(_v, eventName, event);  
        }10.➥   function dispatchEvent(_v, eventName, event) {  
            return handleEvent(_v, eventName, event)  
        }  
11.➥   listenToElementOutputs(button, outputs, new AppComponent())  
    </script>  
</body></html>
```

We just simulated how Angular implements event listener.

We began by creating a button element `1.`. We created two classes AppComponent `2.`, it holds the clickEvent method to be called when the `1.` is clicked and DOMRenderer class `3.`, it has a listen method which will call the addEventListener function on an HTMLElement to register any supplied event. `4.` we get the HTMLElement instance of the button element and stores it in the button variable. `5.` outputs array holds the array of events to be registered against the button element. `6.` renderer variable holds the instance of the DOMRenderer class. `7.` We define the handleEvent function, as we know this is the global callback function for any event found in the outputs array to be registered against any element. `8.` This function loops through the outputs array and attaches each event to the target element. `9.` This function returns a closure callback function. `10.` calls the global callback function handleEvent and returns its results.

I used the same function names as in Angular so we could better understand what is happening.

We can run the app by loading it in a browser with JavaScript enabled.

The listenToElementOutputs function is called `11.` when the page loads.

We passed into it, the `button` HTMLElement instance, the outputs array and an instance of the AppComponent class.

If we click on the Click Me button we will see `Clicked!!!` logged on the Console.

**NB:** Registering the handleEvent function as the callback function for each event should have been:

```
target.addEventListener(event, handleEvent(_v, en, $event){...})
```

the handleEvent function has params \_v, en and $event which it uses to know what event and function to call. But registering an event like above won’t pass in these params. An event callback function only takes in a $event object from the browser.

```
target.addEventListener(event, evtCallBack(event){...})
```

Then, how do we pass the `_v, en, $event` params to handleFunction so it could successfully run? Angular uses closure.

> *A closure is formed when the inner function is returned by the outer function, maintaining access to any variables declared inside the enclosing function.*

We called the renderEventHandlerClosure function with the handleEvent function requirements. renderEventHandlerClosure returns a function `(event) => dispatchEvent(_v, eventName, event);` and assigns it to handleEventClosure.

That is:

```
handleEventClosure == (event) => dispatchEvent(_v, eventName, event);
```

So when we register the event thorugh the listen method we are passing `(event) => dispatchEvent(_v, eventName, event);`

```
renderer.listen(target, event, handleEventClosure) ===renderer.listen(target, event, /*handleEventClosure*/(event) => dispatchEvent(_v, eventName, event);)
```

You see we have a callback with the event param, so when it is called by the browser, it calls dispatchEvent function with the params passed to it by the renderEventHandlerClosure function. So, handleEvent function gets the intended parameters. Though renderEventHandlerClosure has since exited its variables `_v, eventName` still kept "alive".

## Multiple Events

When can register multiple events to an element, like this:

```
<button (click)="clickEvent()" (mouseenter)="mouseEnterEvent()">Click Me</button>
```

We have a `click` event and `mouseenter` event registered to our button element.

The factory will look like this:

```
export function View_AppComponent_0(_l) {  
    return i1.ɵvid(0, [  
        (_l()(), i1.ɵeld(0, 0, null, null, 1, "button", [], null, [  
            [null, "click"],  
➥          [null, "mouseenter"]  
        ], function(_v, en, $event) {  
            var ad = true;  
            var _co = _v.component;  
            if (("click" === en)) {  
                var pd_0 = (_co.clickEvent() !== false);  
                ad = (pd_0 && ad);  
            }  
➥          if (("mouseenter" === en)) {  
                var pd_1 = (_co.mouseEnterEvent() !== false);  
                ad = (pd_1 && ad);  
            }  
            return ad;  
        }, null, null)),  
        (_l()(), i1.ɵted(-1, null, ["Click Me"]))  
    ], null, null);  
}
```

The new thing here is an extra `if` statement for the new event `mouseenter` and an extra item in the outputs array.

Our demo above still holds for this multiple events.

To add an extra event like mouseenter to our Click Me button. We just add the event name `mouseenter` to the outputs array and add an `if-` check logic to the handleEvent for the mouseenter event. Also, we define the method to be called on the `mouseenter` event in our AppComponent class:

```
<!doctype html>  
<html lang="en"><head>  
    <meta charset="utf-8">  
    <title>Event Binding</title>    <meta name="viewport" content="width=device-width, initial-scale=1">  
    <link rel="icon" type="image/x-icon" href="favicon.ico">  
</head><body>  
    <button id="button">Click Me</button>    <script>  
        class AppComponent {  
            clickEvent() {  
                console.log('Clicked!!!')  
            }  
➥          mouseEnterEvent() {  
                console.log('Mouse Over Us!!!')  
            }  
        }  
        class DOMRenderer {  
            listen(target, event, callback) {  
                target.addEventListener(event, callback)  
            }  
        }        const button = document.getElementById("button")  
➥      let outputs = ["click", "mouseenter"]  
        let renderer = new DOMRenderer()        let handleEvent = function(_v, en, $event) {  
            if (("click" === en)) {  
                _v.clickEvent();  
            }  
➥          if (("mouseenter" === en)) {  
                _v.mouseEnterEvent();  
            }  
        }        function listenToElementOutputs(target, outputs, _v) {  
            for (var index = 0; index < outputs.length; index++) {  
                const event = outputs[index]  
                const handleEventClosure = renderEventHandlerClosure(_v, event)  
                renderer.listen(target, event, handleEventClosure)  
            }  
        }        function renderEventHandlerClosure(_v, eventName) {  
            return (event) => dispatchEvent(_v, eventName, event);  
        }        function dispatchEvent(_v, eventName, event) {  
            return handleEvent(_v, eventName, event)  
        }  
        listenToElementOutputs(button, outputs, new AppComponent())  
    </script>  
</body></html>
```

Drag your mouse over the button and you will see `Mouse Over Us!!!` logged on the Console.

## Event Binding on Directives using @HostListener

Events can be bound by directives. Let’s say we have a directive that changes the background color of its host element:

```
<div highLight>I will change color</div>
```

The implementation:

```
@Directive({  
    selector: '[highLight]'  
})  
export class HighLight implements OnInit{  
    constructor(private el: ElementRef){}    ngOnInit() {  
        this.el.nativeElement.style.backgroundColor = 'red'   
    }  
}
```

We can make our directive interactive by making it change color on an event. Let’s when we click on it changes color to blue and when we hover our mouse over it, the color changes to green.

To add events on Directives, @HostListener decorator is used.

> *Angular HostListeners are annotations that allow you to bind a method in your class to a DOM event.*

```
@Directive({  
    selector: '[highLight]'  
})  
export class HighLight implements OnInit {  
    constructor(private el: ElementRef){}➥  @HostListener('mouseenter')  
    onMouseEnter() {  
        this.el.nativeElement.style.backgroundColor = 'blue'   
    }    ngOnInit() {  
        this.el.nativeElement.style.backgroundColor = 'red'   
    }  
}
```

We want the onMouseEnter method to be called when the mouseenter event is fired. The method changes the host element backgrond color to blue.

```
@Component({  
  selector: 'app-root',  
  template: `<div highLight>I will change color</div>`,  
})  
export class AppComponent {  
}
```

Let’s see the component factory generated:

```
export function View_AppComponent_0(_l) {  
    return i1.ɵvid(0, [  
        (_l()(), i1.ɵeld(0, 0, null, null, 2, "h2", [  
            ["highLight", ""]  
          ], null,   
➥        [  
            [null, "mouseenter"]  
          ],   
➥        function(_v, en, $event) {  
            var ad = true;  
            if (("mouseenter" === en)) {  
                var pd_0 = (i1.ɵnov(_v, 1).onMouseEnter() !== false);  
                ad = (pd_0 && ad);  
            }  
            return ad;  
        }, null, null)),  
        i1.ɵdid(1, 81920, null, 0, i2.HighLight, [i1.ElementRef], null, null),  
        (_l()(), i1.ɵted(-1, null, ["I will change color"]))  
    ], function(_ck, _v) { _ck(_v, 1, 0); }, null);  
}
```

The mouseenter event is registered on the div element. Directives have no view so their host element take their events. The difference here is that on the event emission the instance of the directive is used to call the callback function.

The statement `i1.ɵnov()` is used to retrieve the instance of directives. It refers to nodeValue function at the @angular/core library. We pass in the view definition and the node index of our directive node definition.

## Conclusion

The mechanics of event binding in Angular is quite simple. We saw how Angular attach events to elements and how it also attach events to directives host element using the @HostListener decorator.

If you have any question regarding this post or the short demo on Angular event binding mechanism, feel free to comment below and ask anything 😸

Thanks !!! :)

## Learn more

[## Angular Signals: A Complete Guide

### Angular Signals: A Complete Guide

Angular Signals: A Complete Guidekurtwanger40.medium.com](https://kurtwanger40.medium.com/angular-signals-a-complete-guide-04fa33155a46?source=post_page-----b38f0e46d2ed---------------------------------------)

[## 6 Useful Decorators to use in your Angular projects

### 6 Useful Decorators to use in your Angular projects

Useful Decorators to use in your Angular projectsblog.bitsrc.io](/6-useful-decorators-to-use-in-your-angular-projects-777e9b4c8c62?source=post_page-----b38f0e46d2ed---------------------------------------)

[## 6 Ways to Unsubscribe from Observables in Angular

### A review of the different ways you can unsubscribe from Observables in Angular

blog.bitsrc.io](/6-ways-to-unsubscribe-from-observables-in-angular-ab912819a78f?source=post_page-----b38f0e46d2ed---------------------------------------)

[## Component Inheritance in Angular

### Respect the DRY rule! Learn how to write code efficiently using component inheritance

blog.bitsrc.io](/component-inheritance-in-angular-acd1215d5dd8?source=post_page-----b38f0e46d2ed---------------------------------------)

[## One-way property binding mechanism in Angular

### In-depth dive of how Angular updates properties on directives/elements and runs a DOM re-render to reflect changes.

blog.bitsrc.io](/one-way-property-binding-mechanism-in-angular-f1b25cf00de7?source=post_page-----b38f0e46d2ed---------------------------------------)

[## Creating Modals in Angular

### Different methods and tools for building modals in Angular

blog.bitsrc.io](/creating-modals-in-angular-cb32b126a88e?source=post_page-----b38f0e46d2ed---------------------------------------)

[## Using Google Analytics with Angular

### by Chidume Nnamdi

codeburst.io](https://codeburst.io/using-google-analytics-with-angular-25c93bffaa18?source=post_page-----b38f0e46d2ed---------------------------------------)