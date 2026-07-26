---
name: github
description: "GitHub operations: PRs, issues, comments, reviews, CI checks, and API queries via gh CLI."
metadata:
  category: "Development"
  tags:
    - github
    - prs
    - issues
    - ci
    - reviews
---

# GitHub

Use `gh` for GitHub. Use `git` for local commits/branches/push/pull. Use code-reading tools for deep reviews.

## Writing Rules

- **Always use regular hyphen (-), never em dash (—).** The em dash isn't on a standard keyboard and makes it obvious the text wasn't written by a developer. This applies to PR descriptions, comments, issues, and any GitHub-facing text.

## Auth

```bash
gh auth status
gh auth login
```

## PRs

```bash
gh pr list --repo owner/repo --json number,title,state,author,url
gh pr view 55 --repo owner/repo --json title,body,author,files,commits,reviews,reviewDecision
gh pr checks 55 --repo owner/repo
gh pr diff 55 --repo owner/repo
gh pr create --repo owner/repo --title "feat: title" --body-file /tmp/pr.md
gh pr merge 55 --repo owner/repo --squash
```

URLs work directly: `gh pr view https://github.com/owner/repo/pull/55`.

## Issues

```bash
gh issue list --repo owner/repo --state open --json number,title,labels,url
gh issue view 42 --repo owner/repo --json title,body,comments,labels,state
gh issue create --repo owner/repo --title "Bug: ..." --body-file /tmp/issue.md
gh issue comment 42 --repo owner/repo --body-file /tmp/comment.md
gh issue close 42 --repo owner/repo --comment "Fixed in ..."
```

## CI / Runs

```bash
gh run list --repo owner/repo --limit 10
gh run view <run-id> --repo owner/repo --json status,conclusion,headSha,url
gh run view <run-id> --repo owner/repo --log-failed
gh run rerun <run-id> --repo owner/repo --failed
```

## API

```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
gh api repos/owner/repo/labels --jq '.[].name'
gh api --cache 1h repos/owner/repo --jq '{stars: .stargazers_count, forks: .forks_count}'
```

Use `--json` + `--jq` for structured output. Use `--body-file` for comments/bodies containing backticks, shell snippets, env names, or user text.

## Comments & Reviews

```bash
# Post a comment
gh api repos/owner/repo/issues/42/comments -f body="Your comment here"

# Get all comments on an issue/PR
gh api repos/owner/repo/issues/42/comments --paginate

# Get a specific comment by ID
gh api repos/owner/repo/issues/comments/<comment-id>

# Reply to a review
gh api repos/owner/repo/pulls/55/comments -f body="Thanks, fixed!" -f in_reply_to=<review-comment-id>
```

## Related

- [gh-issue-planner](../gh-issue-planner): For planning projects into GitHub Issues (epics -> stories -> subtasks). ONLY for personal repos.
