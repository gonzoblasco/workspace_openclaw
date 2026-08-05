import SearchBar from './search.jsx';
import Logout from './logout.jsx';
import UserBar from './user.jsx';
import { UserConsumer } from '../../context/user.jsx';

export default function Bar({ changeLoginState }) {
  return (
    <div className="topbar">
      <div className="inner">
        <SearchBar />
        <UserConsumer>
          <UserBar />
        </UserConsumer>
        <div className="buttons">
          <Logout changeLoginState={changeLoginState} />
        </div>
      </div>
    </div>
  );
}
