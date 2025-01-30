from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import tempfile

router = APIRouter()

# Global variables (shared across RAG techniques)
vector_store = None
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyAWkIlKzsQCnXXE-RnN3FQ345CxinN3CsM")

def load_pdf(uploaded_file):
    """Save the uploaded file temporarily and process it with PyPDFLoader."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.file.read())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)

def setup_vectorstore(all_splits):
    """Creates a FAISS vector store from document splits."""
    return FAISS.from_documents(all_splits, embeddings)

@router.post("/knowledge_base/")
async def create_knowledge_base(file: UploadFile = File(...)):
    """
    Uploads a PDF, processes it into a vector store, and makes it available for retrieval.
    """
    try:
        global vector_store
        all_splits = load_pdf(file)
        vector_store = setup_vectorstore(all_splits)
        return JSONResponse(content={"message": "Knowledge base created successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def get_vector_store():
    """Provides access to the shared vector store for different RAG techniques."""
    return vector_store
