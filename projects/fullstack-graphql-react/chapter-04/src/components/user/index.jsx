import { useGetPostsQuery } from '../../apollo/queries/getPosts.js';
import { useGetUserQuery } from '../../apollo/queries/getUser.js';
import FeedList from '../post/feedlist.jsx';
import UserHeader from './header.jsx';
import Loading from '../Loading.jsx';
import ErrorMessage from '../ErrorMessage.jsx';

export default function UserProfile({ username }) {
  const { data: userData, loading: userLoading } = useGetUserQuery({ username });
  const { loading, error, data: postsData, fetchMore } = useGetPostsQuery({ username });

  if (loading || userLoading) return <Loading />;
  if (error) return <ErrorMessage><p>{error.message}</p></ErrorMessage>;

  return (
    <div className="user">
      <div className="inner">
        <UserHeader user={userData.user} />
      </div>
      <div className="container">
        <FeedList posts={postsData.postsFeed.posts} fetchMore={fetchMore} />
      </div>
    </div>
  );
}
