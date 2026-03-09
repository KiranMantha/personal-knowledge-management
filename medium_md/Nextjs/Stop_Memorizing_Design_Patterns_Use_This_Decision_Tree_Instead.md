---
title: "Stop Memorizing Design Patterns: Use This Decision Tree Instead"
url: https://medium.com/p/e84f22fca9fa
---

# Stop Memorizing Design Patterns: Use This Decision Tree Instead

[Original](https://medium.com/p/e84f22fca9fa)

Member-only story

# Stop Memorizing Design Patterns: Use This Decision Tree Instead

## Choose design patterns based on pain points: apply the right pattern with minimal over-engineering in any OO language.

[![Alina Kovtun✨](https://miro.medium.com/v2/resize:fill:64:64/1*Ddgp0_7ZDX4yDLhl_wbF4w@2x.jpeg)](/@akovtun?source=post_page---byline--e84f22fca9fa---------------------------------------)

[Alina Kovtun✨](/@akovtun?source=post_page---byline--e84f22fca9fa---------------------------------------)

10 min read

·

Jan 29, 2026

--

46

Listen

Share

More

Design patterns rarely fail because they are “wrong.” They fail because we reach for them at the wrong moment, for the wrong reason, or as a substitute for naming the real problem. Usually, the hard part is not remembering that Strategy exists, it is deciding whether Strategy is what your code needs right now, or whether a simpler move would do more.

> [**If you’re not a member of Medium, you can read the full article for free here.**](/@akovtun/stop-memorizing-design-patterns-use-this-decision-tree-instead-e84f22fca9fa?sk=d8ce25c71ba530c026c9b90e9c8d38f0)

Press enter or click to view image in full size

![]()

This is why a decision tree helps. It forces one step of discipline before you pick a pattern: ***you describe the friction you are trying to remove.***

Are you struggling with object creation that keeps getting more complex? Are you fighting boundaries between components or external dependencies? Or is the main issue that behaviour keeps changing and your code is adding conditionals?

The goal of this article is to give you a small set of questions that lead to a short list of patterns that fit your situation. You still need judgment, but you will spend less time guessing and more time making decisions.

## Why design patterns are useful?

Patterns earn their place when they reduce a recurring cost.   
In practice, that cost usually looks like one of these:

* changes require touching too many files
* tests are slow or brittle because the code has no clean seam
* external APIs leak into domain logic and spread “translation” code everywhere
* constructors and initialization code keep growing, and valid combinations become unclear
* the same logic is duplicated because there is no stable place for it to live

The mistake is treating a pattern as an upgrade in itself. It is not. A pattern is a way of paying for flexibility in a controlled place instead of paying for it everywhere, repeatedly.

## The decision tree in three questions

Start with one question: ***where is the pain coming from?***

Then narrow down:

1. ***Is the pain about creating objects?***
2. ***Is the pain about how objects fit together?***
3. ***Is the pain about behaviour that changes across cases or over time?***

These map to creational, structural, and behavioural patterns. You can ignore the categories if you want; the questions are what matter.

## Branch 1: Creating objects (Creational patterns)

Use this branch when creation logic becomes its own problem: too many parameters, repeated setup, unclear defaults, or “which implementation should I create here?” logic spread across the codebase.

### Step 1: Do you truly need exactly one instance?

If you reach for Singleton, be specific about why. “Easy access” is not a strong reason; it often hides dependencies and makes tests harder.

Singleton can be reasonable when the object is **effectively stateless** or **safe to share** (for example: a read-only config snapshot, a process-wide logger wrapper). It becomes risky when it stores mutable state, request context, or anything that must be reset between tests.

Press enter or click to view image in full size

![]()

If what you want is controlled construction and explicit wiring, dependency injection or a small application container tends to age better than a global instance.

### Step 2: Is construction complex or easy to misuse?

When constructors accumulate optional arguments and configuration combinations start to matter, **Builder** is usually the cleanest move. The point is not chaining for aesthetics; the point is making object creation explicit and validating it early.

```
# Without a Builder: hard to read and easy to misuse  
request = Request.new(url, method, headers, body, timeout, retry_count, cache, auth)  
  
# With a Builder: clearer intent, easier validation  
request = RequestBuilder.new  
  .url("https://api.example.com")  
  .method(:post)  
  .headers(auth_headers)  
  .timeout(2)  
  .build
```

Builders also make it easier to expose a small set of “known good” presets (for example: a default retry strategy) without forcing every caller to assemble a long argument list.

Press enter or click to view image in full size

![]()

### Step 3: Are you choosing implementations based on context?

When code repeatedly decides which concrete class to instantiate based on configuration, file type, provider, feature flags, or environment, that decision should be centralised.

* **Factory Method** works well when a base class defines a contract and subclasses decide what concrete type to create.

Press enter or click to view image in full size

![]()

* **Abstract Factory** fits when you need a *family* of related objects that must match each other (for example: provider-specific client + mapper + validator).

Press enter or click to view image in full size

![]()

* **Prototype** is useful when cloning an existing configured object is cheaper or safer than rebuilding it, especially if initialisation is expensive.

Press enter or click to view image in full size

![]()

## Branch 2: Structuring objects (Structural patterns)

Use this branch when code is correct but awkward because boundaries are unclear: external interfaces bleed into application logic, subsystems require too many steps to use safely, or composition is hard to manage.

### Step 1: Are you bridging incompatible interfaces?

When your internal code expects one interface and an external dependency provides another, **Adapter** is the straightforward solution. It protects your domain from vendor-specific shapes and naming.

```
# Your app expects:  
payment_processor.process(amount, card)  
  
# Provider offers:  
provider.execute_payment(card_info, transaction_amount)  
  
class ProviderAdapter  
  def initialize(provider)  
    @provider = provider  
  end  
  
  def process(amount, card)  
    @provider.execute_payment(card.to_provider_format, amount)  
  end  
end
```

***A useful rule***: keep adapters focused on translation. When an adapter starts containing business rules, split those rules into a separate component so the boundary stays clean.

Press enter or click to view image in full size

![]()

### Step 2: Is a subsystem too complex to use correctly?

If a library or internal subsystem has multiple steps that must be invoked in the right order, introduce a **Facade**. A good facade makes the safe path easy and reduces the chance that engineers will call low-level pieces incorrectly.

Press enter or click to view image in full size

![]()

Example: a “video conversion” workflow might involve probing, transcoding, metadata extraction, storage upload, and cleanup. A facade can expose a single entry point, while leaving the internal orchestration free to evolve.

### Step 3: Do you need optional features without subclass explosion?

When you need combinations like logging + encryption + compression + caching, subclassing becomes a combinatorial mess. **Decorator** gives you composition that stays local and explicit.

Press enter or click to view image in full size

![]()

Decorator works best when each wrapper is small and predictable. If wrappers start depending on each other, it becomes difficult to reason about call order and side effects.

### Step 4: Do you need a stand-in object?

Use **Proxy** when you want lazy loading, caching, access control, instrumentation, or remote calls behind a local-looking interface.

Press enter or click to view image in full size

![]()

### Step 5: Do you have a tree and want uniform treatment?

Use **Composite** when your domain naturally forms a hierarchy and you want to treat leaf nodes and containers the same way (file systems are the classic example; UI components and nested content structures are also common).

Press enter or click to view image in full size

![]()

### Step 6: Are you paying a memory cost for repeated shared state?

**Flyweight** matters when many objects share identical data and duplicating it is expensive. It is less common in typical web app code, but it is worth keeping in mind for editors, renderers, or large in-memory models.

Press enter or click to view image in full size

![]()

### Step 7: Do you want to vary abstraction and implementation independently?

Use **Bridge** when you have two dimensions of change and want to avoid a matrix of subclasses (for example: “export format” vs “export destination”, or “device type” vs “control type”).

Press enter or click to view image in full size

![]()

## Branch 3: Handling behaviour (Behavioural patterns)

Use this branch when the main issue is changing rules and workflow logic: a method accumulating `if` branches, an algorithm changing per customer or plan, or a pipeline that is hard to extend cleanly.

### Step 1: Do requests flow through a sequence of independent steps?

**Chain of Responsibility** fits middleware-style pipelines where each step may stop processing or pass the request along.

```
class Handler  
  def initialize(next_handler = nil)  
    @next = next_handler  
  end  
    
  def call(request)  
    return unless handle?(request)  
    @next&.call(request)  
  end  
end
```

The pattern stays healthy when each handler has a single responsibility and a clear “stop vs continue” contract. It breaks down when handlers mutate shared state unpredictably or depend on each other’s internal behaviour.

Press enter or click to view image in full size

![]()

### Step 2: Do you need to queue actions, log them, retry them, or undo them?

Use **Command** when representing actions as objects gives you operational benefits: job queues, retries, audit logs, “run later” workflows, or undo stacks.

Press enter or click to view image in full size

![]()

### Step 3: Do you need to swap algorithms without changing the caller?

**Strategy** is the high-ROI answer when you have multiple implementations of the same behaviour and you want the caller to stay stable. This is common for payment providers, routing decisions, recommendation policies, rate limiting algorithms, and formatting logic.

Press enter or click to view image in full size

![]()

The practical signal is recurring branching: “if plan is X do this, if plan is Y do that,” plus tests that duplicate setup across branches.

### Step 4: Is behaviour driven by state and conditionals keep multiplying?

Use **State** when you have well-defined modes and transitions (connections, approval workflows, session lifecycles). State reduces complex branching by making behaviour explicit per state.

Press enter or click to view image in full size

![]()

### Step 5: Do you need one-to-many notifications?

Use **Observer** for subscription-style updates. It can be clean, especially with domain events, but it can also hide control flow. Keep observers visible and avoid introducing surprising side effects.

Press enter or click to view image in full size

![]()

### Step 6: Do you need snapshots and restores?

**Memento** fits undo features, rollbacks, and restoring prior versions without exposing internal representation.

Press enter or click to view image in full size

![]()

### Step 7: Do you need a coordinator so objects don’t depend on each other directly?

**Mediator** can reduce coupling in complex coordination scenarios, especially in UI logic or workflow orchestration. The risk is concentrating too much logic into one place. Mediators stay manageable when their responsibilities are narrow and well-defined.

Press enter or click to view image in full size

![]()

### Step 8: Do you need new operations over a stable object structure?

**Visitor** is most useful when the structure is stable (like an AST — Abstract Syntax Tree) and you need to add new operations without changing the structure. In application code, it’s less common than Strategy or Chain, but still valuable in the right domain.

Press enter or click to view image in full size

![]()

## The Complete Decision Tree

![]()

## Applying the tree to common situations

### 1) Notification delivery (email, SMS, push)

When delivery rules grow and channels expand, branching becomes the default implementation strategy. Strategy is a better fit because you can add a new channel without rewriting the caller.

A practical implementation is an interface such as `NotificationChannel#send(user, message)` with concrete implementations per channel, and a selector that chooses the strategy based on configuration or feature flags.

### 2) API request processing (rate limiting → auth → handler)

When a request must pass through multiple checks in a defined order, Chain of Responsibility keeps each step small and testable. It also makes reordering or inserting steps safer, because the contract is explicit.

### 3) Report generation (many options, multiple formats)

Builder helps when report configuration has many parameters and valid combinations matter. Strategy helps when you want to choose PDF/CSV/XLSX generation without burying formatting logic inside conditionals.

*If you are interested in becoming a stronger engineer in the long term, I also write about software design fundamentals and architecture.*

[## How to Make Your Next Career Move in Tech

### A mentoring-based framework to clarify your target role, upgrade your CV/LinkedIn, and land more interviews

medium.com](/womenintechnology/how-to-make-your-next-career-move-in-tech-b7db30ad5f3f?source=post_page-----e84f22fca9fa---------------------------------------)

[## Live Coding in the Age of AI

### It’s time to start interviewing humans for what they actually do.

medium.com](/@akovtun/live-coding-in-the-age-of-ai-f10d39869abe?source=post_page-----e84f22fca9fa---------------------------------------)

[## Database First Aid: Index vs Denormalize vs Cache vs Partition

### Identify whether you have CPU, IO, lock contention, or query-shape problems.

medium.com](/womenintechnology/database-first-aid-index-vs-denormalize-vs-cache-vs-partition-8596cc4a9bb9?source=post_page-----e84f22fca9fa---------------------------------------)

![Alina Kovtun✨](https://miro.medium.com/v2/resize:fill:40:40/1*Ddgp0_7ZDX4yDLhl_wbF4w@2x.jpeg)

[Alina Kovtun✨](/@akovtun?source=post_page-----e84f22fca9fa---------------------------------------)

## SOLID

[View list](/@akovtun/list/solid-f250412eb47e?source=post_page-----e84f22fca9fa---------------------------------------)

5 stories

![](https://miro.medium.com/v2/resize:fill:388:388/1*WeUs7We-S2G42EaAiNP41g.png)

![](https://miro.medium.com/v2/da:true/resize:fill:388:388/0*1UhD0Oo4BaXNmGfS)

![](https://miro.medium.com/v2/resize:fill:388:388/1*Q5HS_kIwmgJH7sO3oOZc5w.jpeg)

[## Building a Maintainable ETL Pipeline: Lessons from Refactoring Our Analytics Import

### What we learned refactoring 1,000 lines of fragile import code into something we could actually reason about

medium.com](/womenintechnology/building-a-maintainable-etl-pipeline-lessons-from-refactoring-our-analytics-import-8f966dadf34a?source=post_page-----e84f22fca9fa---------------------------------------)

*These pieces are written from a practical engineering perspective, not as textbook summaries. I focus on real-world trade-offs, mistakes, and patterns that appear once systems grow beyond tutorials and pet projects.*

**P.S.** I know how discouraging it is to send applications and hear nothing back. I put together [***The High-Conversion CV Guide***](https://alinakovtun.gumroad.com/l/your-cv-guide)to help you build a high-signal CV that actually gets read — 70+ pages of practical, step-by-step advice on how to build a resume that stands out in a crowded market.   
**P.P.S.** If you’re aiming to grow from trainee to senior, I’ve collected my mentoring frameworks into one guide: [***From Bootcamp to Senior***](https://alinakovtun.gumroad.com/l/career-progression).

***Now a bundle is available with 20% discount with promocode*** [***CAREER2026***](https://alinakovtun.gumroad.com/l/career-cv/CAREER2026)

✔️ If you like my blog, you can [***Buy Me a Coffee here***](http://www.buymeacoffee.com/akovtun).  
✔️ Connect with me on [***Linkedin***](http://www.linkedin.com/in/alina-kovtun)***.***✔️ Press and hold the 👏 button to give up to 50 claps to this article!

[## The Terminal as a Slot Machine: The Rise of the AI Creation Psychosis

### For years, the universal truth of software engineering was simple: We are limited by our hands.

medium.com](/@akovtun/the-terminal-as-a-slot-machine-the-rise-of-the-ai-creation-psychosis-7b10d04ebf16?source=post_page-----e84f22fca9fa---------------------------------------)