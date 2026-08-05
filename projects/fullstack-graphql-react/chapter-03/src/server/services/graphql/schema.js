const typeDefinitions = `
  type User {
    id: Int
    avatar: String
    username: String
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
    postsFeed(page: Int, limit: Int): PostFeed
    chats: [Chat]
    chat(chatId: Int): Chat
    usersSearch(page: Int, limit: Int, text: String!): UsersSearch
  }

  type RootMutation {
    addPost(post: PostInput!): Post
    deletePost(postId: Int!): Response
    addChat(chat: ChatInput!): Chat
    addMessage(message: MessageInput!): Message
  }

  schema {
    query: RootQuery
    mutation: RootMutation
  }
`;

export default [typeDefinitions];
