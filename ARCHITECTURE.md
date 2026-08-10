# MemoryGuard Architecture

## System Overview

AI Agent with Memory
↓
MemoryGuard System
├─ Layer 1: Feature Extraction
├─ Layer 2: Rule-Based Detection
├─ Layer 3: ML Models
└─ Decision Engine
↓
Accept or Quarantine


## Components

### 1. Memory Layer
- Stores agent memories
- Vector embeddings
- Semantic search

### 2. Detection Layers
- Feature extraction (8 features)
- Rule-based detection (4 rules)
- Anomaly detection (Z-score)

### 3. ML Models
- Logistic Regression (81.8% accuracy)
- Random Forest (90.9% accuracy) ⭐

### 4. Explanation Layer
- Why decisions are made
- Evidence-based explanations

## Performance

- Baseline: 63.2% F1
- Logistic Regression: 72.7% F1
- Random Forest: 80.0% F1 ⭐

## Data Flow

Training Phase:

Dataset → Feature Extraction → Model Training → Evaluation


Inference Phase:

New Memory → Feature Extraction → Detection → Decision