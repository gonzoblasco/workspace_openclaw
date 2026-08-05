import { ApolloClient, InMemoryCache, from } from '@apollo/client';
import { onError } from '@apollo/client/link/error';
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
    new UploadHttpLink({
      uri: 'http://localhost:8000/graphql',
      credentials: 'same-origin',
    }),
  ]),
  cache: new InMemoryCache().restore(initialState),
});

export default client;
