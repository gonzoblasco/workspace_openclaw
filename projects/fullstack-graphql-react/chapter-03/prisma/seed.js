import { PrismaClient } from '../src/generated/client.ts';
import { PrismaBetterSqlite3 } from '@prisma/adapter-better-sqlite3';
import Database from 'better-sqlite3';

const connection = new Database('./prisma/dev.db');
const adapter = new PrismaBetterSqlite3(connection);
const prisma = new PrismaClient({ adapter });

async function main() {
  // Create users
  const user1 = await prisma.user.create({
    data: {
      avatar: '/uploads/avatar1.png',
      username: 'Test User',
    },
  });

  const user2 = await prisma.user.create({
    data: {
      avatar: '/uploads/avatar2.png',
      username: 'Test User 2',
    },
  });

  // Create posts
  await prisma.post.create({
    data: {
      text: 'Lorem ipsum 1',
      userId: user1.id,
    },
  });

  await prisma.post.create({
    data: {
      text: 'Lorem ipsum 2',
      userId: user2.id,
    },
  });

  // Create a chat
  const chat = await prisma.chat.create({
    data: {},
  });

  // Associate users with the chat (many-to-many)
  await prisma.userChat.create({
    data: { userId: user1.id, chatId: chat.id },
  });
  await prisma.userChat.create({
    data: { userId: user2.id, chatId: chat.id },
  });

  // Create messages in the chat
  await prisma.message.create({
    data: {
      text: 'This is a test message.',
      userId: user1.id,
      chatId: chat.id,
    },
  });

  await prisma.message.create({
    data: {
      text: 'This is a second test message.',
      userId: user2.id,
      chatId: chat.id,
    },
  });

  console.log('Seed data inserted successfully');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
