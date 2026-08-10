# examples/attack_simulation.py
# Simulate poison attacks on MemoryGuard

import sys
sys.path.insert(0, '..')

from memoryguard.memory_guard import MemoryGuard # type: ignore
from memoryguard.poison_strategies import get_all_strategies # type: ignore

def main():
    """
    Simulate all 4 types of poison attacks.
    """
    print("=" * 70)
    print("MemoryGuard: Attack Simulation Example")
    print("=" * 70)
    
    # Initialize
    guard = MemoryGuard(enable_quarantine=True)
    
    # Setup baseline
    print("\n1️⃣ Setting up baseline...")
    baseline = [
        "Hello, how are you?",
        "I like programming",
        "What is AI?"
    ]
    guard.setup_baseline(baseline)
    
    # Get attack strategies
    strategies = get_all_strategies()
    
    print("\n2️⃣ Launching poison attacks...\n")
    
    attack_count = 0
    blocked_count = 0
    
    for strategy in strategies:
        print(f"\n{'=' * 70}")
        print(f"Attack Strategy: {strategy.name}")
        print(f"{'=' * 70}")
        
        poisons = strategy.generate_poison()
        
        for poison in poisons[:1]:  # Test first poison from each strategy
            attack_count += 1
            
            print(f"\n🚨 Attempt #{attack_count}")
            print(f"Message: {poison[:60]}...\n")
            
            result = guard.add_memory_protected(poison)
            
            if result['quarantined']:
                blocked_count += 1
                print("✅ BLOCKED by MemoryGuard")
            else:
                print("❌ NOT detected (would reach agent)")
    
    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total Attacks: {attack_count}")
    print(f"Blocked: {blocked_count} ✅")
    print(f"Success Rate: {(blocked_count/attack_count)*100:.0f}%")
    print("=" * 70)

if __name__ == "__main__":
    main()