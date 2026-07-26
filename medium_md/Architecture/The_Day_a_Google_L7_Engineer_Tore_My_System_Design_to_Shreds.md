---
title: "The Day a Google L7 Engineer Tore My System Design to Shreds"
url: https://medium.com/p/0b3834fded07
---

# The Day a Google L7 Engineer Tore My System Design to Shreds

[Original](https://medium.com/p/0b3834fded07)

Press enter or click to view image in full size

![]()

Member-only story

## Updated: 29/06/2025

# The Day a Google L7 Engineer Tore My System Design to Shreds

[![Cloud With Azeem](https://miro.medium.com/v2/resize:fill:64:64/1*oJWwUx75Cf5oGoEfAefJpw.png)](/?source=post_page---byline--0b3834fded07---------------------------------------)

[Cloud With Azeem](/?source=post_page---byline--0b3834fded07---------------------------------------)

7 min read

·

Feb 16, 2026

--

52

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0b3834fded07&operation=register&redirect=https%3A%2F%2Fcloudwithazeem.medium.com%2Fgoogle-l7-system-design-interview-lessons-0b3834fded07&source=---header_actions--0b3834fded07---------------------post_audio_button------------------)

Share

> If you are not a medium member, [read here for free](/0b3834fded07?sk=2053ca003c75ca37fc300eb1bbb62aa3)

> @
>
> [Cloud With Azeem](https://medium.com/u/f34a895a19b4?source=post_page---user_mention--0b3834fded07---------------------------------------)

I walked into the interview room with the quiet confidence of someone who had “beaten” the system. I had memorized the blueprints. I knew the difference between MongoDB and Cassandra, I could draw a Content Delivery Network (CDN) in my sleep, and I had the Netflix tech stack etched into my brain like a holy text. I was ready to talk about microservices, sharding, and high availability.

Then I met the interviewer — a soft-spoken L7 Staff Engineer who had spent the last decade keeping systems alive that handle more traffic in a second than most apps see in a year.

The problem he gave me was deceptively simple: **“Design a URL shortener.”**

I smirked. This was the “Hello World” of system design. I grabbed the marker and started flying through the motions. API Gateway here, Load Balancer there, a NoSQL database for the mapping, and a Redis cache to keep things snappy. I was talking about **$O(1)$ lookups** and **Base62** encoding. I felt like a rockstar.

Then he leaned forward. “This looks great for a startup with a few thousand users. But what happens to your architecture…