---
title: "An alternative way of writing Single Page Applications (SPA)"
url: https://medium.com/p/635f8c9280b1
---

# An alternative way of writing Single Page Applications (SPA)

[Original](https://medium.com/p/635f8c9280b1)

# An alternative way of writing Single Page Applications (SPA)

[![Kevin Babu](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*q1TDyXbljgoPPE4J)](/@kevinmwita7?source=post_page---byline--635f8c9280b1---------------------------------------)

[Kevin Babu](/@kevinmwita7?source=post_page---byline--635f8c9280b1---------------------------------------)

10 min read

·

Oct 25, 2023

--

Listen

Share

More

“*An SPA (Single-page application) is a web app implementation that loads only a single web document, and then updates the body content of that single document via JavaScript APIs such as* `XMLHttpRequest` *and* [*Fetch*](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) *when different content is to be shown. This therefore allows users to use websites without loading whole new pages from the server, which can result in performance gains and a more dynamic experience*” — [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Glossary/SPA).

This is usually achieved from the client side using JavaScript libraries and frameworks such as React, Solid.JS, Angular and Vue.JS. However, there is another way to achieve this without using JavaScript.

Press enter or click to view image in full size

![Server and browser holding hands]()

## Overview

Before we proceed, I’d like to make a confession. In the beginning I declared that an SPA can be written without JavaScript. This was a lie. We still need some JavaScript to intercept clicks on links, make a request to the server using APIs such as [**Fetch**](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API), and subsequently update specific parts of the webpage with the retrieved HTML content leaving unchanged part as is. Two notable libraries capable of achieving this functionality are [**Turbo**](https://turbo.hotwired.dev/) and [**htmx**](https://htmx.org/docs/). For this tutorial, I will use Turbo and for the backend, I will be using [**Django**](https://docs.djangoproject.com/en/4.2/), a popular Python framework. However, you can build your server using your preferred framework.

## Step 1 - Setting Up Django

For those who want to follow along, start by installing Python from [here](https://www.python.org/downloads/) if you don’t have it already. Once done, clone the repository from [here](https://github.com/KevinMwita7/server-spa). It contains starter code for the website we will be working on. Within it, there is a Django project called **server\_spa** and a Django app called **demo\_app.**

Our website’s code is structured in such a way that the main layout is located in one file, **base.html**, then the other HTML files combine their content with that of **base.html** to create the complete webpage. This is in accordance with the concept of **Don’t Repeat Yourself (DRY).** If I wanted to change the website layout, I simply need to edit **base.html** as opposed to every single HTML file. Django helps us achieve this decoupling via [**template inheritance**](https://docs.djangoproject.com/en/4.2/ref/templates/language/#template-inheritance).

After cloning the repository, navigate into the cloned repo folder and create a Python virtual environment by running `python -m venv env_name`. Replace `env_name` with a suitable name such as `.venv` , which is usually the convention. To learn why a virtual environment is needed, click [here](https://docs.python.org/3/library/venv.html).

Once the command completes a folder with the name you gave to your virtual environmentis created. I am assuming that you named it .`venv`. Run `.venv\Scripts\activate.bat` if using Windows or `source .venv/bin/activate` if you are on Linux to activate the virtual environment. The terminal displays **(.venv)** in front of the path indicating that the virtual environment is now active. To quit the virtual environment, simply type `deactivate`. You’ll do this once the tutorial is complete.

Within the project, there is a file called **requirements.txt** which contains a list of all the modules required by our project. Run `pip install -r requirements.txt` to install the modules listed within it. To learn more on how to create and use a **requirements.txt** file, click [here](https://learnpython.com/blog/python-requirements-file/).

Once done, run `python server_spa\manage.py runserver` and visit [localhost:8000](http://localhost:8000) to see the website running.

## Step 2 — Setting up Turbo

To install **Turbo,** simply include the script below in the `<head>` tag of **server\_spa\demo\_app\templates\demo\_app\base.html** .

```
<!--rest of tags in head-->  
<script type="module">  
  import hotwiredTurbo from 'https://cdn.skypack.dev/@hotwired/turbo';  
</script>
```

I know your masters told you that placing scripts in `<head>` is bad and that such an abomination should never go unpunished. However, the reason for my insolence is that Turbo needs to be initialized early in the page lifecycle to properly intercept navigation events and handle them in a Turbo-driven way. Placing it in the head ensures that it’s available and active as soon as possible.

Now any link that will be clicked is intercepted by **Turbo** which then makes the request on our behalf. However, **Turbo** stills fetches the whole HTML instead of the portion that changed as can be seen on the right sidebar in the image below.

![Turbo fetches the webpage]()

To make **Turbo** only update the changed sections, we need to do the following:

* Wrap the HTML templates in **Turbo’s** custom `<turbo-frame>` tag
* Attach **X-Requested-With** header to each request made by **Turbo.** This helps the server differentiate browser requests from **Turbo** requests
* Send appropriate HTML from server i.e. if it is a browser request deliver whole page else deliver only new section

Let’s start by wrapping all the HTML templates, apart from **base.html**, in `<turbo-frame id="main" data-turbo-action="advance">`tag. From the project’s root folder, the templates are located in `server_spa\demo_app\templates\demo_app`. Use the examples below to guide you on how to wrap pages in `<turbo-frame>` .

![Wrap templates with turbo-frame tag]()

Ensure that all the turbo-frames you create have same id attribute. This way **Turbo** knows which content to replace. Also, ensure that the turbo-frames have the data attribute **turbo-action** with the value **advance**. This tells **Turbo** to push the new webpage into the browser’s history stack thus changing the URL in the address bar. Read more [here](https://turbo.hotwired.dev/handbook/drive#application-visits).

Next, we need to attach the X-Requested-With header to each request made by **Turbo.** We will do this by listening to **Turbo’s** `turbo:before-fetch-request` event. In **base.html**, just before the body’s closing tag, add the code below.

```
<script>  
  document.addEventListener("turbo:before-fetch-request", event => {  
      event.preventDefault();  
      event.detail.fetchOptions.headers["X-Requested-With"] = 'XMLHttpRequest';  
      event.detail.resume();  
  });  
</script>
```

The script tag is added to **base.html** since all the other templates inherit from it. This ensures that when the user visits our website for the first time, the script tag will always be loaded, regardless of the page.

![X-Requested-With header is attached to request made by Turbo]()

Finally, we need to respond with the appropriate HTML from the server. Start by adding a file called **base\_empty.html** in the templates folder. The **base\_empty.html** file differs from **base.html** in that it does not have the extra `<head>`, `<body>`, `<script>` and `<header>` tags. It will simply be an empty file in which our views place their content. Place the code below in the file:

```
{% block content %}{% endblock %}
```

Afterwards, from the project’s root folder, open `server_spa\demo_app\views.py` . On the last line of the file, there is a function called \_base\_template. This function currently returns a string `demo_app/base.html` . We need to modify it to return either **base.html** or **base\_empty.html** depending on whether the X-Requested-With header is present. Replace the current \_base\_template function with the one below:

```
def _base_template(request):  
    return "demo_app/base_empty.html" if "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest" else "demo_app/base.html"
```

Also remember to pass in the `request` argument everywhere you’ve called the `_base_template`function. The final **views.py** file resembles the one below:

```
from django.shortcuts import render, redirect  
from django.http import HttpResponseRedirect  
from .forms import ContactUsForm  
  
# Create your views here.  
def index(request):  
    return render(request, "demo_app/index.html", { "template": _base_template(request) })  
  
def pricing(request):  
    return render(request, "demo_app/pricing.html", { "template": _base_template(request) })  
  
def faq(request):  
    return render(request, "demo_app/faq.html", { "template": _base_template(request) })  
  
def privacy(request):  
    return render(request, "demo_app/privacy.html", { "template": _base_template(request) })  
  
def about(request):  
    return render(request, "demo_app/about.html", { "template": _base_template(request) })  
  
def contact_us(request):  
    if (request.method == "POST"):  
        form = ContactUsForm(request.POST)  
        if (form.is_valid()):  
            response = redirect("/success")  
            response.status_code = 303  
            return response  
    else:  
        form = ContactUsForm()  
  
    return render(request, "demo_app/contact_us.html", { "template": _base_template(request), "form": form })  
  
def success(request):  
    # This page can only be accessed on successful form submissions  
    if "X-Requested-With" not in request.headers or request.headers["X-Requested-With"] != "XMLHttpRequest":   
        return HttpResponseRedirect("/")  
    return render(request, "demo_app/success.html", { "template": _base_template(request) })  
  
# Python has no private access modifiers. To work around this, one adds an underscore (_) before the function  
# or variable to signal to other devs that they are meant to be private. Note that they can still be accessed  
# outside the module since Python does not enforce the convention. It simply trusts that everyone is a "consenting adult"  
def _base_template(request):  
    return "demo_app/base_empty.html" if "X-Requested-With" in request.headers and request.headers["X-Requested-With"] == "XMLHttpRequest" else "demo_app/base.html"
```

Now whenever a request contains the header X-Requested-With, our server knows that its **Turbo** making a request and uses the **base\_empty.html** template to avoid inserting content that already exists in the browser. If the X-Requested-With header does not exist, it means that the browser initiated the requested and we serve **base.html** which contains the extra tags e.g. `<head>`, `<script>` and `<header>`.

Clicking links in our index page’s hero work as expected. However, links in our navbar don’t. The navbar disappears once a user clicks a link in it. We’ll fix this in the next step.

## Step 3 — Decomposition

Remember, that a key feature of Turbo is the `<turbo-frame>` tag, which acts as a container for dynamic content updates. When a link inside a `turbo-frame` is clicked, Turbo seamlessly fetches the linked content via AJAX, replacing only the frame from where the click originated. If a link outside of a `turbo-frame` is clicked, Turbo does not have a specific target for the returned content. In such cases, it reverts to a default behavior, replacing the entire body of the page with the new content. To ensure smooth navigation, it's crucial to correctly configure links and `turbo-frame` targets. This way, Turbo knows precisely where to place the returned content, providing a seamless and fast-paced browsing experience. Therefore, we need to wrap the navbar with a `<turbo-frame>` too.

From the root of the project, open `server_spa\demo_app\templates\demo_app\base.html` . Wrap the header tag in a turbo-frame with an appropriate id, **data-turbo-action** set to **advance** and the **target** set to **main** as shown below:

![Wrap header in turbo-frame tag]()

In the code snippet provided, the `target` attribute instructs **Turbo** on where to place the returned HTML when child links within the enclosing `turbo-frame` tag is clicked. In this case, the `target` attribute is set to "**main**". This means that when a link inside the `turbo-frame` wrapping our header is clicked, Turbo will ensure that the resulting content is inserted into the element on the page whose id matches the value of "**main**".

## Step 4 — Dynamically loading scripts

Now that our SPA is working, we need to find a way to inject scripts when serving HTML fragments to Turbo. **Turbo’s** documentation states that, “*When you navigate to a new page, Turbo Drive looks for any* `<script>` *elements in the new page’s* `<head>` *which aren’t present on the current page. Then it appends them to the current* `<head>` *where they’re loaded and evaluated by the browser. You can use this to load additional JavaScript files on-demand*.” For my case I didn’t see the `<script>` elements in the returned fragments being attached to the `<head>` . However, the JavaScript in returned fragments works. To see code where I included a `<script>` element, check out `server_spa\demo_app\templates\demo_app\faq.html` . You’ll notice that I have set a [**defer**](https://www.w3schools.com/tags/att_script_defer.asp) attribute to the script. This simply instructs the browser to run the the script once it has finished parsing the page.

If you find a way to make Turbo append `<script>` tags from the returned fragments into the `<head>` tag of the HTML document, as is depicted in the [documentation](https://turbo.hotwired.dev/handbook/building#working-with-script-elements), please leave a comment and I will try it.

## **Step 5 — Forms**

In the code snippet below, whenever a POST request is submitted to our `contact_us` view, the form is validated and if valid, the server redirects the browser to a **success** route. **Turbo** will [follow this redirect](https://turbo.hotwired.dev/handbook/drive#redirecting-after-a-form-submission) and place whatever HTML is returned from the server in the browser without tearing the rest of unchanged sections. If the form is not valid we return the form with errors. The advantage of this approach is that we write code to handle validation on one place, server side only, as opposed to both client and server as is done in typical SPA’s.

```
def contact_us(request):  
    if (request.method == "POST"):  
        form = ContactUsForm(request.POST)  
        if (form.is_valid()):  
            response = redirect("/success")  
            # 303 instructs the client to use a GET request for the redirected resource  
            response.status_code = 303  
            return response  
    else:  
        form = ContactUsForm()  
  
    return render(request, "demo_app/contact_us.html", { "template": _base_template(request), "form": form })
```

Finally comes the part where you have to include **CSRF** tokens. In my case, I don’t need to do anything extra as my tokens are hidden within the form and will be submitted and regenerated automatically on each request. This is done by the `{% csrf_token %}` tag in the **contact\_us.html** template. However, when submitting forms via AJAX, one needs to add a `<meta>` tag on initial page load i.e. **base.html** with either the name **csrf-token** or **csrf-param** and Turbo will take the value of this tag and attach it to a header `X-CSRF-TOKEN` on each form submission. See [here](https://turbo.hotwired.dev/handbook/frames#anti-forgery-support-(csrf)).

## Conclusion

The completed code can be found in the **final** branch of the repo [**here**](https://github.com/KevinMwita7/server-spa)**.** Run `git checkout final` from within the cloned repo folder to access it. Additionally, Turbo has more features to offer and we have only just scratched the surface. For instace it has an extremely interesting feature called [Streams](https://turbo.hotwired.dev/handbook/streams) which I would implore you to read about. Finally, if you have any questions, suggestions or need further clarification, don’t hesitate to ask in the comments. I’m here to help! Thanks.