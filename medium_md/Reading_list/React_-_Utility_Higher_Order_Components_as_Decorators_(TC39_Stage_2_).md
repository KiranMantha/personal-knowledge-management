---
title: "React - Utility Higher Order Components as Decorators (TC39 Stage 2 )"
url: https://medium.com/p/9e9f3a17688a
---

# React - Utility Higher Order Components as Decorators (TC39 Stage 2 )

[Original](https://medium.com/p/9e9f3a17688a)

# React - Utility Higher Order Components as Decorators (TC39 Stage 2 )

[![Rahat Khanna](https://miro.medium.com/v2/resize:fill:64:64/0*UDsVLu4jwIH3UveH.png)](/@mappmechanic?source=post_page---byline--9e9f3a17688a---------------------------------------)

[Rahat Khanna](/@mappmechanic?source=post_page---byline--9e9f3a17688a---------------------------------------)

7 min read

·

Dec 28, 2016

--

2

Listen

Share

More

We all know that Function is a first class citizen in Javascript. Although with the popularity of ES6 we have started using ES6 Classes but internally it is also a function only (literally with Babel it transpiles into functions). Functional Programming is an eloquent style for Javascript Programmers which is being adopted by almost all newgen JS developers.

**Summary of Article**

![]()

In this article we will be talking about the concept of Higher Order Functions and then using this concept to build utility based Higher Order Components in ReactJS. Also, as utility HOCs need to be used at multiple places quite a number of times, we want an elegant and yet simple way of adding HOC to any component. The Decorator pattern can be used for this and TC39 Proposal of EcmaScript Decorators which is being widely used in many projects suits for our requirement.

We will be writing a simple React App using these utility decorators and few components with examples about the use of these decorators. The utilities we will be creating for the purview of this article are A/B Testing & Analytics. A/B Testing has become an important part of any UI app because Customer Experience is the top most priority and A/B helps in optimising our UI to provide optimum customer experience according to Data insights.

**What is Higher Order Function ?**

> Functions that operate on other functions, either by taking them as arguments or by returning them, are called higher-order functions. — Eloquent Javascript

Simply if we see, we have been using higher order functions since long time. All functions in JS like **Array.map**, **Array.reduce** etc are Higher Order Functions and they take other functions as arguments and operate on them. Also, the second candidate for Higher Order Functions are Closures which return any function. The below given function can be termed as a Higher Order Function.

```
// Getting a Specific Getter from Generic get  
function get(prop){  
  return function(obj){  
    return obj[prop];  
  }  
}  
  
let getName = get("name");  
let name = getName({"name": "Rahat"});
```

## Introduction to Higher Order Components

Higher Order components in React follow the important concept of Composition. In React, Large Components can be composed of smaller components to implement separation of concerns. Any React App can be seen as a composition of Hierarchical Components.

Higher Order Component in ReactJS is similar to HOF and can be defined as any function that takes a Component as Argument and returns another Component. The returned component will contain/compose the initial argument passed in the argument to the function.

```
export default HOC(ComposedComponent) {  
  class WrapperComponent extends React.Component {  
    componentDidMount(){  
      this.newProps = transformationFunc(this.props);  
    }  
      
    render(){  
      <ComposedComponent {...this.props} {...this.newProps} />  
    }  
  }  
  return WrapperComponent;  
}
```

In the above code, we have created a Function that takes a Component to be composed and returns us a WrapperComponent which includes the ComposedComponent in its render method. The HOC/WrapperComponent can add new props or modify the existing props also. It can also get hooks to the lifecycle methods of the ComposedComponents. The props are passed as it is using the ES6 spread operator.

**Advantages of HOCs**

* **Replacement for Mixins**Mixins provided us great capability to add/augment common functionalities to our components. We could make generic Mixins and use with multiple Components. Now the same is possible with a HOC.
* **Control over Inputs**Using HOC, we can have control over the inputs passed to the composed component. We can restrict any input, mask it or transform it even.
* **Establish Connection to a Store/API Service**If there is a generic store/ API service like Analytics or A/B which we want multiple components to be connected to, we can do that using HOCs.
* **Intercept Rendering/Component Lifecycle Methods**It can be used in places where we want to intercept the rendering method or any other component lifecycle method. For Ex: If we are creating a HOC for managing Access to a certain component, we can disable Render, partial render etc. for that component according to Access permissions from some store.
* **Connecting to State/Firing Actions for Dumb Components**  
  Generally we do not expect our Dump components to fire actions or state but there are generic methods like Error Reporting or Logging.

We conclude till here that HOC are a cleaner way of implementing reusable capabilities for multiple components. We should start using HOCs in our React Apps to abstract common functionalities and reduce code redundancy.

Also, we can simplify the code structure for our React App with all these HOCs using a new construct called Decorators which is currently in advanced stage of TC39 and is being used in current projects by most developers possible using transpiler like babel.

## **Introduction to Decorators**

Decorators is a syntactical structure which enables us to modify Javascript Classes, properties (methods also) and object literals at design time while keeping the syntax declarative. Decorators in EcmaScript are currently in Stage 2 as a TC39 Proposal from Yehuda Katz (co-creator of EmberJS).

An ES2016 Decorator is an expression which returns a function and can take a target, name and property descriptor as arguments. In able to use the Decorators in your existing ReactApp or any ES6 app, you have to install a babel plugin.

```
npm install --save-dev babel-plugin-transform-decorators-legacy
```

Also, after installing the npm dependency package we have to also include this plugin in either Webpack Config(**webpack.config.js**) or else **.babelrc** file.

```
...  
"presets": ["es2015", "stage-0", "react"],  
"plugins": [ "transform-decorators-legacy" ]  
...
```

**A. Property Decorators**

Now, let us look at the most simple Decorator we can write for one single property.

```
import { readonly } from 'decorators';  
   
 class MyClass {  
   @readonly  
   myproperty = 'Test123';  
 }
```

The implementation of the readonly decorator looks as follow:

```
// decorators.js  
function readonly(target, key, descriptor) {  
  descriptor.writable = false;  
  return descriptor;  
}  
  
export default { readonly }
```

The decorator function will get the target, key and the descriptor. Either, we can add any annotation properties to target or change some attributes of the descriptor like it is done in the code snippet given above.

**B. Method Decorators**

The method decorators can help in running the decorator method before execution of the method which is decorated with it. We will see code for example of a **MethodLogger** decorator which will log that this method has been called along with its arguments.

```
import React,{ Component } from 'react';  
  
export default function MethodLogger(IncludeArguments){  
  return (target, key, descriptor) => {  
    const msg = 'Called Method';  
    const name = target.constructor.name;  
    const func = descriptor.value;  
    descriptor.value = function ( ...args )  
    {  
      if(IncludeArguments){  
        console.log( `${name}#${key} Called with Args: ${args}` );  
      }else{  
        console.log( `${name}#${key} Called` );  
      }  
      return func.apply( this, args );  
    };  
    return descriptor;  
  };  
}
```

In the above code we just return a function from the Descriptor method, which will take target, key & descriptor as arguments. If we need to do some processing before calling that actual function, we can store the initial function pointer to a reference **const func** and then replace another function on **descriptor.value** in which we want to put our custom logic. At last we can call the reference const func with **func.apply(this, args);**

Usage of above decorator in any method of a React Component:

```
import React,{ Component } from 'react';  
import autobind from 'autobind-decorator';  
  
