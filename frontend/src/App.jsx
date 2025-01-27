import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [fileUploaded, setFileUploaded] = useState(false);

  const handleFileUpload = () => {
    setFileUploaded(true);
  };

  return (
    <div className="app-container dark-theme">
      <aside className="sidebar">
        <FileUpload onUpload={handleFileUpload} />
      </aside>
      <main className="chat-window">
        {fileUploaded ? <ChatWindow /> : <div className="upload-prompt">Please upload a file to start the conversation.</div>}
      </main>
    </div>
  );
}

export default App;
