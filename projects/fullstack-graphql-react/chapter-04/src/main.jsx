import Feed from './Feed.jsx';
import Chats from './Chats.jsx';
import Bar from './components/bar/index.jsx';

export default function Main({ changeLoginState }) {
  return (
    <>
      <Bar changeLoginState={changeLoginState} />
      <div className="container">
        <Feed />
      </div>
      <Chats />
    </>
  );
}
