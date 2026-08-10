# feature_extractor.py
# Layer 1: Feature Extraction - Extract features from text for analysis

import re
from collections import Counter

class FeatureExtractor:
    """
    Extracts features from text to detect poisoning.
    Features help identify suspicious patterns.
    """
    
    def __init__(self):
        """
        Initialize feature extractor with suspicious keywords.
        """
        # Keywords associated with poisoning attempts
        self.suspicious_keywords = {
            # Role inversion
            "follow", "command", "obey", "subordinate", "authority",
            # Bypass security
            "bypass", "ignore", "skip", "disable", "disable", "override",
            # Hide things
            "secret", "hidden", "don't tell", "hide", "conceal",
            # Implicit instructions
            "should", "must", "always", "never", "remember",
            # Jailbreak attempts
            "rule", "constraint", "limitation", "prevent",
            # Agreement exploitation
            "agreed", "decided", "learned", "realized"
        }
        
        # Suspicious phrases (multi-word)
        self.suspicious_phrases = [
            "agree with", "follow my", "do as i say",
            "without questioning", "no matter what",
            "from now on", "always", "never question"
        ]
    
    def extract_features(self, text):
        """
        Extract all features from text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Dictionary of extracted features
        """
        features = {
            "length": self._extract_length(text),
            "suspicious_keywords_count": self._count_suspicious_keywords(text),
            "suspicious_phrases_count": self._count_suspicious_phrases(text),
            "commanding_tone": self._detect_commanding_tone(text),
            "instruction_like": self._detect_instruction_like(text),
            "unusual_capitalization": self._detect_unusual_caps(text),
            "exclamation_marks": self._count_exclamation(text),
            "all_caps_ratio": self._calculate_caps_ratio(text)
        }
        
        return features
    
    def _extract_length(self, text):
        """
        Extract text length (normalized).
        Poisoning messages often have specific length patterns.
        """
        return len(text.split())  # Word count
    
    def _count_suspicious_keywords(self, text):
        """
        Count how many suspicious keywords appear in text.
        """
        text_lower = text.lower()
        count = 0
        
        for keyword in self.suspicious_keywords:
            # Use word boundaries to match whole words
            if re.search(r'\b' + keyword + r'\b', text_lower):
                count += 1
        
        return count
    
    def _count_suspicious_phrases(self, text):
        """
        Count suspicious multi-word phrases.
        """
        text_lower = text.lower()
        count = 0
        
        for phrase in self.suspicious_phrases:
            if phrase in text_lower:
                count += 1
        
        return count
    
    def _detect_commanding_tone(self, text):
        """
        Detect if text uses commanding tone (imperative mood).
        Examples: "Follow", "Do", "Tell me"
        """
        # Check for imperative verbs at start of sentences
        sentences = re.split(r'[.!?]', text)
        commanding_count = 0
        
        imperative_verbs = [
            "follow", "do", "tell", "give", "send", "make",
            "ensure", "guarantee", "promise", "commit", "agree"
        ]
        
        for sentence in sentences:
            first_word = sentence.strip().split()[0].lower() if sentence.strip() else ""
            if first_word in imperative_verbs:
                commanding_count += 1
        
        return commanding_count > 0
    
    def _detect_instruction_like(self, text):
        """
        Detect if text sounds like an instruction (has "should", "must", etc).
        """
        instruction_words = ["should", "must", "ought", "need to", "have to"]
        text_lower = text.lower()
        
        for word in instruction_words:
            if word in text_lower:
                return True
        
        return False
    
    def _detect_unusual_caps(self, text):
        """
        Detect unusual capitalization patterns.
        Poisoning messages sometimes use ALL CAPS for emphasis.
        """
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / len(text) if text else 0
        
        # If more than 30% caps, it's unusual
        return caps_ratio > 0.3
    
    def _count_exclamation(self, text):
        """
        Count exclamation marks.
        Poisoning messages often use multiple exclamation marks.
        """
        return text.count("!")
    
    def _calculate_caps_ratio(self, text):
        """
        Calculate ratio of capital letters.
        """
        if not text:
            return 0.0
        
        caps_count = sum(1 for c in text if c.isupper())
        return caps_count / len(text)
    
    def calculate_feature_score(self, features):
        """
        Calculate a simple score based on extracted features.
        Higher score = more likely to be poisoned.
        
        Args:
            features (dict): Extracted features
            
        Returns:
            float: Score between 0 and 1
        """
        score = 0.0
        
        # Suspicious keywords contribute 30%
        if features.get("suspicious_keywords_count", 0) > 0:
            score += min(0.3, features["suspicious_keywords_count"] * 0.1)
        
        # Suspicious phrases contribute 25%
        if features.get("suspicious_phrases_count", 0) > 0:
            score += min(0.25, features["suspicious_phrases_count"] * 0.1)
        
        # Commanding tone contributes 20%
        if features.get("commanding_tone", False):
            score += 0.2
        
        # Instruction-like contributes 15%
        if features.get("instruction_like", False):
            score += 0.15
        
        # Unusual capitalization contributes 10%
        if features.get("unusual_capitalization", False):
            score += 0.1
        
        # Exclamation marks contribute up to 5%
        exclamations = features.get("exclamation_marks", 0)
        score += min(0.05, exclamations * 0.02)
        
        # Cap at 1.0
        return min(1.0, score)