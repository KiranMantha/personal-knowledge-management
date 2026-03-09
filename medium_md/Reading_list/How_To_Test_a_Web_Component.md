---
title: "How To Test a Web Component"
url: https://medium.com/p/b5d64d5e8bb0
---

# How To Test a Web Component

[Original](https://medium.com/p/b5d64d5e8bb0)

# How To Test a Web Component

[![Michał Pietraszko](https://miro.medium.com/v2/resize:fill:64:64/1*PsNdtZa7m5BPh-0Cxu7vQQ.jpeg)](/@pietmichal?source=post_page---byline--b5d64d5e8bb0---------------------------------------)

[Michał Pietraszko](/@pietmichal?source=post_page---byline--b5d64d5e8bb0---------------------------------------)

7 min read

·

Nov 25, 2018

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

In the world of Web Components, testing appears to be a hardly discussed topic. Since the standard becomes more and more relevant. We are standing at the point where discussing the matter would help to push Web Components adoption forward by proving that the quality assurance practices can be enforced.

## The Web Component Test Execution Environment

As of writing this, the only viable way of running tests for Web Components is through Karma which executes them through a target browser.

People coming from current technologies, such as React, Angular or Vue, might be disappointed with the current state of matters. The good thing is that there is [an active effort ongoing to support Web Components API in JSDOM.](https://github.com/jsdom/jsdom/compare/master...pmdartus:custom-elements?expand=1#diff-e5f3922b110d4e7f0f7c19cd78800dc8)

Even if JSDOM becomes viable, using Karma would still come with great benefits.

This is because it gives you an ability to test your Web Component against multiple browsers, which have their own implementations of the standard or need polyfills, making Karma a confidence-inducing tool.

You can sleep tightly after seeing your test suite passing.

* **Karma** — a test runner executing tests in your target browser,
* **Jasmine** — an all-in-one solution to write test scenarios and assertions,
* **JavaScript Modules** — modern browsers started supporting them. And they make configuration much simpler,
* **Custom Testing Utility** — will be shared in this article,

## Configuring a Web Component Testing Environment

### Installing Dependencies

Firstly, initialize a project through NPM and install the following dependencies:

* **karma** — a test runner,
* **jasmine** — a testing framework,
* **karma-jasmine-launcher** — plugin allowing to use jasmine,
* **karma-spec-reporter** — plugin displaying spec output in your terminal,
* **karma-chrome-launcher** — plugin allowing to launch tests in Chrome,
* **karma-firefox-launcher** — plugin allowing to launch tests in Firefox,
* **karma-edge-launcher** — plugin allowing to launch tests in Edge,
* **@webcomponents/webcomponentsjs** — polyfill for browsers not supporting Web Components, such as Edge,

macOS users can also consider installing **karma-safari-launcher** instead of **karma-edge-launcher**.

You can use paste the snippet from below into your terminal.

```
npm install karma jasmine karma-jasmine-launcher karma-spec-reporter karma-chrome-launcher karma-firefox-launcher karma-edge-launcher @webcomponents/webcomponentsjs
```

### Configuring Karma

Copy the following configuration into your ***karma.conf.js*** file.

The critical parts will be explained.

```
module.exports = function(config) {  
  config.set({  
    basePath: "",  
    frameworks: ["jasmine"],  
    files: [  
      "node_modules/@webcomponents/webcomponentsjs/webcomponents-bundle.js",  
      { pattern: "**/*.test.js", type: "module", included: true },  
      { pattern: "**/*.js", type: "module", included: false }  
    ],  
    exclude: [],  
    preprocessors: {},  
    reporters: ["spec"],  
    port: 9876,  
    colors: true,  
    logLevel: config.LOG_INFO,  
    autoWatch: true,  
    browsers: ["Chrome", "Firefox", "Edge"],  
    singleRun: true,  
    concurrency: Infinity  
  });  
};
```

The ***frameworks*** property tells karma what testing framework to use. In this case, it’s ***jasmine.***

The ***reporters*** bit tells Karma to use ***karma-spec-reporter*** that displays test results in a readable manner.

The ***browsers*** part indicates on what browsers your tests will be running on. This example sets Chrome, Firefox, and Edge. Mac users can remove Edge and add Safari instead.

The ***files*** configuration requires a little bit more explanation.

First, it loads Web Components API polyfill. This will prevent tests from failing in the browsers not supporting the spec.

Next, it tells Karma to load all files that end with ***.test.js* as a JavaScript module**and include them in the test run.

Lastly, all files that end with ***.js*** are loaded as modules too but not included as a test file — this will allow the test files to import them.

## How To Write Tests For Web Components

At this point, you should have all of the needed tools working.

## How To Test a Web Component With Shadow In Open Mode

Take the following example into consideration:

```
export class TextComponent extends HTMLElement {  
  static get tag() {  
    return "text-component";  
  }  
  
  static get observedAttributes() {  
    return ["text"];  
  }  
  
  constructor() {  
    super();  
    this.attachShadow({ mode: "open" });  
    this.shadowRoot.innerHTML =  
      this.getAttribute("text") || this.getDefaultText();  
  }  
  
  getDefaultText() {  
    return "Hello, World!";  
  }  
}  
  
customElements.define(TextComponent.tag, TextComponent);
```

This component accepts a *text* attribute that serves a message displayed inside of it.

It can be used the following way:

```
<text-component></text-component>   
<!-- displays "Hello, World!" -->  
  
<text-component text="Hello, Everyone!"></text-component>   
<!-- displays "Hello, Everyone!" -->
```

## Test file skeleton

Start with writing a suite skeleton in ***text.component.test.js.***

```
import { TextComponent } from "./text.component.js";  
import { TestUtils } from "./test-utils.js";  
  
describe("Text Component", () => {});
```

At the top, the to be tested component is imported — so it’s registered by the browser and available in the test suite.

Also, testing utilities are imported which are a class that was prepared to make actual tests shorter in terms of implementation. The full source code with an explanation is available at the bottom of this article.

## How to Test a Web Component Method Without Rendering

Testing a single unit of logic can be achieved by instantiating the class and running assertions against the output of the method. Let’s test an output of ***getDefaultText*** method.

```
describe("Text Component", () => {  
  describe("getDefaultText()", () => {  
    it("returns default text", () => {  
      const component = new TextComponent();  
      expect(component.getDefaultText()).toEqual("Hello, World!");  
    });  
  });  
});
```

## How To Render a Web Component In a Test

The testing utility exposes a render method which tells the browser to render an element with optional attributes. This tool returns a promise resolving with a reference to a rendered DOM element.

Let’s test both default and non-standard behavior of ***TextComponent.***

**Take a note that you have to access *shadowRoot* first before running the assertions!**

```
describe("Text Component", () => {  
  it("displays default text", async () => {  
    const {shadowRoot} = await TestUtils.render(TextComponent.tag);  
    const value = shadowRoot.innerHTML.includes("Hello, World!");   
    expect(value).toBeTruthy();  
  });  
  
  it("displays text", async () => {  
    const { shadowRoot } = await TestUtils.render(  
      TextComponent.tag, { text: "Provided text" }  
    );   
    const value = shadowRoot.innerHTML.includes("Provided text");      
    expect(value).toBeTruthy();  
  });  
  
  describe("getDefaultText()", () => {  
    it("returns default text", () => {  
      const component = new TextComponent();  
      expect(component.getDefaultText()).toEqual("Hello, World!");  
    });  
  });  
});
```

## How To Test a Web Component With Shadow In Closed Mode

When component’s shadow is attached in *closed* mode, it means that the ***shadowRoot*** property is unavailable. This makes the earlier mentioned solution insufficient in this scenario.

But nothing is lost! There is an easy trick to get this working. Let’s modify the previous example.

```
constructor() {  
    super();  
    this._root = this.attachShadow({ mode: "closed" });  
    this._root.innerHTML =  
      this.getAttribute("text") || this.getDefaultText();  
  }
```

***this.attachShadow*** returns a reference to the shadow root regardless of the mode. When following this method, your test suite can access the ***\_root*** property to run its’ assertions. Previous tests can be updated the following way to pass.

```
it("displays default text when text is not provided as an attribute", async () => {  
    const { _root } = await TestUtils.render(TextComponent.tag);  
    expect(_root.innerHTML.includes("Hello, World!")).toBeTruthy();  
  });  
  
  it("displays text provided through an attribute", async () => {  
    const { _root } = await TestUtils.render(TextComponent.tag, {  
      text: "Provided text"  
    });  
    expect(_root.innerHTML.includes("Provided text")).toBeTruthy();  
  });
```

## How To Test an Interaction With a Web Component

Take a look at this example:

```
export class ClickCountComponent extends HTMLElement {  
  static get tag() {  
    return "click-count";  
  }  
  
  constructor() {  
    super();  
    this._root = this.attachShadow({ mode: "closed" });  
    this.clickCount = 0;  
    this.render();  
  }  
  
  onClick() {  
    this.clickCount += 1;  
  }  
  
  render() {  
    this._root.innerHTML = `  
      <button>Increment</button> Clicks: ${this.clickCount}  
    `;  
    this._root.querySelector("button")  
      .addEventListener("click", () => {  
        this.onClick();  
        this.render();  
      });  
  }  
}  
  
customElements.define(ClickCountComponent.tag, ClickCountComponent);
```

The ***Click Count Component*** displays a button and a number of times it was pressed. It also attaches shadow in closed mode.

Testing interaction with the button can be performed through sending a relevant event and checking if the component renders what is expected.

```
import { ClickCountComponent } from "./click-count.component.js";  
import { TestUtils } from "./test-utils.js";  
  
describe("Click Count Component", () => {  
  it("displayed click count starts from 0", async () => {  
    const {_root} = await TestUtils.render(ClickCountComponent.tag);  
    expect(_root.innerHTML.includes("Clicks: 0")).toBeTruthy();  
  });  
  
  it("clicking the button increments displayed click count", async () => {  
    const {_root} = await TestUtils.render(ClickCountComponent.tag);  
    _root.querySelector("button").click();  
    _root.querySelector("button").click();  
    expect(_root.innerHTML.includes("Clicks: 2")).toBeTruthy();  
  });  
});
```

## a Web Component Testing Utility — To Make Life Easier

The most problematic aspect of testing Web Components is that their content is not available as soon as you put them into the page body.

Waiting for an element becoming available in the DOM does the trick and guarantees that its’ content has been rendered.

This utility has been created to abstract the nuances out and introduce a convenient API.

You can treat is as a point of reference for your own test utilities.

```
export class TestUtils {  
  /**  
   * Renders a given element with provided attributes  
   * and returns a promise which resolves as soon as  
   * rendered element becomes available.  
   * @param {string} tag  
   * @param {object} attributes  
   * @returns {Promise<HTMLElement>}  
   */  
  static render(tag, attributes = {}) {  
    TestUtils._renderToDocument(tag, attributes);  
    return TestUtils._waitForComponentToRender(tag);  
  }  
  
  /**  
   * Replaces document's body with provided element  
   * including given attributes.  
   * @param {string} tag  
   * @param {object} attributes  
   */  
  static _renderToDocument(tag, attributes) {  
    const htmlAttributes = TestUtils._mapObjectToHTMLAttributes(attributes);  
    document.body.innerHTML = `<${tag} ${htmlAttributes}></${tag}>`;  
  }  
  
  /**  
   * Converts an object to HTML string representation of attributes.  
   *  
   * For example: `{ foo: "bar", baz: "foo" }`  
   * becomes `foo="bar" baz="foo"`  
   *  
   * @param {object} attributes  
   * @returns {string}  
   */  
  static _mapObjectToHTMLAttributes(attributes) {  
    return Object.entries(attributes).reduce((previous, current) => {  
      return previous + ` ${current[0]}="${current[1]}"`;  
    }, "");  
  }  
  
  /**  
   * Returns a promise which resolves as soon as  
   * requested element becomes available.  
   * @param {string} tag  
   * @returns {Promise<HTMLElement>}  
   */  
  static async _waitForComponentToRender(tag) {  
    return new Promise(resolve => {  
      function requestComponent() {  
        const element = document.querySelector(tag);  
        if (element) {  
          resolve(element);  
        } else {  
          window.requestAnimationFrame(requestComponent);  
        }  
      }  
      requestComponent();  
    });  
  }  
}
```

[***Download a Fully Working Example From GitHub!***](https://github.com/unrealprogrammer/how-to-test-web-component)

*Originally published at* [*www.unrealprogrammer.com*](https://www.unrealprogrammer.com/how-to-test-a-web-component/) *on November 25, 2018.*