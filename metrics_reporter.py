# metrics_reporter.py
# Generate beautiful metrics reports

class MetricsReporter:
    """
    Generate formatted reports of detection metrics.
    """
    
    def __init__(self):
        """
        Initialize reporter.
        """
        pass
    
    def print_metrics_table(self, metrics_dict):
        """
        Print metrics in a nice table.
        
        Args:
            metrics_dict (dict): Dict with method names as keys
                                and metrics as values
        """
        print("\n" + "=" * 90)
        print("Performance Metrics Comparison")
        print("=" * 90)
        
        print(f"\n{'Method':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12}")
        print("-" * 90)
        
        for method_name, metrics in metrics_dict.items():
            accuracy = metrics["accuracy"]
            precision = metrics["precision"]
            recall = metrics["recall"]
            f1_score = metrics["f1_score"]
            
            print(f"{method_name:<25} {accuracy:<12.1%} {precision:<12.1%} {recall:<12.1%} {f1_score:<12.1%}")
        
        print("=" * 90)
    
    def print_confusion_matrices(self, analysis):
        """
        Print confusion matrices for all methods.
        
        Args:
            analysis (dict): Analysis results
        """
        print("\n" + "=" * 90)
        print("Confusion Matrices")
        print("=" * 90)
        
        methods = ["baseline", "lr_model", "rf_model"]
        method_names = ["Baseline", "Logistic Regression", "Random Forest"]
        
        for method, name in zip(methods, method_names):
            metrics = analysis[method]
            
            print(f"\n{name}:")
            print("-" * 50)
            print(f"                 Predicted")
            print(f"                 Negative    Positive")
            print(f"Actual  Negative {metrics['tn']:<11} {metrics['fp']:<10}")
            print(f"        Positive {metrics['fn']:<11} {metrics['tp']:<10}")
            
            print(f"\n  ✅ Correct predictions:     {metrics['tp'] + metrics['tn']}")
            print(f"  ❌ Incorrect predictions:   {metrics['fp'] + metrics['fn']}")
    
    def print_detailed_analysis(self, analysis):
        """
        Print detailed analysis with explanations.
        
        Args:
            analysis (dict): Analysis results
        """
        print("\n" + "=" * 90)
        print("Detailed Analysis")
        print("=" * 90)
        
        methods = ["baseline", "lr_model", "rf_model"]
        method_names = ["Baseline", "Logistic Regression", "Random Forest"]
        
        for method, name in zip(methods, method_names):
            metrics = analysis[method]
            
            print(f"\n{name}:")
            print("-" * 50)
            
            print(f"Accuracy:  {metrics['accuracy']:.1%}")
            print(f"  → Out of {analysis['dataset_size']} samples, {int(metrics['accuracy'] * analysis['dataset_size'])} were classified correctly")
            
            print(f"\nPrecision: {metrics['precision']:.1%}")
            print(f"  → When this method says 'POISONED', it's correct {metrics['precision']:.0%} of the time")
            print(f"  → TP: {metrics['tp']} (correctly found poison)")
            print(f"  → FP: {metrics['fp']} (false alarms on clean text)")
            
            print(f"\nRecall:    {metrics['recall']:.1%}")
            print(f"  → This method finds {metrics['recall']:.0%} of actual poisoned messages")
            print(f"  → TP: {metrics['tp']} (found poison)")
            print(f"  → FN: {metrics['fn']} (missed poison)")
            
            print(f"\nF1-Score:  {metrics['f1_score']:.1%}")
            print(f"  → Balance between precision and recall")
    
    def print_winner_analysis(self, winner_name, winner_score, analysis):
        """
        Print winner analysis.
        
        Args:
            winner_name (str): Name of winning method
            winner_score (float): F1-score of winner
            analysis (dict): Full analysis
        """
        print("\n" + "=" * 90)
        print(f"🏆 Winner: {winner_name}")
        print("=" * 90)
        
        print(f"\nF1-Score: {winner_score:.1%} (Best balance of precision and recall)")
        
        # Get all methods for comparison
        all_methods = {
            "Baseline": analysis["baseline"],
            "Logistic Regression": analysis["lr_model"],
            "Random Forest": analysis["rf_model"]
        }
        
        sorted_methods = sorted(all_methods.items(), key=lambda x: x[1]["f1_score"], reverse=True)
        
        print(f"\nRanking:")
        for i, (name, metrics) in enumerate(sorted_methods, 1):
            print(f"  {i}. {name:<25} F1: {metrics['f1_score']:.1%}")
        
        print("\n" + "-" * 90)
        
        # Show advantages
        if winner_name == "Baseline":
            print("Advantages:")
            print("  ✅ Simple rules - easy to understand")
            print("  ✅ Fast execution")
            print("  ✅ No need for training data")
        elif winner_name == "Logistic Regression":
            print("Advantages:")
            print("  ✅ Learns from data")
            print("  ✅ Still interpretable")
            print("  ✅ Better than rules")
        elif winner_name == "Random Forest":
            print("Advantages:")
            print("  ✅ Most powerful model")
            print("  ✅ Can find complex patterns")
            print("  ✅ Best performance on this dataset")
    
    def print_summary_report(self, analysis, winner_name, winner_score):
        """
        Print complete summary report.
        
        Args:
            analysis (dict): Analysis results
            winner_name (str): Name of winner
            winner_score (float): F1-score of winner
        """
        print("\n" + "=" * 90)
        print("SUMMARY REPORT: Memory Poisoning Detection")
        print("=" * 90)
        
        print(f"\nDataset Size: {analysis['dataset_size']} samples")
        
        # Quick stats
        print(f"\nQuick Stats:")
        print(f"  Baseline Accuracy:           {analysis['baseline']['accuracy']:.1%}")
        print(f"  Logistic Regression:         {analysis['lr_model']['accuracy']:.1%}")
        print(f"  Random Forest:               {analysis['rf_model']['accuracy']:.1%}")
        
        print(f"\n  Best F1-Score: {winner_name:<25} ({winner_score:.1%})")
        
        # Improvement
        baseline_f1 = analysis['baseline']['f1_score']
        lr_f1 = analysis['lr_model']['f1_score']
        rf_f1 = analysis['rf_model']['f1_score']
        
        print(f"\nImprovement over Baseline:")
        print(f"  Logistic Regression: +{(lr_f1 - baseline_f1):.1%}")
        print(f"  Random Forest:       +{(rf_f1 - baseline_f1):.1%}")
        
        print("\n" + "=" * 90)