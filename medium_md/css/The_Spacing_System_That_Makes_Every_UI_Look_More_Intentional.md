---
title: "The Spacing System That Makes Every UI Look More Intentional"
url: https://medium.com/p/52251ae61c2f
---

# The Spacing System That Makes Every UI Look More Intentional

[Original](https://medium.com/p/52251ae61c2f)

# The Spacing System That Makes Every UI Look More Intentional

## *You can get the colors right, the fonts right, and still have something that looks like it was assembled by guesswork. Spacing is usually why.*

[![Mohit Phogat](https://miro.medium.com/v2/resize:fill:64:64/1*lXzrQpFfJ25kN6SFPoKH6Q.png)](/?source=post_page---byline--52251ae61c2f---------------------------------------)

[Mohit Phogat](/?source=post_page---byline--52251ae61c2f---------------------------------------)

8 min read

·

Jun 22, 2026

--

8

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D52251ae61c2f&operation=register&redirect=https%3A%2F%2Fmohitphogat.medium.com%2Fthe-spacing-system-that-makes-every-ui-look-more-intentional-52251ae61c2f&source=---header_actions--52251ae61c2f---------------------post_audio_button------------------)

Share

Pull up any interface that feels amateur and look past the colors and fonts for a second. Look only at the gaps. The space between the heading and the paragraph below it. The space between one card and the next. The padding inside a button.

Nine times out of ten, that’s where it falls apart. Not the palette. Not the typeface. The spacing was never decided — it was eyeballed, one element at a time, until nothing relates to anything else.

This is the part of visual design most people skip straight past, because it doesn’t photograph the way color does. Nobody screenshots a layout and says “look at that spacing.” But spacing is doing more work than almost anything else on the screen, and it’s the cheapest thing to fix once you understand the system behind it.

## Why random spacing reads as amateur

Spacing isn’t decoration. It’s communication.

This comes from a basic principle in visual perception called the Gestalt law of proximity: elements that are close to one another tend to be perceived as a group, rather than as individual, unrelated objects. Your brain does this automatically, without being told to. It looks at gaps between things and decides what belongs together before it reads a single word of content.

That means every spacing decision you make is actually a grouping decision, whether you intend it to be or not. A common mistake is placing a field label equidistant between two input fields. The user has to pause and calculate: “Does this label belong to the box above it or below it?” Nobody designed that confusion on purpose. It happened because the spacing was arbitrary instead of intentional.

When spacing is random, the brain still tries to find a pattern in it — and fails. That failure registers as “something’s off” even when the person looking at it can’t say what. Most “messy” UI is a proximity problem, not a colour problem. Colors and fonts can be flawless and the layout will still feel unresolved if the gaps don’t communicate the right relationships.

Press enter or click to view image in full size

![]()

## The base unit system — why 8px specifically

The fix that almost every major design system has converged on is deceptively simple: pick one base unit, and make every spacing value in your interface a multiple of it.

The core idea is simple: use multiples of 8 (8, 16, 24, 32, 40, 48, 56, 64, and so on) to define every spacing value in your design. This applies to margins, padding, widths, heights, line heights, and even icon sizes.

This isn’t an arbitrary number. It exists because screens need math that works everywhere. Most popular screen resolutions divide evenly by 8 on at least one axis, which means your layouts render without half-pixel blurriness on Android, iOS, and desktop displays. Mobile screen widths of 360, 375, 390 all divide cleanly by 8.

Google Material Design uses this system at its core. Apple’s Human Interface Guidelines reference it too, though less strictly. GammaUX notes the 8-point grid became an industry standard between 2017 and 2018, driven by designers like Elliot Dahl and adopted by major companies including Google and IBM. Atlassian’s design system documents the same principle each spacing value is a multiple of the base unit, ranging from 0px to 80px, to allow for flexibility while still maintaining consistency across different layouts.

The actual benefit isn’t aesthetic purity. It’s removing a decision you’d otherwise make hundreds of times. Instead of agonizing over whether a button needs 13px or 15px of padding, the grid narrows your choices: 8px or 16px. That limitation frees you to focus on bigger design problems, like hierarchy and interaction.

For tighter spots — icon-to-label gaps, compact badge padding — most systems allow a 4px sub-unit. If 8px feels too big for a gap and 0px is too small, use 4px. The sub-grid exists for a reason. Consistency matters more than dogma. What you want to avoid is mixing in arbitrary numbers like 13px or 19px just because they “felt right” in the moment. If part of your team uses an 8px grid and another part uses a 5px or 10px grid, you lose all the consistency benefits. Align on one system across the entire project.

A standard scale most teams land on: **4, 8, 12, 16, 24, 32, 48, 64, 96**. That covers the overwhelming majority of spacing needs in a typical interface — from a tight icon gap to the space between major page sections.

Press enter or click to view image in full size

![]()

## Internal vs external spacing — making proximity concrete

Once you’ve picked a scale, the actual skill is deciding which value goes where. This comes down to one rule: spacing inside a group should be smaller than spacing between groups.

Consider a card component with 20px padding inside. If you place two such cards next to each other, you’d want a margin between them of at least 20px, if not more. That way, each card feels like its own unit, with clear “breathing room” around each. If the margin were smaller than the padding, the cards would visually merge together, confusing their grouping.

This is sometimes called the internal-to-external rule, and it applies everywhere, not just to cards. Within the structure of the 8px grid, adjust the spacing to ensure that the internal spacing of elements is never greater than the spacing between them and other elements.

Applied to a form: group form labels with their inputs (4–8px), then leave a clear gap (24px+) before the next group. The visual hierarchy will do the work the eye expects. A label sitting close to its input reads as “these belong together.” The same label with too much breathing room around it leaves the user doing math instead of reading.

Applied to a product card: visually divide your product cards into two categories — Group 1 (Product info): the Price should be visually glued to the title, while the Add to Cart button gets distinct separation as a different kind of action.

The pattern is consistent across every component type. Tight spacing says “these are one idea.” Generous spacing says “these are different ideas.” Get that backwards anywhere in your UI and users have to work to understand structure that should have been obvious.

Press enter or click to view image in full size

![]()

## The 10-minute spacing audit

You don’t need new tooling to check your own work. Open the interface — a live site, a Figma file, doesn’t matter — and walk through this in about ten minutes:

**Step 1 — Measure five gaps.** Pick five visible spacing values: padding inside a card, gap between two cards, space between a label and its input, margin around a button’s text, space between a section heading and the content below it. Measure each one. If any of them land on something like 13px, 19px, or 27px instead of a value on your scale, that’s a flag.

**Step 2 — Squint test for grouping.** Step back from the screen, or zoom out, and ask: based purely on the gaps, what looks like it belongs together? If the visual grouping doesn’t match the actual logical grouping of your content, the spacing is misleading users regardless of what the copy says.

**Step 3 — Check the internal-to-external ratio.** For every container — card, form group, navigation item — confirm the padding inside is equal to or smaller than the margin outside. Adjust the spacing to ensure that the internal spacing of elements is never greater than the spacing between them and other elements.

**Step 4 — Trace one reading path.** Pick one screen and trace how your eye moves through it, top to bottom or left to right. Note every place your eye pauses or backtracks. Those pause points are usually spacing inconsistencies — a gap that’s too small where it should be a clear break, or too large where it should read as continuous.

If most of your five measured values are off-scale, or the grouping doesn’t match the content, you’ve found exactly where to fix things — and exactly why the layout felt slightly off before you could explain why.

## Common mistakes worth naming directly

**Too much padding inside cards.** This is the most common overcorrection. Someone reads that “white space looks premium” and applies it without limits — 32px or 40px of padding inside every card, regardless of how much content is in it. The result is cards that feel hollow rather than spacious, and a layout that wastes vertical space without adding any clarity. Internal padding should scale with content density, not with a vague sense that more is better.

**Too little between sections.** The opposite mistake, usually born from trying to fit more content above the fold. Adding space between unrelated items reduces visual clutter and makes structure clear. When section breaks get compressed to save vertical space, users lose the visual cue that tells them one topic has ended and another has begun. They end up reading section three as a continuation of section two.

**Inconsistent spacing across similar components.** Inconsistent spacing blurs relationships and leaves users unsure of what belongs with what. If one card on a page has 16px padding and the next has 20px, most users won’t consciously notice — but the layout will feel subtly unsettled, the same way a slightly crooked picture frame bothers you before you identify why.

**Ignoring mobile.** Elements may appear grouped on desktop but misaligned on mobile, confusing users. A spacing decision that creates clear grouping at 1440px can completely collapse at 375px if the layout wasn’t checked at both sizes.

## Tools that make this practical

**Figma’s spacing nudge settings.** Use Figma’s nudge settings: go to Preferences and set the “Big nudge” to 8px. Now every Shift + Arrow press moves elements exactly one grid unit. This single setting removes most of the temptation to eyeball a gap, because the easiest way to move something is already locked to your scale.

**Define your scale as variables, not raw numbers.** Define your spacing scale as local variables (space/100 = 8, space/200 = 16, etc.) so every team member references the same tokens.

**CSS custom properties for the same scale on the dev side:**

```
:root {  
  --space-1: 4px;  
  --space-2: 8px;  
  --space-3: 12px;  
  --space-4: 16px;  
  --space-6: 24px;  
  --space-8: 32px;  
  --space-12: 48px;  
  --space-16: 64px;  
}  
.card {  
  padding: var(--space-4);  
  margin-bottom: var(--space-6);  
}
```

Every space token should be used in place of the raw pixel or rem values when adding space between components or objects on a page. Once this exists in your CSS, nobody on the team types a raw pixel value into a margin or padding property again — they reach for a token, and the token is always on-scale by definition.

The spacing system itself isn’t the interesting part. It’s a short list of numbers. What it does is take a decision you’d otherwise make badly, hundreds of times, and turn it into a decision you make once. Everything after that is just applying it — and that’s the part that actually makes an interface look like someone meant it.

Press enter or click to view image in full size

![]()

If this helped, follow me here. I write about UI, UX, and the fundamentals that quietly separate work that looks intentional from work that looks rushed.