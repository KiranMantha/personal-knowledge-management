---
title: "Andrej Karpathy Just Built an Entire GPT in 243 Lines of Python"
url: https://medium.com/p/7d66cfdfa301
---

# Andrej Karpathy Just Built an Entire GPT in 243 Lines of Python

[Original](https://medium.com/p/7d66cfdfa301)

Member-only story

# Andrej Karpathy Just Built an Entire GPT in 243 Lines of Python

## *No PyTorch. No TensorFlow. Just pure Python and basic math.*

[![Sumit Pandey](https://miro.medium.com/v2/resize:fill:64:64/1*66cJkvGe-pOi8_tQ2f5FKg.jpeg)](https://medium.com/@sumit.ai?source=post_page---byline--7d66cfdfa301---------------------------------------)

[Sumit Pandey](https://medium.com/@sumit.ai?source=post_page---byline--7d66cfdfa301---------------------------------------)

9 min read

·

Feb 15, 2026

--

50

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D7d66cfdfa301&operation=register&redirect=https%3A%2F%2Fwww.towardsdeeplearning.com%2Fandrej-karpathy-just-built-an-entire-gpt-in-243-lines-of-python-7d66cfdfa301&source=---header_actions--7d66cfdfa301---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I’ve read many transformer implementations during my PhD. Dense codebases. Thousands of files. Dependencies stacked on top of dependencies. You open a repo, run `pip install -r requirements.txt`, and watch 400 packages download before you can even see your model train (than errors , dependency issues … etc.).

Then on February 11, 2026, **Andrej Karpathy** dropped a single Python file that trains and runs a GPT from scratch. 243 lines. Zero dependencies.

**If you cant read the article further than please click** [**here**](https://medium.com/@sumit.ai/7d66cfdfa301?sk=9b4707253d587c22c81b8d166e85c9e9)

His only imports? `os`, `math`, `random`, and `argparse`. That’s it. That’s the entire LLM. He called it an “**art project.**” I call it the best AI education that exists on the internet right now. Let me walk you through every piece of this code like I’m explaining it to a friend over coffee.

## First, What Is This Thing Actually Doing?

Before we touch the code, let’s be clear about what [microGPT](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) does. It downloads a list of baby names. It learns the patterns in those names. Then it generates new, fake names that *sound* real but never existed.