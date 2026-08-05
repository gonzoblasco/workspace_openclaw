import { useState } from 'react';
import { useQuery } from '@apollo/client/react';
import { GET_CHAT } from './apollo/queries/getChat.js';
import { useAddMessageMutation } from './apollo/mutations/addMessage.js';

function Chat({ chatId, closeChat }) {
  const [text, setText] = useState('');
  const { loading, error, data } = useQuery(GET_CHAT, {
    variables: { chatId },
  });

  const [addMessage] = useAddMessageMutation();

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && text.length) {
      addMessage({ variables: { message: { text, chatId } } }).then(() => {
        setText('');
      });
    }
  };

  if (loading) return <div className="chatWindow"><p>Loading...</p></div>;
  if (error) return <div className="chatWindow"><p>{error.message}</p></div>;

  const { chat } = data;

  return (
    <div className="chatWindow">
      <div className="header">
        <span>{chat.users[1]?.username || 'Chat'}</span>
        <button onClick={() => closeChat(chatId)} className="close">X</button>
      </div>
      <div className="messages">
        {chat.messages.map((message) => (
          <div
            key={'message' + message.id}
            className={'message ' + (message.user.id > 1 ? 'left' : 'right')}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div className="input">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyPress}
        />
      </div>
    </div>
  );
}

export default Chat;
