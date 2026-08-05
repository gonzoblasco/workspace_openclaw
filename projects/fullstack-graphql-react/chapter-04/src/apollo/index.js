import { ApolloClient, InMemoryCache, from, split } from '@apollo/client';
import { onError } from '@apollo/client/link/error';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';
import { getMainDefinition } from '@apollo/client/utilities';
import UploadHttpLink from 'apollo-upload-client/UploadHttpLink.mjs';

const AuthLink = (operation, next) => {
  const token = localStorage.getItem('jwt');
  if (token) {
    operation.setContext((context) => ({
      ...context,
      headers: {
        ...context.headers,
        Authorization: `Bearer ${token}`,
      },
    }));
  }
  return next(operation);
};

// WebSocket link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:8000/subscriptions',
    connectionParams: () => {
      const token = localStorage.getItem('jwt');
      if (token) {
        return { authToken: token };
      }
      return {};
    },
  }),
);

// HTTP link for queries and mutations
const httpLink = new UploadHttpLink({
  uri: 'http://localhost:8000/graphql',
  credentials: 'same-origin',
});

// Split: send subscriptions via WS, everything else via HTTP
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink,
);

// Restore SSR cache if available
const initialState = typeof window !== 'undefined' ? window.__APOLLO_STATE__ : undefined;

const client = new ApolloClient({
  link: from([
    onError(({ graphQLErrors, networkError }) => {
      if (graphQLErrors) {
        graphQLErrors.forEach(({ message, locations, path, extensions }) => {
          if (extensions?.code === 'UNAUTHENTICATED') {
            localStorage.removeItem('jwt');
            client.clearStore();
          }
          console.log(
            `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
          );
        });
      }
      if (networkError) {
        console.log(`[Network error]: ${networkError}`);
      }
    }),
    AuthLink,
    splitLink,
  ]),
  cache: new InMemoryCache().restore(initialState),
});

export default client;
