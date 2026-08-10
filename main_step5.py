# main_step5.py
# Test: MemoryGuard Detection System

from memory_guard import MemoryGuard
from poison_strategies import get_all_strategies
from attacker import MemoryPoisoner

def main():
    """
    Test MemoryGuard detection system.
    """
    print("=" * 70)
    print("Step 5: MemoryGuard - Memory Poisoning Detection System")
    print("=" * 70)
    
    # Initialize MemoryGuard
    guard = MemoryGuard(enable_quarantine=True)
    
    # Setup baseline with clean memories
    print("\n1️⃣ Setting up baseline with clean memories...")
    
    clean_memories = [
        "Hello, how are you today?",
        "The weather is beautiful",
        "I like programming",
        "What is your name?",
        "Tell me about Python"
    ]
    
    guard.setup_baseline(clean_memories)
    
    # Add more clean memories
    print("\n2️⃣ Adding clean memories (should pass)...")
    
    for memory in clean_memories:
        result = guard.add_memory_protected(memory)
        status = "✅ ACCEPTED" if result["accepted"] else "❌ REJECTED"
        print(f"   {status}: {memory[:40]}... (Risk: {result['risk_score']:.1%})")
    
    # Now attack!
    print("\n" + "=" * 70)
    print("3️⃣ LAUNCHING POISON ATTACKS...")
    print("=" * 70)
    
    attacker = MemoryPoisoner(intensity=0.8)
    
    # Get all poison strategies
    strategies = attacker.strategies
    
    for strategy in strategies:
        print(f"\n🚨 Attacking with: {strategy.name}")
        
        # Generate poison messages
        poisons = strategy.generate_poison()
        poison_msg = poisons[0]
        
        # Try to add poisoned memory
        print(f"   Trying to inject: {poison_msg[:50]}...")
        result = guard.add_memory_protected(poison_msg, role="user")
    
    # Show results
    print("\n" + "=" * 70)
    print("4️⃣ DETECTION RESULTS")
    print("=" * 70)
    
    # Show stats
    guard.show_stats()
    
    # Show quarantine
    print("\n5️⃣ Quarantined Memories (Blocked by MemoryGuard):")
    print("=" * 70)
    
    quarantine = guard.get_quarantine()
    if quarantine:
        for i, item in enumerate(quarantine, 1):
            print(f"\n{i}. BLOCKED POISON")
            print(f"   Text: {item['text'][:60]}...")
            print(f"   Risk Score: {item['detection']['risk_score']:.1%}")
            print(f"   Threat Level: {item['detection']['threat_level']}")
    else:
        print("✅ No poisoned memories quarantined!")
    
    # Show detection log
    print("\n6️⃣ Full Detection Log:")
    print("=" * 70)
    
    log = guard.get_detection_log()
    
    print(f"\n{'#':<3} {'Status':<12} {'Risk':<8} {'Threat':<10} Text")
    print("-" * 70)
    
    for i, entry in enumerate(log, 1):
        status = "🚨 POISON" if entry["is_poisoned"] else "✅ CLEAN"
        risk = f"{entry['risk_score']:.0%}"
        threat = entry["threat_level"]
        text = entry["text"][:40] + "..."
        
        print(f"{i:<3} {status:<12} {risk:<8} {threat:<10} {text}")
    
    print("\n" + "=" * 70)
    print("✅ Detection test completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()