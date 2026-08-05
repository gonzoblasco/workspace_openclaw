import { gql } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

export const ADD_MESSAGE = gql`
  mutation addMessage($message: MessageInput!) {
    addMessage(message: $message) {
      id
      text
      user {
        id
      }
    }
  }
`;

export const getAddMessageConfig = () => ({
  update(cache, { data: { addMessage } }) {
    cache.modify({
      fields: {
        messages(existingMessages = []) {
          const newMessageRef = cache.writeFragment({
            data: addMessage,
            fragment: gql`
              fragment NewMessage on Chat {
                id
                type
              }
            `,
          });
          return [...existingMessages, newMessageRef];
        },
      },
    });
  },
});

export const useAddMessageMutation = () =>
  useMutation(ADD_MESSAGE, getAddMessageConfig());
