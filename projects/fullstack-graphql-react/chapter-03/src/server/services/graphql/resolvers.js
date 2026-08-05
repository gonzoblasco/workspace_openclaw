import { asc, like, or } from 'drizzle-orm';
import logger from '../../helpers/logger.js';
import { db, users, posts, chats, messages, userChats, eq, desc } from '../../database.js';

const resolvers = {
  Post: {
    user(post) {
      return db.select().from(users).where(eq(users.id, post.userId)).get();
    },
  },
  PostFeed: {
    posts(postFeed) {
      return postFeed.posts;
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
      return db.select().from(messages).where(eq(messages.chatId, chat.id)).orderBy(asc(messages.id)).all();
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
    lastMessage(chat) {
      const msgs = db.select().from(messages)
        .where(eq(messages.chatId, chat.id))
        .orderBy(desc(messages.id))
        .limit(1)
        .all();
      return msgs[0] || null;
    },
  },
  RootQuery: {
    posts() {
      return db.select().from(posts).orderBy(desc(posts.createdAt)).all();
    },
    postsFeed(root, { page, limit }) {
      const skip = page && limit ? page * limit : 0;
      const query = db.select().from(posts).orderBy(desc(posts.createdAt)).limit(limit).offset(skip);
      return {
        posts: query.all(),
      };
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
    usersSearch(root, { page, limit, text }) {
      if (text.length < 3) {
        return { users: [] };
      }
      const skip = page && limit ? page * limit : 0;
      const result = db.select()
        .from(users)
        .where(like(users.username, `%${text}%`))
        .orderBy(desc(users.createdAt))
        .limit(limit)
        .offset(skip)
        .all();
      return { users: result };
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
    deletePost(root, { postId }) {
      const result = db.delete(posts).where(eq(posts.id, postId)).run();
      const success = result.changes === 1;
      if (success) {
        logger.log({ level: 'info', message: 'Post ' + postId + ' was deleted' });
      }
      return { success };
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