import MethodLogger from '../util-decorators/logger';  
  
@autobind  
class ActionComponent extends Component {  
  
  @MethodLogger(true)  
  onActionClick(buttonName){  
    // Any Logic on Button Click  
  }  
...  
...  
<button style={buttonStyle} onClick={() => this.onActionClick('StaticButton1') }> StaticButton1 </button>
```

In the above code we have also used an open source **autobind-decorator** which helps in eliminating the need of binding any methods explicitly in the constructor of the ES6 class.

**C. Class Decorators**

The last type of Decorators are Class Decorators. These are actually implemented using Higher Order Components. We just have to return a HOC from the Decorator method. As we have already discussed about HOCs, we will just see example of a Decorator for adding A/B Tests for any component. The Decorator will provide the ABData as extra props or can also override existing props if the A/B prop matches any existing props.

```
import React,{ Component } from 'react';  
import abdata from '../mockdata/abdata';  
  
export default function ABTestDecorator(SubscribedExperiments, overrideProps){  
  return (InnerComponent) => {  
    class ABTestHoC extends Component {      render() {  
        let overridenProps = Object.assign({},this.props);  
        let subscribedABData = {};  
        SubscribedExperiments.map((experimentName) => {  
          if(abdata.experiments[experimentName] && abdata.experiments[experimentName].isActive){  
            subscribedABData = Object.assign({}, subscribedABData, abdata.experiments[experimentName].metaData);  
          }  
        });  
  
        if(overrideProps) {  
          Object.keys(subscribedABData).map((propName) => {  
            overridenProps[propName] = subscribedABData[propName];  
          });  
        }  
  
        return <InnerComponent {...overridenProps} abData={subscribedABData} />;  
      }  
    };  
  
    return ABTestHoC;  
  };  
}
```

In the above decorator we return ABTestHoc, which gets some A/B Experiments data from mockdata which contains list of Experiments for the React App. Any component can subscribe to one or many experiments, so we iterate over all experiments in the map function and get data of only the subscribed experiments. If the decorator argument **overrideProps** evaluates to true, then we iterate over existing props and override them if similar prop is available in A/B Data.

The above decorator can be used in any component by just writing @ABTestDecorator([‘Exp1’,’Exp2'], true/false) with list of experiments to be subscribed as first argument and boolean to overrideProps or not as second argument.

```
import React,{ Component } from 'react';  
import ABTestDecorator from '../util-decorators/abtest';  
  
@ABTestDecorator(['DynamicInfoExperiment'], true)  
class InfoComponent extends Component {  
...
```

I have written examples and library for these utility decorators at this repo:  
<https://github.com/mappmechanic/react-utility-decorators>

Let me know if you have any followup questions for the same.  
<http://twitter.com/mappmechanic>  
<http://linkedin.com/in/rahatkh>