import { useState, useEffect } from 'react';

export default function SearchList({ data: { usersSearch: { users } } }) {
  const [show, setShowList] = useState(false);

  useEffect(() => {
    if (users.length) {
      setShowList(true);
    } else {
      setShowList(false);
    }
  }, [users]);

  useEffect(() => {
    const handleClick = () => setShowList(false);
    if (show) {
      document.addEventListener('click', handleClick, true);
    }
    return () => {
      document.removeEventListener('click', handleClick, true);
    };
  }, [show]);

  if (!show) return null;

  return (
    <div className="result">
      {users.map((user) => (
        <div key={user.id} className="user">
          <img src={user.avatar} alt={user.username} />
          <span>{user.username}</span>
        </div>
      ))}
    </div>
  );
}
