---
title: "Automated Penetration Testing Useing OWASP ZAP"
url: https://medium.com/p/fe88abaf8e38
---

# Automated Penetration Testing Useing OWASP ZAP

[Original](https://medium.com/p/fe88abaf8e38)

# Automated Penetration Testing Useing OWASP ZAP

[![CYBERencoding](https://miro.medium.com/v2/resize:fill:64:64/1*PwmuBX13_c88lTVdXkf1jA.jpeg)](/@ms3.sooraj.sivadas?source=post_page---byline--fe88abaf8e38---------------------------------------)

[CYBERencoding](/@ms3.sooraj.sivadas?source=post_page---byline--fe88abaf8e38---------------------------------------)

8 min read

·

Feb 4, 2024

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## Intro to ZAP

OWASP Zap is a security testing framework much like Burp Suite. It acts as a very robust enumeration tool. It’s used to test web applications.

**Why wouldn’t I use Burp Suite?**

That’s a GOOD question! Most people in the Info-sec community DO just use Burp Suite. But OWASP ZAP has a few benefits and features that the Burp Suite does not and it’s my preferred program of the two.

**What are the benefits to OWASP ZAP?**

It’s completely open source and free. There is no premium version, no features are locked behind a paywall, and there is no proprietary code.

There’s a couple of feature benefits too with using OWASP ZAP over Burp Suite:

* Automated Web Application Scan: This will automatically passively and actively scan a web application, build a sitemap, and discover vulnerabilities. This is a paid feature in Burp.
* Web Spidering: You can passively build a website map with Spidering. This is a paid feature in Burp.
* Unthrottled Intruder: You can bruteforce login pages within OWASP as fast as your machine and the web-server can handle. This is a paid feature in Burp.
* No need to forward individual requests through Burp: When doing manual attacks, having to change windows to send a request through the browser, and then forward in burp, can be tedious. OWASP handles both and you can just browse the site and OWASP will intercept automatically. This is NOT a feature in Burp.

If you’re already familiar with Burp the keywords translate over like so:

Press enter or click to view image in full size

![]()

This guide will teach you how to do the following in ZAP:

* Automated Scan
* Directory Bruteforce
* Authenticated Scan
* Login Page Bruteforce
* Install ZAP Extensions

This room will be using OWASP Zap against the DVWA machine, feel free to deploy your own instance and follow along.

## Disclaimer

ZAP is a great tool that’s totally slept on, and I personally prefer it over Burp, but the documentation and support for the tool is microscopic compared to the titan that is Burp.

Burp has some extensions and features that ZAP does not have, as an example ZAP is unable to perform Login timing attacks. Burp can. If you wish to learn more about login timing attacks you can check out the TryHackMe room [Hackernote](https://tryhackme.com/room/hackernote).

ZAP can be used as your go-to tool to start Web Application testing but it should not be your *only* tool. ZAP is just one of many tools to put under your hacker utility belt.

## Installation

OWASP ZAP has a handy installer for Windows, Mac OS, and Linux systems.

kali Linux and other Linux : `sudo apt install zaproxy`

Download and install it from the official website: <https://www.zaproxy.org/download/>

## How to perform an automated scan

Lets perform an automated scan. Click the big Automated Scan button and input your target.

Press enter or click to view image in full size

![]()

The automated scan performs both passive and automated scans to build a sitemap and detect vulnerabilities.

On the next page you may see the options to select either to use “traditional spider” or “Ajax spider”.

A traditional spider scan is a passive scan that enumerates links and directories of the website. It builds a website index without brute-forcing. This is much quieter than a brute-force attack and can still net a login page or other juicy details, but is not as comprehensive as a bruteforce.

The Ajax Spider is an add-on that integrates in ZAP a crawler of AJAX rich sites called Crawljax. You can use it in conjunction with the traditional spider for better results. It uses your web browser and proxy.

The easiest way to use the Ajax Spider is with HTMLUnit.

To install HTML Unit use the command

sudo apt install libjenkins-htmlunit-core-js-java

And then select HtmlUnity from the Ajax Spider Dropdown.

Both utilities can further be configured in the options menu (Ctrl+Alt+O)

Example Automated Scan Output:

Press enter or click to view image in full size

![]()

With very minimal setup we were able to do an automated scan that gave us a sitemap and a handful of vulnerabilities.

## Manual Scanning

Lets perform a manual scan against the DVWA machine.

Like Burp, you should set-up your proxy between OWASP ZAP and your Browser. We’ll be using Firefox.

=============================================================

**OWASP Proxy Setup:**

![]()

Open Options

Press enter or click to view image in full size

![]()

Change Local Proxy settings to the above.

=============================================================

**Add ZAP Certificates:**

Without importing ZAP Certificates, ZAP is unable to handle simultaneous Web request forwarding and intercepting. Do not skip this step.

Press enter or click to view image in full size

![]()

In the same options menu, navigate to Dynamic SSL Certificates and save the certificate somewhere you’ll remember and not delete.

Press enter or click to view image in full size

![]()

Then, open Firefox, navigate to your preferences, and search for certificates and click “View Certificates”

![]()

Then click “Import” and then navigate to the earlier downloaded certificate and open it.

![]()

Select both and then hit OK.

=============================================================

**Firefox Proxy Setup:**

Press enter or click to view image in full size

![]()

Go back to your Firefox preferences and search for “proxy”. Click Settings.

Press enter or click to view image in full size

![]()

Adjust your Manual Proxy Configuration to match and then click OK.

Now you’re set-up! Time to get into the fun stuff :)

## Scanning an Authenticated Web Application

Without your Zap application being authenticated, it can’t scan pages that are only accessible when you’ve logged in. Lets set up the OWASP ZAP application to scan these pages, using your logged in session.

Lets go to the DVWA machine (<http://MACHINE_IP>), and login using the following credentials:

**Username**: admin

**Password**: password

Press enter or click to view image in full size

![]()

After logging in you should see this.

![]()

For the purpose of this exercise, once you’ve logged in, navigate to the DVWA Security tab and set the Security level to Low and then hit submit.

We’re going to pass our authentication token into ZAP so that we can use the tool to scan authenticated webpages.

Press enter or click to view image in full size

![]()

Enter inspect element and take note of your PHPSESSION cookie.

Press enter or click to view image in full size

![]()

In ZAP open the HTTP Sessions tab with the new tab button, and set the authenticated session as active.

Now re-scan the application. You’ll see it’s able to pick up *a lot* more. This is because its able to see all of the sections of DVWA that was previously behind the login page.

## Brute-force Directories

If the passive scans are not enough, you can use a wordlist attack and directory bruteforce through ZAP just as you would with gobuster. This would pick up pages that are not indexed.

Press enter or click to view image in full size

![]()

First. Go into your ZAP Options (at the bottom navigation panel, with the screen plus button), navigate to Forced Browse, and add the Custom Wordlist. You can also add more threads and turn off recursive brute-forcing.

Press enter or click to view image in full size

![]()

Then, right click the site->attack->forced browse site

![]()

Select your imported wordlist from the list menu, and then hit the play button! We recommend using [this](https://github.com/thesp0nge/enchant/blob/master/db/directory-list-2.3-medium.txt) wordlist for this exercise.

ZAP will now bruteforce the entire website with your wordlist.

## Bruteforce Web Login

Lets brute-force a form to get credentials. Although we already know the credentials, lets see if we can use Zap to obtain credentials through a Brute-Force attack.

If you wanted to do this with BurpSuite, you’d need to intercept the request, and then pass it to Hydra. However, this process is much easier with ZAP!

![]()

Navigate to the Brute Force page on DVWA and attempt login as “admin” with the password “test123”

Press enter or click to view image in full size

![]()

Then, find the GET request and open the Fuzz menu.

Press enter or click to view image in full size

![]()

Then highlight the password you attempted and add a wordlist. This selects the area of the request you wish to replace with other data.

Press enter or click to view image in full size

![]()

For speed we can use fasttrack.txt which is located in your /usr/share/wordlists if you’re using Kali Linux.

Press enter or click to view image in full size

![]()

After running the fuzzer, sort the state tab to show Reflected results first. Sometimes you will get false-positives, but you can ignore the passwords that are less than 8 characters in length.

## ZAP Extensions

Want to further enhance ZAPs capabilities? Look at some of it’s downloadable extensions!

<https://github.com/zaproxy/zap-extensions>

<https://github.com/bugcrowd/HUNT>

Let’s install the bugcrowd HUNT extensions for OWASP ZAP. This will passively scan for known vulnerabilities in web applications.

Press enter or click to view image in full size

![]()

First navigate in your terminal somewhere you’d like to store the scripts

` git clone <https://github.com/bugcrowd/HUNT> `

Press enter or click to view image in full size

![]()

Then in ZAP click the “Manage Add-Ons” icon

Press enter or click to view image in full size

![]()

From the Marketplace install “Python Scripting” and “Community Scripts”

Press enter or click to view image in full size

![]()

In ZAP Options, under Passive Scanner, make sure “Only scan messages in scope” is enabled. Then hit OK.

![]()

In ZAP open the Scripts tab.

![]()

And under Passive Rules, find and enable the HUNT.py script

Now when you browse sites and HUNT will passively scan for SQLi, LFI, RFI, SSRF, and others. Exciting!

## Further Reading

Wow! You reached the end! Good job! Try your new ZAP skills on some Web Application CTFs. TryHackMe has quite the variety. My personal favorite is HackPark.

Desktop eManuel: <https://www.zaproxy.org/docs/desktop/ui/>

OWASP ZAP Forums: <https://groups.google.com/forum/#!forum/zaproxy-users>

ZAP in Ten: <https://www.zaproxy.org/zap-in-ten/>

Yeah that’s pretty much all there is. I wasn’t kidding when I said “microscopic” in comparison to Burp suite.

That’s the one major con of ZAP is the pitiful amount of documentation there is. The project is still active and contributed to though. Just no one’s really writing guides.