---
title: "I Spent 6 Months Tuning Claude Code. Here’s the Exact Setup That Finally Worked."
url: https://medium.com/p/b41c67628478
---

# I Spent 6 Months Tuning Claude Code. Here’s the Exact Setup That Finally Worked.

[Original](https://medium.com/p/b41c67628478)

Member-only story

# I Spent 6 Months Tuning Claude Code. Here’s the Exact Setup That Finally Worked.

## CLAUDE.md, subagents, hooks, skills, worktrees, and the five MCP servers that earn their place

[![Anubhav](https://miro.medium.com/v2/resize:fill:64:64/1*a96ICyCx5Xa078adPFbp5A.jpeg)](/@anubhavgoyal101?source=post_page---byline--b41c67628478---------------------------------------)

[Anubhav](/@anubhavgoyal101?source=post_page---byline--b41c67628478---------------------------------------)

16 min read

·

Apr 24, 2026

--

22

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Db41c67628478&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fdata-science-collective%2Fi-spent-6-months-tuning-claude-code-heres-the-exact-setup-that-finally-worked-b41c67628478&source=---header_actions--b41c67628478---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Open a terminal. Go to your main AI project. Run `tree .claude`

For most engineers using Claude Code right now the answer is “command not found” or a single file containing a vague instruction to write clean code. That is fine. It also leaves roughly 80% of the product on the floor.

> Not a medium member? Read the full article [**here**](https://levelup.gitconnected.com/i-spent-6-months-tuning-claude-code-heres-the-exact-setup-that-finally-worked-b41c67628478?sk=1fe443152d237bb870135a4c95a14272).

Here is what the same command looks like in a repository configured by a power user.

```
.claude/  
├── CLAUDE.md  
├── rules/  
│   ├── langgraph.md  
│   ├── retrieval.md  
│   ├── tests.md  
│   └── python-types.md  
├── agents/  
│   ├── retrieval-reviewer.md  
│   ├── prompt-auditor.md  
│   └── eval-runner.md  
├── skills/  
│   ├── new-rag-eval/  
│   │   └── SKILL.md  
│   └── claude-pr-checklist/  
│       └── SKILL.md  
├── settings.json  
└── .mcp.json
```

None of these files is long. The main memory file is under 500 tokens on purpose. Each rules file is a short path-scoped behavior. Each subagent is maybe thirty lines. The hooks configuration in the settings file is one pre-tool gate and one post-tool formatter. The server…