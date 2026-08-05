import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginRegisterForm from './components/LoginRegister.jsx';
import Main from './Main.jsx';
import User from './User.jsx';

function PrivateRoute({ children, loggedIn }) {
  const location = useLocation();
  if (!loggedIn) {
    return <Navigate to="/" state={{ from: location }} replace />;
  }
  return children;
}

function LoginRoute({ children, loggedIn }) {
  const location = useLocation();
  if (loggedIn) {
    const from = location.state?.from?.pathname || '/app';
    return <Navigate to={from} replace />;
  }
  return children;
}

export default function Router({ loggedIn, changeLoginState }) {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <LoginRoute loggedIn={loggedIn}>
              <LoginRegisterForm changeLoginState={changeLoginState} />
            </LoginRoute>
          }
        />
        <Route
          path="/app"
          element={
            <PrivateRoute loggedIn={loggedIn}>
              <Main changeLoginState={changeLoginState} />
            </PrivateRoute>
          }
        />
        <Route
          path="/user/:username"
          element={
            <PrivateRoute loggedIn={loggedIn}>
              <User changeLoginState={changeLoginState} />
            </PrivateRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
