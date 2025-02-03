from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from create_knowledge_base import get_vector_store
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from typing import List

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from langchain_core.output_parsers import BaseOutputParser

from pydantic import BaseModel, Field



load_dotenv()
rerank_router = APIRouter()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get("GOOGLE_API_KEY"))
cross_encoder_model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
# Models
class QueryRequest(BaseModel):
    question: str
    

class QueryResponse(BaseModel):
    answer: str

def docs2str(docs):
        return "\n\n".join(doc.page_content for doc in docs)

@rerank_router.post("/response/")
async def generate_response(query: QueryRequest):
    """
    API to retrieve relevant documents and generate a response based on the user's question.
    """
    vector_store = get_vector_store()
    if vector_store is None:
        return JSONResponse(content={"error": "Knowledge base not created. Please upload a PDF first."}, status_code=400)

   
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template)


    # Initialize the model
    

    # Select the top 3 documents
    compressor = CrossEncoderReranker(model=cross_encoder_model, top_n=3)

    # Initialize the contextual compression retriever
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )



    rag_chain = (
        {"context": compression_retriever | docs2str, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


    
    response = rag_chain.invoke(query.question)
    
    return  QueryResponse(answer=response)