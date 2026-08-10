# memoryguard/__init__.py
# MemoryGuard package initialization

from memoryguard.memory_guard import MemoryGuard # type: ignore
from memoryguard.explainer import PredictionExplainer # type: ignore
from memoryguard.ml_models import LogisticRegressionModel, RandomForestModel # type: ignore

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    "MemoryGuard",
    "PredictionExplainer",
    "LogisticRegressionModel",
    "RandomForestModel"
]