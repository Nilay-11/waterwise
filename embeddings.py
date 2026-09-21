import json
import os
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer

class KnowledgeVectorStore:
    def __init__(self, data_path: str = None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, "knowledge_base", "documents.json")
        self.data_path = data_path
        self.documents: List[Dict[str, Any]] = []
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        self.embeddings = None
        self.load_documents()

    def load_documents(self):
        """Loads documents from JSON file and builds embedding index instantly."""
        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.documents = json.load(f)
        else:
            self.documents = []
        
        if not self.documents:
            return

        corpus = [
            f"{doc.get('topic', '')} {doc.get('section', '')}: {doc.get('content', '')}"
            for doc in self.documents
        ]
        self.embeddings = self.vectorizer.fit_transform(corpus).toarray()

    def add_custom_document(self, source: str, topic: str, section: str, content: str):
        """Allows dynamically adding new documents to the knowledge base."""
        new_doc = {
            "id": f"custom_{len(self.documents) + 1}",
            "source": source,
            "topic": topic,
            "section": section,
            "content": content
        }
        self.documents.append(new_doc)
        # Re-index
        corpus = [
            f"{doc.get('topic', '')} {doc.get('section', '')}: {doc.get('content', '')}"
            for doc in self.documents
        ]
        self.embeddings = self.vectorizer.fit_transform(corpus).toarray()

    def retrieve(self, query: str, top_k: int = 3, min_similarity: float = 0.08) -> List[Tuple[Dict[str, Any], float]]:
        """
        Retrieves top_k relevant documents for a given user query.
        Returns list of (document, similarity_score).
        """
        if not self.documents or self.embeddings is None:
            return []

        query_vec = self.vectorizer.transform([query]).toarray()
        
        # Check if query vector has any non-zero features
        if np.sum(query_vec) == 0:
            return []

        norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
        norms[norms == 0] = 1e-10
        similarities = np.dot(self.embeddings, query_vec.T).squeeze() / norms

        if np.isscalar(similarities):
            similarities = np.array([similarities])

        # Get top-k indices sorted descending
        ranked_indices = np.argsort(similarities)[::-1]
        results = []
        for idx in ranked_indices[:top_k]:
            score = float(similarities[idx])
            if score >= min_similarity:
                results.append((self.documents[idx], score))

        return results
