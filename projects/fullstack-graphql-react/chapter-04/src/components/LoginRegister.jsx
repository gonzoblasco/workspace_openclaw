import { useState } from 'react';
import { useLoginMutation } from '../apollo/mutations/login.js';
import { useSignupMutation } from '../apollo/mutations/signup.js';
import Loading from './Loading.jsx';
import ErrorMessage from './ErrorMessage.jsx';

function LoginForm({ changeLoginState }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [login, { loading, error }] = useLoginMutation();

  const onSubmit = (event) => {
    event.preventDefault();
    login({
      update(cache, { data: { login } }) {
        if (login.token) {
          localStorage.setItem('jwt', login.token);
          changeLoginState(true);
        }
      },
      variables: { email, password },
    });
  };

  return (
    <div className="login">
      {!loading && (
        <form onSubmit={onSubmit}>
          <label>Email</label>
          <input type="text" onChange={(e) => setEmail(e.target.value)} />
          <label>Password</label>
          <input type="password" onChange={(e) => setPassword(e.target.value)} />
          <input type="submit" value="Login" />
        </form>
      )}
      {loading && <Loading />}
      {error && <ErrorMessage><p>There was an error logging in!</p></ErrorMessage>}
    </div>
  );
}

function RegisterForm({ changeLoginState }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [signup, { loading, error }] = useSignupMutation();

  const onSubmit = (event) => {
    event.preventDefault();
    signup({
      update(cache, { data: { signup } }) {
        if (signup.token) {
          localStorage.setItem('jwt', signup.token);
          changeLoginState(true);
        }
      },
      variables: { email, password, username },
    });
  };

  return (
    <div className="login">
      {!loading && (
        <form onSubmit={onSubmit}>
          <label>Email</label>
          <input type="text" onChange={(e) => setEmail(e.target.value)} />
          <label>Username</label>
          <input type="text" onChange={(e) => setUsername(e.target.value)} />
          <label>Password</label>
          <input type="password" onChange={(e) => setPassword(e.target.value)} />
          <input type="submit" value="Sign up" />
        </form>
      )}
      {loading && <Loading />}
      {error && <ErrorMessage><p>There was an error signing up!</p></ErrorMessage>}
    </div>
  );
}

function LoginRegisterForm({ changeLoginState }) {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <div className="authModal">
      {showLogin && (
        <div>
          <LoginForm changeLoginState={changeLoginState} />
          <a onClick={() => setShowLogin(false)}>Want to sign up? Click here</a>
        </div>
      )}
      {!showLogin && (
        <div>
          <RegisterForm changeLoginState={changeLoginState} />
          <a onClick={() => setShowLogin(true)}>Want to login? Click here</a>
        </div>
      )}
    </div>
  );
}

export default LoginRegisterForm;
