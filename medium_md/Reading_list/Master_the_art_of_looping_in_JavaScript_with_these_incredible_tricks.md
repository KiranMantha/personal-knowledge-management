---
title: "Master the art of looping in JavaScript with these incredible tricks"
url: https://medium.com/p/a5da1aa1d6c5
---

# Master the art of looping in JavaScript with these incredible tricks

[Original](https://medium.com/p/a5da1aa1d6c5)

# Master the art of looping in JavaScript with these incredible tricks

[![Yogi](https://miro.medium.com/v2/resize:fill:64:64/1*dbLshUeIWu50o2a963ywDg.jpeg)](/@yogihosting?source=post_page---byline--a5da1aa1d6c5---------------------------------------)

[Yogi](/@yogihosting?source=post_page---byline--a5da1aa1d6c5---------------------------------------)

10 min read

·

Jan 7, 2019

--

10

Listen

Share

More

![]()

Many times in your code you require to loop through an **array of numbers, strings or object**. There are just so many ways to do it, and this tutorial aims to teach you all of them so that you become a Master of ‘Looping in JavaScript’.

See this ninja cat who is the master of jumping.

Like the cat, you will also become a Master of JavaScript Looping, after you know all the looping tricks.

## **1. The “For” Loop**

The **For Loop** is the most basic way to loop in your JavaScript code. It is very handy to execute a block of code a number of times. It uses a **counter**, whose value is first initialized, and then its final value is specified.

The **counter is increased by a specific value** every time the loop runs. The for loop checks if the counter is inside the limits (initial value to final value), and the loop ends when the counter value goes over the final value.

Let me show you some examples.

### a. Looping through an Array

In the below code, I am looping through all the **numbers in an array**, and printing each of them on the console window.

```
var numbers = [10, 20, 30, 40, 50];  
for (var i = 0; i < numbers.length; i++) {  
    console.log(numbers[i]);  
}
```

In the same way you can loop through arrays of string too.

### b. Looping through DOM elements

Suppose you want to **find and color all the anchors** in the page red. Then here too, you can use the **For Loop** like this:

```
var elements = document.querySelectorAll("a");  
for (var i= 0; i < elements.length; i++) {  
    elements[i].style.color = "red";  
}
```

*Explanation*: I first got all the anchors in an array by using `document.querySelectorAll("a")`. Then I simply looped through them and changed their color to red.

I went to the W3Schools site and ran the above code on the browser console, and see what it did:

Press enter or click to view image in full size

![]()

> Note: **jQuery** also has a very good looping method called [**jQuery Each method**](https://www.yogihosting.com/jquery-each/) which helps you loop through arrays, objects, DOM elements, JSON & XML quite easily. If you are using jQuery in your website then consider using it while looping.

## **2. The “For In” loop**

The **For In** loop is used for looping through the **properties of an object/array** without using a ‘counter’. So it is a simplified version of the **For Loop**.

The block of code inside the loop will be executed once for each property.

### a. Looping through an Object Properties

I have an object that contains some properties. I will use the **For In loop** to search out every property and it’s value.

The below code **prints all the properties and their values** in the console window.

```
var person = { fname: "Nick", lname: "Jonas", age: 26 };  
for (var x in person) {  
    console.log(x + ": " + person[x])  
}
```

![]()

### b. Looping through JSON

**JSON** is a very popular format to transmit data objects consisting of **attribute–value** pairs and array data types. Websites use JSON to share their information with external websites. Now I will tell you how to extract data from a JSON.

Suppose I have some JSON containing some information, as shown below:

```
jsonData: {  
one: [11, 12, 13, 14, 15],  
two: [21, 22, 23],  
three: [31, 32]  
}
```

The JSON has a root node called ‘*jsonData*’, and this contains 3 nodes — ‘*one*’, ‘*two*’, ‘*three*’. The nodes are also called keys.

The below code shows how to extract information from JSON using the *For In* loop:

```
var json = {  
jsonData: {  
one: [11, 12, 13, 14, 15],  
two: [21, 22, 23],  
three: [31, 32]  
}  
};for (var key in json.jsonData) {  
    for (var key1 in json.jsonData[key]) {  
        console.log(json.jsonData[key][key1])  
    }  
}
```

*Explanation*: There are **2 For In loops** in the above code — Outer loop & Inner loop.

The **Outer Loop** runs 3 times and covers nodes ‘one’, ‘two’ & ‘three’.   
   
 The **Inner Loop** covers all the values inside the selected node i.e the nodes ‘one’, ‘two’, & ‘three’.

Run the code in your web page or in your browser’s console window, and you will see all the values of the nodes printed, like in the below image:

![]()

### **Going a little deeper into the JSON**

The same JSON can be expressed by putting **[]** to contain the 3 nodes ‘one’, ‘two’, ‘three’:

```
jsonData: [{  
one: [11, 12, 13, 14, 15]  
}, {  
two: [21, 22, 23]  
}, {  
three: [31, 32]  
}]
```

Now I will use a combination of **For & For In** loops to extract all information from this JSON. The below code does this work for me:

```
var json = {  
jsonData: [{  
one: [11, 12, 13, 14, 15]  
}, {  
two: [21, 22, 23]  
}, {  
three: [31, 32]  
}]  
};for (var i = 0; i < json.jsonData.length; i++) {  
    for (var key in json.jsonData[i]) {  
        for (var j = 0; j < json.jsonData[i][key].length; j++) {  
            console.log(json.jsonData[i][key][j])  
        }  
    }  
}
```

## **3. The “While” loop**

The **While Loop** has a condition specified in it. It checks the condition and executes the code block as long as the **condition is true**. Note that the while loop **does not have** **a counter** like the for loop.

### a. Looping through an HTML table element

Suppose I have an **HTML table** that shows the prices of different products. This HTML table looks like the below image:

![]()

You can see that this table does not show the **total price** of all the products. So if there is a requirement for you to show the total price then you can **loop through all the prices** and show the total in the table footer. This is how you will do it.

Add the HTML Table code to your web page:

```
<table id="priceTable">  
    <tr>  
        <th>Id</th>  
        <th>Product Name</th>  
        <th>Product Price</th>  
    </tr>  
    <tr>   
        <td>1</td>  
        <td>Shirts</td>  
        <td>49.99</td>  
    </tr>  
    <tr>  
        <td>2</td>  
        <td>Pants</td>  
        <td>55.50</td>  
    </tr>  
    <tr>   
        <td>3</td>  
        <td>Socks</td>  
        <td>20</td>  
    </tr>  
    <tr>  
        <td>4</td>  
        <td>Shoes</td>  
        <td>99</td>  
    </tr>  
    <tr>  
        <td>5</td>  
        <td>Jackets</td>  
        <td>88.90</td>  
    </tr>  
</table>
```

Next, add the CSS for giving proper design to this html table:

```
<style>  
    #priceTable {  
       font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;  
       border-collapse: collapse;  
       width: 100%;  
    }        #priceTable td, #priceTable th {  
            border: 1px solid #ddd;  
            padding: 8px;  
        }        #priceTable tr {  
            background-color: #f2f2f2;  
        }        #priceTable th {  
            padding-top: 12px;  
            padding-bottom: 12px;  
            text-align: left;  
            background-color: #4CAF50;  
            color: white;  
        }  
</style>
```

Now loop through the table with the **While loop** and calculate the sum of all products. So add the below JavaScript code to your web page that does this work:

```
var table = document.getElementById("priceTable");var i = 1;  
var sum = 0;  
while (i < table.rows.length) {  
    sum += parseFloat(table.rows[i].cells[2].innerHTML)  
    i++;  
}var row = table.insertRow(i);  
var cell1 = row.insertCell(0);  
var cell2 = row.insertCell(1);  
var cell3 = row.insertCell(2);cell2.innerHTML = "Total Price";  
cell3.innerHTML = sum;
```

*Explanation*: First I get the reference of the table by using `var table = document.getElementById("priceTable")`. Then I added 2 variables called ‘i’ and ‘sum’. The variable ‘i’ is the conditional variable of the while loop, while ‘sum’ will keep adding the price of every product into it.

So I ran the **while loop** for the variable ‘i’ value from 1 to the (total rows -1). I got the total rows in the table by **table.rows.length** and added it to the condition of the while loop:

`while (i < table.rows.length) {  
 //…  
 }`

*Note*: The table has 6 rows from index 0 to 5, and each row has 3 columns from index 0 to 2. I specifically ran the loop from ‘i’ variable value of 1 and not 0. This is because in the 0th index of the table’s row there is the column’s name (which I don’t need).

Inside the while loop I kept on adding the values of each product’s price to the sum variable like this:`sum += parseFloat(table.rows[i].cells[2].innerHTML)` and at the end increased the value of ‘i’ by 1.

For example, when ‘i’ value is 1 then `table.rows[1]` gives me the first row (first ‘tr’ element). Similarly `table.rows[1].cells[2]` will give the value of price column (price ‘td’ element) of the first row.

After the loop completes, I am adding a **new row to the table** at the very end. Inside this row I am adding the 3 columns — 0th index, 1st index, and 2nd index. Finally I am showing the string ‘total’ in the 1st column and total price contained in the ‘sum’ variable in the **2nd column**.

The code which does the addition of this new row is:

```
var row = table.insertRow(i);  
var cell1 = row.insertCell(0);  
var cell2 = row.insertCell(1);  
var cell3 = row.insertCell(2);cell2.innerHTML = "Total Price";  
cell3.innerHTML = sum;
```

The `table.insertRow(i)` will add a 6th row because variable ‘i’ value is 6 at the time the **While Loop** ends.

Columns (‘td’ element) are added to this new row by `row.insertCell(0), row.insertCell(1), row.insertCell(2)`.

I show a value inside the column by:

```
cell2.innerHTML = "Total Price";  
cell3.innerHTML = sum;
```

The above JavaScript code will create a new row containing the total price of the product. Now the table will look like:

![]()

### b. An infinite Looping

Below is the infinite loop in the While statement:

```
var infiVal = true;while (infiVal) {  
// your code  
}
```

Note: Infinite loops can hang the browser so it is required to run the loop at a gap of a few milliseconds. You can use the **JavaScript setInterval method** to run a given function every 1000 milliseconds. See the below code:

```
var myVar = setInterval(myTimer, 1000);function myTimer() {  
// your code  
}
```

> Reference Tutorial — [**Understanding “setTimeout()” and “setInterval()” timer methods in jQuery/JavaScript**](https://www.yogihosting.com/settimeout-setinterval-functions/)

## **4. The “Do While” loop**

In **Do While loop** the condition to be **checked is given at the end,** and so the loop executes at least once even if the condition is not true. Check the below code that will give a ‘Hello’ message on the alert box, even if the condition is false right from the beginning (as variable ‘i’ value is always greater than 1).

```
var i = 2;do {  
    alert("Hello");  
    i++;  
}  
while (i < 1);
```

### a. Looping through XML

Now I will use the **Do While loop** for how to **loop through XML** and extract data from it. I have an XML file called ‘XMLFile1.xml’ whose content is:

```
<?xml version="1.0" encoding="utf-8" ?>  
<cities>  
    <city>Washington DC</city>      
    <city>Islamabad</city>  
    <city>Beijing</city>  
    <city>Tokyo</city>  
</cities>
```

I will use **AJAX to read this XML file** and then loop through it with Do While loop. The below code prints all the names of the cities (given in the XML file) in the console window.

```
var xhttp = new XMLHttpRequest();  
xhttp.onreadystatechange = function () {  
    if (this.readyState == 4 && this.status == 200) {  
        myFunction(this);  
    }  
};  
xhttp.open("GET", "XMLFile1.xml", true);  
xhttp.send();function myFunction(xml) {  
    var xmlDoc = xml.responseXML;  
    var cityNames = Array.from(xmlDoc.getElementsByTagName("city"));  
    var i = 0;    
      
    do {  
        console.log(cityNames[i].innerHTML);  
        i++;  
    }  
    while (i < cityNames.length);  
}
```

*Explanation*: I created an **XMLHttpRequest** object for making the AJAX call. When the XML file is read then the event called **onreadystatechange** is raised, see below code:

```
xhttp.onreadystatechange = function () {  
    if (this.readyState == 4 && this.status == 200) {  
        myFunction(this);  
    }  
};
```

In this event I am calling my custom function called **myFunction()**. Here, I store the XML contents inside a variable called **xmlDoc**:

`var xmlDoc = xml.responseXML;`

Then I converted all the city names into an **array**:

`var cityNames = Array.from(xmlDoc.getElementsByTagName("city"));`

Finally I loop through this array of cities using **Do While loop** and print each city name in the console window:

```
var i = 0;  
do {  
    console.log(cityNames[i].innerHTML);  
    i++;  
}  
while (i < cityNames.length);
```

The below image illustrates the output printed on the console:

![]()

## **5. The “.forEach()” method**

The ES6 edition of JavaScript introduced a new method called `.forEach()` for looping through an array elements. You will find it very handy when dealing with Arrays.

### a. Looping through an array with .forEach() method:

In this situation I loop through an array element with the **.forEach()** method and print the **index** and **value** of every **element** in the console window. See the code below:

```
var names = ["jerry", "tom", "pluto", "micky", "mini"];  
names.forEach(Function1);function Function1(currentValue, index) {  
    console.log("Array Current Index is: " + index + " :: Value is: " + currentValue);  
}
```

**Function1** is the name of the function which gets called for every element of the array. In my case it will be called 5 times. It accepts 2 parameters — ‘index’ and ‘value’ of the current element.

**Note** that you can convert an object to an array by using the **Array.from()** method:

```
var linksArr = Array.from(links);
```

## ***Conclusion***

Thank you for your time reading this tutorial. I hope it has taught you something new about dealing with loops in JavaScript. Now you can apply any of your favourite loop tactics, described in this tutorial, in your web project.

![]()

I publish 2 web development articles per week. Consider following me and get notification whenever I publish a new tutorial on Medium. If this post was helpful, please click the clap button for a few times to show your support! *It will bring a smile on my face and motivate me to write more for the readers like you.*

> I have also published another tutorial on freeCodeCamp, you would like to see it too — [How to create a login feature with Bootstrap Modal and jQuery AJAX](https://medium.freecodecamp.org/how-to-create-a-login-feature-with-bootstrap-modal-and-jquery-ajax-53dc0d281609)

Thanks and Happy Coding!