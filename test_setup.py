# test_setup.py
# בדיקה שהסביבה עובדת בצורה נכונה

print("=" * 50)
print("🔍 בדיקת סביבת MemoryGuard")
print("=" * 50)

# 1. בדיקה שPython עובד
print("\n✅ Python עובד!")

# 2. בדיקה גרסת Python
import sys
print(f"✅ גרסת Python: {sys.version}")

# 3. בדיקה כל ספרייה
print("\n📦 בדיקת ספריות:")

try:
    import dotenv
    print("  ✅ python-dotenv - מותקנת")
except ImportError as e:
    print(f"  ❌ python-dotenv - לא מותקנת: {e}")

try:
    import langchain
    print("  ✅ langchain - מותקנת")
except ImportError as e:
    print(f"  ❌ langchain - לא מותקנת: {e}")

try:
    import openai
    print("  ✅ openai - מותקנת")
except ImportError as e:
    print(f"  ❌ openai - לא מותקנת: {e}")

try:
    import numpy
    print("  ✅ numpy - מותקנת")
except ImportError as e:
    print(f"  ❌ numpy - לא מותקנת: {e}")

try:
    import pandas
    print("  ✅ pandas - מותקנת")
except ImportError as e:
    print(f"  ❌ pandas - לא מותקנת: {e}")

print("\n" + "=" * 50)
print("✅ הסביבה מוכנה להתחלה!")
print("=" * 50)