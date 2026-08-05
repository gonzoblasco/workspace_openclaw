import { useState } from 'react';
import { useQuery } from '@apollo/client/react';
import { GET_POSTS } from './apollo/queries/getPosts.js';
import { useAddPostMutation } from './apollo/mutations/addPost.js';
import FeedList from './components/post/feedlist.jsx';
import Loading from './components/Loading.jsx';
import ErrorMessage from './components/ErrorMessage.jsx';

function Feed() {
  const [postContent, setPostContent] = useState('');

  const { loading, error, data, fetchMore } = useQuery(GET_POSTS, {
    pollInterval: 5000,
    variables: { page: 0, limit: 10 },
  });

  const [addPost] = useAddPostMutation(postContent);

  const handleSubmit = (event) => {
    event.preventDefault();
    addPost({ variables: { post: { text: postContent } } });
    setPostContent('');
  };

  if (loading) return <Loading />;
  if (error) return <ErrorMessage><p>{error.message}</p></ErrorMessage>;

  const { postsFeed } = data;
  const { posts } = postsFeed;

  return (
    <div>
      <div className="postForm">
        <form onSubmit={handleSubmit}>
          <textarea
            value={postContent}
            onChange={(e) => setPostContent(e.target.value)}
            placeholder="Write your custom post!"
          />
          <input type="submit" value="Submit" />
        </form>
      </div>
      <FeedList posts={posts} fetchMore={fetchMore} />
    </div>
  );
}

export default Feed;
