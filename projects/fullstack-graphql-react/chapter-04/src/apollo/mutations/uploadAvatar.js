import { gql } from '@apollo/client';
import { useMutation } from '@apollo/client/react';

export const UPLOAD_AVATAR = gql`
  mutation uploadAvatar($file: Upload!) {
    uploadAvatar(file: $file) {
      filename
      url
    }
  }
`;

export const getUploadAvatarConfig = () => ({
  update(cache, { data: { uploadAvatar } }) {
    if (uploadAvatar?.url) {
      cache.modify({
        fields: {
          currentUser(user) {
            cache.modify({
              id: user,
              fields: {
                avatar() {
                  return uploadAvatar.url;
                },
              },
            });
          },
        },
      });
    }
  },
});

export const useUploadAvatarMutation = () =>
  useMutation(UPLOAD_AVATAR, getUploadAvatarConfig());
