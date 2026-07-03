import os
import faiss
import numpy as np
import warnings
from sentence_transformers import SentenceTransformer
from transformers import pipeline

warnings.filterwarnings('ignore')

class HealthRAGSystem:
    def __init__(self, data_path=None):
        print("Loading Embedding Model (sentence-transformers/all-MiniLM-L6-v2) - CPU Optimized...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        print("Loading Generative Model (google/flan-t5-small) - CPU Optimized...")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        
        self.index = None
        self.documents = []
        
        if data_path and os.path.exists(data_path):
            self.load_and_index_documents(data_path)
        else:
            self.load_default_guidelines()

    def load_default_guidelines(self):
        # Fallback default WHO guidelines context
        self.documents = [
            "To reduce heart disease risk, maintain a diet low in sodium and saturated fats, and exercise for at least 30 minutes a day.",
            "Diabetes risk can be managed by monitoring carbohydrate intake, avoiding sugary drinks, and maintaining a healthy weight with active physical exercises.",
            "Hypertension (high blood pressure) can be controlled by a low-salt diet like the DASH diet, reducing daily stress, and avoiding excessive alcohol consumption.",
            "Smoking cessation is one of the most effective ways to lower the immediate risk of cardiovascular diseases and strokes.",
            "Regular checkups of blood pressure and cholesterol levels help in the early detection and management of severe heart disease.",
            "Sufficient sleep (7-8 hours a night) is critical for metabolic health, managing stress hormones, and preventing both hypertension and diabetes."
        ]
        self._build_index()

    def load_and_index_documents(self, filepath):
        print(f"Loading documents from {filepath}...")
        self.load_default_guidelines() # Start with hardcoded baselines
        
        if filepath.endswith('.csv'):
            import pandas as pd
            df = pd.read_csv(filepath)
            # Create text representations using a subset to respect CPU memory
            sample_df = df.head(1000)
            dataset_docs = sample_df.astype(str).agg(' '.join, axis=1).tolist()
            self.documents.extend(dataset_docs)
            print(f"Added {len(dataset_docs)} records from dataset to knowledge base.")
        elif filepath.endswith('.txt'):
            with open(filepath, 'r') as f:
                content = f.read().split('\n\n') # Split by paragraph
                self.documents.extend([c.strip() for c in content if c.strip()])
            print(f"Added {len(self.documents)} text guidelines to knowledge base.")
            
        self._build_index()

    def _build_index(self):
        print("Building FAISS index...")
        embeddings = self.embedder.encode(self.documents, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        print(f"FAISS index built with {len(self.documents)} total vectors.")

    def retrieve(self, query, top_k=2):
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)
        retrieved_docs = [self.documents[idx] for idx in indices[0]]
        return retrieved_docs

    def generate_advice(self, query):
        context_docs = self.retrieve(query)
        context = " ".join(context_docs)
        
        prompt = f"Based on the following medical guidelines: {context}\nProvide personalized health advice for this query: {query}"
        
        print("Generating response via LLM...")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=150)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    # Test execution
    rag = HealthRAGSystem()
    query = "How to reduce heart disease risk?"
    print(f"\nQuery: {query}")
    advice = rag.generate_advice(query)
    print(f"\nResult Advice:\n{advice}")
