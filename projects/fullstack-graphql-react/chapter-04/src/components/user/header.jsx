export default function UserProfileHeader({ user }) {
  const { avatar, username } = user;

  return (
    <div className="profileHeader">
      <div className="avatar">
        <img src={avatar} alt={username} />
      </div>
      <div className="information">
        <p>{username}</p>
        <p>
          You can provide further information here and build your really personal
          header component for your users.
        </p>
      </div>
    </div>
  );
}
