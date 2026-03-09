---
title: "FlashList vs. FlatList: Understanding the Key Differences for React Native Performance"
url: https://medium.com/p/15f59236a39c
---

# FlashList vs. FlatList: Understanding the Key Differences for React Native Performance

[Original](https://medium.com/p/15f59236a39c)

# FlashList vs. FlatList: Understanding the Key Differences for React Native Performance

## In this article, we explain how we improved performance and UX issues using FlashList as a better alternative to FlatList. We’ll cover why FlashList’s cell recycling strategy outperforms FlatList’s virtualization for complex layouts and share practical tips to fine-tune performance, improve FPS, and avoid crashes.

[![Whitespectre](https://miro.medium.com/v2/resize:fill:64:64/1*Ple8HWsNye1jr3MMXzKRAQ.png)](/@whitespectre?source=post_page---byline--15f59236a39c---------------------------------------)

[Whitespectre](/@whitespectre?source=post_page---byline--15f59236a39c---------------------------------------)

6 min read

·

Jan 28, 2025

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

Scrolling performance plays a crucial role in defining the quality of user experience in mobile apps, especially when handling complex or long lists.

Whether it’s an infinite social media feed with videos and images, an e-commerce catalog, or a meal menu with multiple categories: As complexity increases — with features like animations, auto-scrolling, custom filters, and sorting rules — the performance demands also grow. Keeping a smooth experience becomes progressively more challenging, particularly when managing large lists and ensuring good performance across all types of devices.

We faced this challenge when building a project where one of the core parts of the app featured categorized menus with nested lists, dynamic content, and animations. Despite using React Native’s FlatList, performance issues surfaced during our testing before the Android launch, even though the iOS version was already in production and running well. These issues were particularly noticeable on low-end Android devices, which resulted in laggy scrolling, animation stuttering, and even crashes.

In this article, we’ll explore how we addressed these challenges using FlashList, share tips and strategies to fine-tune scrolling performance, and explain why, in certain scenarios, FlashList can deliver a smoother and more efficient user experience, with its recycler view approach, than FlatList, which relies on a virtualization strategy.

## FlatList: A reliable choice, but…

React Native has a built-in component for handling large lists, that you’ve probably already heard of, named FlatList. It uses a technique called virtualization to optimize rendering, that means that instead of rendering all items at once, like a View or ScrollView would, FlatList renders only the items currently visible, with a buffer at the top and bottom to support smooth scrolling. Items outside the viewport are unmounted to save memory and improve performance.

While this approach works well for most cases, it introduces some expected overhead because mounting and unmounting components consume device resources. When list items are complex, such as including animations or dynamic content, this overhead can lead to performance issues. These problems are even more noticeable on low-end devices, where limited processing power can result in laggy performance and a poor user experience.

## The Solution: Introducing FlashList

Unlike FlatList, FlashList uses a cell recycling strategy instead of virtualization. It works by keeping a fixed pool of component instances in memory. When an item scrolls out of view, it reuses the same component with new data instead of destroying and re-creating it.

![]()

This approach can drastically improve performance, especially in scenarios where the list is complex, making the mounting and unmounting very costly on low-end devices.

## Our Experience: From FlatList to FlashList

When we encountered performance issues related to this complex nested list on the project we were working on, we decided to give FlashList a try. Since it is designed as a drop-in replacement for FlatList and uses a recycling approach, it was well-suited to improve performance on devices with limited resources, so the replacement process was very straightforward.

After the change, we immediately noticed a performance boost, and scrolling became significantly smoother. But, after further investigation and a closer review of the documentation, we realized there was still room for additional improvements and by applying a few optimizations, we were able to enhance performance and user experience even further.

## FlashList Fine-Tuning Tips

Based on insights from the documentation, we implemented some key enhancements:

* **Data Reorganization:** We merged multiple sub-lists into a single flat list, making it easier to handle recycling.

Press enter or click to view image in full size

![]()

* **estimatedItemSize:** This mandatory prop helps FlashList determine how many items to render initially and while scrolling. Since our list contained different types of components, we followed the documentation’s recommendation to use an average or median value for estimatedItemSize to optimize performance.

Press enter or click to view image in full size

![]()

* **getItemType:** By transitioning from a nested list to a flat list, we were able to group items by type (headers vs. items), and use the **getItemType** prop, enabling smarter recycling.

![]()

* **overrideItemLayout:** This has a higher priority over **estimatedItemSize**. Assigning fixed heights for headers and meals improved scroll precision for the auto-scroll feature.

Press enter or click to view image in full size

![]()

After implementing all these optimizations, our list component looked like this:

Press enter or click to view image in full size

![]()

## Results

After implementing FlatList and fine-tunning properties, we saw a significant improvement in performance, to measure it we used Flashlight a Lighthouse-like tool for mobile apps, with the same environment and Android device.

Average FPS improved from 36.9 FPS to 56.9 FPS, a 54% increase

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

The average CPU usage decreased from 198.9% to 36.5%, an 82% reduction. Improving app responsiveness, particularly on low-end devices

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

We also saw a substantial improvement on React Native JS thread CPU usage. Previously, it exhibited consistent utilization above 90%, leading to potential scrolling and transition bottlenecks. After using FlashList and optimizing it, the JS thread stayed consistently below 10%.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Below, you can see a summary of the comparison results:

Press enter or click to view image in full size

![]()

## Conclusion

FlatList is a solid choice for most applications, especially simpler lists. But, it can struggle with performance when handling complex layouts and animations. That’s where FlashList might be a good choice, due to its cell recycling strategy.

That said, like almost everything in software development, it’s not a silver bullet. It works best when matched with the right use case and properly configured. When used in the right scenario, FlashList can deliver noticeable performance improvements and a smoother, more responsive user experience.