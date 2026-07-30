---
title: list of accessibility tools
topic: css
tags:
  - accessibility
  - tools
source_type: hands-on
confidence: confirmed
created: '2026-07-29'
---
# Opensource accessibility audit tools you must know
Accessibility is the ability to make websites usable by everyone. When a website is not accessible, we are creating barriers and making their impairment a disability. We need to build websites and include accessibility testing in our STLC to cater to people with disabilities for both better business and usability. Accessibility testing involves checking whether a website abides by WCAG guidelines and accessibility legislation and yields better SEO.

Accessibility (a11y) audit is a combination of automated and manual testing done using assistive tools. An audit tool helps the recipient to understand the issues, provides steps to reproduce the issue, recommendations for guidance and output the compliance goal.

Let's explore some of the widely-used accessibility audit tools

### Lighthouse

[Lighthouse](https://developers.google.com/web/tools/lighthouse) is an open-source, automated tool that can audit web pages regarding performance or accessibility issues. 

Lighthouse audit report consists of accessibility score, rules that elements fail to meet, passed audits, ‘additional items to manually check’ and ‘not applicable audit for the web page’. Audit scoring is done based on the categories mentioned below and a report is generated:

*   Navigation
*   ARIA
*   Names and Labels
*   Contrast
*   Tables and list
*   Best Practices
*   Audio and video
*   Internationalization and localization
*   Additional items to manually check

**Lighthouse is available in three workflows:**

*   Chrome DevTools
*   Command Line (Node CLI)
*   Chrome/Firefox Extension

#### A\] Chrome DevTools

Lighthouse is built-in the Chrome browser, with no setup or extensions to install, and can be used to test both local sites and authenticated pages. Here’s how you can audit URLs accessibility via Lighthouse Chrome DevTools: 

1.  Launch the URL you want to audit in Google Chrome
2.  Open the Chrome DevTools (**_Shortcut_** - _Command+Option+C (Mac), Control+Shift+C (Windows, Linux, Chrome OS)_)
3.  Click on the **_Lighthouse_** panel
4.  DevTools shows a list of audit categories
5.  Select ‘Desktop’, ‘Accessibility’, ‘No throttling’ and ‘Clear storage’ options
6.  Click ‘Run audits’
7.  Google Lighthouse gives your page a score out of 100

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312c1_image13_1.png)

Attached to each section of the report is a **documentation/link** explaining why that part of your page was audited and how to fix it. 

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312a2_image14_2.png)

#### B\] Command Line (Node CLI)

Lighthouse can be configured and reported for advance usage via Node CLI. Follow the below-mentioned steps: 

1.  Download Node [here](https://nodejs.org/en/). If you have it installed already, skip this step
2.  Install Lighthouse  
    

```

npm install -g lighthouse

```


1.  3\. Run your audit

```

# Run audit on the given url
lighthouse https:www.qed42.com
```


1.  4\. By default, Lighthouse generates the report in an HTML format. The report can also be displayed in **JSON** format by passing flags.

‍

```

# JSON output sent to stdout
lighthouse --output json

# Saves `./report.json`
lighthouse --output json --output-path ./report.json
```


####   
C\] Chrome Extension

1.  Install the [Lighthouse Chrome Extension](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk) from the Chrome Webstore
2.  Navigate to the page you want to audit
3.  Click Lighthouse Icon, next to the Chrome address bar
4.  Click Generate report.

**_Note:_** _“The DevTools workflow is the best as it provides the same benefits as the extension workflow, with the added bonus of no installation needed.”_

### WAVE

The [WAVE](https://wave.webaim.org/) tool is a web accessibility evaluation tool, which helps analyze a website for accessibility and compliance with Web Content Accessibility Guidelines (WCAG) standard. WAVE is hosted by webaim.org, and is available as a ‘Website’ and as an ‘extension for Chrome/Firefox browsers’.

####   
A\] The WAVE website

1.  Visit  [http://wave.webaim.org](http://wave.webaim.org/) and enter the webpage URL in the address field and hit “Enter”
2.  WAVE displays a version of the web page, highlighting essential accessibility information using inline icons 
3.  The WAVE report will be generated with a summary on the left-hand side of the navigation

####   
B\] WAVE Browser Extensions

The WAVE [Chrome](https://chrome.google.com/webstore/detail/wave-evaluation-tool/jbbplnpkjmmeebjpijfedlgcdilocofh) and [Firefox](https://addons.mozilla.org/en-US/firefox/addon/wave-accessibility-tool/) extensions allow you to evaluate web content for accessibility issues directly within Chrome and Firefox browsers. The extension checks intranet, password-protected, dynamically generated, or sensitive web pages. It can also evaluate locally displayed styles and dynamically-generated content from scripts or AJAX. Follow these simple steps: 

1.  Add WAVE extension to Chrome/Firefox browser
2.  Click on the **WAVE** icon to the right of the browser address bar. _(You can also trigger a WAVE report by pressing Control + Shift + U / Command + Shift + U on Mac)_
3.  The WAVE extension will generate an audit report displaying the summary on the left-hand side of the navigation
4.  Click the icon again or refresh the page to remove the WAVE interface

**What does a WAVE Audit Report** include? 

*   **Summary -** This tab displays the findings of evaluation in six categories - _Errors, Contrast Errors, Alerts, Features, Structural Elements and ARIA._
*   **Details -** This tab shows the breakdown of every icon displayed on the page, grouped by category. Clicking on the icon under the details tab will highlight the issue on the page. You can click this highlighted icon on the page to open the tooltip with the issue description, ‘Reference’ and ‘Code’ panel links. In case an icon does not appear within the page, turn off the “Styles” switch to view it.

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312a6_audit%2520table.png)

