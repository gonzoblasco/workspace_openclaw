import { StrictMode } from 'react';
import { hydrateRoot } from 'react-dom/client';
import { ApolloProvider } from '@apollo/client/react';
import App from './App.jsx';
import client from './apollo/index.js';
import './index.css';

hydrateRoot(
  document.getElementById('root'),
  <StrictMode>
    <ApolloProvider client={client}>
      <App />
    </ApolloProvider>
  </StrictMode>,
);
