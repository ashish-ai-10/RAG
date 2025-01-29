import React, { useState } from 'react';
import axios from 'axios';
import Message from './Message';
import ChatInput from './ChatInput';

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const handleSendMessage = async (message) => {
    setMessages([...messages, { text: message, sender: 'user' }]);

    try {
      const response = await axios.post("http://localhost:8000/response/", { question: message });
      setMessages(prevMessages => [
        ...prevMessages,
        { text: response.data.answer, sender: 'bot' }
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages(prevMessages => [
        ...prevMessages,
        { text: "Error getting response from server.", sender: 'bot' }
      ]);
    }
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