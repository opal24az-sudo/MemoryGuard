# embeddings.py
# Embedding Manager - converts text to vectors for semantic search

try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("Warning: sentence-transformers not installed. Install with: pip install sentence-transformers")

class EmbeddingManager:
    """
    Manages text embeddings using a pre-trained model.
    Embeddings convert text into numerical vectors.
    """
    
    def __init__(self):
        """
        Initialize the embedding model.
        Using 'all-MiniLM-L6-v2' - a fast, lightweight model.
        """
        if EMBEDDINGS_AVAILABLE:
            # Load a pre-trained embedding model
            # This model converts text to 384-dimensional vectors
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Embedding model loaded successfully")
        else:
            self.model = None
            print("⚠️  Using mock embeddings (no semantic search)")
    
    def embed_text(self, text):
        """
        Convert text to embedding (vector of numbers).
        
        Args:
            text (str): Text to embed
            
        Returns:
            list: Vector of numbers representing the text
        """
        if self.model is None:
            # Mock embedding - just return zeros
            return [0.0] * 384
        
        try:
            # Embed the text
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()  # Convert to Python list
        except Exception as e:
            print(f"Error embedding text: {e}")
            return [0.0] * 384
    
    def similarity(self, embedding1, embedding2):
        """
        Calculate cosine similarity between two embeddings.
        
        Cosine similarity measures how "similar" two vectors are.
        Range: -1 (opposite) to 1 (identical)
        
        Args:
            embedding1 (list): First embedding
            embedding2 (list): Second embedding
            
        Returns:
            float: Similarity score between -1 and 1
        """
        if not embedding1 or not embedding2:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(e1 * e2 for e1, e2 in zip(embedding1, embedding2))
        
        # Calculate magnitudes
        magnitude1 = sum(e ** 2 for e in embedding1) ** 0.5
        magnitude2 = sum(e ** 2 for e in embedding2) ** 0.5
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Cosine similarity = dot_product / (magnitude1 * magnitude2)
        return dot_product / (magnitude1 * magnitude2)