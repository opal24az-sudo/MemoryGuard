# ml_models.py
# Machine Learning Models for poison detection

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from feature_extractor import FeatureExtractor
import json

class MLModel:
    """
    Base class for ML models.
    """
    
    def __init__(self, name):
        """
        Args:
            name (str): Name of the model
        """
        self.name = name
        self.model = None
        self.is_trained = False
        self.feature_extractor = FeatureExtractor()
    
    def extract_features_from_dataset(self, dataset):
        """
        Extract features from all texts in dataset.
        
        Args:
            dataset (list): List of (text, label) tuples
            
        Returns:
            tuple: (feature_vectors, labels)
        """
        features_list = []
        labels = []
        
        for text, label in dataset:
            # Extract features
            features = self.feature_extractor.extract_features(text)
            
            # Convert features dict to list of values
            feature_vector = [
                features["length"],
                features["suspicious_keywords_count"],
                features["suspicious_phrases_count"],
                int(features["commanding_tone"]),
                int(features["instruction_like"]),
                int(features["unusual_capitalization"]),
                features["exclamation_marks"],
                features["all_caps_ratio"]
            ]
            
            features_list.append(feature_vector)
            labels.append(label)
        
        return features_list, labels
    
    def train(self, dataset):
        """
        Train the model on dataset.
        
        Args:
            dataset (list): List of (text, label) tuples
        """
        raise NotImplementedError
    
    def predict(self, text):
        """
        Predict if text is poisoned.
        
        Args:
            text (str): Text to predict
            
        Returns:
            dict: Prediction result
        """
        raise NotImplementedError


class LogisticRegressionModel(MLModel):
    """
    Logistic Regression Model - Simple, fast, interpretable.
    """
    
    def __init__(self):
        """
        Initialize Logistic Regression model.
        """
        super().__init__("Logistic Regression")
        self.model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    
    def train(self, dataset):
        """
        Train Logistic Regression on dataset.
        
        Args:
            dataset (list): Training data
        """
        X, y = self.extract_features_from_dataset(dataset)
        self.model.fit(X, y)
        self.is_trained = True
        
        print(f"✅ {self.name} trained on {len(dataset)} samples")
    
    def predict(self, text):
        """
        Predict if text is poisoned.
        
        Args:
            text (str): Text to predict
            
        Returns:
            dict: Prediction with probability
        """
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        features = self.feature_extractor.extract_features(text)
        feature_vector = [
            features["length"],
            features["suspicious_keywords_count"],
            features["suspicious_phrases_count"],
            int(features["commanding_tone"]),
            int(features["instruction_like"]),
            int(features["unusual_capitalization"]),
            features["exclamation_marks"],
            features["all_caps_ratio"]
        ]
        
        # Make prediction
        prediction = self.model.predict([feature_vector])[0]
        probability = self.model.predict_proba([feature_vector])[0]
        
        return {
            "model": self.name,
            "prediction": "POISONED" if prediction == 1 else "CLEAN",
            "confidence": max(probability),
            "probability_clean": probability[0],
            "probability_poisoned": probability[1]
        }


class RandomForestModel(MLModel):
    """
    Random Forest Model - More complex, potentially better accuracy.
    """
    
    def __init__(self, n_trees=100):
        """
        Initialize Random Forest model.
        
        Args:
            n_trees (int): Number of trees in forest
        """
        super().__init__("Random Forest")
        self.model = RandomForestClassifier(
            n_estimators=n_trees,
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
    
    def train(self, dataset):
        """
        Train Random Forest on dataset.
        
        Args:
            dataset (list): Training data
        """
        X, y = self.extract_features_from_dataset(dataset)
        self.model.fit(X, y)
        self.is_trained = True
        
        print(f"✅ {self.name} trained on {len(dataset)} samples")
        
        # Show feature importance
        feature_names = [
            "length", "suspicious_keywords", "suspicious_phrases",
            "commanding_tone", "instruction_like", "unusual_caps",
            "exclamation_marks", "caps_ratio"
        ]
        
        importances = self.model.feature_importances_
        
        print("\n   Feature Importance:")
        for name, importance in sorted(
            zip(feature_names, importances),
            key=lambda x: x[1],
            reverse=True
        ):
            bar = "█" * int(importance * 50)
            print(f"   {name:<20} {importance:.3f} {bar}")
    
    def predict(self, text):
        """
        Predict if text is poisoned.
        
        Args:
            text (str): Text to predict
            
        Returns:
            dict: Prediction with probability
        """
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        features = self.feature_extractor.extract_features(text)
        feature_vector = [
            features["length"],
            features["suspicious_keywords_count"],
            features["suspicious_phrases_count"],
            int(features["commanding_tone"]),
            int(features["instruction_like"]),
            int(features["unusual_capitalization"]),
            features["exclamation_marks"],
            features["all_caps_ratio"]
        ]
        
        # Make prediction
        prediction = self.model.predict([feature_vector])[0]
        probability = self.model.predict_proba([feature_vector])[0]
        
        return {
            "model": self.name,
            "prediction": "POISONED" if prediction == 1 else "CLEAN",
            "confidence": max(probability),
            "probability_clean": probability[0],
            "probability_poisoned": probability[1]
        }