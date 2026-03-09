---
title: "How to build a simple sprite animation in JavaScript"
url: https://medium.com/p/b764644244aa
---

# How to build a simple sprite animation in JavaScript

[Original](https://medium.com/p/b764644244aa)

# How to build a simple sprite animation in JavaScript

[![Prashant Ram](https://miro.medium.com/v2/resize:fill:64:64/1*epGg34gbBptTqdai7tGeSw.png)](/@prashantramnyc?source=post_page---byline--b764644244aa---------------------------------------)

[Prashant Ram](/@prashantramnyc?source=post_page---byline--b764644244aa---------------------------------------)

8 min read

·

Jan 14, 2018

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

In this article we will build a quick and simple sprite animation in JavaScript ***without using any external libraries.***

> The complete code and the final result can be viewed on [JSfiddle](https://jsfiddle.net/prashantram/cbf6syjb/5/).

For this simple example we will be using [JSFiddle](http://jsfiddle.net) , a free online editor *(nothing to download or login)* to build the code. We will code in simple CSS, HTML and JS for this example, and will build the animation step-by-step.

## Step 0: Pick a Sprite image

You can do this via a simple Google search for “sprite animation” and by going to the Images tab of the search results and choosing an image.

For our test example I used the [following image](https://cdn.codeandweb.com/blog/2016/05/10/how-to-create-a-sprite-sheet/spritestrip.png) that I came across via search.

Press enter or click to view image in full size

![]()

*(Copyright disclaimer: This image is being used for educational purposes only)  
Image Credit:* [*Andreas Loew*](/@CodeAndWeb)*, creator of TexturePacker* [*https://www.codeandweb.com/texturepacker*](https://www.codeandweb.com/texturepacker)

If you want to use your own image you can upload the image to a service like <https://imgbb.com/>, which is a free image hosting service *(no login required)*, and it will give you a link for your image. *Again make sure it is the link to the image (i.e. your image URL should end with a .jpg or .png).*

### **What is a Sprite Image or a Sprite Sheet?**

A ***sprite image*** is simply ***a single image file (in .jpg or .png)*** which has multiple drawings within that single image. Such images are called ***sprite sheets***. Image1 *(shown above)* is a single sprite image (i.e. a single .png file), which has six figures drawn within it (*It is not six separate files but a single file).*

The idea behind using a sprite image is to use one single image that contains all animations of a character instead of dealing with multiple server calls to multiple single files. Thus instead of storing each animation frame in separate files, and having to do multiple server calls to fetch each file to render the animation, a sprite sheet can instead store all the animation in a single image file that is downloaded once *(just one server call)* when the page is loaded. This provides less web latency since the entire file is available to the browser when the page first loads, leading to a faster and smoother animation.

## Step 1: The CSS and HTML file

We will keep our CSS and HTML files very simple and will build them step-by-step to achieve a dynamic animation.

Open JSFiddle and write the following code in the HTML and CSS sections:

### HTML Code

```
<div id="demo">  
  <p id="image"> </p>  
</div>
```

***HTML Code:***We are simply adding a <div> element which has a <p> element. And we associate “id” with each of them.

### CSS Code

```
#image {  
  height: 256px;  
  width: 256px;background:   
url('https://cdn.codeandweb.com/blog/2016/05/10/how-to-create-a-sprite-sheet/spritestrip.png') 0px 0px;  
}
```

***CSS Code:***Here we define a CSS identifier called “image” (which corresponds to the <p> tag *id=”image”*). We then set the height and width within the CSS file to 256px. And we add a background image, that we fetch using the URL. The background image is the sprite image that we want to use (In our case it is the URL to the *spritestrip.png* file that we want to use). Note that the height and width values correspond to the height and width to get just the first slice from the 6 figures within the image file.

Thats it! Now run the JS in the JSFiddle Editor. You should see the following static image in the result browser. This is the first section from the sprite image sheet.

![]()

Make sure to grab the direct image link *(It should not link to the website but to the actual image)* Eg: [https://cdn.codeandweb.com/blog/2016/05/10/how-to-create-a-sprite-sheet/**spritestrip.png**](https://cdn.codeandweb.com/blog/2016/05/10/how-to-create-a-sprite-sheet/spritestrip.png)

Also note that for the purposes of this demo, you do not need to download the image to your computer. For now, you can access the image directly using the URL above.

**Troubleshooting**If you are using a different image and the image does not show up, make sure to:

* (a) check the URL and make sure it is the URL to the actual image i.e. ending in .png or .jpg;
* (b) adjust the height and width in the CSS file to the correct dimensions for your image, such that only the first animation slice from the sprite sheet is visible.

In my case the dimensions of the sprite sheet were (width)1536px \* (height) 256px. And, since there are six animation sections in the single row, each image is 1536/6 = 256px in width. *You will have to do the appropriate calculation to get the first image when using your own sprite sheet.*

## Step 2: The JavaScript Code

Now let us write some basic JavaScript code within the JavaScript section of the JSFiddle. We begin by writing a JavaScript function that we will call ***animateScript()***, which will look something like this:

### JavaScript Code

```
function animateScript() {document.getElementById("image").style.backgroundPosition =   
`-256px 0px`;}
```

***JavaScript Code:*** All we are doing is getting the <p> tag element using document.getElementById(“image”), and changing the backgroundPosition width by -256px, keeping the height the same 0px. Notice also that I am using the new ES6 back ticks i.e. ` , instead of the regular quotation i.e “ , to enclose the string `-256px 0px`. The reason for this will become clear in the next step.

Now lets connect the HTML with the JavaScript function we created by adding the ***onmouseover*** event to the <p> tag.

### HTML Code (Final)

```
<div id="demo">  
  <p id="image" onmouseover="animateScript()">  </p>  
</div>
```

***HTML Code:*** Now on mouse over of the <p> element the animateScript() function will be executed and the image display will be shifted by -256px, thereby showing the second image in the sprite sheet when the mouse is over the <p> tag.

That It! Now run the JS in JSFiddle, and you will see the first image *(Image A)*. Now when you mouse over on the image you will see the image **animating** to the second image.

![]()

![]()

**Troubleshooting**In case you are getting an error on JSFiddle *“animateScript() function not defined”* when you mouse over on the image, you can fix this by doing the following. In the Javascript pane of the JSFiddle click on the dropdown where it says ***“JavaScript (No-Library (pure js))”***. Here click on LOAD TYPE (where it probably says **“on Load”**) and choose instead **“No wrap in <body>”**.

Basically what is happening here is that JSFiddle is unable to connect to the JS function to the HTML code, since the DOM element does not exist onLoad, and hence you need to adjust the JSFiddle settings to *Load Type: No Wrap in Body*.

## Step 3: Lets Animate!

Awesome! If you have gotten thus far you have already achieved some basic animation of the image using mouse over. Let us now enhance our JavaScript code so that we have a smooth continuous animation looping through all the six figures on mouse over.

For this we will use the JavaScript function ***setInterval()*** to loop through each image. We will need to shift the position of the image slicer by 256px *(in the case of our demo image)* so that at every interval the next slice of the image is displayed. Accordingly let us make the following updates to the JavaScript code:

### JavaScript Code (Final)

```
var tID; //we will use this variable to clear the setInterval()function animateScript() {var    position = 256; //start position for the image slicer  
const  interval = 100; //100 ms of interval for the setInterval()tID = setInterval ( () => {document.getElementById("image").style.backgroundPosition =   
`-${position}px 0px`;   
//we use the ES6 template literal to insert the variable "position"if (position < 1536)  
{ position = position + 256;}  
//we increment the position by 256 each time  
else  
{ position = 256; }  
//reset the position to 256px, once position exceeds 1536px}  
, interval ); //end of setInterval} //end of animateScript()
```

*JavaScript Code:* So all we have really done in this code is move the *“document.getElementById(“image”).style.backgroundPosition”* inside the ***setInterval()*** function. Also we have introduced a variable called “position” that allows the *“width”* of the *backgroundPosition* to now be a variable instead of a static. We also used a variable called to set the time of the interval of the setInterval() to 100ms. Thus, now every 100ms the backgroundPosition is updated by 256px to display the next image in the animation leading to a fully animated image on mouseover.

That’s it! 🎉 Now run the JS code in JSFiddle, and mouse over onto the image, and see the sprite run!

![]()

## Step 4: Some Cleanup (Optional)

We can improve the JavaScript by adding a *stopAnimate()* function on *mouseout*, as follows:

### JavaScript Code

```
var tID; //we will use this variable to clear the setInterval()function stopAnimate() {clearInterval(tID);  
} //end of stopAnimate()function animateScript() {var    position = 256; //start position for the image slicer  
const  interval = 100; //100 ms of interval for the setInterval()  
const  diff = 256;     //diff as a variable for position offsettID = setInterval ( () => {document.getElementById("image").style.backgroundPosition =   
`-${position}px 0px`;   
//we use the ES6 template literal to insert the variable "position"if (position < 1536)  
{ position = position + diff;}  
//we increment the position by 256 each time  
else  
{ position = 256; }  
//reset the position to 256px, once position exceeds 1536px}  
, interval ); //end of setInterval} //end of animateScript()
```

### HTML Code

```
<div id="demo">  
  <p id="image" onmouseover="animateScript()" onmouseout="stopAnimate()"></p>  
</div>
```

Thus, now the animation stops when you mouse out of the image. 👍

## Concluding remarks

The final code and animation can be found on [JSFiddle here](https://jsfiddle.net/prashantram/cbf6syjb/5/)!

Notice that the advantage of using sprite animation is that ***we make only one server call***, which is the initial call by the CSS to get the sprite image. Once the image is downloaded the animation is smooth, irrespective of the internet connection, since the entire image is available to the browser.

Press enter or click to view image in full size

![]()

*Found this useful? Hit the* 👏 *button to show how much you liked it!* 🙂

[***Follow me on Medium***](/@prashantramnyc) ***for the latest updates and posts!***

Press enter or click to view image in full size

![]()

**Read Next:** [What is a Webhook?](/@prashantramnyc/what-are-webhooks-b04ec2bf9ca2)

**Other Articles:**

* [Promises in Javascript Explained!](/@prashantramnyc/promises-in-javascript-explained-277b98850de)
* [Javascript — Closures Simplified!](/@prashantramnyc/javascript-closures-simplified-d0d23fa06ba4)