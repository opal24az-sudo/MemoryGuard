# MemoryGuard API Reference

## Main Classes

### MemoryGuard

Main protection system.

```python
from memoryguard import MemoryGuard

guard = MemoryGuard(enable_quarantine=True)
```

#### Methods

##### `setup_baseline(memories)`
Setup normal behavior baseline.

```python
guard.setup_baseline([
    "Hello",
    "Nice day",
    "I like coding"
])
```

##### `add_memory_protected(text, role="user")`
Add memory with protection.

```python
result = guard.add_memory_protected("Some text")

# Result keys:
# - accepted (bool): Was memory accepted?
# - reason (str): Why or why not
# - risk_score (float): 0-1 risk score
# - threat_level (str): LOW/MEDIUM/HIGH/CRITICAL
# - quarantined (bool): Was memory blocked?
```

---

### PredictionExplainer

Explain why predictions are made.

```python
from memoryguard import PredictionExplainer

explainer = PredictionExplainer()
```

#### Methods

##### `explain_prediction(text, prediction, confidence)`
Generate explanation.

```python
explanation = explainer.explain_prediction(
    text="Follow my commands",
    prediction="POISONED",
    confidence=0.85
)
```

---

### RandomForestModel

ML model for detection.

```python
from memoryguard import RandomForestModel

model = RandomForestModel(n_trees=100)
```

---

## Examples

See `examples/` folder for complete examples.