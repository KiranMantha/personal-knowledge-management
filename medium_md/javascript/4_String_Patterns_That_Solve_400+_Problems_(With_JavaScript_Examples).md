---
title: "4 String Patterns That Solve 400+ Problems (With JavaScript Examples)"
url: https://medium.com/p/5f0f9344a7f6
---

# 4 String Patterns That Solve 400+ Problems (With JavaScript Examples)

[Original](https://medium.com/p/5f0f9344a7f6)

# 4 String Patterns That Solve 400+ Problems (With JavaScript Examples)

[![devonmobile](https://miro.medium.com/v2/resize:fill:64:64/1*y8dGyx2R432It6C--ujVCg.png)](https://medium.com/@devonmobile?source=post_page---byline--5f0f9344a7f6---------------------------------------)

[devonmobile](https://medium.com/@devonmobile?source=post_page---byline--5f0f9344a7f6---------------------------------------)

4 min read

·

Sep 16, 2025

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D5f0f9344a7f6&operation=register&redirect=https%3A%2F%2Fjavascript.plainenglish.io%2F4-string-patterns-that-solve-400-problems-with-javascript-examples-5f0f9344a7f6&source=---header_actions--5f0f9344a7f6---------------------post_audio_button------------------)

Share

Strings are one of the most common topics in coding interviews. From substring searches to anagram problems, interviewers love to test whether you can spot the **underlying pattern**.

But here’s the good news: Most string problems reduce to just **4 patterns**.  
Master these, and you’ll crack **400+ problems** across LeetCode, Codeforces, or your interviews.

In this article, we’ll explore these 4 patterns with:  
 ✅ When to use them  
 ✅ Step-by-step approaches  
 ✅ JavaScript code examples  
 ✅ Complexity analysis

## Sliding Window / Two Pointers for Substrings

**When to use:**

* Problems involving substrings (continuous parts of a string).
* Tasks like “longest substring without repeats,” or “minimum substring that contains all characters.”

**Approach:**

1. Use two pointers (`left`, `right`) to represent the current substring.
2. Expand `right` to include new characters.
3. Shrink `left` when the substring breaks the condition (e.g., duplicate chars).
4. Track the answer (longest, shortest, etc.) while moving the window.

**JavaScript Example Longest Substring Without Repeating Characters:**

```
function lengthOfLongestSubstring(s) {  
  const set = new Set();  
  let left = 0, best = 0;  
  
  for (let right = 0; right < s.length; right++) {  
    while (set.has(s[right])) {  
      set.delete(s[left++]); // shrink from left  
    }  
    set.add(s[right]);  
    best = Math.max(best, right - left + 1);  
  }  
  return best;  
}
```

**Complexity:**

* Time: O(n) → each character enters and leaves the set once.
* Space: O(k) — up to k distinct characters in the set.

## KMP / Prefix Function / Z-Algorithm

**When to use:**

* Searching for a pattern inside a larger string.
* Implementing `strStr()` or solving repeated substring problems.

**Approach (KMP):**

1. Precompute the **LPS (Longest Prefix Suffix)** array for the pattern.
2. Traverse the text with two pointers (`i` for text, `j` for pattern).
3. On mismatch, jump using `lps[j-1]` instead of restarting from 0.
4. Continue until match is found or text ends.

**JavaScript Example KMP Search:**

```
function kmpSearch(text, pattern) {  
  const lps = buildLPS(pattern);  
  let i = 0, j = 0;  
  
  while (i < text.length) {  
    if (text[i] === pattern[j]) {  
      i++; j++;  
      if (j === pattern.length) return i - j; // found match  
    } else if (j > 0) {  
      j = lps[j - 1]; // jump back  
    } else {  
      i++;  
    }  
  }  
  return -1; // not found  
}  
  
function buildLPS(pat) {  
  const lps = Array(pat.length).fill(0);  
  let len = 0;  
  for (let i = 1; i < pat.length;) {  
    if (pat[i] === pat[len]) {  
      lps[i++] = ++len;  
    } else if (len > 0) {  
      len = lps[len - 1];  
    } else {  
      lps[i++] = 0;  
    }  
  }  
  return lps;  
}
```

**Complexity:**

* Time: O(n + m), where n = text length, m = pattern length.
* Space: O(m), for LPS array.

## Trie / Prefix Tree

**When to use:**

* Problems about prefixes, autocomplete, or checking multiple words quickly.
* Useful for dictionary-like problems.

**Approach:**

1. Build a tree where each node is a character.
2. Insert words by linking characters.
3. Mark the end of a word using a boolean flag (`isEnd`).
4. Searching for words or prefixes means walking through the tree character by character.

**JavaScript Example Basic Trie:**

```
class TrieNode {  
  constructor() {  
    this.children = new Map();  
    this.isEnd = false;  
  }  
}  
  
class Trie {  
  constructor() {  
    this.root = new TrieNode();  
  }  
  
  insert(word) {  
    let node = this.root;  
    for (const ch of word) {  
      if (!node.children.has(ch)) {  
        node.children.set(ch, new TrieNode());  
      }  
      node = node.children.get(ch);  
    }  
    node.isEnd = true;  
  }  
  
  search(word) {  
    let node = this.root;  
    for (const ch of word) {  
      if (!node.children.has(ch)) return false;  
      node = node.children.get(ch);  
    }  
    return node.isEnd;  
  }  
  
  startsWith(prefix) {  
    let node = this.root;  
    for (const ch of prefix) {  
      if (!node.children.has(ch)) return false;  
      node = node.children.get(ch);  
    }  
    return true;  
  }  
}
```

**Complexity:**

* Insert/Search: O(L), where L = word length.
* Space: O(N × L), for N words of average length L.

## Anagram / Frequency Signature

**When to use:**

* Grouping words with the same letters.
* Detecting anagram substrings inside a string.

**Approach:**

1. For each word, compute a **signature** (sorted string or frequency count).
2. Use this signature as the key in a hashmap.
3. Group all words with the same signature together.

**JavaScript Example Group Anagrams:**

```
function groupAnagrams(strs) {  
  const map = new Map();  
  for (const s of strs) {  
    const key = s.split('').sort().join('');  
    if (!map.has(key)) map.set(key, []);  
    map.get(key).push(s);  
  }  
  return Array.from(map.values());  
}
```

**Complexity:**

* Time: O(n \* m log m), n = number of words, m = average word length (sorting).
* Space: O(n \* m), for storing grouped anagrams.

## Final Thoughts

If you look carefully, most string problems are **not unique** they’re variations of these **4 repeatable patterns**:

1. **Sliding Window / Two Pointers** → substrings with constraints.
2. **KMP / Prefix Function / Z-Algorithm** → efficient pattern searching.
3. **Trie / Prefix Tree** → prefix-based word queries.
4. **Anagram / Frequency Signature** → grouping or detecting anagrams.

Once you recognize which pattern applies, the problem becomes straightforward.

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!