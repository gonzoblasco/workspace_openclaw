#!/usr/bin/env node
// OSS PR Tracker - fetches all open PRs by gonzoblasco across repos
// Output: JSON with PR data for the OpenClaw app dashboard

const { execSync } = require("child_process");

// Repos where we contribute: PRs we opened plus repos where we do review work.
const REPOS = [
  "facebook/astryx",
  "radix-ui/primitives",
  "colinhacks/zod",
  "shadcn-ui/ui",
  "carbon-design-system/carbon",
  "carbon-design-system/ibm-products",
  "payloadcms/payload",
];

function gh(args) {
  try {
    const result = execSync(`gh ${args} 2>/dev/null`, {
      encoding: "utf-8",
      timeout: 30000,
      maxBuffer: 1024 * 1024 * 10,
    });
    return result.trim();
  } catch (e) {
    return null;
  }
}

function fetchPRs(repo) {
  const raw = gh(
    `pr list --author gonzoblasco --repo "${repo}" --state open --json number,title,reviewDecision,mergeStateStatus,comments,url,updatedAt,additions,deletions,changedFiles --limit 20`
  );
  if (!raw) return [];
  try {
    const prs = JSON.parse(raw);
    return prs.map((pr) => ({
      repo,
      number: pr.number,
      title: pr.title,
      url: pr.url,
      reviewDecision: pr.reviewDecision || "NONE",
      mergeStateStatus: pr.mergeStateStatus || "UNKNOWN",
      comments: Array.isArray(pr.comments) ? pr.comments.length : 0,
      updatedAt: pr.updatedAt,
      additions: pr.additions || 0,
      deletions: pr.deletions || 0,
      changedFiles: pr.changedFiles || 0,
    }));
  } catch (e) {
    return [];
  }
}

function fetchLastComment(repo, number) {
  const raw = gh(
    `pr view ${number} --repo "${repo}" --json comments 2>/dev/null`
  );
  if (!raw) return null;
  try {
    const data = JSON.parse(raw);
    const comments = data.comments || [];
    if (comments.length === 0) return null;
    const last = comments[comments.length - 1];
    return {
      author: last.author?.login || "unknown",
      createdAt: last.createdAt,
      body: last.body?.slice(0, 200) || "",
    };
  } catch (e) {
    return null;
  }
}

function fetchReviews(repo, number) {
  const raw = gh(
    `pr view ${number} --repo "${repo}" --json reviews 2>/dev/null`
  );
  if (!raw) return [];
  try {
    const data = JSON.parse(raw);
    return (data.reviews || []).map((r) => ({
      author: r.author?.login || "unknown",
      state: r.state,
      submittedAt: r.submittedAt,
    }));
  } catch (e) {
    return [];
  }
}

// Main
const allPRs = [];
const repoSummary = [];

for (const repo of REPOS) {
  const prs = fetchPRs(repo);
  for (const pr of prs) {
    const lastComment = fetchLastComment(repo, pr.number);
    const reviews = fetchReviews(repo, pr.number);
    const lastReview = reviews.length > 0 ? reviews[reviews.length - 1] : null;
    allPRs.push({
      ...pr,
      lastCommentAuthor: lastComment?.author || null,
      lastCommentDate: lastComment?.createdAt || null,
      lastCommentPreview: lastComment?.body || null,
      lastReviewAuthor: lastReview?.author || null,
      lastReviewState: lastReview?.state || null,
      lastReviewDate: lastReview?.submittedAt || null,
    });
  }
  repoSummary.push({
    repo,
    total: prs.length,
    approved: prs.filter((p) => p.reviewDecision === "APPROVED").length,
    changesRequested: prs.filter(
      (p) => p.reviewDecision === "CHANGES_REQUESTED"
    ).length,
    noReview: prs.filter(
      (p) =>
        p.reviewDecision === "NONE" ||
        p.reviewDecision === "REVIEW_REQUIRED" ||
        !p.reviewDecision
    ).length,
  });
}

// Classify actions
const actionable = allPRs.filter(
  (pr) =>
    pr.reviewDecision === "APPROVED" ||
    pr.reviewDecision === "CHANGES_REQUESTED" ||
    (pr.lastCommentAuthor && pr.lastCommentAuthor !== "gonzoblasco" && pr.lastCommentAuthor !== "vercel" && pr.lastCommentAuthor !== "github-actions")
);

const stalled = allPRs.filter((pr) => !actionable.includes(pr));

const output = {
  totalPRs: allPRs.length,
  totalApproved: repoSummary.reduce((s, r) => s + r.approved, 0),
  totalChangesRequested: repoSummary.reduce((s, r) => s + r.changesRequested, 0),
  totalNoReview: repoSummary.reduce((s, r) => s + r.noReview, 0),
  repos: repoSummary,
  prs: allPRs,
  actionable: actionable.map((p) => ({
    repo: p.repo,
    number: p.number,
    title: p.title,
    url: p.url,
    reviewDecision: p.reviewDecision,
    mergeStateStatus: p.mergeStateStatus,
    lastCommentAuthor: p.lastCommentAuthor,
    lastCommentDate: p.lastCommentDate,
    lastCommentPreview: p.lastCommentPreview,
    lastReviewAuthor: p.lastReviewAuthor,
    lastReviewState: p.lastReviewState,
    lastReviewDate: p.lastReviewDate,
    updatedAt: p.updatedAt,
  })),
  stalled: stalled.map((p) => ({
    repo: p.repo,
    number: p.number,
    title: p.title,
    url: p.url,
    reviewDecision: p.reviewDecision,
    mergeStateStatus: p.mergeStateStatus,
    updatedAt: p.updatedAt,
  })),
};

console.log(JSON.stringify(output, null, 0));