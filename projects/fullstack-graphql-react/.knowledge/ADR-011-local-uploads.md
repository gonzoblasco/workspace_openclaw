# ADR-011: Local File Uploads Instead of AWS S3

**Status:** Accepted
**Date:** 2026-08-05
**Source:** Full-Stack Web Development with GraphQL and React (2nd Ed.), Chapter 7
**Scope:** Project

## Context

The book uses AWS S3 for image storage, requiring an AWS account, S3 bucket, and IAM access keys. This adds friction and cost for development.

## Decision

Use local file storage (`uploads/` directory) instead of AWS S3 for development. The GraphQL API and client code remain identical — only the storage backend changes.

## Rationale

- Same GraphQL API: `uploadAvatar(file: Upload!): File` mutation works identically
- Same client code: `apollo-upload-client` handles multipart requests
- Same file handling: `createReadStream`, `filename`, `mimetype`, `encoding`
- Zero cost and zero setup for development
- Easy to swap to S3 for production by changing the resolver

## Changes from Book

| Book (AWS S3) | Local Storage | Reason |
|---|---|---|
| `aws-sdk` + S3 bucket | `fs.createWriteStream` to `uploads/` | No AWS account needed |
| `s3.upload(params).promise()` | `fs.createWriteStream().pipe()` | Same stream-based approach |
| `response.Location` (S3 URL) | `/uploads/filename` (local URL) | Different URL format |
| `ACL: 'public-read'` | Not needed | Local files are served by Express static |
| `graphql-upload` | `graphql-upload-ts` | TypeScript version, maintained |

## Migration to S3

To switch to AWS S3 for production:
1. Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
2. Replace the `uploadAvatar` resolver with the S3 version
3. Update the bucket name and region
4. The GraphQL schema and client code don't change

## ADRs Created
- ADR-011: Local File Uploads Instead of AWS S3
