import React from 'react';

function Message({ text, sender, evalution }) {
  return (
    <div className={`message ${sender === 'user' ? 'user-message' : 'bot-message'}`}>
      {text}

      {/* Show evaluation metrics only for bot messages */}
      {sender === 'bot' && evalution && (
        <div>
          <p>Relevancy: {evalution.relevancy}</p>
          <p>Faithfulness: {evalution.Faithfulness}</p>
          <p>LLM Context Precision: {evalution["LLM Context Precision"]}</p>
        </div>
      )}
    </div>
  );
}

export default Message;
