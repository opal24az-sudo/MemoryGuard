# comparison_analysis.py
# Compare Baseline Detection with ML Models

from detectors import CombinedDetector
from ml_models import LogisticRegressionModel, RandomForestModel
from feature_extractor import FeatureExtractor

class ComparisonAnalysis:
    """
    Compares Baseline (rule-based) with ML models.
    """
    
    def __init__(self, baseline_detector, lr_model, rf_model):
        """
        Initialize comparison.
        
        Args:
            baseline_detector: CombinedDetector from step 5
            lr_model: Logistic Regression model from step 6
            rf_model: Random Forest model from step 6
        """
        self.baseline = baseline_detector
        self.lr_model = lr_model
        self.rf_model = rf_model
        self.feature_extractor = FeatureExtractor()
    
    def compare_on_dataset(self, dataset):
        """
        Compare all methods on a dataset.
        
        Args:
            dataset (list): List of (text, true_label) tuples
            
        Returns:
            dict: Comparison results
        """
        baseline_results = []
        lr_results = []
        rf_results = []
        true_labels = []
        
        for text, true_label in dataset:
            true_labels.append(true_label)
            
            # Baseline detection
            baseline_pred = self.baseline.detect_poison(text)
            baseline_results.append({
                "is_poisoned": baseline_pred["is_poisoned"],
                "risk_score": baseline_pred["risk_score"]
            })
            
            # LR model prediction
            lr_pred = self.lr_model.predict(text)
            lr_results.append({
                "is_poisoned": lr_pred["prediction"] == "POISONED",
                "confidence": lr_pred["confidence"]
            })
            
            # RF model prediction
            rf_pred = self.rf_model.predict(text)
            rf_results.append({
                "is_poisoned": rf_pred["prediction"] == "POISONED",
                "confidence": rf_pred["confidence"]
            })
        
        return {
            "baseline": baseline_results,
            "lr_model": lr_results,
            "rf_model": rf_results,
            "true_labels": true_labels,
            "dataset_size": len(dataset)
        }
    
    def calculate_metrics(self, predictions, true_labels):
        """
        Calculate performance metrics.
        
        Args:
            predictions (list): List of boolean predictions
            true_labels (list): List of true labels (0 or 1)
            
        Returns:
            dict: Calculated metrics
        """
        TP = sum(1 for pred, true in zip(predictions, true_labels) 
                 if pred and true == 1)
        TN = sum(1 for pred, true in zip(predictions, true_labels) 
                 if not pred and true == 0)
        FP = sum(1 for pred, true in zip(predictions, true_labels) 
                 if pred and true == 0)
        FN = sum(1 for pred, true in zip(predictions, true_labels) 
                 if not pred and true == 1)
        
        total = len(predictions)
        
        accuracy = (TP + TN) / total if total > 0 else 0
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "tp": TP,
            "tn": TN,
            "fp": FP,
            "fn": FN
        }
    
    def analyze_comparison(self, comparison_data):
        """
        Full analysis comparing all methods.
        
        Args:
            comparison_data (dict): Results from compare_on_dataset()
            
        Returns:
            dict: Complete analysis
        """
        true_labels = comparison_data["true_labels"]
        
        # Extract predictions
        baseline_preds = [r["is_poisoned"] for r in comparison_data["baseline"]]
        lr_preds = [r["is_poisoned"] for r in comparison_data["lr_model"]]
        rf_preds = [r["is_poisoned"] for r in comparison_data["rf_model"]]
        
        # Calculate metrics for each method
        baseline_metrics = self.calculate_metrics(baseline_preds, true_labels)
        lr_metrics = self.calculate_metrics(lr_preds, true_labels)
        rf_metrics = self.calculate_metrics(rf_preds, true_labels)
        
        return {
            "baseline": baseline_metrics,
            "lr_model": lr_metrics,
            "rf_model": rf_metrics,
            "dataset_size": comparison_data["dataset_size"]
        }
    
    def get_winner(self, analysis):
        """
        Determine which method performs best.
        
        Args:
            analysis (dict): Analysis results
            
        Returns:
            str: Name of best method
        """
        methods = {
            "Baseline": analysis["baseline"]["f1_score"],
            "Logistic Regression": analysis["lr_model"]["f1_score"],
            "Random Forest": analysis["rf_model"]["f1_score"]
        }
        
        winner = max(methods, key=methods.get)
        return winner, methods[winner]