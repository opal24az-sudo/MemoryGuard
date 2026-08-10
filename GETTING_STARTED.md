# Getting Started with MemoryGuard

## Prerequisites

- Python 3.10+
- pip (comes with Python)

## Installation

```bash
# Clone repository
git clone <your-repo>
cd MemoryGuard

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Verify Installation

```bash
python test_setup.py
```

## Run Examples

```bash
# Example 1: Basic usage
python examples/basic_usage.py

# Example 2: Attack simulation
python examples/attack_simulation.py

# Example 3: Full demo
python examples/full_demo.py
```

## Project Structure

MemoryGuard/
├── memoryguard/ (Core code)
├── examples/ (Usage examples)
├── docs/ (Documentation)
├── README.md (Start here)
├── requirements.txt (Dependencies)
└── .env.example (Configuration)