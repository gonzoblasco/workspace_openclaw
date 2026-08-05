import { useState, useEffect } from 'react';
import { useApolloClient } from '@apollo/client/react';
import { Helmet, HelmetProvider } from 'react-helmet-async';
import { useCurrentUserQuery } from './apollo/queries/currentUserQuery.js';
import Router from './router.jsx';
import Loading from './components/Loading.jsx';
import { UserProvider } from './context/user.jsx';
import './components/fontawesome.js';

function App() {
  const client = useApolloClient();
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('jwt'));
  const { loading, refetch } = useCurrentUserQuery();

  const handleLogin = (status) => {
    refetch().then(() => {
      setLoggedIn(status);
    }).catch(() => {
      setLoggedIn(status);
    });
  };

  useEffect(() => {
    const unsubscribe = client.onClearStore(() => {
      if (loggedIn) {
        setLoggedIn(false);
      }
    });
    return () => {
      unsubscribe();
    };
  }, [client, loggedIn]);

  if (loading) return <Loading />;

  return (
    <HelmetProvider>
      <Helmet>
        <title>Graphbook - Feed</title>
        <meta name="description" content="Newsfeed of all your friends on Graphbook" />
      </Helmet>

      <UserProvider>
        <Router loggedIn={loggedIn} changeLoginState={handleLogin} />
      </UserProvider>
    </HelmetProvider>
  );
}

export default App;
