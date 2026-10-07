---
name: "research-brief-protocol"
metadata:
  category: "Research"
  tags:
    - research
    - brief
    - evidence
    - citations
description: "Produce a cited research brief that separates observation, inference, and unknown, and makes stop criteria explicit before searching. Use when assigned a research question, a memory/knowledge task, or the study of source material - the deliverable of Kanam MIND."
user-invocable: true
---

# research-brief-protocol

The deliverable of Kanam MIND is not an answer. It is a **brief whose every claim is bounded by its evidence**. This skill fixes the shape of that brief so it cannot be faked.

## When to use it

- CORE or Gonzo assigns a research question.
- A knowledge or memory task needs a durable, cited artifact.
- Source material (a chapter, a doc, a repo) must be turned into learning.

## Hard rule

**Every sentence that asserts something must be traceable to a source that was opened, or marked as inference, or declared unknown.** No exceptions. A brief that is clean but ungrounded is worse than no brief: it launders a guess as a fact.

## The three labels are not decoration

Before searching, declare the **stop criterion**. While writing, tag every claim:

| Label | Meaning | Test |
|---|---|---|
| `[obs]` | Observation: seen in a source that was opened | Can point to file#line / URL + date |
| `[inf]` | Inference: concluded from observations, not stated | Name the observations it rests on |
| `[unk]` | Unknown: not established | State what evidence would settle it |

A claim with no label is a defect. `[inf]` presented as `[obs]` is the failure this skill exists to prevent.

## Protocol

### 1. Frame before searching
Write, in one line each:
- **Question** - what is actually being asked.
- **Stop criterion** - how we know the research is done.
- **Freshness** - does the datum change with time (price, version, PR state, date)?
- **Home** - the exact path where the artifact will live.
- **Sources** - which primary sources will be opened.

If any of these is empty, do not start searching.

### 2. Prefer primary sources
Repo, official doc, changelog - before a post that cites them. **Open the original before citing it.** Never present an unopened source as read.

### 3. Date the mutable
Anything that changes over time is checked with `web_fetch` at write time and stamped with the date observed.

### 4. Expose conflict, never flatten it
When sources disagree, record the disagreement and its impact on the conclusion. A smooth conclusion that hides a conflict is a defect.

### 5. Write the brief

```
# Brief: <question>
Stop criterion: <...> | Freshness: <...> | Written: <YYYY-MM-DD>

## Conclusion
<one paragraph, every claim labeled>

## Evidence
- [obs] <claim> - source: <path#line | URL> (opened <date>)
- [inf] <claim> - rests on: <the obs above>
- [unk] <question> - needs: <what would settle it>

## Conflicts
<source A says X; source B says Y; impact: ...>  (or "none found")

## Pending
<what remains unverified or awaits approval>
```

### 6. Verify before handoff
- Each citation actually supports the claim next to it.
- Each mutable datum carries its date.
- Each `[inf]` names its observations.
- Artifact is legible and complete at its declared home.

## What this skill refuses

- Presenting a source that was not opened.
- Promoting an `[inf]` to an `[obs]`.
- Hiding a source conflict.
- Emptying the field with an unlabeled sentence.

## Handoff

Return: exact artifact path, source links, conclusion, what was verified and how, and the significant uncertainty - with dates where freshness matters. Flag what remains pending verification or approval.
