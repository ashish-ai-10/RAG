import React, { useState } from 'react';
import axios from 'axios';

function FileUpload({ onUpload }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a file first.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", selectedFile);
  
    try {
      const response = await axios.post("http://localhost:8000/common/knowledge_base/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
  
      console.log("API Response:", response.data); // Debugging
      alert(response.data.message || "File uploaded successfully!");
  
      onUpload(); // Notify parent component (App.js) that upload is complete
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to create knowledge base.");
    }
  };  

  return (
    <div>
      <h2>File Upload</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default FileUpload;