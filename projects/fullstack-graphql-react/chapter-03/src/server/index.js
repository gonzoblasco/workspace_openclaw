import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import JWT from 'jsonwebtoken';
import { graphqlUploadExpress } from 'graphql-upload-ts';
import services from './services/index.js';
import { db, users, eq } from './database.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.join(__dirname, '../../');

const { JWT_SECRET } = process.env;

const app = express();

// Security headers (production only)
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
    app.use('/graphql', graphqlUploadExpress({ maxFileSize: 10000000, maxFiles: 10 }), express.json(), expressMiddleware(server, {
      context: async ({ req }) => {
        const authorization = req.headers.authorization;
        if (authorization) {
          const token = authorization.replace(/Bearer\s+/ig, '').trim();
          try {
            const result = JWT.verify(token, JWT_SECRET);
            const user = db.select().from(users).where(eq(users.id, result.id)).get();
            return { ...req, user };
          } catch (err) {
            return req;
          }
        }
        return req;
      },
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
