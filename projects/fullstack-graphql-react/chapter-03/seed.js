import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { users, posts, chats, messages, userChats } from './drizzle/schema.js';

const sqlite = new Database('./drizzle/dev.db');
const db = drizzle(sqlite);

// Create users
const user1 = db.insert(users).values({
  avatar: '/uploads/avatar1.png',
  username: 'Test User',
}).returning().get();

const user2 = db.insert(users).values({
  avatar: '/uploads/avatar2.png',
  username: 'Test User 2',
}).returning().get();

// Create posts
db.insert(posts).values([
  { text: 'Lorem ipsum 1', userId: user1.id },
  { text: 'Lorem ipsum 2', userId: user2.id },
]).run();

// Create a chat
const chat = db.insert(chats).values({}).returning().get();

// Associate users with the chat
db.insert(userChats).values([
  { userId: user1.id, chatId: chat.id },
  { userId: user2.id, chatId: chat.id },
]).run();

// Create messages
db.insert(messages).values([
  { text: 'This is a test message.', userId: user1.id, chatId: chat.id },
  { text: 'This is a second test message.', userId: user2.id, chatId: chat.id },
]).run();

console.log('Seed data inserted successfully');
