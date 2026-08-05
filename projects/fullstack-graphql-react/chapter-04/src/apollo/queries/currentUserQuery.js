import { gql } from '@apollo/client';
import { useQuery } from '@apollo/client/react';

export const GET_CURRENT_USER = gql`
  query currentUser {
    currentUser {
      id
      username
      avatar
    }
  }
`;

export const useCurrentUserQuery = (options) => useQuery(GET_CURRENT_USER, options);
