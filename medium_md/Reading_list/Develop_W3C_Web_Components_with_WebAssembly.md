---
title: "Develop W3C Web Components with WebAssembly"
url: https://medium.com/p/d65938284255
---

# Develop W3C Web Components with WebAssembly

[Original](https://medium.com/p/d65938284255)

# Develop W3C Web Components with WebAssembly

## WebAssembly and Web Components are two emerging standards that have a big chance of significantly influencing the future of web as a platform. And the interesting question is, can we combine the two technologies? Can we create a Web Component using WebAssembly? Find out here.

[![nicole](https://miro.medium.com/v2/resize:fill:64:64/0*Kq2YcyRx6gXPTg6i.png)](/@ConnectCode?source=post_page---byline--d65938284255---------------------------------------)

[nicole](/@ConnectCode?source=post_page---byline--d65938284255---------------------------------------)

9 min read

·

Aug 16, 2018

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

### Web Components

Web Components are a set of features in the HTML and DOM specifications introduced by the World Wide Web Consortium (W3C) for creation of reusable widgets or components in web documents and web applications. The intention is to bring component-based software engineering to the World Wide Web. The simplest way of understanding Web Components is through an example. Imagine your colleague has developed a Web Component for displaying barcodes on web pages. To use the component, you simply need to do the following:

```
<html>   
<body>  <barcode input="12345678"></barcode>    </body>   
</html>
```

You only need to declare a HTML tag to use the component in your web pages or applications. There is no need to write any codes to call the component or meddle around to understand how the component works internally. This enables you to simplify your web development with the use of components.

### Web Components by W3C includes the following 4 features

* Custom elements — to add new HTML elements into the DOM
* Shadow DOM — to create a unique DOM encapsulated by HTML markup
* HTML imports — to import HTML code and reuse your components in other pages
* HTML template — to write reusable code and declare how it should look

The above may still be subjected to changes.

Also on a side note, Google provides and maintains Polymer, an open-source JavaScript library for building web applications using Web Components.

### WebAssembly

WebAssembly is a web standard, developed by W3C, that defines an assembly-like binary code format (wasm) for execution in web pages. The executing code runs nearly as fast as native machine code and is meant to speed up performance of web applications significantly. As WebAssembly is a low level binary bytecode, it supports compilation from different programming languages.

Besides being a compilation target for the different programming languages, WebAssembly also offers an alternative to web development in languages other than the JavaScript. Since 2017, WebAssembly has been natively supported by all major browsers including Firefox, Chrome, Safari and Edge.

The easiest way to understand WebAssembly is also through an example. The source code below shows the content of a “hello\_world.c” file. It is a program written in the C programming language.

```
#include     
int main()   
{   printf("hello, world!\n");        
return 0; }
```

In the past, you use a C/C++ compiler to compile the above to binary executables to run in the command line. Moving forward, you can compile the above program to WebAssembly and run the program inside a browser.

One of the tools that allows you to do so is Emscripten. This tool basically compiles C/C++ code to WASM, a WebAssembly module. The WASM module can then be loaded into web pages (HTML) to display the “hello, world” of the “printf” function.

### Can you mix WebAssembly and Web Components?

This two-emerging standard stands a big chance of significantly influencing the future of web as a platform. And the interesting question is can we combine the two technologies? Can we create a Web Component using WebAssembly? Has anyone tried this? A simple search on the web does not return any results.

After some research, I have come to conclude that the answer is Yes! The section below illustrates how to do this. However, do take note that some of the codes, scripts or HTML are subjected to change due to changes in the specifications and the evolution of the standards.

### Creating a Web Component using WebAssembly

To make this example useful and non-trivial, we are going to create a Barcode Web Component using WebAssembly. Specifically, we are going to create a component that generates a Code 39 barcode. We will be using a free Code 39 barcode web font from [https://www.barcoderesource.com](https://www.barcoderesource.com/) to display our barcode.

For those who cannot wait, you can just scroll to the bottom of this page to download the zip file containing a working copy of the sample codes. For those who want to understand a little more, do read on.

1. Download and install Emscripten from

<http://kripken.github.io/emscripten-site/>

Emscripten is a toolchain for compiling to asm.js and WebAssembly, built using LLVM, that lets you run C and C++ on the web at near-native speed without plugins.

2. Create a “code39.cpp” file using Notepad with the following contents.

```
#include <iostream>  
#include <cstdlib>  
#include <emscripten/bind.h>using namespace emscripten;class Code39 {public:  
  Code39()  
  {  
 inputData="12345678";  
 checkDigit=1;  
  }Code39(std::string inputData, int checkDigit)  
    : checkDigit(checkDigit)  
    , inputData(inputData)  
  {}std::string encode()   
{std::string filteredData=filterInput(inputData);int filteredlength = filteredData.length();  
std::string result;  
if (checkDigit==1)  
  result="*"+filteredData+generateCheckDigit(filteredData)+"*";  
else  
  result="*"+filteredData+"*";std::string mappedResult;  
for (int x=0;x<result.length();x++)  
 {          
         mappedResult=mappedResult+"&#"+  
         std::to_string((unsigned char)result[x])+";";    
 }  
result=mappedResult;human_readable_text=result;  
return result;}int getCheckDigit() const { return checkDigit; }  
void setCheckDigit(int checkDigit_) { checkDigit = checkDigit_; }std::string getInputData() const { return inputData; }void setInputData(std::string inputData_)   
{   
inputData = inputData;   
}std::string getHumanReadableText() const   
{   
return human_readable_text;   
}private:std::string inputData;  
std::string human_readable_text;  
int checkDigit;  
std::string result;  
std::string CODE39MAP[43]={"0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","-","."," ","$","/","+","%"};int getCode39Value(char inputchar)   
{  
int RVal=-1;  
int i=0;  
for (i=0;i<43;i++)  
{  
  if (inputchar==CODE39MAP[i][0])  
  {  
   RVal=i;  
  }  
}  
return RVal;  
}std::string generateCheckDigit(std::string data)  
{  
 std::string checkDigit;  
 int datalength=data.length();  
 int sumValue=0;  
 int x=0;  
 for (x=0;x<datalength;x++)  
 {  
  sumValue=sumValue+getCode39Value(data[x]);  
 }  
 sumValue=sumValue % 43;  
 return CODE39MAP[sumValue];  
}std::string filterInput(std::string data)  
{  
 std::string result;  
 int x=0;  
 int y=0;  
 for (x=0; x < data.length() && y < 255; x++)  
 {  
  if (getCode39Value(data[x]) != -1)  
  {  
   result=result+data[x];  
   y++;   
  }  
 }  
return result;  
}};// Binding code  
EMSCRIPTEN_BINDINGS(connectcode_code39) {  
  class_<Code39>("Code39")  
    .constructor<>()  
    .constructor<std::string, int>()  
    .function("encode", &Code39::encode)  
    .property("checkDigit",   
		&Code39::getCheckDigit,   
		&Code39::setCheckDigit)  
    .property("inputData",   
		&Code39::getInputData,   
		&Code39::setInputData)  
    .property("humanReadableText", &Code39::getHumanReadableText)  
    ;  
}
```

The above codes define a C++ class and the necessary functions for generating a Code 39 barcode, as explained below.

```
.constructor<std::string, int>()
```

The line above defines a constructor of an input data (first parameter) for the barcode and an indicator (second parameter) of whether a check digit is required.

```
.function("encode", &Code39::encode)
```

The above line is the function that we execute to generate the Code 39 barcode. Or more specifically, it generates some output characters that when applied with a barcode font, displays a Code 39 barcode.

```
.property("checkDigit", &Code39::getCheckDigit, &Code39::setCheckDigit)
```

The above property is used to indicate whether to generate a check digit before executing the “encode” function.

```
.property("inputData", &Code39::getInputData, &Code39::setInputData)
```

The above property is used to get or set the input data. You can change the input data using this property and execute the “encode” function to generate a different Code 39 barcode.

```
.property("humanReadableText", &Code39::getHumanReadableText)
```

The above property is used to get the human readable text that commonly appears below a barcode. The human readable text is not the same as the input data as the Code 39 barcode, and may require addition of start/stop and check characters.

3. Compile the “code39.cpp” with the following command in Emscripten. This provides us with a WASM module that we can later use in our Web Component. Launch a command prompt and execute the following command.

```
emcc --bind -o code39.js -s WASM=1 -O2 code39.cpp
```

If the “emcc” command cannot be found in your command prompt, you can go to your Emscripten folder and execute the “emcmdprompt.bat” script file to set it up.

With the above we have a WebAssembly module that we can use in a web page. However, remember that our aim is to make use of this WebAssembly to create a W3C standard compliant Web Component. So, our WebAssembly module will be executed from our Web Component instead.

4. Next we are going to create a Web Component from scratch without the help of any frameworks.

Using Notepad create a “code39-barcode.html” file.

```
<!-- Defines element markup --><template>  
    <style TYPE="text/css" media="screen,print">  
     @font-face {  
       font-family: CCode39_S3_Trial;  
       src: url("fonts/ConnectCode39_S3_Trial.woff") format("woff");  
     }  
     .barcode {font-weight: normal; font-style: normal; line-height:normal;   
 font-family: 'CCode39_S3_Trial', sans-serif; font-size: 32px}  
</style><div style="width:5in">  
<center>  
<div class="barcode">12345678</div>  
<div class="barcode_text"></div>  
</center>  
</div>  
<br></template><script type="text/javascript" src="code39.js"></script><script>(function(window, document, undefined) {	var thatDoc = document;  
        var thisDoc =  (thatDoc._currentScript || 					thatDoc.currentScript).ownerDocument;  
        var template = thisDoc.querySelector('template').content;  
        var MyElementProto = Object.create(HTMLElement.prototype);  
        MyElementProto.barcodeData = '';  
        MyElementProto.createdCallback = function() {  
        var shadowRoot = this.createShadowRoot();  
        var clone = thatDoc.importNode(template, true);  
        shadowRoot.appendChild(clone);  
        if (this.hasAttribute('inputData')) {  
            var data = this.getAttribute('inputData');  
            this.setData(data);  
        }  
        else {  
            this.setData(this.data);  
        }  
    };MyElementProto.attributeChangedCallback = function(attr, oldVal, newVal) {  
        if (attr === 'inputData') {  
            this.setData(newVal);  
        }  
    };MyElementProto.setData = function(val) {  
        this.barcodeInputData = val;};window.MyElement = thatDoc.registerElement('code39-barcode', {  
        prototype: MyElementProto  
    });Module['onRuntimeInitialized'] = onRuntimeInitialized;function onRuntimeInitialized() {var thatDoc = document;  
    var list = document.getElementsByTagName("code39-barcode")[0];  
    var elements=list.shadowRoot.querySelector(".barcode");  
    var elementsHR=list.shadowRoot.querySelector(".barcode_text");var instance = new Module.Code39();  
    instance.inputData = list.barcodeInputData;  
    instance.checkDigit = 1;  
    elements.innerHTML=instance.encode();  
    elementsHR.innerHTML=instance.humanReadableText;  
    instance.delete();};})(window, document);</script>
```

This HTML file contains three sections. The first section contains a HTML “template”, the second section contains the Javascript code that creates and register the Web Component and the third section execute our WebAssembly module.

The HTML “template” is used by the following code to create a Shadow DOM. You can think of shadow DOM as a scoped subtree inside your element that can create components.

```
var MyElementProto = Object.create(HTMLElement.prototype);		  
MyElementProto.barcodeData = '';  
MyElementProto.createdCallback = function() {  
var shadowRoot = this.createShadowRoot();  
var clone = thatDoc.importNode(template, true);  
shadowRoot.appendChild(clone);
```

The following line registers our Custom Element “MYElementProto” in the browser so that we can use “code39-barcode” as a tag.

```
window.MyElement = thatDoc.registerElement('code39-barcode', {  
        prototype: MyElementProto  
    });
```

Before we can execute our WebAssembly module, we will need to load the WASM file. The following line loads a Javascript generated by the Emscripten tool. This Javascript is generated to help us load the WebAssembly module.

To some of us, we may find this counter intuitive as we need to load a Javascript module in order to load a WebAssembly module. This is something that I believe will be improved in the future. At some point, we will be able to treat the WebAssembly modules as first-class citizens in a HTML web page.

```
<script type="text/javascript" src="code39.js"></script>
```

The “onRuntimeInitialized” function is a function will be executed when the WASM module has been loaded completely. In this function, we get the “barcode” and “barcode\_text” div element from our Web Component. We are doing this to get the input data from our Web Component tag and subsequently returning our barcode to the “barcode” div element.

```
var thatDoc = document;  
var list = document.getElementsByTagName("code39-barcode")[0];  
var elements=list.shadowRoot.querySelector(".barcode");  
var elementsHR=list.shadowRoot.querySelector(".barcode_text");
```

The following line declares an instance for our WebAssembly Module Code39 Class.

```
var instance = new Module.Code39();
```

And next, we use the “instance” to generate the barcode (barcode characters) based on the input data. Once a barcode is generated with the “encode” function, we can also get the “humanReadableText” from the “instance”.

```
instance.inputData = list.barcodeInputData;  
instance.checkDigit = 1;  
elements.innerHTML=instance.encode();  
elementsHR.innerHTML=instance.humanReadableText;
```

6. We have completed the development of our Web Component and the use of WebAssembly in the component to generate a barcode. We can create a simple HTML file to test our Web Component.

Using Notepad, create an “index.html” file with the following contents.

```
<!doctype html>  
<html>  
<head><meta charset="utf-8">  
<title><hello-world></title><style TYPE="text/css" media="screen,print">  
     @font-face {  
       font-family: CCode39;  
       src: url("fonts/CCode39.woff") format("woff");  
     }  
     .barcode {font-weight: normal; font-style: normal; line-height:normal; font-family: 'CCode39', sans-serif; font-size: 32px}  
</style><link rel="import" href="code39-barcode.html"></head>  
<body>Input : 12345678  
Barcode : Code39  
Check Digit : 1 (On)  
Font Name : ConnectCode39_S3Output :     <code39-barcode input="12345678"></body>  
</html>
```

The first line as shown below includes the Web Component and the second line uses the Web Component tag we have declared earlier.

```
<link rel="import" href="code39-barcode.html">   
.  
.  
.	   
<code39-barcode input="12345678">
```

7. Save the HTML file and run the following command in your command prompt to launch the Chrome browser to view our Web Component.

```
emrun --browser chrome index.html
```

You should see the following:

Press enter or click to view image in full size

![]()

This tutorial illustrates the many possibilities that the future will bring.

* A software vendor can ship and sell very optimized (WebAssembly) and standardized (Web Components) components without shipping the source code to other users.
* A web developer can easily integrate a third-party component in a standardized manner.
* We can imagine platforms such as Java or .NET can be ported to run as WebAssembly in the browsers. Developers can develop their Web Components using their favorite tools and programming languages.

Download the runnable zip file:

* [pwa\_webcomponents\_webassembly.zip](https://barcoderesource.com/pwa_webcomponents_webassembly.zip)

**Browser Tested On**

* Google Chrome 65.0.3325.181 (or above)

Note — The above tutorial can work on many more browsers by using a polyfill from frameworks such as Polymer.

> Join Coinmonks [Telegram Channel](https://t.me/coincodecap) and [Youtube Channel](https://www.youtube.com/c/coinmonks/videos) get daily [Crypto News](http://coincodecap.com/)

### Also, Read

* [Copy Trading](/coinmonks/top-10-crypto-copy-trading-platforms-for-beginners-d0c37c7d698c) | [Crypto Tax Software](/coinmonks/crypto-tax-software-ed4b4810e338)
* [Grid Trading](https://coincodecap.com/grid-trading) | [Crypto Hardware Wallet](/coinmonks/the-best-cryptocurrency-hardware-wallets-of-2020-e28b1c124069)
* Crypto Telegram Signals | [Crypto Trading Bot](/coinmonks/crypto-trading-bot-c2ffce8acb2a)
* [Best Crypto Exchange](/coinmonks/crypto-exchange-dd2f9d6f3769) | [Best Crypto Exchange in India](/coinmonks/bitcoin-exchange-in-india-7f1fe79715c9)
* [Binance vs Bitstamp](https://coincodecap.com/binance-vs-bitstamp) | [Bitpanda vs Coinbase vs Coinsbit](https://coincodecap.com/bitpanda-coinbase-coinsbit)
* [How to buy Ripple (XRP)](https://coincodecap.com/buy-ripple-india) | [Best Crypto Exchanges in Africa](https://coincodecap.com/crypto-exchange-africa)
* [Best Crypto Exchanges in Africa](https://coincodecap.com/crypto-exchange-africa) | [Hoo Exchange Review](https://coincodecap.com/hoo-exchange-review)
* [eToro vs Robinhood](https://coincodecap.com/etoro-robinhood) | [MoonXBT vs Bybit vs Bityard](https://coincodecap.com/bybit-bityard-moonxbt)
* [Best Crypto APIs](/coinmonks/best-crypto-apis-for-developers-5efe3a597a9f) for Developers
* Best [Crypto Lending Platform](/coinmonks/top-5-crypto-lending-platforms-in-2020-that-you-need-to-know-a1b675cec3fa)
* [Free Crypto Signals](/coinmonks/free-crypto-signals-48b25e61a8da) | [Crypto Trading Bots](/coinmonks/crypto-trading-bot-c2ffce8acb2a)
* An ultimate guide to [Leveraged Token](/coinmonks/leveraged-token-3f5257808b22)