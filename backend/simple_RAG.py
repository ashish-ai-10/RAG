from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from create_knowledge_base import get_vector_store
import os
from dotenv import load_dotenv
from evaluateRAG import evalute_rag_ragas
load_dotenv()
router = APIRouter()


# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get("GOOGLE_API_KEY"))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.environ.get("GOOGLE_API_KEY"))

# Models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    rag_evalution:dict

@router.post("/response/")
async def generate_response(query: QueryRequest):
    """
    API to retrieve relevant documents and generate a response based on the user's question.
    """
    vector_store = get_vector_store()
    if vector_store is None:
        return JSONResponse(content={"error": "Knowledge base not created. Please upload a PDF first."}, status_code=400)

    contexts=[]
    # Retrieve relevant documents
    retrieved_docs = vector_store.similarity_search(query.question)
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
   
    # Generate a response
    prompt_text = f"Question: {query.question}\n\nContext: {docs_content}\n\nAnswer:"
    response = llm.invoke(prompt_text)

    rag_data={
        "query":query.question,
        "relevant_docs":docs_content,
        "response":response.content
    }
    rag_evalution_result=await evalute_rag_ragas(rag_data,llm,embeddings)
    print("###############")


    return QueryResponse(answer=response.content,rag_evalution=rag_evalution_result)
