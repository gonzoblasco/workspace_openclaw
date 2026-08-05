import { gql } from '@apollo/client';
import { useQuery } from '@apollo/client/react';
import { USER_ATTRIBUTES } from '../../apollo/fragments/userAttributes.js';

export const GET_USER = gql`
  query user($username: String!) {
    user(username: $username) {
      ...userAttributes
    }
  }
  ${USER_ATTRIBUTES}
`;

export const useGetUserQuery = (variables) =>
  useQuery(GET_USER, { variables: { ...variables } });
