import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { users, posts, chats, messages, userChats } from '../../drizzle/schema.js';
import { eq, desc } from 'drizzle-orm';

const sqlite = new Database('./drizzle/dev.db');
const db = drizzle(sqlite);

export { db, users, posts, chats, messages, userChats, eq, desc };