*   **References -** This tab explains the issue, how an issue will impact users with disabilities, what can be done to fix it, the algorithm used to detect it and links to relevant WCAG requirements. There is also an icon index link that displays all of the WAVE’s icons grouped by category.
*   **Structural Elements -** It displays regions of the page that have been identified with HTML or ARIA. It also displays the heading structure for the page. WAVE identifies hidden page elements, lists the regions and heading and indicates nesting of page elements.
*   **Contrast panel -** It identifies text that does not meet WCAG Level AA contrast ratio requirement of at least 4.5:1. WAVE also provides information for the lower 3:1 contrast ratio requirement for large text.
*   **Code panel -** This panel appears at the bottom of the window. The place in the code where the issue appears is highlighted and marked with an icon. Reviewing the code reveals the cause of the issue and helps in fixing it.

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c49988fb9940431372_image7_5.gif)

###   
**PA11Y**

[Pa11y](https://pa11y.org/) is an open-source project that helps designers and developers make their web pages more accessible. There is a range of Pa11y free and open-source tools available.

####   
A\] Pa11y

Pa11y is a command-line interface that loads web pages and highlights any accessibility issues it finds. It is useful when you want to run a one-off test against a web page. The Pa11y test result consists of _Type, Message, Code, Context and Selector_ fields.

‍

```

# Run an accessibility test to output result in human-readable format
pa11y https://google.com
```


![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312e9_image19_0.png)

‍

```

# Using Reporter, run an accessibility test to output result in csv file or json array or html format
pa11y --reporter csv https://google.com > report.csv
pa11y --reporter json https://google.com > report.json

pa11y --reporter cli https://google.com
pa11y --reporter html https://google.com > report.html

```


![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c49988fb99404312f2_image3_27.png)

#### **B\] Pa11y CI**

Pa11y CI can be used to run accessibility tests against multiple URLs or viewports and highlight the issues. You simply need to add the web page URLs in the .pa11yci JSON file (a config file in the current working directory).

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb994043129e_image4_17.png)

```

# Run an accessibility test using pa11y-ci
pa11y-ci
```


![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312b0_image2_25.png)

#### 

C\] Pa11y Dashboard

Pa11y Dashboard is an open-source web interface that helps keep a track of automated accessibility tests over time. It allows users to view, manage audit tasks, trigger audits and generate reports. Follow these steps: 

1.  Create a task by clicking on “Add new URL”
2.  Enter details of the test URL and save it
3.  You will be taken to the task page having links: “Edit this task”, “Delete this task” and “Run Pa11y”
4.  Click “Run Pa11y” and generate the report
5.  Pa11y dashboard will display the output in three categories -  Error, Warnings and Notices. There is a short description of each issue along with its location in the HTML
6.  You can export reports in CSV and JSON format
7.  The dashboard also displays a graph that illustrates the delta in errors, warnings, and notices over time
8.  By default, automated audits are performed daily and can track each audit.

**Note:** **Refer to our Pa11y blog for installation and configuration steps**

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312cd_image18_0.png)

### axeTools

#### **A\] axe DevTools**

axe DevTools is an accessibility testing and audit tool maintained by [deque](https://deque.com/). By using a combination of automated and guided testing, dev teams can catch up to 84% of common accessibility issues without requiring accessibility expertise. Steps to implement axe DevTools: 

1.  Install “axe DevTools” [Chrome](https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/axe-devtools/) extension to your respective browser

1.  Open the webpage you want to audit

1.  Open the browser’s developer tool and click on the “axe DevTools” tab

1.  _Scan the webpage and audit result will be displayed_

1.  The audit result contains the issue summary and a detailed description of each issue.

1.  Now save the results

Axe DevTools provides Intelligent Guided Test functionality. These guided tests raise accessibility issues about page content and then build an issue report. This helps developers to identify issues in less time, resulting in cleaner code and a more accessible experience.

Axe DevTools helps present results in a variety of management reports:

*   A dashboard view to show accessibility progress 

*   Using “**Export Issues**”, you can export reports in JSON and CSV formats (This feature is available with axe DevTools Pro)

*   Project reports for CI tools, such as Jenkins, Bamboo, or CircleCI can include accessibility metrics. (This feature is available with axeDevTools Enterprise plan)

![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c59988fb99404313b6_image6_0.gif)

#### **B\] axe - cli**

axe-cli is a command-line interface for the axe to rapidly run accessibility tests in headless chrome.

_‍_

```

#Install axe CLI globally
npm install @axe-core/cli -g

#Run axe CLI test on the webpage
axe https://www.qed42.com
 
#Run axe CLI test on the multiple webpages
axe https://www.qed42.com, https://www.deque.com

#Run all wcag2a rules on the web page
axe www.deque.com --tags wcag2a

#To pipe the results to a file
axe --stdout www.deque.com > report.json

```


![Accessibility Audit](https://assets-global.website-files.com/6470768de8327f36a7ae11a5/64ccd7c39988fb99404312d4_image9_6.png)

### **Conclusion**

Accessibility testing is most effective when combined with manual testing and an accessibility audit. When you are choosing an A11y audit tool, focus on factors such as how – the tool manages multiple websites, collects accessibility issues and remediates them, how easy it is to use by both technical and non-technical team members and cost. In this way, you can use audit tools in your project and make the website more accessible.

We help build and maintain digital accessibility by embedding testing and best practices into your development process. Reach out to us at [business@qed42.com](mailto:business@qed42.com) for integrating accessibility into your operations. 

**Happy A11y Auditing!!!**

Original Article: https://www.qed42.com/insights/4-opensource-accessibility-audit-tools-you-must-know
