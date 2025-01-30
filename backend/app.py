from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from create_knowledge_base import router as common_router
from simple_RAG import router as simple_rag_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the knowledge base router (common for all RAG techniques)
app.include_router(common_router, prefix="/common")

# Include specific RAG technique routers
app.include_router(simple_rag_router, prefix="/simple_rag")
