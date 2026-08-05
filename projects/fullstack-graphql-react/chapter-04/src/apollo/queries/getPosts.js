import { gql } from '@apollo/client';
import { useQuery } from '@apollo/client/react';
import { USER_ATTRIBUTES } from '../fragments/userAttributes.js';

export const GET_POSTS = gql`
  query postsFeed($page: Int, $limit: Int, $username: String) {
    postsFeed(page: $page, limit: $limit, username: $username) {
      posts {
        id
        text
        user {
          ...userAttributes
        }
      }
    }
  }
  ${USER_ATTRIBUTES}
`;

export const useGetPostsQuery = (variables) =>
  useQuery(GET_POSTS, {
    pollInterval: 5000,
    variables: { page: 0, limit: 10, ...variables },
  });
