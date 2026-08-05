import { sqliteTable, text, integer, unique, index } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  avatar: text('avatar'),
  username: text('username'),
  email: text('email'),
  password: text('password'),
  createdAt: text('created_at').notNull().default('CURRENT_TIMESTAMP'),
  updatedAt: text('updated_at').notNull().default('CURRENT_TIMESTAMP'),
});

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  text: text('text'),
  userId: integer('user_id').references(() => users.id, { onDelete: 'cascade' }),
  createdAt: text('created_at').notNull().default('CURRENT_TIMESTAMP'),
  updatedAt: text('updated_at').notNull().default('CURRENT_TIMESTAMP'),
});

export const chats = sqliteTable('chats', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  createdAt: text('created_at').notNull().default('CURRENT_TIMESTAMP'),
  updatedAt: text('updated_at').notNull().default('CURRENT_TIMESTAMP'),
});

export const messages = sqliteTable('messages', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  text: text('text'),
  userId: integer('user_id').references(() => users.id, { onDelete: 'set null' }),
  chatId: integer('chat_id').references(() => chats.id, { onDelete: 'cascade' }),
  createdAt: text('created_at').notNull().default('CURRENT_TIMESTAMP'),
  updatedAt: text('updated_at').notNull().default('CURRENT_TIMESTAMP'),
});

export const userChats = sqliteTable('user_chats', {
  userId: integer('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  chatId: integer('chat_id').notNull().references(() => chats.id, { onDelete: 'cascade' }),
  createdAt: text('created_at').notNull().default('CURRENT_TIMESTAMP'),
  updatedAt: text('updated_at').notNull().default('CURRENT_TIMESTAMP'),
}, (table) => ({
  pk: unique().on(table.userId, table.chatId),
  chatIdx: index('chat_idx').on(table.chatId),
}));
