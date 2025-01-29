from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for the knowledge base
vector_store = None
llm = None
embeddings = None

# Models for API requests and responses
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# Initialize LLM and embeddings
def setup_models():
    global llm, embeddings
    llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key="gemini-api-key")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="gemini-api-key")

# Load PDF and split it into chunks
import tempfile

def load_pdf(uploaded_file):
    """Save the uploaded file temporarily and then process it with PyPDFLoader."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.file.read())  # Save file content
        temp_file_path = temp_file.name  # Get the temp file path

    # Load PDF using the valid file path
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)


# Create vector store
def setup_vectorstore(embeddings, all_splits):
    return FAISS.from_documents(all_splits, embeddings)

@app.post("/knowledge_base/")
async def create_knowledge_base(file: UploadFile = File(...)):
    try:
        global vector_store
        setup_models()

        all_splits = load_pdf(file)  # Use the corrected function
        vector_store = setup_vectorstore(embeddings, all_splits)

        return JSONResponse(content={"message": "Knowledge base created successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/response/")
async def generate_response(query: QueryRequest):
    """
        API to retrieve relevant documents and generate a response based on the user's question.
    """
    if vector_store is None:
        return {"error": "Knowledge base not created. Please upload a PDF first."}

    # Retrieve documents
    retrieved_docs = vector_store.similarity_search(query.question)

    # Generate a response
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    # Ensure we pass a valid string to the LLM
    prompt_text = f"Question: {query.question}\n\nContext: {docs_content}\n\nAnswer:"

    response = llm.invoke(prompt_text)  # ✅ Pass a valid string

    return QueryResponse(answer=response.content)