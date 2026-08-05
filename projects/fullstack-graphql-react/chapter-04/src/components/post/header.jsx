import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Dropdown from '../Dropdown.jsx';
import { useDeletePostMutation } from '../../apollo/mutations/deletePost.js';

export default function PostHeader({ post }) {
  const [deletePost] = useDeletePostMutation(post.id);

  return (
    <div className="header">
      <img src={post.user.avatar} alt={post.user.username} />
      <div>
        <h2>{post.user.username}</h2>
      </div>
      <Dropdown trigger={<FontAwesomeIcon icon="angle-down" />}>
        <button onClick={() => deletePost({ variables: { postId: post.id } })}>
          Delete
        </button>
      </Dropdown>
    </div>
  );
}
