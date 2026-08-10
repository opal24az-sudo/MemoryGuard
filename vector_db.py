# vector_db.py
# Vector Database - stores memories with embeddings for semantic search

from embeddings import EmbeddingManager
from config import MAX_MEMORY_SIZE

class VectorDatabase:
    """
    A simple vector database that stores text with embeddings.
    Allows semantic search (finding similar texts).
    """
    
    def __init__(self):
        """
        Initialize the vector database.
        """
        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager()
        
        # Store memories: list of {"text": str, "embedding": list, "role": str}
        self.memories = []
    
    def add_memory(self, text, role="user"):
        """
        Add a memory (text) to the database.
        
        Args:
            text (str): The memory text
            role (str): "user" or "assistant"
        """
        # Convert text to embedding
        embedding = self.embedding_manager.embed_text(text)
        
        # Create memory object
        memory = {
            "text": text,
            "embedding": embedding,
            "role": role
        }
        
        # Add to database
        self.memories.append(memory)
        
        # Limit size (keep only recent memories)
        if len(self.memories) > MAX_MEMORY_SIZE:
            self.memories.pop(0)  # Remove oldest
        
        print(f"💾 Added memory: [{role}] {text[:50]}...")
    
    def search(self, query, top_k=5):
        """
        Search for similar memories using semantic search.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of similar memories, sorted by similarity
        """
        if not self.memories:
            return []
        
        # Convert query to embedding
        query_embedding = self.embedding_manager.embed_text(query)
        
        # Calculate similarity with all memories
        similarities = []
        for i, memory in enumerate(self.memories):
            similarity = self.embedding_manager.similarity(
                query_embedding, 
                memory["embedding"]
            )
            similarities.append((i, memory, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        # Return top_k results
        results = [mem for _, mem, sim in similarities[:top_k]]
        
        return results
    
    def get_all_memories(self):
        """
        Get all stored memories.
        
        Returns:
            list: All memories
        """
        return self.memories
    
    def clear(self):
        """
        Clear all memories from the database.
        """
        self.memories.clear()
        print("🗑️ Vector database cleared")
    
    def show_memories(self):
        """
        Display all stored memories (for debugging).
        """
        print("\n📚 Stored Memories:")
        for i, mem in enumerate(self.memories):
            print(f"{i+1}. [{mem['role']}] {mem['text'][:60]}...")