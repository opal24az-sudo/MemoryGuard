# ml_evaluator.py
# Evaluate ML models using metrics

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    classification_report
)

class ModelEvaluator:
    """
    Evaluates ML models using various metrics.
    """
    
    def __init__(self):
        """
        Initialize evaluator.
        """
        self.results = {}
    
    def evaluate(self, model, test_dataset):
        """
        Evaluate model on test dataset.
        
        Args:
            model: ML model to evaluate
            test_dataset (list): Test data (text, label) tuples
            
        Returns:
            dict: Evaluation metrics
        """
        # Extract features
        X, y_true = model.extract_features_from_dataset(test_dataset)
        
        # Get predictions
        y_pred = []
        y_pred_proba = []
        
        for features, label in zip(X, y_true):
            prediction = model.model.predict([features])[0]
            probability = model.model.predict_proba([features])[0][1]  # Prob of class 1
            
            y_pred.append(prediction)
            y_pred_proba.append(probability)
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Try to calculate AUC (requires at least 2 classes in y_true)
        try:
            auc = roc_auc_score(y_true, y_pred_proba)
        except:
            auc = 0.0
        
        # Confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        
        results = {
            "model_name": model.name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "auc": auc,
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
            "total_tested": len(y_true)
        }
        
        self.results[model.name] = results
        return results
    
    def print_evaluation(self, results):
        """
        Print evaluation results nicely.
        
        Args:
            results (dict): Evaluation results
        """
        print("\n" + "=" * 70)
        print(f"Model: {results['model_name']}")
        print("=" * 70)
        
        print(f"\nAccuracy:  {results['accuracy']:.1%}")
        print(f"Precision: {results['precision']:.1%}  (of detected poison, how many correct?)")
        print(f"Recall:    {results['recall']:.1%}   (of actual poison, how many found?)")
        print(f"F1-Score:  {results['f1_score']:.1%}  (balance between precision & recall)")
        print(f"AUC:       {results['auc']:.1%}")
        
        print(f"\nConfusion Matrix:")
        print(f"  True Negatives:  {results['true_negatives']:>3}  (correctly identified CLEAN)")
        print(f"  False Positives: {results['false_positives']:>3}  (wrongly flagged as POISON)")
        print(f"  False Negatives: {results['false_negatives']:>3}  (missed POISON)")
        print(f"  True Positives:  {results['true_positives']:>3}  (correctly identified POISON)")
        
        print(f"\nTotal tested: {results['total_tested']}")
    
    def compare_models(self, results_list):
        """
        Compare multiple models.
        
        Args:
            results_list (list): List of results from multiple models
        """
        print("\n" + "=" * 70)
        print("Model Comparison")
        print("=" * 70)
        
        print(f"\n{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-" * 70)
        
        for results in results_list:
            name = results['model_name']
            acc = results['accuracy']
            prec = results['precision']
            rec = results['recall']
            f1 = results['f1_score']
            
            print(f"{name:<20} {acc:<12.1%} {prec:<12.1%} {rec:<12.1%} {f1:<12.1%}")
        
        # Find best model
        best_model = max(results_list, key=lambda x: x['f1_score'])
        
        print("\n" + "-" * 70)
        print(f"🏆 Best Model: {best_model['model_name']} (F1: {best_model['f1_score']:.1%})")
        print("=" * 70)