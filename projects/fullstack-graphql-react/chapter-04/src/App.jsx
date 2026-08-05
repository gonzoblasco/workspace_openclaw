import { Helmet, HelmetProvider } from 'react-helmet-async';
import Feed from './Feed.jsx';
import Chats from './Chats.jsx';

function App() {
  return (
    <HelmetProvider>
      <Helmet>
        <title>Graphbook - Feed</title>
        <meta name="description" content="Newsfeed of all your friends on Graphbook" />
      </Helmet>

      <div className="container">
        <Feed />
      </div>
      <Chats />
    </HelmetProvider>
  );
}

export default App;
