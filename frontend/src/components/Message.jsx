import React from 'react';

function Message({ text, sender }) {
  return (
    <div className={`message ${sender === 'user' ? 'user-message' : 'bot-message'}`}>
      {text}
    </div>
  );
}

export default Message;
