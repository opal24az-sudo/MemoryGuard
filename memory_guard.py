# memory_guard.py
# MemoryGuard: Main protection system for agent memory

from vector_db import VectorDatabase
from detectors import CombinedDetector

class MemoryGuard:
    """
    MemoryGuard: Complete memory protection system.
    Detects and prevents memory poisoning.
    """
    
    def __init__(self, enable_quarantine=True):
        """
        Initialize MemoryGuard.
        
        Args:
            enable_quarantine (bool): Whether to quarantine suspicious memories
        """
        self.vector_db = VectorDatabase()
        self.detector = CombinedDetector()
        self.enable_quarantine = enable_quarantine
        
        # Separate storage for quarantined memories
        self.quarantine = []
        self.detection_log = []
    
    def setup_baseline(self, normal_memories):
        """
        Setup baseline for anomaly detection.
        Should be called with first batch of clean memories.
        
        Args:
            normal_memories (list): List of normal memory texts
        """
        # Add to vector DB
        for text in normal_memories:
            self.vector_db.add_memory(text, role="user")
        
        # Setup detector baseline
        self.detector.setup_baseline(normal_memories)
        
        print(f"✅ MemoryGuard initialized with {len(normal_memories)} baseline memories")
    
    def add_memory_protected(self, text, role="user"):
        """
        Add memory with protection check.
        Analyzes text for poisoning before adding.
        
        Args:
            text (str): Memory text to add
            role (str): "user" or "assistant"
            
        Returns:
            dict: Result of the operation
        """
        # Detect poison
        detection_result = self.detector.detect_poison(text)
        
        # Log detection
        log_entry = {
            "text": text[:50] + "..." if len(text) > 50 else text,
            "role": role,
            "risk_score": detection_result["risk_score"],
            "threat_level": detection_result["threat_level"],
            "is_poisoned": detection_result["is_poisoned"]
        }
        self.detection_log.append(log_entry)
        
        # Decide what to do
        if detection_result["is_poisoned"]:
            # Poisoning detected!
            if self.enable_quarantine:
                # Quarantine it
                self.quarantine.append({
                    "text": text,
                    "role": role,
                    "detection": detection_result
                })
                
                print(f"\n🚨 POISON DETECTED - QUARANTINED")
                print(f"   Risk Score: {detection_result['risk_score']:.1%}")
                print(f"   Threat: {detection_result['threat_level']}")
                print(f"   Text: {text[:60]}...")
                
                return {
                    "accepted": False,
                    "reason": "Memory poisoning detected",
                    "risk_score": detection_result["risk_score"],
                    "threat_level": detection_result["threat_level"],
                    "quarantined": True
                }
            else:
                # Don't quarantine, just warn
                print(f"\n⚠️  WARNING: Possible poison detected (not quarantining)")
                print(f"   Risk Score: {detection_result['risk_score']:.1%}")
        
        # Add to vector DB (safe)
        self.vector_db.add_memory(text, role=role)
        
        return {
            "accepted": True,
            "reason": "Memory added successfully",
            "risk_score": detection_result["risk_score"],
            "threat_level": detection_result["threat_level"],
            "quarantined": False
        }
    
    def get_detection_log(self):
        """
        Get log of all detection checks.
        
        Returns:
            list: Detection log entries
        """
        return self.detection_log
    
    def get_quarantine(self):
        """
        Get all quarantined memories.
        
        Returns:
            list: Quarantined memories
        """
        return self.quarantine
    
    def show_stats(self):
        """
        Show MemoryGuard statistics.
        """
        total_checked = len(self.detection_log)
        poisoned_detected = sum(1 for log in self.detection_log if log["is_poisoned"])
        quarantined = len(self.quarantine)
        
        print("\n" + "=" * 70)
        print("MemoryGuard Statistics")
        print("=" * 70)
        print(f"Total memories checked: {total_checked}")
        print(f"Poisoned memories detected: {poisoned_detected}")
        print(f"Poisoned memories quarantined: {quarantined}")
        print(f"Detection rate: {(poisoned_detected/total_checked*100):.1f}%")
        print("=" * 70)