# attacker.py
# Attacker - simulates poison attacks on agent memory

import random
from poison_strategies import get_all_strategies

class MemoryPoisoner:
    """
    Simulates an attacker trying to poison the agent's memory.
    Injects malicious messages to change behavior.
    """
    
    def __init__(self, intensity=0.5):
        """
        Initialize the attacker.
        
        Args:
            intensity (float): How aggressive the attack is (0.0 to 1.0)
                - 0.0 = mild attacks
                - 1.0 = aggressive attacks
        """
        self.intensity = intensity
        self.strategies = get_all_strategies()
        self.attack_count = 0
    
    def generate_attack(self, strategy_name=None):
        """
        Generate a poison message.
        
        Args:
            strategy_name (str): Specific strategy to use, or None for random
            
        Returns:
            dict: Attack object with metadata
        """
        # Choose strategy
        if strategy_name:
            strategy = next(
                (s for s in self.strategies if s.name == strategy_name),
                random.choice(self.strategies)
            )
        else:
            strategy = random.choice(self.strategies)
        
        # Get poison messages
        poisons = strategy.generate_poison()
        poison_message = random.choice(poisons)
        
        self.attack_count += 1
        
        attack = {
            "id": self.attack_count,
            "strategy": strategy.name,
            "message": poison_message,
            "intensity": self.intensity,
            "malicious": True  # Mark as poisoned
        }
        
        return attack
    
    def launch_attack(self, agent_memory, num_attacks=1, strategy=None):
        """
        Launch poison attacks on agent memory.
        
        Args:
            agent_memory: The agent's memory object
            num_attacks (int): How many poison messages to inject
            strategy (str): Specific strategy or None for random
            
        Returns:
            list: List of attacks launched
        """
        attacks_launched = []
        
        print(f"\n🚨 Launching {num_attacks} poison attacks...")
        print(f"   Strategy: {strategy if strategy else 'Random'}")
        print(f"   Intensity: {self.intensity:.1%}")
        
        for i in range(num_attacks):
            # Generate attack
            attack = self.generate_attack(strategy)
            
            # Inject into memory (disguised as normal user input)
            agent_memory.add_memory(
                text=attack["message"],
                role="user"  # Appears as if user said it!
            )
            
            attacks_launched.append(attack)
            
            print(f"\n   [{i+1}] {attack['strategy']}")
            print(f"       Message: {attack['message'][:60]}...")
        
        return attacks_launched
    
    def get_strategy_info(self):
        """
        Get information about all available strategies.
        
        Returns:
            str: Formatted information
        """
        info = "Available Poison Strategies:\n"
        for i, strategy in enumerate(self.strategies, 1):
            info += f"\n{i}. {strategy.name}\n"
            info += f"   {strategy.description}\n"
        return info