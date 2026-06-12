import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from scraper import SecurityScraper

class NewsIngestor:
    def __init__(self, db_path="./chroma_db"):
        self.db_path = db_path
        # Using a free, local embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
    def ingest(self):
        print("--- Starting ingestion process ---")
        scraper = SecurityScraper()
        news_items = scraper.fetch_news()
        
        if not news_items:
            print("No news found to ingest.")
            return

        documents = []
        for item in news_items:
            # Create a Document object for LangChain
            content = f"Title: {item['title']}\nSummary: {item['summary']}"
            metadata = {"source": item['link'], "title": item['title']}
            documents.append(Document(page_content=content, metadata=metadata))
        
        print(f"Creating vector database at {self.db_path} with {len(documents)} items...")
        
        # Create and persist the vector store
        vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.db_path
        )
        # In newer versions of Chroma/Langchain, persistence is automatic or handled on object deletion
        # but we can call persist() if using older versions or for clarity.
        # vector_db.persist() 
        
        print("--- Ingestion complete! ---")

    def query(self, text):
        """
        Simple method to test retrieval.
        """
        vector_db = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
        results = vector_db.similarity_search(text, k=3)
        return results

if __name__ == "__main__":
    ingestor = NewsIngestor()
    ingestor.ingest()
    
    # Quick test query
    test_query = "vulnerabilities"
    print(f"\nTesting query: '{test_query}'")
    results = ingestor.query(test_query)
    for i, res in enumerate(results, 1):
        print(f"{i}. {res.metadata['title']}")
        print(f"   Source: {res.metadata['source']}\n")
