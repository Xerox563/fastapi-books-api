from fastapi import FastAPI
from pydantic import BaseModel
from search_engine import SemanticSearchEngine

app = FastAPI(title="Resume Semantic Search")

# Initialize engine
engine = SemanticSearchEngine()
engine.embed_resumes()

class SearchQuery(BaseModel):
    """Search request"""
    query: str
    top_k: int = 3

class SearchResult(BaseModel):
    """Search result"""
    candidate: str
    similarity: float
    content: str

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Resume Semantic Search Engine",
        "endpoints": {
            "search": "POST /search",
            "search_by_keywords": "POST /search/keywords",
            "search_by_role": "POST /search/role"
        }
    }

@app.post("/search")
def search(query: SearchQuery):
    """
    WHY: REST endpoint for semantic search
    HOW: Accept query, return ranked matches
    RESULT: JSON with top matches
    """
    results = engine.search(query.query, query.top_k)
    return {
        "query": query.query,
        "results": results
    }

@app.post("/search/keywords")
def search_keywords(keywords: list[str], top_k: int = 3):
    """Search by specific keywords"""
    results = engine.search_by_keywords(keywords, top_k)
    return {
        "keywords": keywords,
        "results": results
    }

@app.post("/search/role")
def search_role(role: str, top_k: int = 3):
    """Search candidates for a role"""
    results = engine.search_by_role(role, top_k)
    return {
        "role": role,
        "results": results
    }

# Run with:
# uvicorn api:app --reload