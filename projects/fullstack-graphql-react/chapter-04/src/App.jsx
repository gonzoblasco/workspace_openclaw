import { Helmet, HelmetProvider } from 'react-helmet-async';
import Feed from './Feed.jsx';
import Chats from './Chats.jsx';
import Bar from './components/bar/index.jsx';
import { UserProvider } from './context/user.jsx';
import './components/fontawesome.js';

function App() {
  return (
    <HelmetProvider>
      <Helmet>
        <title>Graphbook - Feed</title>
        <meta name="description" content="Newsfeed of all your friends on Graphbook" />
      </Helmet>

      <UserProvider>
        <Bar />
        <div className="container">
          <Feed />
        </div>
        <Chats />
      </UserProvider>
    </HelmetProvider>
  );
}

export default App;
