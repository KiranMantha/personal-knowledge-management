---
title: "The Placement of Script Tags in HTML: Choosing Between Top and Bottom"
url: https://medium.com/p/70c975d1d91b
---

# The Placement of Script Tags in HTML: Choosing Between Top and Bottom

[Original](https://medium.com/p/70c975d1d91b)

# The Placement of Script Tags in HTML: Choosing Between Top and Bottom

[![Sagar Bawane](https://miro.medium.com/v2/resize:fill:64:64/1*wBTOEVnxcLsEc9DgVs19Vg.jpeg)](/@sagarbawane?source=post_page---byline--70c975d1d91b---------------------------------------)

[Sagar Bawane](/@sagarbawane?source=post_page---byline--70c975d1d91b---------------------------------------)

3 min read

·

Jun 22, 2023

--

Listen

Share

More

Introduction

When including JavaScript code in an HTML document, one important consideration is the placement of the script tags. Traditionally, it was recommended to place script tags at the bottom of the HTML document, just before the closing </body> tag. However, with advancements in web development practices and browser optimizations, the placement of script tags has become more flexible. In this article, we will explore both the traditional and modern approaches to help you make an informed decision on where to position your script tags.

The Traditional Approach: Placing Script Tags at the Bottom

The traditional recommendation of placing script tags at the bottom of the HTML document stems from several reasons:

1. Page Loading Performance: Placing script tags at the bottom allows the browser to load and render the HTML, CSS, and other content first, without being delayed by JavaScript execution. This can result in faster page loading times, especially for larger JavaScript files.
2. Render Blocking: JavaScript execution can block the rendering of the page. By placing scripts at the bottom, the critical content of the page is displayed to the user before JavaScript execution occurs, preventing any potential delays in rendering.
3. Perceived Performance: Users often perceive a webpage as faster when they see visual content loading quickly. By prioritizing the rendering of visible elements over JavaScript execution, placing script tags at the bottom can give users a sense of progress and responsiveness, improving the overall user experience.

The Modern Approach: Asynchronous and Deferred Loading

With advancements in web technologies, alternative approaches to script loading have emerged:

1. Asynchronous Loading: By adding the “async” attribute to the script tag, you can load the script asynchronously. This means that the browser will continue parsing and rendering the HTML document while the script is being downloaded in the background. Asynchronous loading is suitable for scripts that don’t rely on the page’s structure or other scripts and can enhance loading speed by allowing multiple scripts to be downloaded concurrently.
2. Deferred Loading: The “defer” attribute, when added to the script tag, allows the script to be deferred until after the HTML document has been parsed. Deferred scripts are executed in the order they appear in the document, just before the </body> tag. Deferred loading is beneficial for scripts that depend on the page’s structure or other scripts, ensuring that they are executed in the correct order.

Choosing the Right Approach

When deciding where to place your script tags, consider the following guidelines:

1. Critical Scripts: Scripts necessary for the initial rendering and functionality of the page should be placed in the head section, preferably with the “async” or “defer” attribute, to ensure they are loaded and executed early in the page lifecycle.
2. Non-Critical Scripts: Scripts that enhance functionality but are not essential for the initial page rendering can be placed at the bottom, just before the closing </body> tag. This allows the page content to load first, providing a better user experience.
3. Optimization and Compatibility: Assess the specific requirements of your website and consider browser compatibility. Modern browsers handle script loading optimizations more effectively, but if you need to support older browsers, the traditional approach of placing scripts at the bottom may be more suitable.

Conclusion

The placement of script tags in HTML documents has evolved with the advancements in web development practices and browser technologies. While the traditional recommendation suggests placing scripts at the bottom, the modern approach allows for more flexibility through asynchronous and deferred loading. Consider the criticality of your scripts, page loading performance, and browser compatibility when determining the ideal placement for script tags. By choosing the right approach, you can optimize the loading speed and user experience of your web pages.