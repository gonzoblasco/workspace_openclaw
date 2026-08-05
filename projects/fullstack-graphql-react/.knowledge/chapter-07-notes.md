# Chapter 7: Handling Image Uploads

## Core Concepts

1. **Upload scalar:** GraphQL `Upload` type for file transfer
2. **Multipart requests:** Files sent as `FormData` instead of JSON
3. **Stream-based uploads:** `createReadStream` for efficient file handling
4. **Image cropping:** `react-cropper` for client-side crop before upload
5. **Dropzone:** `react-dropzone` for drag-and-drop file selection
6. **Modal dialogs:** `react-modal` for overlay components
7. **Cache update:** Update Apollo cache after avatar upload

## Key Changes from Book

| Book (AWS S3) | Local Storage | Reason |
|---|---|---|
| `aws-sdk` + S3 bucket | `fs.createWriteStream` to `uploads/` | No AWS account needed |
| `graphql-upload` | `graphql-upload-ts` | TypeScript version, maintained |
| `apollo-upload-client` (old API) | `apollo-upload-client` v20 `UploadHttpLink` | Newer API |
| `createUploadLink` | `new UploadHttpLink({...})` | API change in v20 |

## Upload Flow

```
1. User clicks avatar → AvatarModal opens
2. User drops/selects image → react-dropzone
3. Image displayed in Cropper.js → user crops
4. User clicks Save → dataURI converted to Blob
5. Blob sent via uploadAvatar mutation (multipart FormData)
6. Server receives file via graphql-upload-ts
7. File saved to uploads/ directory
8. User avatar URL updated in database
9. Apollo cache updated → UI reflects new avatar
```

## Backend Changes (chapter-03)

- Added `Upload` scalar to GraphQL schema
- Added `File` type (`filename`, `mimetype`, `encoding`, `url`)
- Added `uploadAvatar(file: Upload!): File @auth` mutation
- Added `graphql-upload-ts` middleware for multipart parsing
- Files saved to `uploads/` directory with unique names

## Frontend Changes (chapter-04)

- Added `apollo-upload-client` v20 with `UploadHttpLink`
- Added `react-modal`, `react-dropzone`, `react-cropper`
- `AvatarModal` component with crop + upload
- `UserBar` component with click-to-upload avatar
- Cache update on successful upload

## Running

```bash
# Terminal 1: Backend
cd projects/fullstack-graphql-react/chapter-03
JWT_SECRET="***" npm run server

# Terminal 2: Frontend
cd projects/fullstack-graphql-react/chapter-04
npm run dev
```

Login with `test1@example.com` / `123456789`, then click your avatar to upload.
