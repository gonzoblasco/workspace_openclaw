import SearchBar from './search.jsx';
import Logout from './logout.jsx';

export default function Bar({ changeLoginState }) {
  return (
    <div className="topbar">
      <div className="inner">
        <SearchBar />
        <div className="buttons">
          <Logout changeLoginState={changeLoginState} />
        </div>
      </div>
    </div>
  );
}
