import { useApolloClient } from '@apollo/client/react';
import { useLogoutMutation } from '../../apollo/mutations/logout.js';

export default function Logout({ changeLoginState }) {
  const client = useApolloClient();
  const [logoutMutation] = useLogoutMutation();

  const logout = () => {
    logoutMutation().then(() => {
      localStorage.removeItem('jwt');
      changeLoginState(false);
      client.stop();
      client.resetStore();
    });
  };

  return (
    <button className="logout" onClick={logout}>
      Logout
    </button>
  );
}
