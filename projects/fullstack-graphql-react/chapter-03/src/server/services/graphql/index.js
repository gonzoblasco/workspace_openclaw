import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@as-integrations/express5';
import { makeExecutableSchema } from '@graphql-tools/schema';
import JWT from 'jsonwebtoken';
import Resolvers from './resolvers.js';
import Schema from './schema.js';
import authDirective from './auth.js';

const { JWT_SECRET } = process.env;

const { authDirectiveTypeDefs, authDirectiveTransformer } = authDirective('auth');

let executableSchema = makeExecutableSchema({
  typeDefs: [authDirectiveTypeDefs, Schema],
  resolvers: Resolvers,
});

executableSchema = authDirectiveTransformer(executableSchema);

const server = new ApolloServer({
  schema: executableSchema,
});

export { server, expressMiddleware, JWT_SECRET };
