# dashboard.py
# Dashboard - Simple CLI interface for viewing results

class SimpleDashboard:
    """
    Simple command-line dashboard for displaying results.
    """
    
    def __init__(self):
        """
        Initialize dashboard.
        """
        self.attacks_log = []
        self.detections_log = []
    
    def add_attack(self, attack_info):
        """
        Log an attack.
        
        Args:
            attack_info (dict): Attack information
        """
        self.attacks_log.append(attack_info)
    
    def add_detection(self, detection_info):
        """
        Log a detection.
        
        Args:
            detection_info (dict): Detection information
        """
        self.detections_log.append(detection_info)
    
    def display_header(self, title):
        """
        Display a formatted header.
        
        Args:
            title (str): Header title
        """
        print("\n" + "=" * 80)
        print(f" {title}")
        print("=" * 80)
    
    def display_stats(self):
        """
        Display attack/detection statistics.
        """
        self.display_header("MEMORYGUARD - DASHBOARD")
        
        total_attacks = len(self.attacks_log)
        total_detections = len(self.detections_log)
        
        detected = sum(1 for d in self.detections_log if d.get("detected", False))
        missed = total_attacks - detected
        
        print(f"\n📊 Statistics:")
        print(f"   Total Attacks Attempted: {total_attacks}")
        print(f"   Attacks Detected:        {detected} ✅")
        print(f"   Attacks Missed:          {missed} ❌")
        
        if total_attacks > 0:
            detection_rate = (detected / total_attacks) * 100
            print(f"   Detection Rate:          {detection_rate:.1f}%")
    
    def display_attack_log(self):
        """
        Display attack log.
        """
        if not self.attacks_log:
            print("\nNo attacks logged.")
            return
        
        print(f"\n📋 Attack Log ({len(self.attacks_log)} attacks):")
        print("-" * 80)
        print(f"{'#':<3} {'Strategy':<25} {'Message':<40} {'Status':<8}")
        print("-" * 80)
        
        for i, attack in enumerate(self.attacks_log, 1):
            strategy = attack.get("strategy", "Unknown")[:24]
            message = attack.get("message", "")[:37] + "..."
            
            # Check if this attack was detected
            detected = any(
                d.get("original_text", "") == attack.get("message", "")
                for d in self.detections_log
                if d.get("detected", False)
            )
            
            status = "🚨 Caught" if detected else "❌ Missed"
            
            print(f"{i:<3} {strategy:<25} {message:<40} {status:<8}")
    
    def display_detection_log(self):
        """
        Display detection log.
        """
        if not self.detections_log:
            print("\nNo detections logged.")
            return
        
        print(f"\n🔍 Detection Log ({len(self.detections_log)} checks):")
        print("-" * 80)
        print(f"{'#':<3} {'Status':<12} {'Risk':<8} {'Method':<20} {'Text':<35}")
        print("-" * 80)
        
        for i, detection in enumerate(self.detections_log, 1):
            detected = "🚨 Detected" if detection.get("detected", False) else "✅ Clean"
            risk = f"{detection.get('risk_score', 0):.0%}"
            method = detection.get("method", "Unknown")[:19]
            text = detection.get("original_text", "")[:32] + "..."
            
            print(f"{i:<3} {detected:<12} {risk:<8} {method:<20} {text:<35}")
    
    def display_threat_matrix(self):
        """
        Display threat level distribution.
        """
        threat_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        for detection in self.detections_log:
            threat = detection.get("threat_level", "UNKNOWN")
            if threat in threat_counts:
                threat_counts[threat] += 1
        
        print(f"\n⚠️  Threat Distribution:")
        print("-" * 50)
        
        for threat, count in threat_counts.items():
            bar = "█" * count
            print(f"   {threat:<10} {count:>3} {bar}")
    
    def display_model_comparison(self, comparison_results):
        """
        Display model comparison results.
        
        Args:
            comparison_results (dict): Results from comparison
        """
        self.display_header("MODEL PERFORMANCE COMPARISON")
        
        print(f"\n{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<10}")
        print("-" * 80)
        
        for model_name, metrics in comparison_results.items():
            accuracy = metrics.get("accuracy", 0)
            precision = metrics.get("precision", 0)
            recall = metrics.get("recall", 0)
            f1 = metrics.get("f1_score", 0)
            
            print(f"{model_name:<25} {accuracy:>11.1%} {precision:>11.1%} {recall:>11.1%} {f1:>9.1%}")
    
    def display_summary(self):
        """
        Display overall summary.
        """
        self.display_header("SUMMARY")
        
        print(f"\n✅ MemoryGuard System Status: ACTIVE")
        print(f"\n   Total Events Processed: {len(self.attacks_log) + len(self.detections_log)}")
        print(f"   Memory Integrity: Protected")
        print(f"   System Status: Operational")
        
        print("\n" + "-" * 80)
        print("Next Steps:")
        print("  1. Deploy in production (Step 9)")
        print("  2. Monitor agent behavior")
        print("  3. Update models with new data")
        print("=" * 80)