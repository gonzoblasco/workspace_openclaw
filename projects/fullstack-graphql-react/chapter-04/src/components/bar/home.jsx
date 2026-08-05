import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  const goHome = () => {
    navigate('/app');
  };

  return (
    <button className="goHome" onClick={goHome}>
      Home
    </button>
  );
}
