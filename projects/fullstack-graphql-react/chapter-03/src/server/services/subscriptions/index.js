import { makeExecutableSchema } from '@graphql-tools/schema';
import { useServer } from 'graphql-ws/use/ws';
import { WebSocketServer } from 'ws';
import { execute, subscribe } from 'graphql';
import JWT from 'jsonwebtoken';
import Resolvers from '../graphql/resolvers.js';
import Schema from '../graphql/schema.js';
import authDirective from '../graphql/auth.js';
import { db, users, eq } from '../../database.js';

const { JWT_SECRET } = process.env;

export default (utils) => (server) => {
  const { authDirectiveTypeDefs, authDirectiveTransformer } = authDirective('auth');

  let executableSchema = makeExecutableSchema({
    typeDefs: [authDirectiveTypeDefs, Schema],
    resolvers: Resolvers,
  });

  executableSchema = authDirectiveTransformer(executableSchema);

  const wsServer = new WebSocketServer({
    server,
    path: '/subscriptions',
  });

  useServer(
    {
      schema: executableSchema,
      execute,
      subscribe,
      onConnect: async (ctx) => {
        const authToken = ctx.connectionParams?.authToken;
        if (authToken) {
          try {
            const result = JWT.verify(authToken, JWT_SECRET);
            const user = db.select().from(users).where(eq(users.id, result.id)).get();
            ctx.user = user;
            return true;
          } catch {
            throw new Error('Invalid auth token');
          }
        }
        throw new Error('Missing auth token');
      },
      context: async (ctx) => {
        return { user: ctx.user };
      },
    },
    wsServer,
  );

  console.log('WebSocket server ready at ws://localhost:8000/subscriptions');
};
