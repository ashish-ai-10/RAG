import React, { useState } from 'react';
import Message from './Message';
import ChatInput from './ChatInput'

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = (message) => {
    setMessages([...messages, { text: message, sender: 'user' }]);
    // Simulate a chatbot response
    setTimeout(() => {
      setMessages(prevMessages => [
        ...prevMessages,
        { text: 'This is a response from the chatbot.', sender: 'bot' }
      ]);
    }, 1000);
  };

  return (
    <div className="chat-content">
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
      </div>
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
}

export default ChatWindow;
