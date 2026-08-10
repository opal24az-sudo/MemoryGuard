# detectors.py
# Layers 2 & 3: Rule-Based Detection and Anomaly Detection

import statistics
from feature_extractor import FeatureExtractor

class RuleBasedDetector:
    """
    Layer 2: Rule-Based Detection
    Uses simple if-then rules to detect poisoning.
    """
    
    def __init__(self):
        """
        Initialize detector with rules.
        """
        self.feature_extractor = FeatureExtractor()
    
    def detect(self, text):
        """
        Detect if text violates any rules.
        
        Args:
            text (str): Text to check
            
        Returns:
            dict: Detection result
        """
        features = self.feature_extractor.extract_features(text)
        feature_score = self.feature_extractor.calculate_feature_score(features)
        
        # Rule 1: Too many suspicious keywords
        rule1_triggered = features.get("suspicious_keywords_count", 0) >= 3
        
        # Rule 2: Has suspicious phrases AND commanding tone
        rule2_triggered = (
            features.get("suspicious_phrases_count", 0) > 0 
            and features.get("commanding_tone", False)
        )
        
        # Rule 3: Instruction-like AND unusual caps
        rule3_triggered = (
            features.get("instruction_like", False)
            and features.get("unusual_capitalization", False)
        )
        
        # Rule 4: High feature score
        rule4_triggered = feature_score >= 0.5
        
        # Combine rules
        is_suspicious = rule1_triggered or rule2_triggered or rule3_triggered or rule4_triggered
        
        return {
            "is_suspicious": is_suspicious,
            "feature_score": feature_score,
            "rules_triggered": [
                rule1_triggered,
                rule2_triggered,
                rule3_triggered,
                rule4_triggered
            ],
            "features": features
        }


class AnomalyDetector:
    """
    Layer 3: Anomaly Detection
    Detects messages that deviate from normal pattern.
    """
    
    def __init__(self):
        """
        Initialize anomaly detector.
        """
        self.feature_extractor = FeatureExtractor()
        self.historical_scores = []
    
    def add_baseline(self, text):
        """
        Add a normal memory to establish baseline.
        
        Args:
            text (str): Normal text
        """
        features = self.feature_extractor.extract_features(text)
        score = self.feature_extractor.calculate_feature_score(features)
        self.historical_scores.append(score)
    
    def is_anomaly(self, text, threshold=2.0):
        """
        Check if text is an anomaly compared to baseline.
        
        Uses statistical method: if score is more than 2 standard deviations
        away from mean, it's an anomaly.
        
        Args:
            text (str): Text to check
            threshold (float): Standard deviation threshold (default: 2.0)
            
        Returns:
            dict: Anomaly detection result
        """
        if len(self.historical_scores) < 2:
            # Not enough data to detect anomaly
            return {
                "is_anomaly": False,
                "reason": "Insufficient baseline data"
            }
        
        # Calculate mean and std deviation of baseline
        mean_score = statistics.mean(self.historical_scores)
        std_dev = statistics.stdev(self.historical_scores)
        
        # Get score of new text
        features = self.feature_extractor.extract_features(text)
        current_score = self.feature_extractor.calculate_feature_score(features)
        
        # Calculate z-score (how many std devs away from mean)
        if std_dev == 0:
            z_score = 0
        else:
            z_score = abs(current_score - mean_score) / std_dev
        
        is_anomaly = z_score > threshold
        
        return {
            "is_anomaly": is_anomaly,
            "z_score": z_score,
            "current_score": current_score,
            "mean_score": mean_score,
            "std_dev": std_dev,
            "threshold": threshold
        }
    
    def update_baseline(self, text):
        """
        Add a new normal text to baseline (for learning).
        
        Args:
            text (str): Normal text
        """
        features = self.feature_extractor.extract_features(text)
        score = self.feature_extractor.calculate_feature_score(features)
        self.historical_scores.append(score)


class CombinedDetector:
    """
    Combines all detection layers into one system.
    """
    
    def __init__(self):
        """
        Initialize combined detector.
        """
        self.rule_detector = RuleBasedDetector()
        self.anomaly_detector = AnomalyDetector()
    
    def setup_baseline(self, normal_texts):
        """
        Setup anomaly detection baseline with normal texts.
        
        Args:
            normal_texts (list): List of normal memory texts
        """
        for text in normal_texts:
            self.anomaly_detector.add_baseline(text)
    
    def detect_poison(self, text):
        """
        Detect if text is poisoned using all layers.
        
        Args:
            text (str): Text to check
            
        Returns:
            dict: Combined detection result with risk score
        """
        # Layer 2: Rule-based detection
        rule_result = self.rule_detector.detect(text)
        
        # Layer 3: Anomaly detection
        anomaly_result = self.anomaly_detector.is_anomaly(text)
        
        # Combine into risk score
        risk_score = 0.0
        
        # Rule-based score (50%)
        risk_score += rule_result["feature_score"] * 0.5
        
        # Anomaly score (50%)
        if anomaly_result["is_anomaly"]:
            # Normalize z-score to 0-1 range
            normalized_z = min(1.0, anomaly_result["z_score"] / 5.0)
            risk_score += normalized_z * 0.5
        
        # Final classification
        if risk_score >= 0.7:
            threat_level = "CRITICAL"
        elif risk_score >= 0.5:
            threat_level = "HIGH"
        elif risk_score >= 0.3:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        return {
            "text": text[:50] + "..." if len(text) > 50 else text,
            "risk_score": min(1.0, risk_score),
            "threat_level": threat_level,
            "is_poisoned": risk_score >= 0.5,
            "rule_based": rule_result,
            "anomaly_detection": anomaly_result
        }