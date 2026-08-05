import { asc, like, or, eq } from 'drizzle-orm';
import bcrypt from 'bcrypt';
import JWT from 'jsonwebtoken';
import { GraphQLUpload } from 'graphql-upload-ts';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import logger from '../../helpers/logger.js';
import { db, users, posts, chats, messages, userChats, desc } from '../../database.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const uploadsDir = path.join(__dirname, '../../../../uploads');

// Ensure uploads directory exists
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

const { JWT_SECRET } = process.env;

const resolvers = {
  Upload: GraphQLUpload,

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
    chats(root, args, context) {
      if (!context.user) return [];
      return db.select().from(chats)
        .innerJoin(userChats, eq(userChats.chatId, chats.id))
        .where(eq(userChats.userId, context.user.id))
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
    currentUser(root, args, context) {
      return context.user;
    },
  },
  RootMutation: {
    login(root, { email, password }) {
      const user = db.select().from(users).where(eq(users.email, email)).get();
      if (!user) {
        throw new Error('User not found');
      }
      const passwordValid = bcrypt.compareSync(password, user.password);
      if (!passwordValid) {
        throw new Error('Password does not match');
      }
      const token = JWT.sign({ email, id: user.id }, JWT_SECRET, {
        expiresIn: '1d',
      });
      return { token };
    },
    signup(root, { email, password, username }) {
      const existing = db.select().from(users)
        .where(or(eq(users.email, email), eq(users.username, username)))
        .all();
      if (existing.length) {
        throw new Error('User already exists');
      }
      const hash = bcrypt.hashSync(password, 10);
      const newUser = db.insert(users).values({
        email,
        password: hash,
        username,
        avatar: '/uploads/avatar1.png',
      }).returning().get();

      const token = JWT.sign({ email, id: newUser.id }, JWT_SECRET, {
        expiresIn: '1d',
      });
      return { token };
    },
    addPost(root, { post }, context) {
      if (!context.user) throw new Error('Not authenticated');
      const newPost = db.insert(posts).values({
        text: post.text,
        userId: context.user.id,
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
    addChat(root, { chat }, context) {
      if (!context.user) throw new Error('Not authenticated');
      const newChat = db.insert(chats).values({}).returning().get();
      // Add the current user to the chat
      db.insert(userChats).values({ userId: context.user.id, chatId: newChat.id }).run();
      if (chat.users) {
        for (const userId of chat.users) {
          if (userId !== context.user.id) {
            db.insert(userChats).values({ userId, chatId: newChat.id }).run();
          }
        }
      }
      logger.log({ level: 'info', message: 'Chat was created' });
      return newChat;
    },
    addMessage(root, { message }, context) {
      if (!context.user) throw new Error('Not authenticated');
      const newMessage = db.insert(messages).values({
        text: message.text,
        userId: context.user.id,
        chatId: message.chatId,
      }).returning().get();
      logger.log({ level: 'info', message: 'Message was created' });
      return newMessage;
    },
    async uploadAvatar(root, { file }, context) {
      if (!context.user) throw new Error('Not authenticated');
      const { createReadStream, filename, mimetype, encoding } = await file;

      // Save file locally
      const uniqueName = `${Date.now()}-${filename}`;
      const filePath = path.join(uploadsDir, uniqueName);
      const writeStream = fs.createWriteStream(filePath);
      await new Promise((resolve, reject) => {
        createReadStream()
          .pipe(writeStream)
          .on('finish', resolve)
          .on('error', reject);
      });

      const url = `/uploads/${uniqueName}`;

      // Update user avatar
      db.update(users)
        .set({ avatar: url })
        .where(eq(users.id, context.user.id))
        .run();

      logger.log({ level: 'info', message: 'Avatar uploaded for user ' + context.user.id });
      return { filename, mimetype, encoding, url };
    },
  },
};

export default resolvers;
