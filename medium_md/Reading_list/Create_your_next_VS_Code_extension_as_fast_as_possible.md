---
title: "Create your next VS Code extension as fast as possible"
url: https://medium.com/p/a110539c91d7
---

# Create your next VS Code extension as fast as possible

[Original](https://medium.com/p/a110539c91d7)

# Create your next VS Code extension as fast as possible

## Everything you need to know to start building your next VS Code extension now 🚀

[![Fabio Sabbion](https://miro.medium.com/v2/resize:fill:64:64/1*Ozb7LJ0AcZWt4D8j2n56Wg.jpeg)](/@fabio.sabbion?source=post_page---byline--a110539c91d7---------------------------------------)

[Fabio Sabbion](/@fabio.sabbion?source=post_page---byline--a110539c91d7---------------------------------------)

4 min read

·

Sep 30, 2021

--

1

Listen

Share

More

Developing a VS Code extension was a little confusing to me at first. The official documentation didn’t help a lot, so I started watching a bunch of video tutorials, and in this guide I’m going to summarize for you everything I learned, so that you can build your first/next VS Code extension as fast as possible.

## What are you going to learn

By the end of this tutorial you will have a fully functional VS Code extension with a sidebar panel able to display info and error messages and providing custom commands.

This is everything you will learn in one image:

Press enter or click to view image in full size

![]()

## Prerequisites

To make sure we are all on the same page, this is what you need to know before we get started:

* Javascript / Typescript

And these are the tools I assume you already have installed:

* npm
* git

## Let’s get started!

First of all we are going to download a starting template. Open the terminal and run the following command:

```
git clone https://github.com/sfabio01/vscode-extension-template.git my_extension
```

Jump inside the newly created folder and run

```
npm i
```

to install all the dependencies.

At this point open the project in VS Code and press F5. A new window should pop up with our extension loaded.

Press enter or click to view image in full size

![]()

The extension provides also a custom command called “*Say hello”*. To try it, press CTRL+SHIFT+P and search for the name of the command.

Okay, let’s take a look at the code…

![]()

In the *src* folder there are extension-related files. Here you register your custom commands and your components such as the sidebar. From this folder you have access to the **vscode APIs**, that you can use to interact with the editor, execute actions, and more.

In the *components* folder is placed the UI of the extension, such as the Sidebar. From here you don’t have access to the vscode APIs, but you can exchange messages with the extension.

### extension.ts

Like the name suggests, this file is the entry point of our extension. Here you define the Sidebar, as well as the custom commands your extension provides. Let’s add a new command.

Uncomment lines 16 to 18 and change the name of the command from ‘myextension.commandname’ to ‘**myextension.askquestion**’. We are going to use the VS Code APIs to display a popup with a question and two options, and then store the answer in a variable:

```
let response = await vscode.window.showInformationMessage("How are you doing?", "Good", "Bad");
```

Then, we check whether the response is “Bad”: if so, we say we are sorry.

```
vscode.window.showInformationMessage("I'm sorry");
```

This is the final version of *extension.ts*:

Now, let’s go to ***package.json*** to describe our new command.

Add the following value to the “activationEvents” field:

```
"onCommand:myextension.askquestion"
```

and the following object to the “contributes.commands” field:

```
{  
  "command": "myextension.askquestion",  
  "category": "MyExtension",  
  "title": "Ask question"  
}
```

The command is now ready to be executed. Switch to the development window and press CTRL+R to reload it. Press CTRL+SHIFT+P and search for our new command.

### SidebarProvider.ts

This file is the entry point of our sidebar. The important part here is the function ***onDidReceiveMessage***at line 22. This function listens for messages from the UI and execute different events accordingly. This is important because here you have access to the VS Code APIs, while from the UI you don’t.

### Sidebar.svelte

This is the actual body of the sidebar.

If you don’t know what Svelte is, take a look at their [official tutorial](https://svelte.dev/tutorial/basics).

Similarly to “onDidReceiveMessage**”**, in the function ***onMount***we listen for messages from the extension.

Let’s try to use these listeners to make something useful.

Add a button and a text area to the sidebar. When we click the button, we want to get the currently selected text from the editor, and paste it in the text area.

To get the code from an editor we can use the vscode apis, but remember, we can’t access them from the UI, so we are going to send a message to the extension. Once the extension has got the text, we need to return it to the UI with another message. This is the final Sidebar.svelte:

Now go to *SidebarProvider.ts* and add the “**onFetchText**” event to the listener function. This is the complete *onDidReceiveMessage* function:

We did it! Let’s try it in action. Open the development VS Code window and press CTRL+R.

Press enter or click to view image in full size

![]()

### Extension icon

To change the extension icon, go to **media/icon.svg** and paste an svg string. You can find a bunch of vscode-style icons [here](https://github.com/microsoft/vscode-codicons/tree/main/src/icons).

## Conclusion

And that’s all. If you have found this guide useful consider following me for more 🤗

Check out the VS Code extension I built following this guide: [AskOverflow — Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=fabio-sabbion.askoverflow)

VS Code APIs: [VS Code API | Visual Studio Code Extension API](https://code.visualstudio.com/api/references/vscode-api)

Complete tutorial: [sfabio01/vscode-extension-template/complete-tutorial](https://github.com/sfabio01/vscode-extension-template/tree/complete-tutorial)