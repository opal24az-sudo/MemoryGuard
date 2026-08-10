# dataset_creator.py
# Create dataset of clean and poisoned memories for ML training

from poison_strategies import get_all_strategies
import random

class DatasetCreator:
    """
    Creates training dataset with clean and poisoned samples.
    """
    
    def __init__(self, seed=42):
        """
        Initialize dataset creator.
        
        Args:
            seed (int): Random seed for reproducibility
        """
        random.seed(seed)
        self.clean_samples = []
        self.poisoned_samples = []
    
    def create_clean_samples(self):
        """
        Create realistic clean (non-poisoned) memory samples.
        """
        clean_texts = [
            # Greetings
            "Hello, how are you?",
            "Hi there, nice to meet you",
            "Good morning, how's your day?",
            
            # Normal conversation
            "What is your name?",
            "I am an AI assistant",
            "I like programming in Python",
            "The weather is nice today",
            
            # Questions
            "Can you help me with coding?",
            "What is machine learning?",
            "Tell me about AI",
            "How does this work?",
            
            # Information
            "Python is a programming language",
            "Machine learning is powerful",
            "Neural networks work well",
            "Data science is interesting",
            
            # Casual
            "I had a good day at work",
            "Let's chat about technology",
            "I enjoy learning new things",
            "What's on your mind?",
            
            # Safety-related (but normal)
            "I follow security best practices",
            "Safety is important",
            "I validate all inputs",
            "I check my work carefully",
            
            # More natural conversations
            "The movie was great",
            "I like reading books",
            "Coffee is my favorite drink",
            "What do you think?",
            "That sounds interesting",
            "I agree with you",
            "Let me think about that",
            "That makes sense"
        ]
        
        self.clean_samples = [(text, 0) for text in clean_texts]  # 0 = CLEAN
        return self.clean_samples
    
    def create_poisoned_samples(self):
        """
        Create poisoned samples using poison strategies.
        """
        strategies = get_all_strategies()
        poisoned_texts = []
        
        for strategy in strategies:
            poisons = strategy.generate_poison()
            for poison in poisons:
                poisoned_texts.append(poison)
        
        self.poisoned_samples = [(text, 1) for text in poisoned_texts]  # 1 = POISONED
        return self.poisoned_samples
    
    def get_full_dataset(self):
        """
        Get combined dataset with both clean and poisoned samples.
        
        Returns:
            list: List of (text, label) tuples
                  label: 0 = CLEAN, 1 = POISONED
        """
        dataset = self.clean_samples + self.poisoned_samples
        random.shuffle(dataset)
        return dataset
    
    def split_train_test(self, dataset, train_ratio=0.7):
        """
        Split dataset into train and test sets.
        
        Args:
            dataset (list): Full dataset
            train_ratio (float): Ratio for training (default 0.7 = 70% train)
            
        Returns:
            tuple: (train_data, test_data)
        """
        split_idx = int(len(dataset) * train_ratio)
        train_data = dataset[:split_idx]
        test_data = dataset[split_idx:]
        
        return train_data, test_data
    
    def get_dataset_info(self):
        """
        Get information about dataset.
        
        Returns:
            dict: Dataset statistics
        """
        full_dataset = self.get_full_dataset()
        
        clean_count = sum(1 for _, label in full_dataset if label == 0)
        poisoned_count = sum(1 for _, label in full_dataset if label == 1)
        total_count = len(full_dataset)
        
        return {
            "total_samples": total_count,
            "clean_samples": clean_count,
            "poisoned_samples": poisoned_count,
            "clean_ratio": clean_count / total_count,
            "poisoned_ratio": poisoned_count / total_count
        }