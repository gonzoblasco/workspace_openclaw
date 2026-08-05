import { gql } from '@apollo/client';
import { useSubscription } from '@apollo/client/react';

export const MESSAGES_SUBSCRIPTION = gql`
  subscription onMessageAdded {
    messageAdded {
      id
      text
      chat {
        id
      }
      user {
        id
      }
    }
  }
`;

export const useMessageAddedSubscription = (options) =>
  useSubscription(MESSAGES_SUBSCRIPTION, options);
