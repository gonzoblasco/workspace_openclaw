import logger from '../../helpers/logger.js';
import { db, users, posts, chats, messages, userChats, eq, desc } from '../../database.js';

const resolvers = {
  Post: {
    user(post) {
      return db.select().from(users).where(eq(users.id, post.userId)).get();
    },
  },
  Message: {
    user(message) {
      return db.select().from(users).where(eq(users.id, message.userId)).get();
    },
    chat(message) {
      return db.select().from(chats).where(eq(chats.id, message.chatId)).get();
    },
  },
  Chat: {
    messages(chat) {
      return db.select().from(messages).where(eq(messages.chatId, chat.id)).orderBy(desc(messages.id)).all();
    },
    users(chat) {
      return db.select({
        id: users.id,
        avatar: users.avatar,
        username: users.username,
      }).from(userChats)
        .innerJoin(users, eq(users.id, userChats.userId))
        .where(eq(userChats.chatId, chat.id))
        .all();
    },
  },
  RootQuery: {
    posts() {
      return db.select().from(posts).orderBy(desc(posts.createdAt)).all();
    },
    chats() {
      const firstUser = db.select().from(users).limit(1).all();
      if (!firstUser.length) return [];

      return db.select().from(chats)
        .innerJoin(userChats, eq(userChats.chatId, chats.id))
        .where(eq(userChats.userId, firstUser[0].id))
        .all()
        .map((row) => row.chats);
    },
    chat(root, { chatId }) {
      return db.select().from(chats).where(eq(chats.id, chatId)).get();
    },
  },
  RootMutation: {
    addPost(root, { post }) {
      const firstUser = db.select().from(users).limit(1).all();
      if (!firstUser.length) throw new Error('No users found');

      const newPost = db.insert(posts).values({
        text: post.text,
        userId: firstUser[0].id,
      }).returning().get();

      logger.log({ level: 'info', message: 'Post was created' });
      return newPost;
    },
    addChat(root, { chat }) {
      const newChat = db.insert(chats).values({}).returning().get();

      if (chat.users) {
        for (const userId of chat.users) {
          db.insert(userChats).values({ userId, chatId: newChat.id }).run();
        }
      }

      logger.log({ level: 'info', message: 'Chat was created' });
      return newChat;
    },
    addMessage(root, { message }) {
      const firstUser = db.select().from(users).limit(1).all();
      if (!firstUser.length) throw new Error('No users found');

      const newMessage = db.insert(messages).values({
        text: message.text,
        userId: firstUser[0].id,
        chatId: message.chatId,
      }).returning().get();

      logger.log({ level: 'info', message: 'Message was created' });
      return newMessage;
    },
  },
};

export default resolvers;
