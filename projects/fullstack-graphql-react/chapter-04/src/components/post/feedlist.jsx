import { useState } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './index.jsx';

export default function FeedList({ fetchMore, posts }) {
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);

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

  return (
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
  );
}
