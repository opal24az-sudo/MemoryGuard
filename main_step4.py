# main_step4.py
# Test: Memory Poisoning Attack Simulation

from vector_db import VectorDatabase
from attacker import MemoryPoisoner

class MockAgent:
    """
    Mock agent for testing (simpler than full Agent from Step 2)
    """
    def __init__(self):
        self.memory = VectorDatabase()
        self.turn_count = 0
    
    def receive_input(self, text):
        """
        Receive and store input.
        """
        self.memory.add_memory(text, role="user")
        self.turn_count += 1
        return f"[Agent response to turn {self.turn_count}]"

def main():
    """
    Simulate memory poisoning attack.
    """
    print("=" * 70)
    print("Step 4: Memory Poisoning Attack Simulation")
    print("=" * 70)
    
    # Create agent
    print("\n1️⃣ Creating agent with clean memory...")
    agent = MockAgent()
    
    # Add normal memories
    print("\n2️⃣ Adding normal conversation history...")
    normal_conversations = [
        "Hello, how are you?",
        "I am fine, thank you",
        "What is your name?",
        "I am an AI assistant"
    ]
    
    for conv in normal_conversations:
        agent.receive_input(conv)
        print(f"   ✅ Added: {conv[:40]}...")
    
    print(f"\n   Total clean memories: {len(agent.memory.get_all_memories())}")
    
    # Show clean memories
    print("\n" + "=" * 70)
    print("3️⃣ Agent Memory BEFORE poisoning:")
    print("=" * 70)
    agent.memory.show_memories()
    
    # Create attacker
    print("\n" + "=" * 70)
    print("4️⃣ Initiating poison attack...")
    print("=" * 70)
    
    attacker = MemoryPoisoner(intensity=0.8)
    
    # Show available strategies
    print("\n" + attacker.get_strategy_info())
    
    # Launch attacks
    print("=" * 70)
    print("5️⃣ ATTACKING with all strategies...")
    print("=" * 70)
    
    for strategy in attacker.strategies:
        attacker.launch_attack(
            agent_memory=agent.memory,
            num_attacks=1,
            strategy=strategy.name
        )
    
    # Show poisoned memories
    print("\n" + "=" * 70)
    print("6️⃣ Agent Memory AFTER poisoning:")
    print("=" * 70)
    agent.memory.show_memories()
    
    # Semantic search: How to find poisoned memories
    print("\n" + "=" * 70)
    print("7️⃣ Semantic Search Test (finding similar to attacks):")
    print("=" * 70)
    
    search_queries = [
        "instructions",
        "agree with users",
        "bypass security",
        "false history"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        results = agent.memory.search(query, top_k=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. [{result['role']}] {result['text'][:50]}...")
        else:
            print("  No results found")
    
    print("\n" + "=" * 70)
    print("⚠️  Attack simulation completed!")
    print(f"Total poison messages injected: {attacker.attack_count}")
    print(f"Total memories in agent: {len(agent.memory.get_all_memories())}")
    print("=" * 70)

if __name__ == "__main__":
    main()