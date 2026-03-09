---
title: "Learn Firebase CRUD App with Vanilla JavaScript NOW — Part 2"
url: https://medium.com/p/c3ca4f4da15d
---

# Learn Firebase CRUD App with Vanilla JavaScript NOW — Part 2

[Original](https://medium.com/p/c3ca4f4da15d)

Member-only story

# Learn Firebase CRUD App with Vanilla JavaScript NOW — Part 2

[![Raja Tamil](https://miro.medium.com/v2/resize:fill:64:64/1*4qFeRXdMqceYBGAwnlcImQ@2x.jpeg)](/?source=post_page---byline--c3ca4f4da15d---------------------------------------)

[Raja Tamil](/?source=post_page---byline--c3ca4f4da15d---------------------------------------)

10 min read

·

Mar 10, 2018

--

Listen

Share

More

![]()

In this Firebase CRUD JavaScript Web Tutorial, You will be learning how to do CREATE, UPDATE and DELETE operations with [Firebase](https://console.firebase.google.com/)Real-time database.

I will be showing you a simple web app example to demonstration Firebase JavaScript CRUD operations.

This is a second part of the Firebase CRUD JavaScript Tutorial series.

The first part covers how to get started with Firebase from **setting up a project** to how to **READ** data from Firebase database.

[**🔥 Part #1: Firebase CRUD JavaScript Tutorial → Setup and Read Data**](http://softauthor.com/learn-to-build-firebase-crud-app-with-javascript-part01-reading-data/)

[**🔥 Part #2: Firebase CRUD JavaScript Tutorial → Insert/Update/Delete data (you’re here)**](http://softauthor.com/firebase-crud-javascript-web-tutorial-part-2-create-update-delete/)

[**1.INSERT:** Add/Insert New User Data to the Firebase Database](#firebase-javascript-crud-add-data)

[**2 UPDATE:** Update/Edit an Existing User](#firebase-javascript-crud-update-data)

[**3 DELETE:** Delete a User from the Firebase Database](#firebase-javascript-crud-delete-data)

**Note**: *I will not be using any permission check when doing these operations. You can check out my other blog* [User Authentication with Firebase](http://softauthor.com/firebase-user-authentication-is-easy-fast-and-secure/)*.*

## [STEP#1. Add/Insert A New User Data to the Firebase Database using Push()](#firebase-javascript-crud-add-data)

There are **three** ways to save data to the Firebase Database that are

* **Push**()
* **Set**() and
* **Update()**

## Push(data, callback):

* **push()** method will insert new data to a given Database reference path and it takes two arguments, one is the actual data that you want to insert and the callback function that will run once the operation is done.
* Thismethod will create a **unique id/key** in a given path as a key and add the data that we passed as a value of that key.

The image below shows the unique keys added to the given Firebase Database reference path when you use push() method.

Press enter or click to view image in full size

![]()

*Note:* As you know, in the first part, I imported JSON data to the Database on the firebase console which is an index-based, like the image below

[caption id=”attachment\_5822" align=”alignnone” width=”2548"]

Press enter or click to view image in full size

![]()

firebase database JSON data structure[/caption]

I recommend using **push unique key** because it has a timestamp in it to avoid overwrites when multiple users push() data at the same time.

I hope I convinced you to use push() method. :)

Oh. Let me explain other two methods **set()** and **update()** later in the [STEP #2 Update](http://www.google.com) section.

Okay, Enough explanation…let’s get started with coding part.

[Here](https://github.com/softauthor/firebase-crud-javascript-02) is the starter project that you can download and follow along with me if you wish.

**1. Add (+) button and User Form:** Add the following HTML code to your **index.html**. This HTML code contains a **<section>** element in which there is a (+) **add button** and a **New User Form**.

```
<!-- add user module -->  
<section id="add-user-module" >  
  <button id="open-add-user-form-btn">+</button>  
  <form>  
    <h2>Add User</h2>  
    name:<br>  
    <input type='text' data-key='name' class='user-input'><br>  
    age:<br>  
    <input type='text' data-key='age' class='user-input'><br>  
    email:<br>  
    <input type='text' data-key='email' class='user-input'><br>  
    <button type='button' id="add-user-btn">add user</button>  
 </form>  
</section>
```

Inside the **Add User Form,** I have three **<input>** fields for **name**, **age**, and **email** andeach one contains a class called **user-input** and an attribute called **data-key.**

**2. Show the Add User Form when a user hovers (+) button:** I have used CSS style to achieve this using **position absolute**. Go ahead and copy the code below and past it into your style.css file.

```
/* Add User Module */  
#add-user-module {  
 width:30px;  
 margin-bottom: 1px;  
 margin-left: 10px;  
 margin-top:10px;  
}#add-user-module #open-add-user-form-btn {  
background: #54bb7d;  
font-size: 1.5em;  
color: white;  
padding-bottom: 5px;  
}#add-user-module form {  
 position: absolute;  
 padding: 10px;  
 width: 150px;  
 background-color: #e1e1e1;  
 border: 1px solid #999;  
 display: none;  
}#add-user-module form input {  
 width: 97%;  
 margin: 2px 0;  
}#add-user-module form button {  
 background: #54bb7d;  
 font-size: 1em;  
 padding: 0px 10px;  
 color: white;  
 margin-top: 10px;  
}#add-user-module:hover form {  
 display: block;  
}
```

At this stage, the form should show when you hover the (+) button…

Moving on…

**Note**: At the top of JavaScript, You need to replace the **config** object with your own credentials otherwise your app will NOT work. If you are not sure where to find your Firebase app config object check out [here](http://softauthor.com/learn-to-build-firebase-crud-app-with-javascript-part01-reading-data/#initialize-firebase-in-app-js).

**3. Attach Click Event to the Add User Button:** Cache **#add-user-btn** DOM element which is inside the **Add User Form.** Then, attach a click event to it with the callback function **addUserBtnClicked()**.

```
const addUserBtnUI = document.getElementById("add-user-btn");  
addUserBtnUI.addEventListener("click", addUserBtnClicked);
```

**4. Create a new user Object**: Inside the call back function, create a Firebase Database reference path where you want to insert the new user data.

```
const usersRef = dbRef.child('users');
```

Then, Get all the input fields from the Add User Form and cache them into an array variable **addUserInputsUI** like so.

```
const addUserInputsUI = document.getElementsByClassName("user-input");
```

After that…create an empty JavaScript object in which I am going to store a new user data as key-value pairs.

```
// this object will hold the new user information  
 let newUser = {};
```

Now, Loop though **addUserInputsUI** array that has three input fields. Then, Inside each iteration get the value of input attribute **data-key** and store it into the variable **key**.

After that… create another variable called **value** and store it in the actual user typed value.

```
// loop through View to get the data for the model   
for (let i = 0, len = addUserInputsUI.length; i < len; i++) {let key = addUserInputsUI[i].getAttribute('data-key');  
let value = addUserInputsUI[i].value;  
newUser[key] = value;  
}
```

Assign the **key** and **value** variables to the **newUser** object on each iteration. So, you will have an object something like this.

```
{  
"age" : "21",  
"email" : "rtamil@email.com",  
"name" : "Raja Tamil"  
}
```

**5. Push it to the Firebase Database:** Finally, push() method will go ahead insert the new user data to the Firebase Database in a given path which is in usersRef.

```
usersRef.push(newUser, function(){  
   console.log("data has been inserted");  
 })
```

That’s simple eh!

As you notice, my user list on the browser has been updated automatically because I am using Firebase event called **value** to get a list of users.

The cool thing about **value** event is that it’s triggered whenever there is a change which could be Add, Delete or Edit in the database reference that this event runs on. You can check out the **value** event more in my other tutorial [here](http://www.google.com)

Next…

## [STEP #2. Edit/Update An Existing User Data in the Firebase Database using](#firebase-javascript-crud-update-data) 📝

You can either use **Update()** or **Set()** to make any change to an existing user data.

Let’s take a look at Update first…

## Update(data, callback):

• You can make changes to one or more values of a user using **update()**. For example, If I want to update just a **name,** I can do it without affecting other keys such as **name** and **age**.

• What happens if I send an object that has a key which is not in the Firebase Database? well, the cool thing about the **update()** method is whenever there is a key match, this method will update the value of it.

• If there is no key match, then update() method will insert it in as a new key.

On the other hand,

**Set(data, callback):**

• **set()** method will replace everything in a given Firebase Database Reference path. For example, if the javascript object that you’re going to update, has the only {name: “raja”}**, set()** method will overwriteeverything in that specific pathandall other keys will be deleted. It’s kind of dangerous because you may lose data without knowing.

• If you want to intentionally change any user object value to be **null, set()** method would be great for it.

Let’s make the edit user functionality working…

**1. Edit User Form:** Add the below HTML code for **Edit User Form** to index.html file. This form is very similar to **Add User Form** except for one extra **hidden** input field with the class name **edit-userid** whichisused to set and get the user id.

```
<!-- edit user module -->  
 <section id="edit-user-module">  
 <form>  
 <h2>Edit user</h2>  
 <input type="hidden" class="edit-userid">  
 name:<br>  
 <input type='text' data-key='name' class='edit-user-input'><br>  
 age:<br>  
 <input type='text' data-key='age' class='edit-user-input'><br>  
 email:<br>  
 <input type='text' data-key='email' class='edit-user-input'><br>  
 <button type='button' id="edit-user-btn">save</button>  
 </form>  
 </section>
```

**2. Make Edit Form Pretty:** Add the CSS code below to the style.css. As you can see I use **display: none** to hide the form initially, then I will use JavaScript to show when a user clicks the edit button which I will add the next.

```
/*Edit*/  
#edit-user-module {  
  display: none;  
  position: absolute;  
  background-color: #e1e1e1;  
  border: 1px solid #999;  
  top:149px;  
  left: 160px;  
  padding: 10px;  
  width: 150px;  
}#user-list li:hover~#edit-user-module {  
  display: none;  
}#edit-user-module form button {  
 background: #54bb7d;  
 font-size: 1em;  
 padding: 0px 10px;  
 color: white;  
 margin-top: 10px;  
}
```

Let’s add the edit button next…

**3. Add Edit button:** Add Edit icon (✎) inside **<li>** via JavaScript

```
// edit icon  
 let editIconUI = document.createElement("span");  
 editIconUI.class = "edit-user";  
 editIconUI.innerHTML = " ✎";  
 editIconUI.setAttribute("userid", key);  
 editIconUI.addEventListener("click", editButtonClicked)  
 // Append after li.innerHTML = value.name  
 $li.append(editIconUI);
```

Create **editIconUI** span element, then attach a click event to it with a callback function **editButtonClicked()**.

Make sure to append **editIconUI** to **<li>** after appending li.innerHTML, so that the edit icon will be shown after the username text.

4. **Show Edit Form with the User Data:** Get the Edit User Form DOM element and set the display property to **block** which makes the Form visible.

```
// show the Edit User Form  
 document.getElementById('edit-user-module').style.display = "block";
```

Then, assign **user id** which you get from the edit button with an attribute **userid** to the hidden **<input>** text field **edit-userid**. So that I will have user id is available when I click the save button from the Edit From to update the user data later.

```
//set user id to the hidden input field  
 document.querySelector(".edit-userid").value = e.target.getAttribute("userid");
```

After that, create a Firebase Database reference path where to get selected user data by **userid**.

```
const userRef = dbRef.child('users/' + e.target.getAttribute("userid"));
```

Next, create a variable that will have all the input fields from the Edit User Form

```
// set data to the user field  
 const editUserInputsUI = document.querySelectorAll(".edit-user-input");
```

Now, I am going to define afirebase event called “**value**” on the **userRef** variable. The second argument in that event is a call back function with parameter **snap** which will have the selected user data.

```
userRef.on("value", snap => {  
 for(var i = 0, len = editUserInputsUI.length; i < len; i++) {  
  var key = editUserInputsUI[i].getAttribute("data-key");  
   editUserInputsUI[i].value = snap.val()[key];  
 }  
});
```

Inside that callback event, loop through the **editUserInputsUI** array and get the value of an attribute **data-key** on each iteration and store it in a variable key**.** So that I can assign an appropriate value from **snap.val()[key]** to the input field.

*Note*: **value** Firebase event will return promise as well as a callback. For the simplicity sake, I am not going to handle the error using callback/promises.

At this stage, a user will be able to see the **Edit User Form** with selected user data filled in when the edit button is clicked.

5. **Save the updated user data on to the Firebase Database:** When a user makes some changes and hit **save** button, the edited data will be saved to the Firebase database.

To do that, Get a save button and attach a click event to that with the callback function **editButtonClicked().**

```
const saveBtn = document.querySelector("#edit-user-btn");  
 saveBtn.addEventListener("click", saveUserBtnClicked)
```

As you can see I have created **saveBtn** and attache click event with the callback function **saveUserBtnClicked.**

Inside the callback function, create variable that will have the userid value which you can get it from the hidden text field.

```
const userID = document.querySelector(".edit-userid").value;
```

Then, create a database reference where you want to update the new changes**.**

```
const userRef = dbRef.child('users/' + userID);
```

After that, create an empty object that I will store the updated data from the user input fields.

```
var editedUserObject = {}
```

Get all the **<input>** fields from **Edit User Form** and store them in an array **editUserInputsUI.**

```
const editUserInputsUI = document.querySelectorAll(".edit-user-input");
```

Now, Loop though **editUserInputsUI** array and in each iteration get the value from the <input> attribute **data-key** and store it in the **key** variable and get the user typed value from <input> field and store in the variable **value.**

```
editUserInputsUI.forEach(function(textField) {  
 let key = textField.getAttribute("data-key");  
 let value = textField.value;  
 editedUserObject[textField.getAttribute("data-key")] = textField.value  
 });
```

Then, assign the **key** and **value** variables to the **editedUserObject** object on each iteration.

Now, you will have an object that is ready to update.

Finally, user update() method.

```
userRef.update(editUser, function(){  
   console.log("user has been updated");   
 });
```

One more thing, I need to do for the usability purpose which is to hide the **Edit User Form** when a user clicks the save button.

```
document.getElementById('edit-user-module').style.display = "none";
```

## [3. DELETE: Remove/Delete a user data from the Firebase Database](#firebase-javascript-crud-update-data)

## remove(data, callback)

The remove() method will remove everything from a given database reference path and it takes two arguments, one is the data *in this case user id* and the callback function that will run once the delete operation is completed.

If you want to keep the userid and remove all the data inside it, you could use **set()** to replace with **null**

1. **Add a Delete Icon to the <li>**

```
// delete icon  
 let deleteIconUI = document.createElement("span");  
 deleteIconUI.class = "delete-user";  
 deleteIconUI.innerHTML = " ☓";  
 deleteIconUI.setAttribute("userid", key);  
 deleteIconUI.addEventListener("click", deleteButtonClicked)  
   
 $li.append(deleteIconUI)
```

Similar to edit Icon, append **delete icon** after **li.innertHTML** line, so that the delete icon will be on the right side.

**2. deleteButtonClicked():** Inside this callback function, I use **e.stopPropagation()** that will stop clicking the **<li>** when you click the delete button it called **Event Bubbling**.

```
function deleteButtonClicked(e) {  
  e.stopPropagation();  
  const userID = e.target.getAttribute("userid");  
  const userRef = dbRef.child('users/' + userID);  
  userRef.remove()  
}
```

Then, get the user id that you want to delete from the delete button using **userid** attribute.

Next, create a database path reference where you want to remove the data from.

Finally, invoke **remove()** method on **userRef**.

That’s it.

## In conclusion

Congratulations, You have successfully completed Firebase CRUD JavaScript/js tutorial by creating a simple User Web App with the CRUD operations.

Along the way I also showed you the **value** Firebase Event and as well as Firebase methods such as **Push**, **Set** and **Update** and their differences.

You can find the full source code [here](https://github.com/softauthor/firebase-crud-javascript-02).

Let me know what kind of application is going to build with Firebase and JavaScript?

Feel free to **comment** below if you have any **question** about what you have learned or **suggestion**.

## Recommended

🔥 [JavaScript + Firebase: Get Logged In User Data [RTDB]](https://softauthor.com/javascript-firebase-get-logged-in-user-data-real-time-database/)  
🔥 [How To Query, Filter And Sort Firebase Real-Time Database](https://softauthor.com/firebase-querying-sorting-filtering-database-with-nodejs-client/)  
🔥 [FirebaseUI + Vue.js: Build A Complete Login Page](https://softauthor.com/firebaseui-vue-login-with-facebook-google-and-email-pasword/)