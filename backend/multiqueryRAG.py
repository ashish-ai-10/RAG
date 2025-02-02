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

from langchain_core.output_parsers import BaseOutputParser

from pydantic import BaseModel, Field



load_dotenv()
multiquery_router = APIRouter()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.environ.get("GOOGLE_API_KEY"))

# Models
class QueryRequest(BaseModel):
    question: str
    query_transformation_option:str

class QueryResponse(BaseModel):
    answer: str


# Function for rewriting a query to improve retrieval
def rewrite_query(original_query):
    print("function called")
    query_rewrite_template = """You are an AI assistant tasked with reformulating user queries to improve retrieval in a RAG system. 
        Given the original query, rewrite it to be more specific, detailed, and likely to retrieve relevant information.

        Original query: {original_query}

        Rewritten query:"""
    

    query_rewriter = PromptTemplate(input_variables=["original_query"],template=query_rewrite_template) | llm
    response = query_rewriter.invoke(original_query)
    print("new query",response)
    return response.content

def generate_step_back_query(original_query):
    
    step_back_template = """You are an AI assistant tasked with generating broader, more general queries to improve context retrieval in a RAG system.
        Given the original query, generate a step-back query that is more general and can help retrieve relevant background information.

        Original query: {original_query}

        Step-back query:"""
    
    setback_generator = PromptTemplate(input_variables=["original_query"],template=step_back_template) | llm
    response = setback_generator.invoke(original_query)
    print("new setback query",response)
    return response.content


# Output parser will split the LLM result into a list of queries
class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines

output_parser = LineListOutputParser()

def decompose_query(question,retriver):

    
    subquery_decomposition_template = """You are an AI assistant tasked with breaking down complex queries into simpler sub-queries for a RAG system.
    Given the original query, decompose it into 2-4 simpler sub-queries that, when answered together, would provide a comprehensive response to the original query.

    Original query: {question}

    example: What are the impacts of climate change on the environment?

    Sub-queries:
    1. What are the impacts of climate change on biodiversity?
    2. How does climate change affect the oceans?
    3. What are the effects of climate change on agriculture?
    4. What are the impacts of climate change on human health?
     
    Provide these alternative questions separated by newlines.
    
    """

    suqueries_generator_chain = PromptTemplate(input_variables=["question"],template=subquery_decomposition_template) | llm | output_parser

    multiquery_retriver = MultiQueryRetriever(
    retriever=retriver, llm_chain=suqueries_generator_chain, parser_key="lines"
    )  # "lines" is the key (attribute name) of the parsed output

    return multiquery_retriver
def docs2str(docs):
        return "\n\n".join(doc.page_content for doc in docs)

@multiquery_router.post("/response/")
async def generate_response(query: QueryRequest):
    """
    API to retrieve relevant documents and generate a response based on the user's question.
    """
    vector_store = get_vector_store()
    if vector_store is None:
        return JSONResponse(content={"error": "Knowledge base not created. Please upload a PDF first."}, status_code=400)

    new_query=""
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    Answer: """

    prompt = ChatPromptTemplate.from_template(template)

    # Retrieve relevant documents
    if(query.query_transformation_option=="Query Rewriting"):
        new_query=rewrite_query(query.question)
        
    elif(query.query_transformation_option=="Step-back Prompting"):
        new_query=generate_step_back_query(query.question)

    else:
        multiquery_retriver=decompose_query(query.question,retriever)
        
        multiquery_retriver_chain=(
        {"context": multiquery_retriver | docs2str, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        response=multiquery_retriver_chain.invoke(query.question)
        return QueryResponse(answer=response)



       


   


  
    

    rag_chain = (
        {"context": retriever | docs2str, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


    
    response = rag_chain.invoke(new_query)
    
    return  QueryResponse(answer=response)