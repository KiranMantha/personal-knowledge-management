---
title: "Docker Is Dead Weight — I Rebuilt Our Pipeline Without It and Cut Costs 60%"
url: https://medium.com/p/d45aceb0a591
---

# Docker Is Dead Weight — I Rebuilt Our Pipeline Without It and Cut Costs 60%

[Original](https://medium.com/p/d45aceb0a591)

Member-only story

# Docker Is Dead Weight — I Rebuilt Our Pipeline Without It and Cut Costs 60%

[![Ark Protocol](https://miro.medium.com/v2/resize:fill:64:64/1*5Af7Za2-Mu7q8X3FpdM1Kg.jpeg)](/@ArkProtocol1?source=post_page---byline--d45aceb0a591---------------------------------------)

[Ark Protocol](/@ArkProtocol1?source=post_page---byline--d45aceb0a591---------------------------------------)

4 min read

·

May 10, 2026

--

34

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd45aceb0a591&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40ArkProtocol1%2Fdocker-is-dead-weight-i-rebuilt-our-pipeline-without-it-and-cut-costs-60-d45aceb0a591&source=---header_actions--d45aceb0a591---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

We were paying $4,200 a month to build containers nobody asked for.

Not vague infrastructure costs. Real, traceable money: $2,100 in CI runner minutes, $1,680 in data transfer from pushing and pulling 1.8 GB images on every single merge, and $420 sitting in ECR storage for image versions nobody had deployed in months.

When you see it broken down like that, it does not feel like overhead anymore. It feels like a decision someone forgot to revisit.

Nobody on the team was asking questions. So I started asking them.

## The Setup Nobody Questioned

We had three services — a Python API, a Node.js background worker, and a Go binary. Each had its own Dockerfile. Each rebuilt from scratch on every push, regardless of what actually changed. A one-line config correction triggered the same 12-minute cycle as a full feature deploy.

```
[GitHub Push]  
      |  
      v  
[Build Docker Image]  ──────  6 min  
      |  
      v  
[Push to ECR]         ──────  2 min  
      |  
      v  
[Pull on Server]      ──────  3 min  
      |  
      v  
[Run Container]       ──────  30 sec
```

For a three-person team pushing 15 to 20 times a day, that is over three hours of pipeline time spent entirely on…