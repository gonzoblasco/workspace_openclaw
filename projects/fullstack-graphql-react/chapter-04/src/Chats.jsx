import { useState, useEffect } from 'react';
import { useQuery } from '@apollo/client/react';
import { GET_CHATS } from './apollo/queries/getChats.js';
import { MESSAGES_SUBSCRIPTION } from './apollo/subscriptions/messageAdded.js';
import { GET_CHAT } from './apollo/queries/getChat.js';
import { NEW_MESSAGE } from './apollo/mutations/addMessage.js';
import Chat from './Chat.jsx';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const usernamesToString = (users) => {
  const userList = users.slice(1);
  let usernamesString = '';
  for (let i = 0; i < userList.length; i++) {
    usernamesString += userList[i].username;
    if (i - 1 === userList.length) {
      usernamesString += ', ';
    }
  }
  return usernamesString;
};

const shorten = (text) => {
  if (text.length > 12) {
    return text.substring(0, text.length - 9) + '...';
  }
  return text;
};

function Chats() {
  const [openChats, setOpenChats] = useState([]);
  const { loading, error, data, subscribeToMore } = useQuery(GET_CHATS);

  // Subscribe to new messages
  useEffect(() => {
    subscribeToMore({
      document: MESSAGES_SUBSCRIPTION,
      updateQuery: (prev, { subscriptionData }) => {
        if (!subscriptionData.data) return prev;
        const newMessage = subscriptionData.data.messageAdded;
        if (!prev.chats || !prev.chats.length) return prev;

        const index = prev.chats.findIndex((c) => c.id === newMessage.chat.id);
        if (index === -1) return prev;

        const newChats = [...prev.chats];
        newChats[index] = {
          ...newChats[index],
          lastMessage: { text: newMessage.text, __typename: 'Message' },
        };

        return { chats: newChats, __typename: 'Query' };
      },
    });
  }, [subscribeToMore]);

  const openChat = (id) => {
    const openChatsTemp = openChats.slice();
    if (openChatsTemp.indexOf(id) === -1) {
      if (openChatsTemp.length > 2) {
        openChatsTemp.splice(0, openChatsTemp.length - 1);
      }
      openChatsTemp.push(id);
    }
    setOpenChats(openChatsTemp);
  };

  const closeChat = (id) => {
    const openChatsTemp = openChats.slice();
    const index = openChatsTemp.indexOf(id);
    openChatsTemp.splice(index, 1);
    setOpenChats(openChatsTemp);
  };

  if (loading) return <div className="chats"><p>Loading...</p></div>;
  if (error) return <div className="chats"><p>{error.message}</p></div>;

  const { chats } = data;

  return (
    <div className="wrapper">
      <ToastContainer />
      <div className="chats">
        {chats.map((chat) => (
          <div
            key={'chat' + chat.id}
            className="chat"
            onClick={() => openChat(chat.id)}
          >
            <div className="header">
              <img
                src={
                  chat.users.length > 2
                    ? '/public/group.png'
                    : chat.users[1]?.avatar
                }
                alt=""
              />
              <div>
                <h2>{shorten(usernamesToString(chat.users))}</h2>
                <span>{chat.lastMessage?.text}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="openChats">
        {openChats.map((chatId) => (
          <Chat
            chatId={chatId}
            key={'chatWindow' + chatId}
            closeChat={closeChat}
          />
        ))}
      </div>
    </div>
  );
}

export default Chats;
