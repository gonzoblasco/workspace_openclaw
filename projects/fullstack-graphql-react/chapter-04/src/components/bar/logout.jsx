import { useApolloClient } from '@apollo/client/react';

export default function Logout({ changeLoginState }) {
  const client = useApolloClient();

  const logout = () => {
    localStorage.removeItem('jwt');
    changeLoginState(false);
    client.stop();
    client.resetStore();
  };

  return (
    <button className="logout" onClick={logout}>
      Logout
    </button>
  );
}
