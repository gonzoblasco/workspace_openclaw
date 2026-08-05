import SearchBar from './search.jsx';
import Logout from './logout.jsx';
import Home from './home.jsx';
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
          <Home />
          <Logout changeLoginState={changeLoginState} />
        </div>
      </div>
    </div>
  );
}
