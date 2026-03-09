---
title: "I Stopped Vibe Coding and Started “Prompt Contracts” — Claude Code Went From Gambling to Shipping"
url: https://medium.com/p/4080ef23efac
---

# I Stopped Vibe Coding and Started “Prompt Contracts” — Claude Code Went From Gambling to Shipping

[Original](https://medium.com/p/4080ef23efac)

Member-only story

# I Stopped Vibe Coding and Started “Prompt Contracts” — Claude Code Went From Gambling to Shipping

## Last Tuesday at 2 AM, I deleted 2,400 lines of code that Claude Code had just generated for me.

[![Phil | Rentier Digital Automation](https://miro.medium.com/v2/resize:fill:64:64/1*8_UYeI21v_IBgt9VUGxsPg.png)](/@rentierdigital?source=post_page---byline--4080ef23efac---------------------------------------)

[Phil | Rentier Digital Automation](/@rentierdigital?source=post_page---byline--4080ef23efac---------------------------------------)

10 min read

·

Feb 11, 2026

--

60

Listen

Share

More

Not because it was bad code. It compiled. It ran. It even looked clean.

But it solved the *wrong problem*. I’d asked for a Supabase auth flow with row-level security. What I got was a beautiful, production-grade auth system — using Firebase.

Claude Code pulled a classic Uno reverse card on my entire stack. Like ordering a pizza and receiving a perfectly cooked risotto. Technically impressive. Fundamentally wrong.

That was the moment I realized something uncomfortable: **I wasn’t coding with Claude Code. I was gambling with it.**

And if you’re typing natural language prompts into Claude Code 🧑‍💻 and hoping for the best, you’re rolling dice too. Except the dungeon master is an AI with zero context and infinite confidence.

Press enter or click to view image in full size

![]()

## The Vibe Coding Trap

Here’s what vibe coding looks like in the wild:

```
> Build me a dashboard for my SaaS
```

Claude Code writes 3,000 lines across 14 files. You squint at the output like you’re trying to see a Magic Eye poster. Some of it looks right.

You run it.

Something breaks.

You say “fix it.”

It fixes one thing, breaks three others. This is not debugging. This is whack-a-mole with a $100/month subscription.

> A few weeks ago, I stumbled on a concept from an ex-OpenAI engineer: **Prompt Contracts**

Forty-five minutes later, you’ve shipped something that *works* but that you don’t fully understand. Congratulations, you’re now maintaining a codebase written by an alien intelligence that doesn’t remember writing it. What could go wrong.

I lived in this loop for months. I shipped two SaaS products almost entirely with Claude Code, and I’m not exaggerating when I say 30% of my time was spent *un-doing* things Claude Code confidently built in the wrong direction. It’s like pair programming with a genius who has amnesia and zero concept of your repo.

The problem was never Claude Code’s intelligence. Opus 4.6 is absurdly capable — it’s basically a senior engineer who read every Stack Overflow answer ever posted and retained all of them, including the wrong ones.

The problem was **my prompts were vibes, not specifications**.

“Make it responsive.” “Add error handling.” “Use best practices.”

These aren’t instructions. They’re horoscopes. And Claude Code isn’t a fortune teller — it’s a contractor. You wouldn’t hand a contractor a napkin that says “build house, make nice” and expect your dream home. You’d get a house. It might even have walls. But the toilet would be in the kitchen because you never said it shouldn’t be.

## Prompt Contracts: The Fix

A few weeks ago, I stumbled on a concept from an ex-OpenAI engineer: **Prompt Contracts**. The idea is simple — instead of writing prompts like creative briefs, write them like legal contracts with four enforceable clauses:

**Goal** — the exact success metric. **Constraints** — hard boundaries that can’t be crossed. **Output Format** — the specific structure you expect. **Failure Conditions** — what makes the output unacceptable.

I thought: “This is cute for ChatGPT blog posts. But can it survive Claude Code building a real backend at 3 AM when you’re running on caffeine and poor life choices?”

So I tested it. For three weeks straight, across two SaaS projects, I replaced every vibe prompt with a Prompt Contract.

Spoiler: I sleep now.

## Component 1: GOAL — Stop Saying “Build Me X”

The single biggest upgrade was forcing myself to define what *done* looks like before Claude Code writes a single line.

**Before (vibe):**

```
> Add a subscription system to the app
```

This is the prompt equivalent of telling your GPS “take me somewhere nice.” You’ll end up *somewhere*. It might be a Michelin star restaurant. It might be a gas station in Ohio.

**After (contract):**

```
> GOAL: Implement Stripe subscription management where users can   
> subscribe to 3 tiers (free/pro/team), upgrade/downgrade instantly,   
> and see billing status on /settings/billing.  
> Success = a free user can subscribe to Pro,   
> see the charge on Stripe dashboard, and access   
> gated features within 5 seconds.
```

The difference isn’t just detail — it’s *testability*. When Claude Code finishes, I can verify the goal in under a minute. No ambiguity. No “well, it kind of works” — the Schrödinger’s cat of software demos.

This alone cut my back-and-forth with Claude Code by roughly half. When the AI knows what the finish line looks like, it stops wandering around the track taking selfies.

## Component 2: CONSTRAINTS — The Walls That Save You

This is where things get Claude Code-specific, because without constraints, Claude Code will *absolutely* reinvent your stack for you. It’s like hiring a kitchen renovator who shows up and says “I also knocked down your living room wall because the feng shui was off.”

I now keep a `CLAUDE.md` at the root of every project that acts as a permanent constraint layer:

```
# CLAUDE.md — Project Constraints (always active)
```

```
## Stack (non-negotiable, I will mass git revert you)  
- Frontend: Next.js 14+ App Router, TypeScript strict  
- Backend: Convex for real-time data, Supabase for auth + storage  
- Auth: Clerk (never roll custom auth, we are not animals)  
- Styling: Tailwind only — no CSS modules, no styled-components## Hard Rules  
- Never install a new dependency without asking first  
- Never modify the database schema without showing the migration plan  
- All API calls go through Convex functions, never direct Supabase   
  client calls from components  
- Environment variables go in .env.local, never hardcoded  
  (I will find you and I will revert you)## Patterns  
- Use server components by default, client components only when   
  interactivity is required  
- Error boundaries on every route segment  
- Zod validation on every user input
```

Before `CLAUDE.md`, Claude Code would randomly decide to use Prisma instead of Convex, or swap Clerk for NextAuth because "it's more common." That's like your barista deciding you actually wanted tea because more people drink tea globally. I didn't ask for a democracy. I asked for Clerk.

Now? It stays in its lane. Every single time.

**Pro tip:** When you start a new Claude Code session, your first message should be:

```
> Read CLAUDE.md and confirm you understand the project constraints   
> before doing anything.
```

This forces a handshake. Think of it as the Miranda rights of your codebase. Claude Code echoes back the constraints, you both agree on reality, and *then* work begins. Without this, you’re essentially starting every session by handing the keys to someone who doesn’t know what car they’re driving.

## Component 3: FORMAT — Tell It Exactly What to Hand You

Vibe coding lets Claude Code decide the structure. This is like telling a chef “surprise me” and then being shocked when you get a deconstructed Caesar salad served inside a shoe.

**Before:**

```
> Create an API endpoint for user onboarding
```

Claude Code decides: one massive file, inline validation, no types, everything in a single 800-line function that does auth, database calls, and email sending in one breath. It works. It’s also a war crime against future-you who has to maintain it.

**After:**

```
> FORMAT:   
> 1. Convex function in convex/users.ts (mutation, not action)  
> 2. Zod schema for input validation in convex/schemas/onboarding.ts  
> 3. TypeScript types exported from convex/types/user.ts  
> 4. Include JSDoc on the public function  
> 5. Return { success: boolean, userId: string, error?: string }
```

Now I get modular, typed, documented code — every time. Not because Claude Code can’t produce this on its own, but because *without explicit format instructions, it optimizes for speed, not maintainability*. It’s speedrunning your codebase. You need it to play the long game.

This matters even more when you’re using Claude Code’s agent teams feature to parallelize work. If your sub-agents don’t follow the same format contract, you end up merging code that looks like it was written by five developers who communicate exclusively through passive-aggressive commit messages.

## Component 4: FAILURE CONDITIONS — The Secret Weapon

This is the component that changed everything. If the Goal is the carrot, Failure Conditions are the stick. And Claude Code responds to sticks like a developer responds to a `production is down` Slack message — immediately and with full attention.

Defining what *breaks* the contract gives Claude Code a negative target. It’s like training a dog: “sit” is good, but “NOT on the couch, NOT on the table, NOT on the visiting in-laws” is what actually saves your furniture.

**Here’s a real Prompt Contract I used last week:**

```
> Build the /dashboard page.  
>  
> GOAL: Display user's active projects with real-time updates.   
> First meaningful paint under 1 second. User can create, archive,   
> and rename projects inline.  
>  
> CONSTRAINTS: Convex useQuery for data, no polling, no SWR.   
> Clerk useUser() for auth check. Redirect to /sign-in if   
> unauthenticated. Max 150 lines per component file.  
>  
> FORMAT: Page component in app/dashboard/page.tsx (server component   
> wrapper), client component in components/dashboard/ProjectList.tsx,   
> Convex query in convex/projects.ts. Tailwind only.  
>  
> FAILURE CONDITIONS:  
> - Uses useState for data that should be in Convex  
> - Any component exceeds 150 lines  
> - Fetches data client-side when it could be server-side  
> - Uses any UI library besides Tailwind utility classes  
> - Missing loading and error states  
> - Missing TypeScript types on any function parameter
```

When I ran this, Claude Code produced a clean, real-time dashboard on the first try. No Firebase. No Prisma. No mystery npm packages from 2019 with 12 GitHub stars and a README that says “TODO.” No 1,200-line god-component that future-me would need therapy to refactor.

Compare that to what happened the month before, when “build me a dashboard” produced a component that imported Material UI (I don’t use Material UI), used `useEffect` for data fetching (we have Convex for a reason), and had zero loading states. Just raw, unprotected optimism that the data would always be there instantly. The software equivalent of leaving your house unlocked because "this is a nice neighborhood."

The failure conditions act as guardrails. Claude Code doesn’t have to guess what “good” means when you’ve already told it what “bad” looks like. It’s the difference between “drive safely” and “don’t exceed 80, don’t run reds, don’t take the highway during rush hour.” One is a prayer. The other is a navigation system.

**🔄 Update:** One contract I didn’t mention in the original version of this article because it didn’t exist yet: `/security-review`. Type it before you push. Claude scans your pending changes for SQL injection, auth bypasses, hardcoded secrets — the stuff you miss when you’re deep in feature-mode. I wrote a [full breakdown of how it works and how to customize it for your stack](/@rentierdigital/anthropic-just-crashed-15-billion-in-cybersecurity-stocks-17d34513d7cd). Shortest version: it’s the post-contract safety net. Your Prompt Contracts make Claude build the right thing. `/security-review` makes sure the right thing doesn’t have a hole in it.

## The Results (3 Weeks of Prompt Contracts)

I tracked my workflow across two active projects. The numbers aren’t peer-reviewed — I’m one developer in a dark room, not a research lab — but the pattern was unmistakable.

**Undo/revert rate** dropped from roughly 1 in 3 generations to about 1 in 10. Claude Code stopped building things I didn’t ask for. My `git revert` muscle memory is already fading. I might need to re-learn the command someday. Or not. I'm at peace with this.

**Time from prompt to usable code** went from an average of 3 rounds of back-and-forth down to 1.2 rounds. Most Prompt Contract outputs were usable on the first or second generation. This freed up time I now spend on important things, like over-engineering my CLAUDE.md and adding failure conditions for failure conditions.

**CLAUDE.md violations** (wrong library, wrong pattern, hardcoded values) went from a few per day to essentially zero once I added the constraint handshake at session start. The `CLAUDE.md` + handshake combo is basically a pre-flight checklist. Pilots don't skip it. Neither should you. Unless you enjoy your code crashing into a metaphorical mountain.

The biggest surprise? **My prompts got shorter over time**, not longer. Once `CLAUDE.md` holds the permanent constraints and you internalize the 4-component structure, a Prompt Contract for a complex feature takes maybe 60 seconds to write. That's 60 seconds that saves you 45 minutes of debugging and questioning your career choices.

This principle extends beyond Claude Code. When I built a custom MCP server to monitor 5 SaaS apps simultaneously, I discovered that the tool descriptions you write for MCP tools are prompt contracts in disguise. A tool described as “query credit data from Convex” returns useless JSON. The same tool described as “find users whose credit balance drifts more than 10% from expected, flag anything over 50 credits as urgent” returns actionable intelligence. [The full build story is here](/@rentierdigital/i-run-5-saas-apps-and-cant-tell-which-one-is-on-fire-so-i-gave-claude-a-tool-to-watch-them-all-d715e435dd0e) — 16 commits, 4 hours of OAuth debugging, and a framework for when you actually need this.

## How to Start Today

You don’t need to overhaul your workflow. You don’t need to read a 400-page book on prompt engineering. You don’t need to watch a 3-hour YouTube video where someone explains the concept in the first 4 minutes and then sells you a course for the remaining 2 hours and 56 minutes.

Start with two things:

* **First**, create a `CLAUDE.md` in your project root with your stack, hard rules, and patterns. This is your permanent Constraints layer. Every Claude Code session starts by reading it. Think of it as the Constitution of your repo — except this one actually gets followed.
* **Second**, next time you’re about to type a vibe prompt like “add user settings page,” stop. Take 30 seconds and add one GOAL, one CONSTRAINT, and one FAILURE CONDITION. Just one of each. You’ll feel the difference immediately. It’s like going from “I hope this works” to “I *know* this works” — a feeling so rare in software development it should be classified as a controlled substance.

The Prompt Contract framework isn’t about writing more. It’s about thinking for 60 seconds so Claude Code doesn’t have to guess for 60 minutes.

I went from gambling to shipping. Your move.

*If you’re building SaaS with Claude Code and want more tactical breakdowns like this, follow me for weekly deep dives. I ship, break, and mass-revert things in public so you don’t have to.*