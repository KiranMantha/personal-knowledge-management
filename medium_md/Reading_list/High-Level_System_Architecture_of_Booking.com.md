---
title: "High-Level System Architecture of Booking.com"
url: https://medium.com/p/06c199003d94
---

# High-Level System Architecture of Booking.com

[Original](https://medium.com/p/06c199003d94)

Member-only story

# High-Level System Architecture of Booking.com

[![Talha Şahin](https://miro.medium.com/v2/resize:fill:64:64/1*7lHrbO7l7da-SgXiDeSC_A@2x.jpeg)](/@sahintalha1?source=post_page---byline--06c199003d94---------------------------------------)

[Talha Şahin](/@sahintalha1?source=post_page---byline--06c199003d94---------------------------------------)

8 min read

·

Jan 10, 2024

--

52

Listen

Share

More

Hello everyone! In this article, we will take an in-depth look at the possible high-level architecture of Booking.com, one of the world’s leading travel and hospitality platforms.

Press enter or click to view image in full size

![]()

## Introduction

Serving millions of users worldwide, Booking.com has a dynamic system architecture to meet ever-changing customer expectations and integrate technological innovations. Starting with Booking.com’s system requirements, the purpose of this paper is to discuss how the platform was designed, how its main components function.

Like other leading companies in the industry, Booking.com needs complex and scalable architectures to continuously improve user experience, increase efficiency and maintain a competitive advantage in the market. In this paper, we will try to understand the technological processes behind such a platform and propose a basic high-level architecture. Whether you are a software developer, a systems engineer or just a tech-savvy person, we hope that this article will give you a better understanding of Booking.com’s technological structure.

## System Requirements

The system architecture of Booking.com is crafted to accommodate the extensive demands of its platform. In 2019, the platform was handling over 1,500,000+ experiences booked every 24 hours [3]. This immense level of traffic indicates the need for a high-capacity, resilient server infrastructure capable of efficiently handling large volumes of data and user interactions, especially during peak usage periods.

Additionally, the platform’s expansive user base, particularly its 100 million mobile users as of 2022, presents significant challenges and opportunities [1]. This substantial number of users implies that the platform is dealing with huge volumes of data and busy traffic on its servers. To manage this effectively, the system architecture must be robust and scalable, ensuring that it can handle the concurrent requests and data processing needs of this large and active user base.

## High-Level Architecture

Press enter or click to view image in full size

![]()

The possible high-level architecture diagram you see above is a visual summary of Booking.com’s service architecture. To better understand the role and functionality of each component within the system, we will discuss the key components in the diagram individually below.

### Architectural Pattern

A critical decision in the high-level architecture of Booking.com is the selection of an architectural pattern that can effectively accommodate the platform's varied and dynamic load across different services. Given the diversity in service loads, such as the higher frequency of users browsing for hotels compared to the number of users making reservations, it is clear that a one-size-fits-all approach to scaling does not suit Booking.com's needs.  
The microservices architecture pattern emerges as the most fitting solution for this scenario. This pattern structures the application as a collection of loosely coupled services, each designed around a specific business capability. This architectural choice enables individual services to be scaled up or down based on demand without impacting other areas of the system.

### Database

In the architecture of Booking.com, the selection of a relational database is strategic, driven by the platform’s operational pattern where the volume of hotel searches substantially exceeds the number of actual reservations made. The efficiency of relational databases in read operations aligns seamlessly with the high number of searches that the platform accommodates. Additionally, the integrity of transactions is paramount in a reservation system, where the ACID properties of relational databases play a crucial role. The relational model also adeptly handles the complex interrelationships within Booking.com’s data, such as the connections between hotels, rooms, and room types, enhancing data integrity and simplifying maintenance.

Insights from the company’s tech blogs suggest that MySQL is their relational database of choice, offering the necessary features, performance, and reliability. The use of MySQL is discussed in many articles on Booking.com’s technical blogs. Readers who would like to get more information and in-depth knowledge on this topic can access the platform’s technical blog via [this link](https://blog.booking.com/#infrastructure).

### Storing Images

The storage and distribution of images aims to accelerate the user experience and increase efficiency. The platform utilizes content delivery network (CDN) technology to provide users with fast access to hotel images. The use of CDN makes it possible to deliver content at high speed to users around the world by serving hotel images from geographically closer servers. System stores URLs of images in the database.

### API Gateway

The API Gateway acts as the first point to receive all incoming API requests, performs authentication and routes them to the appropriate microservices. It also contains rate limiters that protect the system from overloading. This centralized structure effectively manages traffic on the system and provides a secure user experience by controlling access based on users’ authorizations.

### Main Microservices

In Booking.com’s actual system architecture, there may be more microservices than those listed here, or one of the listed microservices may in reality be split into different microservices. The following are what are described as core and core microservices, but this may not represent Booking.com’s full and comprehensive list of services.

**Hotel Service:** This service manages users’ hotel searches and includes detailed information, photos and availability of hotels. The service has its own database where hotels’ record, properties and current status are kept. Also, information such as hotel location, room types, and available amenities rarely changes, so it makes sense to cache this information to ensure high access speed and efficiency.

**Review Service:** Review Service manages the comments and ratings that users write about hotels. Booking.com believes that review systems are critical to the user experience and quality of service, which is why they place a great deal of importance on the platform’s review systems. If you are interested in learning more about how Booking.com’s review systems scale and the technical details of these processes, please see [4].

**Payment Service:** This service processes payment information, transaction history and billing data, enabling users to make payments securely. Payment Service also plays a crucial role in handling system failures such as multiple payment requests or retrying failed transaction. For more details on how duplicate payments are prevented, feel free to explore my article:

[## Idempotency Keys: How PayPal and Stripe Prevent Duplicate Payment

### Explore how payment service providers technically prevent duplicate payment, ensuring secure, single transactions.

medium.com](/@sahintalha1/the-way-psps-such-as-paypal-stripe-and-adyen-prevent-duplicate-payment-idempotency-keys-615845c185bf?source=post_page-----06c199003d94---------------------------------------)

**Booking Management Service:** It is for hotel owners to view and track the reservations made by users, update room availability, and manage booking details. Therefore, it communicates with booking, payment, and hostel service.

Besides these main microservices, Booking.com’s architecture may also include additional services that analyze user behavior and feed a constantly evolving Machine Learning pipeline using booking data. Such services allow the platform to personalize the user experience and continuously improve the quality of service.

### Third-party Components

**Elastic Search:** ElasticSearch is known for its ability to index and query large data sets quickly and efficiently, enabling the Search Service to quickly filter and present a wide and diverse range of accommodation options to users.

**Kafka:** Kafka uses connectors, especially for operations like pulling data from MySQL and feeding data to Elasticsearch. This allows different services in the system, for example the Search Service, to access up-to-date and indexed data. The data from MySQL is fed into Elasticsearch through Kafka, which allows the data to be processed and queried quickly and efficiently. The below process is happening between MySQL clusters for Hotel, Kafka and ElasticSearch.

Press enter or click to view image in full size

![]()

If you want to learn in detail how to transfer data from MySQL to Elasticsearch via Kafka, please see [7].

### Communication Between Microservices

We delve into the sophisticated architecture that enables Booking.com to manage its complex network of services efficiently. The architecture is split into two main components: the control plane and the data plane, each with a distinct role in the system’s overall functionality.

The control plane acts as the brains of the operation. It is responsible for the high-level management of traffic routing, policy enforcement, and service discovery. Tools such as ZooKeeper and Kubernetes play a pivotal role within this plane. ZooKeeper, known for its coordination and configuration management capabilities, works in conjunction with Kubernetes, which excels in orchestrating containerized applications. Together, they ensure that services within Booking.com’s ecosystem can discover each other and operate cohesively according to the rules and configurations set by the operators.

On the other side, the data plane is where the action happens — data packets flow between services through this plane. It is populated by lightweight, high-performance proxies like Envoy, which are tasked with the direct handling of requests and responses. These proxies are dynamically configured by the control plane to apply specific routing rules, handle retries, timeouts, and implement security measures like SSL/TLS encryption for HTTPS traffic.

Press enter or click to view image in full size

![]()

### Global Request Management

Booking.com uses an ADN (Application Delivery Network) based on HAProxy to efficiently manage user requests. HAProxy acts as a high-performance load balancer and proxy server, automatically routing user requests to the most appropriate server. HAProxy dynamically manages the flow of traffic on the network and thus processes user requests taking into account various factors such as geographical location, server health and load.

Requests made by users are routed by HAProxy to the most appropriate data center. This routing is optimized to ensure the lowest latency and highest quality of service.

If you want to learn how HAProxy works in more detail and how Booking.com uses it, please see [5].

## Conclusion

In conclusion, we have examined Booking.com’s high-level architecture and its core microservices, its global application delivery network and how its components work together. As with any technological review, it is important to remember that the information presented here may not be complete and comprehensive and may change over time. You can follow [Booking.com’s technology blog](https://blog.booking.com/#all) to learn latest news about them. Thank you very much for taking your valuable time to read my article. I hope this article has helped you deepen your understanding of Booking.com’s technological structure. Don’t forget to clap if you liked this article 👏🏻

## References

[1] “40+ Booking.com statistics [Latest 2023 Figures!],” [*www.dreambigtravelfarblog.com*.](http://www.dreambigtravelfarblog.com.) <https://www.dreambigtravelfarblog.com/blog/booking-com-statistics>

[2] A. Xu and S. Lam, *System design interview: an insider’s guide volume 2*. Millbrae, California: Byte Code Llc, 2022.

[3] “SREcon19 Europe/Middle East/Africa — SLOs for Data-Intensive Services,” [*www.youtube.com*.](http://www.youtube.com.) <https://www.youtube.com/watch?v=ZdguHXglT8M> (accessed Jan. 09, 2024).

[4] B. Hiltpolt, “Scaling our customer review system for peak traffic,” *Booking.com Engineering*, Nov. 08, 2022. [https://medium.com/booking-com-development/scaling-our-customer-review-system-for-peak-traffic-cb19be434edf](/booking-com-development/scaling-our-customer-review-system-for-peak-traffic-cb19be434edf) (accessed Jan. 09, 2024).

[5] “HAProxyConf 2019 — How Booking.com Powers a Global ADN with HAProxy by Marcin Deranek,” [*www.youtube.com*.](http://www.youtube.com.) <https://www.youtube.com/watch?v=NcpeJV8-OzA> (accessed Jan. 09, 2024).

[6] “Introducing Envoy-Based Service Mesh at Booking.com — Ivan Kruglov, Booking.com,” [*www.youtube.com*.](http://www.youtube.com.) <https://www.youtube.com/watch?v=Pus2ytdEfrQ> (accessed Jan. 09, 2024).

[7] G. Fong, “A Practical Guide to Build Data Streaming from MySQL to Elasticsearch Using Kafka Connectors,” *Medium*, May 13, 2023. <https://blog.devgenius.io/a-practical-guide-to-build-data-streaming-from-mysql-to-elasticsearch-using-kafka-connectors-c311cf29ed38> (accessed Jan. 09, 2024).