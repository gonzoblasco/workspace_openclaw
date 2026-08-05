import { gql } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

export const SIGNUP = gql`
  mutation signup($email: String!, $password: String!, $username: String!) {
    signup(email: $email, password: $password, username: $username) {
      token
    }
  }
`;

export const useSignupMutation = () => useMutation(SIGNUP);
