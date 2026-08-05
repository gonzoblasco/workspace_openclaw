import { useParams } from 'react-router-dom';
import Chats from './Chats.jsx';
import Bar from './components/bar/index.jsx';
import UserProfile from './components/user/index.jsx';

export default function User({ changeLoginState }) {
  const { username } = useParams();

  return (
    <>
      <Bar changeLoginState={changeLoginState} />
      <UserProfile username={username} />
      <Chats />
    </>
  );
}
