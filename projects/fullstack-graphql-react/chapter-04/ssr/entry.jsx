import React from 'react';
import { ApolloProvider } from '@apollo/client/react';
import { StaticRouter } from 'react-router-dom/server.js';
import { RoutesConfig } from '../src/router.jsx';

export default function ServerApp({ client, location, context, loggedIn }) {
  return (
    <ApolloProvider client={client}>
      <StaticRouter location={location} context={context}>
        <RoutesConfig loggedIn={loggedIn} changeLoginState={() => {}} />
      </StaticRouter>
    </ApolloProvider>
  );
}
