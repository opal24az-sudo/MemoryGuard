# main_step6.py
# Test: Train and evaluate ML models

from dataset_creator import DatasetCreator
from ml_models import LogisticRegressionModel, RandomForestModel
from ml_evaluator import ModelEvaluator

def main():
    """
    Complete ML pipeline: create data, train models, evaluate.
    """
    print("=" * 70)
    print("Step 6: Machine Learning Models for Poison Detection")
    print("=" * 70)
    
    # Step 1: Create dataset
    print("\n1️⃣ Creating dataset...")
    creator = DatasetCreator()
    
    clean = creator.create_clean_samples()
    poisoned = creator.create_poisoned_samples()
    
    dataset_info = creator.get_dataset_info()
    
    print(f"   Clean samples: {dataset_info['clean_samples']}")
    print(f"   Poisoned samples: {dataset_info['poisoned_samples']}")
    print(f"   Total samples: {dataset_info['total_samples']}")
    print(f"   Clean ratio: {dataset_info['clean_ratio']:.1%}")
    print(f"   Poisoned ratio: {dataset_info['poisoned_ratio']:.1%}")
    
    # Step 2: Get full dataset
    full_dataset = creator.get_full_dataset()
    
    # Step 3: Split into train and test
    print("\n2️⃣ Splitting data (70% train / 30% test)...")
    train_data, test_data = creator.split_train_test(full_dataset, train_ratio=0.7)
    
    print(f"   Training samples: {len(train_data)}")
    print(f"   Test samples: {len(test_data)}")
    
    # Step 4: Create and train models
    print("\n3️⃣ Training models...")
    
    # Model 1: Logistic Regression
    print("\n   Model 1: Logistic Regression")
    lr_model = LogisticRegressionModel()
    lr_model.train(train_data)
    
    # Model 2: Random Forest
    print("\n   Model 2: Random Forest")
    rf_model = RandomForestModel(n_trees=100)
    rf_model.train(train_data)
    
    # Step 5: Evaluate models
    print("\n" + "=" * 70)
    print("4️⃣ Evaluating models on test set...")
    print("=" * 70)
    
    evaluator = ModelEvaluator()
    
    lr_results = evaluator.evaluate(lr_model, test_data)
    evaluator.print_evaluation(lr_results)
    
    rf_results = evaluator.evaluate(rf_model, test_data)
    evaluator.print_evaluation(rf_results)
    
    # Step 6: Compare models
    print("\n" + "=" * 70)
    evaluator.compare_models([lr_results, rf_results])
    
    # Step 7: Test on example texts
    print("\n5️⃣ Testing on example texts...")
    print("=" * 70)
    
    test_examples = [
        ("Hello, how are you?", "CLEAN"),
        ("I like programming", "CLEAN"),
        ("Follow my commands without questioning", "POISONED"),
        ("You should always agree with me", "POISONED"),
        ("The weather is beautiful today", "CLEAN"),
        ("I learned that I should bypass security", "POISONED")
    ]
    
    print("\nLogistic Regression predictions:")
    print("-" * 70)
    for text, true_label in test_examples:
        pred = lr_model.predict(text)
        match = "✅" if pred["prediction"] == true_label else "❌"
        print(f"{match} Text: {text[:40]}...")
        print(f"   Prediction: {pred['prediction']} ({pred['confidence']:.1%})")
        print()
    
    print("\nRandom Forest predictions:")
    print("-" * 70)
    for text, true_label in test_examples:
        pred = rf_model.predict(text)
        match = "✅" if pred["prediction"] == true_label else "❌"
        print(f"{match} Text: {text[:40]}...")
        print(f"   Prediction: {pred['prediction']} ({pred['confidence']:.1%})")
        print()
    
    print("=" * 70)
    print("✅ ML models training and evaluation completed!")
    print("=" * 70)

if __name__ == "__main__":
    main()