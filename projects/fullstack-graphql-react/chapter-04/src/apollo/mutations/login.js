import { gql } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

export const LOGIN = gql`
  mutation login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      token
    }
  }
`;

export const useLoginMutation = () => useMutation(LOGIN);
