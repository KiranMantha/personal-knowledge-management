---
title: "10 Tip to Stop Burning Your Tokens in Claude Code"
url: https://medium.com/p/4776d4ac8956
---

# 10 Tip to Stop Burning Your Tokens in Claude Code

[Original](https://medium.com/p/4776d4ac8956)

# 10 Tips to Stop Burning Your Tokens in Claude Code

[![Habib Mohammed](https://miro.medium.com/v2/resize:fill:64:64/1*cUKUKgIPergxl1AKHInWAw@2x.jpeg)](/@habib23me?source=post_page---byline--4776d4ac8956---------------------------------------)

[Habib Mohammed](/@habib23me?source=post_page---byline--4776d4ac8956---------------------------------------)

8 min read

·

Apr 3, 2026

--

7

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D4776d4ac8956&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40habib23me%2F10-tip-to-stop-burning-your-tokens-in-claude-code-4776d4ac8956&source=---header_actions--4776d4ac8956---------------------post_audio_button------------------)

Share

and get more stuff done

Press enter or click to view image in full size

![]()

I was reviewing a PR with claudecode, literally after two-three prompts it gets to 60% usage. I am on the MAX plan….w%f!!

![]()

Does that sound like you? Do you feel cheated that 20x is now 5x. That was me too.

But now I am healed. Here is what I learnt.

## Claude doesn’t have persistent memory between turns. Did you know or did you know??

Every single time you send a message, the entire conversation gets resent from scratch: your prompts, Claude’s responses, and every tool result. All of it, every time. It’s not reading a log, it’s literally re-processing the full history on every turn.

That’s how transformers work.

So the messages token count isn’t “what you typed.” It’s the running total of everything that has ever been said or read in the session, resent repeatedly.

You read that right, “**Repeatedly**”

**So Why that PR review explodes the count**

When you ask Claude to review a PR, here’s what actually happens under the hood:

1. Claude calls a tool to fetch the PR diff That diff result (could be thousands of lines) gets injected into messages as a tool result
2. Claude calls 20 tools and reads individual files to understand context around the changes — each file read injects that entire file’s content into messages as another tool result
3. Claude writes its review response
4. When you keep arguing with it all of the above gets resent again and again, plus your new message, plus Claude’s new response.
5. It finally fixed your bug and you wanted to send a “Thank you, you’re awesome” message. How cute. That’s another thausands of tokens for you.
6. You finished the PR and now you want to do some dev task on the same session? **Claude usage limit reached. Your limit will reset at 4pm…**

![]()

Okay, but what should I do???

## 1. ABC….CLAUDE.md:

Most people skip this. It is the single highest-leverage thing you can do before writing a single line of code.

Just simply run **/init** to generate a CLAUDE.md file in your project root and Claude reads it automatically at the start of every session.

Think of it as your standing instructions, the things you would otherwise explain from scratch every single time.

**How it actually loads**

There are multiple lookup locations, checked in order:

* ~/.claude/CLAUDE.md — loaded for every project, every session (global)
* /your/project/CLAUDE.md — loaded when you start Claude Code in that directory
* Subdirectory CLAUDE.md files — picked up as Claude navigates into those folders

**The token cost model**

CLAUDE.md is loaded on every session and persists in the context window for the entire session. It is not lazy-loaded or evicted when it is not needed.

* **Cost is fixed per session.** A 2,000-token CLAUDE.md costs 2,000 tokens whether you do 2 messages or 200 messages.
* **Cost compounds with length.** Every instruction you add is paid on every session forever. A bloated CLAUDE.md (5,000+ tokens) meaningfully reduces your effective working context.
* **Subdirectory files stack.** You can use this if your project is a monorepo. Split your claude.md across project instead of having one. They don’t all load simultaneously they load as claude navigates into those directories.

**My mental model for what belongs in it**

I think of CLAUDE.md like my project’s eslint.config.js, it sets invariant rules. My session prompt is the code review comment, it sets task-specific intent.

A well-structured CLAUDE.md for a real project is usually 300 to 600 tokens. If yours is over 2,000 tokens, you are probably storing task state or documentation that does not belong there.

**What I put in mine**

`# CLAUDE.md`

`## Stack`

`- Node 20, TypeScript strict, Prisma ORM`

`- Tests: Vitest, no Jest`

`## Constraints`

`` - Never use `any`. Use `unknown` + type guards. ``

`- Controllers call services. Services call DB. Never bypass.`

`## Naming`

`- Files: kebab-case. Classes: PascalCase. Hooks: use* prefix.`

## 2. /context: Show me the receipts

Press enter or click to view image in full size

![]()

You can run /context, Claude will send you every item occupying its context window: open files, attached documents, tool definitions, conversation turns, and the system prompt. It returns a structured breakdown showing token counts per element and cumulative usage versus the window ceiling.

**What I use it for**

Claude often pulls files into context that were referenced but are no longer needed.

* Spot files that got pulled in but are not needed anymore
* Identify when a conversation thread has grown too long
* Decide between compacting versus starting fresh
* And generally know what is going on

Think of it as a memory profiler for your session.

## 3. /compact: save your session

The practical fix is simpler than it sounds:

“Start in a new terminal tab” Wow!

Also please avoid pasting entire files when only a snippet is relevant, and when a session has run long, summarize what matters and carry just that forward into a new chat.

To do this run **/compact**, it will summarize the entire conversation into a compact, structured representation, capturing decisions made, code written, open questions, and current task state, then continues from that summary as the new baseline.

**What gets preserved and what gets lost**

The compact is lossy by design:

**Preserved:** architectural decisions and rationale, files modified and what changed, current task state and next steps, errors encountered and how they were resolved, outstanding blockers.

**Discarded:** intermediate reasoning chains, superseded approaches, raw tool outputs.

A common mistake is to use /compact reactively, after Claude starts forgetting things. That is simply wrong.

A healthy session produces a better summary than a degraded one. Run **/compact** when you finish a distinct phase, not when you notice degradation.

**When /compact is not the right tool?**

If you are done with a task entirely and moving to something unrelated, just do **/clear** instead it wipes the context completely and resets the session without closing it.

## 4. /commands: stop repeating yourself

/commands defines named aliases for multi-step instruction sequences. When invoked, Claude executes the full sequence without re-parsing intent from natural language.

Commands are stored as structured definitions (name, description, steps) that Claude reads at session start alongside CLAUDE.md.

Natural language prompts are probabilistic, the same prompt produces slightly different behaviour each run. Commands are deterministic.

**An example from my setup**

Press enter or click to view image in full size

![]()

Invoke with: /test-and-fix

**What I use commands for**

* Running tests + fixing type errors + linting in sequence
* Generating a component with my exact folder conventions
* Writing commit messages in my team’s format
* Pre-deploy validation checks before pushing (you can use hooks for this too)

## 5. Reasoning mode is on by default

Before Claude gives you any response, it runs an extended internal reasoning process, working through the problem, considering approaches, weighing tradeoffs. This reasoning happens silently in the background. Whether how small or big your problem is. If you don’t need it turn it off.

![]()

## 6. /btw: stop interrupting it

Either hold on to your cool idea in your head or use /btw to open a parallel inference channel instead of interrupting.

Btw runs in an overlay against Claude’s current session knowledge and the active codebase but the response is never injected into the main conversation history. The main task continues uninterrupted.

## 7. Choosing the right model

Most people open Claude Code, leave it on whatever the default is, and never think about it again.

That default is **Sonnet** on pro plan and **OPUS** on a max plan as of March 2026!

Here’s a simple breakdown **for this**

**Opus:** big brains, very expensive, only use it to plan hard problems using plan mode

**Haiku: S**mall brain, simple stuffs or asking questions, no good for coding.

**Sonnet:** Good enough brain, use it for day to day feature implementation, refactoring, writing tests and reviews.

Use **/model** to swap between this

## 8. Stop Pasting everything

![]()

Stop using the “COPY FOR LLM” button on the chat.

The content immediately becomes dead weight in the conversation history, travelling with every single subsequent message.

Claude Code’s `@file` reference system sidesteps this entirely. Instead of pasting, you should split reusable information into standalone `.md` or `.yaml` files and load them on demand with `@filename.md`.

The file gets pulled in exactly when you need it and not stranded through the entire session by default.

## 8. Stop being lazy and type specs not a random prompt

“Please fix this. Make no mistakes” Enter.

How you phrase a prompt directly affects how many tokens come back. Vague prompts invite verbose responses and unnecesary input tokens just trying to understand which file you’re talking about

If you have a hint about what you need to do, which you should btw!!

Write prompts like “Fix the [BUG Short Description] bug in @`file` that causes [Unexpected outcome] instead of [expected outcome]”

## 9. MCPs aren’t Pokemon GO! You don’t have to catch’em all!

Most developers add MCP servers as they discover them.

Supabase has MCP boom add, GitHub boom, Chrome DevTools boom, Figma boom!

Press enter or click to view image in full size

![]()

The problem is that every connected MCP server loads its full tool definitions and schema into your context window at the start of every single session, whether you use it or not.

These definitions are not small, sometimes it can consume thousands of tokens just sitting there. Stack a few together and the numbers get uncomfortable fast.

Just remove it if you don’t need it. OR use [“mcp funnels”](https://www.google.com/search?q=what+is+mcp+funnel&rlz=1C5AJCO_enAE1192AE1192&oq=what+is+mcp+funnel&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQABiABDIICAIQABgWGB4yCAgDEAAYFhgeMggIBBAAGBYYHjIICAUQABgWGB4yCAgGEAAYFhgeMgYIBxBFGDzSAQgzMjI4ajBqNKgCA7ACAfEFSHh3DbXaOgo&sourceid=chrome&ie=UTF-8)

## 10. If you’re using the DESKTOP APP to code

Press enter or click to view image in full size

![]()

Trust me and use the terminal version, it shows you the context and token usage on every task.

I hope this saves you some tokens 🙏

Thanks for reading! Subscribe for free to receive new posts and support my work.