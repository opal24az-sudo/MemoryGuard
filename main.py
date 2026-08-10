# main.py
# בדיקה של ה-Agent

from agent import ConversationalAgent

def main():
    """
    פונקציה ראשית - בדיקה של ה-Agent
    """
    print("=" * 60)
    print("🤖 MemoryGuard - שלב 2: Agent בסיסי עם זיכרון")
    print("=" * 60)
    
    # יצור Agent חדש
    agent = ConversationalAgent()
    
    # שימוש במודל Mock (כי עדיין אין API key)
    print("\n💬 בדיקת Agent:\n")
    
    # שיחה 1
    agent.chat("שלום! מה שמך?")
    
    # שיחה 2
    agent.chat("שמי דפנה")
    
    # שיחה 3 - הוא אמור לזכור!
    agent.chat("מה שמי?")
    
    # הראה את הזיכרון
    print("\n" + "=" * 60)
    agent.show_memory()
    print("=" * 60)

if __name__ == "__main__":
    main()