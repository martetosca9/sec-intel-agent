from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ingest import NewsIngestor
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

app = FastAPI(
    title="CyberThreat Intelligence API",
    description="API for scraping and searching cybersecurity news using RAG and local LLM",
    version="1.1.0"
)

# Initialize components
ingestor = NewsIngestor()
llm = OllamaLLM(model="llama3")

class SearchQuery(BaseModel):
    query: str
    k: Optional[int] = 3

class SearchResult(BaseModel):
    title: str
    source: str
    summary: str

class AnalysisResult(BaseModel):
    analysis: str
    sources: List[str]

@app.get("/")
async def root():
    return {"message": "Welcome to the CyberThreat Intelligence Hub API"}

@app.post("/ingest", status_code=201)
async def trigger_ingestion():
    """
    Triggers the scraper to fetch news and update the vector database.
    """
    try:
        ingestor.ingest()
        return {"status": "success", "message": "News ingested and vector database updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=List[SearchResult])
async def search_news(search_data: SearchQuery):
    """
    Searches the vector database for relevant security news.
    """
    try:
        results = ingestor.query(search_data.query)
        formatted_results = []
        for res in results:
            formatted_results.append(SearchResult(
                title=res.metadata.get("title", "No Title"),
                source=res.metadata.get("source", "No Source"),
                summary=res.page_content
            ))
        return formatted_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_threats(search_data: SearchQuery):
    """
    Retrieves relevant news and uses local Llama 3 to provide a summarized security analysis.
    """
    try:
        # 1. Get relevant context from Vector DB
        docs = ingestor.query(search_data.query)
        context = "\n\n".join([f"Source: {d.metadata['source']}\nContent: {d.page_content}" for d in docs])
        sources = [d.metadata['source'] for d in docs]

        if not docs:
            return AnalysisResult(analysis="No relevant news found to analyze.", sources=[])

        # 2. Prepare the prompt for Llama 3
        template = """
        You are a Senior Cyber Threat Intelligence Analyst. 
        Based on the following news snippets, provide a concise professional analysis.
        Focus on:
        - Key risks and vulnerabilities.
        - Potential impact for organizations.
        - One actionable recommendation.

        Answer in Spanish (español).

        CONTEXT:
        {context}

        QUESTION: {question}

        ANALYSIS:
        """
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
        # 3. Generate analysis using Ollama
        chain = prompt | llm
        response = chain.invoke({"context": context, "question": search_data.query})
        
        return AnalysisResult(analysis=response, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
