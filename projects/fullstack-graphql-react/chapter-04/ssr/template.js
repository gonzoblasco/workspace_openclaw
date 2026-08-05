export default function htmlTemplate(content, head, initialState) {
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
    ${head?.title?.toString() || ''}
    ${head?.meta?.toString() || ''}
    <link rel="stylesheet" href="/node_modules/cropperjs/dist/cropper.css" />
  </head>
  <body>
    <div id="root">${content}</div>
    <script>window.__APOLLO_STATE__ = ${JSON.stringify(initialState).replace(/</g, '\\u003c')}</script>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>`;
}
