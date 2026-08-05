import { useState } from 'react';
import AvatarModal from '../AvatarModal.jsx';

export default function UserBar({ user }) {
  const [isOpen, setIsOpen] = useState(false);

  const showModal = () => {
    setIsOpen(!isOpen);
  };

  if (!user) return null;

  return (
    <div className="user">
      <img src={user.avatar} onClick={() => showModal()} alt={user.username} />
      <AvatarModal isOpen={isOpen} showModal={showModal} />
      <span>{user.username}</span>
    </div>
  );
}
