import { ApolloClient, InMemoryCache, from, HttpLink } from '@apollo/client';
import { onError } from '@apollo/client/link/error';

export default function createSsrClient(req, loggedIn) {
  const AuthLink = (operation, next) => {
    if (loggedIn) {
      const token = req.cookies?.get?.('authorization', { signed: true });
      if (token) {
        operation.setContext((context) => ({
          ...context,
          headers: {
            ...context.headers,
            Authorization: `Bearer ${token}`,
          },
        }));
      }
    }
    return next(operation);
  };

  const client = new ApolloClient({
    ssrMode: true,
    link: from([
      onError(({ graphQLErrors, networkError }) => {
        if (graphQLErrors) {
          graphQLErrors.forEach(({ message, locations, path }) =>
            console.log(`[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`),
          );
        }
        if (networkError) {
          console.log(`[Network error]: ${networkError}`);
        }
      }),
      AuthLink,
      new HttpLink({
        uri: 'http://localhost:8000/graphql',
        credentials: 'same-origin',
      }),
    ]),
    cache: new InMemoryCache(),
  });

  return client;
}
