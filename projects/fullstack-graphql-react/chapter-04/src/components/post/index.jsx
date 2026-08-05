import PostHeader from './header.jsx';
import PostContent from './content.jsx';

export default function Post({ post }) {
  return (
    <div className={'post' + (post.id < 0 ? ' optimistic' : '')}>
      <PostHeader post={post} />
      <PostContent post={post} />
    </div>
  );
}
