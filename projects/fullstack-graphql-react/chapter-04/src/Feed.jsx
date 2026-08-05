import { useState } from 'react';
import { useQuery } from '@apollo/client/react';
import InfiniteScroll from 'react-infinite-scroll-component';
import { GET_POSTS } from './apollo/queries/getPosts.js';
import { useAddPostMutation } from './apollo/mutations/addPost.js';
import Post from './components/post/index.jsx';
import Loading from './components/Loading.jsx';
import ErrorMessage from './components/ErrorMessage.jsx';

function Feed() {
  const [postContent, setPostContent] = useState('');
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);

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

  const loadMore = (fetchMoreFn) => {
    fetchMoreFn({
      variables: {
        page: page + 1,
      },
      updateQuery(previousResult, { fetchMoreResult }) {
        if (!fetchMoreResult.postsFeed.posts.length) {
          setHasMore(false);
          return previousResult;
        }
        setPage(page + 1);
        return {
          postsFeed: {
            __typename: 'PostFeed',
            posts: [
              ...previousResult.postsFeed.posts,
              ...fetchMoreResult.postsFeed.posts,
            ],
          },
        };
      },
    });
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

      <div className="feed">
        <InfiniteScroll
          dataLength={posts.length}
          next={() => loadMore(fetchMore)}
          hasMore={hasMore}
          loader={<div className="loader" key="loader">Loading ...</div>}
        >
          {posts.map((post) => (
            <Post key={post.id} post={post} />
          ))}
        </InfiniteScroll>
      </div>
    </div>
  );
}

export default Feed;
