import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_neo4j import Neo4jGraph

app = FastAPI(title="Hybrid RAG Backend")

# Initialize environment variables or defaults
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Initialize Chroma vector store safely using correct parameters
vector_store = Chroma(
    collection_name="hybrid_rag_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Initialize Neo4j graph connection safely
try:
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USER, password=NEO4J_PASSWORD)
except Exception as e:
    graph = None

class ChatRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join("data", file.filename)
        
        # Save the uploaded file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # TODO: Add your PDF text extraction and vector embedding logic here 
        # (e.g., load PDF, split text, and add to vector_store)
        
        return {"filename": file.filename, "message": "File uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        query = request.question
        
        # Example retrieval from vector store
        docs = vector_store.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # Simple response generation using ChatOpenAI
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
        response_text = llm.invoke(f"Context:\n{context}\n\nQuestion: {query}").content

        return {"answer": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "Backend is running successfully"}