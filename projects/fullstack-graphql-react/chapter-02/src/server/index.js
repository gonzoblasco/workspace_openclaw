import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import services from './services/index.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.join(__dirname, '../../');

const app = express();

// Security headers (production only to allow GraphQL playground in dev)
if (process.env.NODE_ENV === 'production') {
  app.use(helmet());
  app.use(
    helmet.contentSecurityPolicy({
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', '*.amazonaws.com'],
      },
    }),
  );
  app.use(helmet.referrerPolicy({ policy: 'same-origin' }));
}

// Compression
app.use(compression());

// CORS
app.use(cors());

// Static files
app.use('/', express.static(path.join(root, 'dist/client')));
app.use('/uploads', express.static(path.join(root, 'uploads')));

// Bind services
const serviceNames = Object.keys(services);
for (let i = 0; i < serviceNames.length; i += 1) {
  const name = serviceNames[i];
  if (name === 'graphql') {
    const { server, expressMiddleware } = services[name];
    await server.start();
    app.use('/graphql', express.json(), expressMiddleware(server, {
      context: async ({ req }) => ({ req }),
    }));
  } else {
    app.use(`/${name}`, services[name]);
  }
}

// Fallback: serve index.html for SPA routing
app.use((req, res) => {
  res.sendFile(path.join(root, 'dist/client/index.html'));
});

app.listen(8000, () => console.log('Listening on port 8000!'));
