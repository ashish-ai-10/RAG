import React, { useState } from 'react';

function ChatInput({ onSend }) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      onSend(inputValue);
      setInputValue('');
    }
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default ChatInput;
