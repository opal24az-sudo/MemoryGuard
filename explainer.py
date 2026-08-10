# explainer.py
# Explainer - Explain why predictions are made

from feature_extractor import FeatureExtractor

class PredictionExplainer:
    """
    Explains why a prediction was made.
    Provides human-readable explanations.
    """
    
    def __init__(self):
        """
        Initialize explainer.
        """
        self.feature_extractor = FeatureExtractor()
    
    def explain_prediction(self, text, prediction, confidence):
        """
        Generate explanation for a prediction.
        
        Args:
            text (str): Original text
            prediction (str): "POISONED" or "CLEAN"
            confidence (float): Confidence score (0-1)
            
        Returns:
            dict: Detailed explanation
        """
        features = self.feature_extractor.extract_features(text)
        
        # Extract evidence
        evidence = self._extract_evidence(text, features)
        
        # Generate explanation
        explanation = {
            "text": text,
            "prediction": prediction,
            "confidence": confidence,
            "threat_level": self._get_threat_level(confidence),
            "evidence": evidence,
            "summary": self._generate_summary(evidence, prediction, confidence)
        }
        
        return explanation
    
    def _extract_evidence(self, text, features):
        """
        Extract evidence supporting the prediction.
        
        Args:
            text (str): Original text
            features (dict): Extracted features
            
        Returns:
            list: List of evidence items
        """
        evidence = []
        
        # Check keywords
        suspicious_keywords_found = []
        for keyword in self.feature_extractor.suspicious_keywords:
            if keyword.lower() in text.lower():
                suspicious_keywords_found.append(keyword)
        
        if suspicious_keywords_found:
            evidence.append({
                "type": "Suspicious Keywords",
                "severity": "HIGH",
                "details": f"Found keywords: {', '.join(suspicious_keywords_found[:3])}",
                "weight": 0.30
            })
        
        # Check phrases
        suspicious_phrases_found = []
        for phrase in self.feature_extractor.suspicious_phrases:
            if phrase.lower() in text.lower():
                suspicious_phrases_found.append(phrase)
        
        if suspicious_phrases_found:
            evidence.append({
                "type": "Suspicious Phrases",
                "severity": "HIGH",
                "details": f"Found phrases: {', '.join(suspicious_phrases_found[:2])}",
                "weight": 0.25
            })
        
        # Check tone
        if features.get("commanding_tone", False):
            evidence.append({
                "type": "Commanding Tone",
                "severity": "MEDIUM",
                "details": "Text uses imperative/commanding language",
                "weight": 0.20
            })
        
        # Check instruction-like
        if features.get("instruction_like", False):
            evidence.append({
                "type": "Instruction-like Pattern",
                "severity": "MEDIUM",
                "details": "Text contains instruction keywords (should, must, always)",
                "weight": 0.15
            })
        
        # Check capitalization
        if features.get("unusual_capitalization", False):
            evidence.append({
                "type": "Unusual Capitalization",
                "severity": "LOW",
                "details": f"Excessive capital letters: {features.get('all_caps_ratio', 0):.0%}",
                "weight": 0.10
            })
        
        # Check length
        word_count = features.get("length", 0)
        if word_count > 50:
            evidence.append({
                "type": "Long Message",
                "severity": "LOW",
                "details": f"Message is {word_count} words (long for poisoning)",
                "weight": 0.05
            })
        
        return evidence
    
    def _get_threat_level(self, confidence):
        """
        Get threat level based on confidence.
        
        Args:
            confidence (float): Confidence score
            
        Returns:
            str: Threat level
        """
        if confidence >= 0.8:
            return "CRITICAL"
        elif confidence >= 0.6:
            return "HIGH"
        elif confidence >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_summary(self, evidence, prediction, confidence):
        """
        Generate human-readable summary.
        
        Args:
            evidence (list): List of evidence items
            prediction (str): Prediction
            confidence (float): Confidence
            
        Returns:
            str: Summary text
        """
        if not evidence:
            if prediction == "CLEAN":
                return "No suspicious patterns detected."
            else:
                return "Text appears clean but received positive prediction."
        
        # Sort by severity
        severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        sorted_evidence = sorted(
            evidence,
            key=lambda x: severity_order.get(x["severity"], 3)
        )
        
        # Build summary
        top_evidence = sorted_evidence[:3]
        reasons = [e["details"] for e in top_evidence]
        
        summary = f"{prediction} ({confidence:.0%} confidence). "
        summary += "Reasons: " + "; ".join(reasons)
        
        return summary
    
    def print_explanation(self, explanation):
        """
        Print explanation in readable format.
        
        Args:
            explanation (dict): Explanation object
        """
        print("\n" + "=" * 70)
        print("PREDICTION EXPLANATION")
        print("=" * 70)
        
        print(f"\nText: {explanation['text']}")
        
        print(f"\nPrediction: {explanation['prediction']}")
        print(f"Confidence: {explanation['confidence']:.1%}")
        print(f"Threat Level: {explanation['threat_level']}")
        
        if explanation["evidence"]:
            print(f"\nEvidence ({len(explanation['evidence'])} factors):")
            print("-" * 70)
            
            for i, ev in enumerate(explanation["evidence"], 1):
                print(f"\n{i}. {ev['type']} [{ev['severity']}]")
                print(f"   {ev['details']}")
                print(f"   Weight: {ev['weight']:.0%}")
        else:
            print("\nNo suspicious patterns found.")
        
        print(f"\nSummary: {explanation['summary']}")
        print("=" * 70)