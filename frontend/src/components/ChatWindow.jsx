import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Message from "./Message";
import ChatInput from "./ChatInput";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [ragMethod, setRagMethod] = useState("simple_rag"); // Default RAG method
  const [queryTransformationOption, setQueryTransformationOption] = useState("");
  const messagesEndRef = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (message) => {
    setMessages([...messages, { text: message, sender: "user" }]);

    try {
      const response = await axios.post(`http://localhost:8000/${ragMethod}/response/`, {
        question: message,
        query_transformation_option: queryTransformationOption, // Pass selected option if Query Transformation RAG is selected
      });

      // Handle the response (single string response expected now)
      if (response.data.answer) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: response.data.answer, sender: "bot" },
        ]);
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Unexpected response from server.", sender: "bot" },
        ]);
      }
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error getting response from server.", sender: "bot" },
      ]);
    }
  };

  return (
    <div className="chat-content" style={{ display: "flex", flexDirection: "column", height: "100vh", overflowY: "auto" }}>
      {/* Dropdown to Select RAG Technique */}
      <div>
        <label>Select RAG Technique: </label>
        <select value={ragMethod} onChange={(e) => setRagMethod(e.target.value)}>
          <option value="simple_rag">Simple RAG</option>
          <option value="query_transformation_rag">Query Transformation RAG</option>
          <option value="re-ranking_rag">Re-Ranking RAG</option>
        </select>
      </div>

      {/* Show additional options for Query Transformation RAG */}
      {ragMethod === "query_transformation_rag" && (
        <div style={{ marginTop: "10px" }}>
          <label>Select Query Transformation Technique: </label>
          <div>
            <input
              type="radio"
              id="technique1"
              name="queryTransformation"  
              value="Query Rewriting"
              checked={queryTransformationOption === "Query Rewriting"}
              onChange={(e) => setQueryTransformationOption(e.target.value)}
            />
            <label htmlFor="technique1">Query Rewriting</label>
          </div>
          <div>
            <input
              type="radio"
              id="technique2"
              name="queryTransformation"  
              value="Step-back Prompting"
              checked={queryTransformationOption === "Step-back Prompting"}
              onChange={(e) => setQueryTransformationOption(e.target.value)}
            />
            <label htmlFor="technique2">Step-back Prompting</label>
          </div>
          <div>
            <input
              type="radio"
              id="technique3"
              name="queryTransformation"  
              value="Sub-query Decomposition"
              checked={queryTransformationOption === "Sub-query Decomposition"}
              onChange={(e) => setQueryTransformationOption(e.target.value)}
            />
            <label htmlFor="technique3">Sub-query Decomposition</label>
          </div>
        </div>
      )}

      {/* Messages Display */}
      <div className="messages" style={{ flex: 1, overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Chat Input */}
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
}

export default ChatWindow;
