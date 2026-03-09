---
title: "Get notified! Improvements to KaiOS push notifications"
url: https://medium.com/p/e801ae6fb720
---

# Get notified! Improvements to KaiOS push notifications

[Original](https://medium.com/p/e801ae6fb720)

# **Get notified! Improvements to KaiOS push notifications**

[![KaiOS Technologies](https://miro.medium.com/v2/resize:fill:64:64/1*U5Ufv9giqNue7tgIWT41Xw.png)](/@kaiostech?source=post_page---byline--e801ae6fb720---------------------------------------)

[KaiOS Technologies](/@kaiostech?source=post_page---byline--e801ae6fb720---------------------------------------)

5 min read

·

May 13, 2020

--

Listen

Share

More

Press enter or click to view image in full size

![]()

*By Fay Wu, UX Designer at KaiOS*

It’s often said that user engagement is highly correlated with the success of an app. The more time users spend interacting with an app, the higher the chances of building customer loyalty and brand exposure as well as driving monetization.

KaiOS apps can send push notifications — which we call *notices* — to reach out to users. App developers use notices to send users updates and reminders.

Since notices are a powerful tool for increasing user engagement, improving their design is a priority for the UX team at KaiOS.

In this article, we’ll share how we improved them to increase their click-through rate (CTR).

## The Original User Flow

We began by tracing the user’s steps and asking questions, including:

* *What do users see when they get a notice on their device screen?*
* *How many steps are necessary to successfully open an app from a notice received?*
* *Are there any barriers to completing tasks?*

**This is what the user journey looked like:**

* When a user received a new notice, a floating message box appeared at the top of the screen. Additionally, a Notices icon with a number counter showed up in the status bar. The Notices Summary on the Lock screen also reflected the new message received.
* To see the notice, the user had to unlock the device, go to the Home screen, and then open the Notices screen by selecting the Notices key in the Softkey Bar.

Press enter or click to view image in full size

![]()

## Issues We Identified

We realized there were a number of issues with the user flow that we could improve on. We’ll describe each of them below.

**Undiscovered Notices Summary**

TheNotices Summary on the Lock screen was the most prominent UI element for letting users know when they received new notice. However, the Lock screen can be disabled, and in flip phones, it’s disabled by default. This means that some users never got to see their Notices Summary.

Also, with the exception of Call, Voicemail, Messages, Calendar, and Email, all other app notifications were categorized as “Others” (last icon). The icons for these six categories were displayed in order of importance, not timeline order. As a result, users had no way of knowing which notice was the most recent.

![]()

**Silent Home Screen**

The Notices counter in the status bar showed the total number of received notices; however, it didn’t differentiate new or unread notices from the rest. The same was true for the Notices key (Left-Softkey / LSK).

Without opening the Notices screen, users couldn’t tell if there were unread notices. New notices were likely to be ignored, especially by users unfamiliar with this feature design.

![]()

## New Design

Once we identified the issues with the original design, we set out to create solutions. We’ll describe the improvements we made below.

**Lock Screen**

Under the new Lock screen design, notices are shown along with their actual app icons and in timeline order sequence.

Notices are grouped together by apps, meaning only notices sent from the same application are categorized together. This helps users sort through notices based on recognizable app icons rather than generic system icons.

![]()

The Notices Summary is now shown on the Home screen after the device is unlocked, delivering actionable information to users directly on the screen that they need to take action on (i.e. opening the Notices screen).

This creates continuity in the user experience and ensures that the Notices Summary is shown even when users disable their Lock Screen.

![]()

To prevent visual clutter, the Notices Summary disappears after a few seconds.

![]()

**Home Screen**

Since the Home screen is the only point of access to the Notices screen, we thought it would make sense to provide helpful information to users there. Therefore, we added a “New notices state” to both the status bar and the Softkey bar.

Now, when a user gets a notice, the number counter changes to red and a small indicator appears in the Notices key.

![]()

This clearly reflects the status of new notices; as a result, users no longer need to constantly open their Notices screen to check if they missed something. The state change of the status bar can be seen from any screen at any time.

Press enter or click to view image in full size

![]()

Once a user opens their Notice screen, the new notices state reverts to its normal state until new notices come in.

Press enter or click to view image in full size

![]()

**Reminder**

From now on, users that haven’t opened their Notices screens in a while and have many unread messages will get occasional reminders (via pop-up dialogs) to check their notifications.

When all other nudges fail, this actionable reminder might be what finally gets the user to complete the task of checking their messages.

![]()

## Summary

The changes can be summarized as follows:

* More timely and accurate information in the Notices Summary
* Notices Summary visible Get on Home screen to prevent information from being overlooked
* “New notices state” added to the status bar and the softkey bar so the latest information can be seen at a glance
* Friendly reminders sent to users to direct them to the Notices screen

## What We Learned

Users don’t always behave the way we think they will, so we need to provide them with clear information and guide them to complete tasks. It helps to use a problem-solving framework to narrow down the focus of design solutions.

Our work is always geared towards improving the design — not just for users, but for app developers and partners who benefit from new ways of engaging their audiences.

*Stay up to date on Kai’s journey by reading* [*our blog*](https://www.kaiostech.com/blog/) *or following us on* [*Twitter*](https://twitter.com/KaiOStech)*,* [*LinkedIn*](https://www.linkedin.com/company/13291989/)*, and* [*Facebook*](https://www.facebook.com/kaiostech/?fref=ts)*.*

![]()