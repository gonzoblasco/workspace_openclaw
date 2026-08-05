import { gql } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

export const LOGOUT = gql`
  mutation logout {
    logout {
      success
    }
  }
`;

export const useLogoutMutation = () => useMutation(LOGOUT);
