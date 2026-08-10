# MemoryGuard: AI Security System for Memory Poisoning Detection

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## 🎯 Project Overview

**MemoryGuard** is an AI security system designed to detect and prevent **memory poisoning attacks** on long-memory AI agents.

### The Problem
Traditional AI agents with long-term memory are vulnerable to subtle attacks where users inject malicious instructions that corrupt the agent's behavior over time.

### The Solution
MemoryGuard uses a **multi-layered detection system** combining:
- Rule-based detection (fast & interpretable)
- Machine Learning models (powerful & adaptive)
- Semantic analysis (context-aware)
- Real-time monitoring & explainability

## 🚀 Quick Start

```bash
# Clone and setup
git clone <your-repo>
cd MemoryGuard
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Run examples
python examples/basic_usage.py
python examples/attack_simulation.py
python examples/full_demo.py
```

## 📊 Results

| Method | Accuracy | Precision | Recall | F1-Score |
|--------|----------|-----------|--------|----------|
| Baseline | 72.7% | 66.7% | 60.0% | 63.2% |
| Logistic Regression | 81.8% | 80.0% | 66.7% | 72.7% |
| Random Forest | **90.9%** | **100.0%** | 66.7% | **80.0%** |

## 📚 Documentation

- [Getting Started](GETTING_STARTED.md)
- [Architecture](ARCHITECTURE.md)
- [Threat Model](THREAT_MODEL.md)

## 🧪 Testing

```bash
python examples/basic_usage.py
python examples/attack_simulation.py
python examples/full_demo.py
```

## 📄 License

MIT License