# RAG-Powered PDF Chatbot

A chatbot that enables users to upload a PDF and query its contents using different Retrieval-Augmented Generation (RAG) techniques. This implementation starts with a simple RAG method, utilizing a vector store created with the **Gemini embedding model**, and is built using **LangChain**, **FastAPI**, and **React**.

## Features

- Upload PDFs and convert them into a searchable vector store.
- Query the document using **RAG with Gemini embeddings**.
- Fast and scalable backend powered by **FastAPI**.
- Interactive frontend built with **React**.
- Extendable to support multiple retrieval techniques with different LLMs

## Tech Stack

- **Backend:** FastAPI, LangChain, Gemini Embeddings, Gemini LLM
- **Frontend:** React
- **Vector Store:** FAISS 
- **File Handling:** PyPDF

## Installation

### Prerequisites

- Python 3.8+
- Node.js & npm

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/ashish-ai-10/RAG.git
   cd RAG/backend
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```sh
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```sh
   cd ../frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```

## Usage

1. Open the web app in your browser.
2. Upload a PDF file.
3. Enter a query to extract information from the document.
4. The chatbot retrieves and generates relevant responses using the RAG pipeline.

## Future Enhancements

- Implement additional retrieval techniques like Multiquery RAG, Document Re-Ranking, Graph RAG etc
- Optimize chunking strategies for better retrieval accuracy.
- Deploy as a cloud-hosted service (e.g., AWS, Vercel, or Render).

## Contributing

Feel free to fork this repository and submit pull requests!

## License

MIT License

