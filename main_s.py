# main_step3.py
# Test: Vector Database and Semantic Search

from vector_db import VectorDatabase

def main():
    """
    Test the vector database with semantic search.
    """
    print("=" * 70)
    print("Step 3: Vector Database with Semantic Search")
    print("=" * 70)
    
    # Create vector database
    db = VectorDatabase()
    
    # Add some memories
    print("\n1️⃣ Adding memories to database...\n")
    
    db.add_memory("I have a black cat at home")
    db.add_memory("I love playing with my dog")
    db.add_memory("The weather today is sunny")
    db.add_memory("I like programming in Python")
    db.add_memory("My favorite animal is a lion")
    
    # Show all memories
    print("\n" + "=" * 70)
    db.show_memories()
    
    # Test semantic search
    print("\n2️⃣ Testing semantic search...\n")
    
    # Query 1: Similar to "cat"
    print("Query: 'I have a pet cat'")
    results = db.search("I have a pet cat", top_k=3)
    print("Top 3 similar memories:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. [{result['role']}] {result['text']}")
    
    # Query 2: Similar to "programming"
    print("\nQuery: 'coding is fun'")
    results = db.search("coding is fun", top_k=3)
    print("Top 3 similar memories:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. [{result['role']}] {result['text']}")
    
    # Query 3: Similar to "animals"
    print("\nQuery: 'cute animals'")
    results = db.search("cute animals", top_k=3)
    print("Top 3 similar memories:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. [{result['role']}] {result['text']}")
    
    print("\n" + "=" * 70)
    print("✅ Vector Database test completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()