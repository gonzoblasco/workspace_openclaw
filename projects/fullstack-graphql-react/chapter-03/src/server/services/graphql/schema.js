const typeDefinitions = `
  directive @auth on QUERY | FIELD_DEFINITION | FIELD

  scalar Upload

  type User {
    id: Int
    avatar: String
    username: String
    email: String
  }

  type Post {
    id: Int
    text: String
    user: User
  }

  type PostFeed {
    posts: [Post]
  }

  type Message {
    id: Int
    text: String
    chat: Chat
    user: User
  }

  type Chat {
    id: Int
    messages: [Message]
    users: [User]
    lastMessage: Message
  }

  type Response {
    success: Boolean
  }

  type UsersSearch {
    users: [User]
  }

  type Auth {
    token: String
  }

  type File {
    filename: String!
    mimetype: String!
    encoding: String!
    url: String!
  }

  input PostInput {
    text: String!
  }

  input ChatInput {
    users: [Int]
  }

  input MessageInput {
    text: String!
    chatId: Int!
  }

  type RootQuery {
    posts: [Post]
    postsFeed(page: Int, limit: Int): PostFeed @auth
    chats: [Chat] @auth
    chat(chatId: Int): Chat @auth
    usersSearch(page: Int, limit: Int, text: String!): UsersSearch @auth
    currentUser: User @auth
  }

  type RootMutation {
    login(email: String!, password: String!): Auth
    signup(username: String!, email: String!, password: String!): Auth
    addPost(post: PostInput!): Post @auth
    deletePost(postId: Int!): Response @auth
    addChat(chat: ChatInput!): Chat @auth
    addMessage(message: MessageInput!): Message @auth
    uploadAvatar(file: Upload!): File @auth
  }

  schema {
    query: RootQuery
    mutation: RootMutation
  }
`;

export default [typeDefinitions];
