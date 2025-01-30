import React, { useState } from "react";
import axios from "axios";
import Message from "./Message";
import ChatInput from "./ChatInput";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [ragMethod, setRagMethod] = useState("simple_rag"); // Default RAG method

  const handleSendMessage = async (message) => {
    setMessages([...messages, { text: message, sender: "user" }]);

    try {
      const response = await axios.post(`http://localhost:8000/${ragMethod}/response/`, {
        question: message,
      });

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.answer, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error getting response from server.", sender: "bot" },
      ]);
    }
  };

  return (
    <div className="chat-content">
      {/* Dropdown to Select RAG Technique */}
      <div>
        <label>Select RAG Technique: </label>
        <select value={ragMethod} onChange={(e) => setRagMethod(e.target.value)}>
          <option value="simple_rag">Simple RAG</option>
          <option value="bm25_rag">BM25 RAG</option>
          <option value="hybrid_rag">Hybrid RAG</option>
        </select>
      </div>

      {/* Messages Display */}
      <div className="messages">
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
      </div>

      {/* Chat Input */}
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
}

export default ChatWindow;
