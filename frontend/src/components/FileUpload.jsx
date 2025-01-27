import React from 'react';

function FileUpload({ onUpload }) {
  return (
    <div>
      <h2>File Upload</h2>
      <input type="file" onChange={e => e.target.files.length > 0 && onUpload()} />
    </div>
  );
}

export default FileUpload;
