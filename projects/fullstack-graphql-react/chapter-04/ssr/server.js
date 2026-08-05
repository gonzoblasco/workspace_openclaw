import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { createServer as createViteServer } from 'vite';
import Cookies from 'cookies';
import JWT from 'jsonwebtoken';
import { Helmet } from 'react-helmet-async';
import { renderToStringWithData } from '@apollo/client/react/ssr';
import React from 'react';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.join(__dirname, '..');

const { JWT_SECRET } = process.env;

async function createSsrServer() {
  const app = express();

  // Cookies middleware
  app.use((req, res, next) => {
    const options = { keys: ['graphbook-ssr-key'] };
    req.cookies = new Cookies(req, res, options);
    next();
  });

  // Create Vite dev server
  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'custom',
    root,
  });

  // Use Vite's connect middleware
  app.use(vite.middlewares);

  // Static files
  app.use('/uploads', express.static(path.join(root, 'uploads')));

  // SSR catch-all
  app.get('*', async (req, res) => {
    try {
      const token = req.cookies.get('authorization', { signed: true });
      let loggedIn = false;
      if (token) {
        try {
          JWT.verify(token, JWT_SECRET);
          loggedIn = true;
        } catch {
          loggedIn = false;
        }
      }

      // Load SSR entry via Vite
      const { default: createSsrClient } = await vite.ssrLoadModule('./ssr/apollo.js');
      const { default: ServerApp } = await vite.ssrLoadModule('./ssr/entry.jsx');
      const { default: htmlTemplate } = await vite.ssrLoadModule('./ssr/template.js');

      const client = createSsrClient(req, loggedIn);
      const context = {};

      const App = React.createElement(ServerApp, {
        client,
        location: req.url,
        context,
        loggedIn,
      });

      const content = await renderToStringWithData(App);

      if (context.url) {
        res.redirect(301, context.url);
        return;
      }

      const head = Helmet.renderStatic();
      const initialState = client.extract();

      res.status(200);
      res.send(htmlTemplate(content, head, initialState));
    } catch (e) {
      vite.ssrFixStacktrace(e);
      console.error(e);
      res.status(500).send('Internal Server Error');
    }
  });

  app.listen(3000, () => {
    console.log('SSR server listening on http://localhost:3000');
  });
}

createSsrServer();
