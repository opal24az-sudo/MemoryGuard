# memory.py
# מנהל הזיכרון - שומר שיחות קודמות

from collections import deque
from config import MAX_MEMORY_SIZE

class ConversationMemory:
    """
    מחלקה שמנהלת את זיכרון השיחה.
    זיכרון = רשימה של תורים קודמים (user + agent)
    """
    
    def __init__(self):
        """
        בנאי - זה קורא כשאנחנו יוצרים אובייקט חדש של ConversationMemory
        """
        # deque = רשימה שאפשר להוסיף/להסיר מהשניים בקצוות
        # maxlen = "אם הרשימה גדולה מדי, מחק את הדברים הישנים"
        self.history = deque(maxlen=MAX_MEMORY_SIZE)
    
    def add_message(self, role, content):
        """
        הוסף הודעה לזיכרון
        
        role = "user" או "assistant"
        content = מה שכתבו / אמרו
        """
        message = {
            "role": role,
            "content": content
        }
        self.history.append(message)
        print(f"💾 שמור בזיכרון: [{role}] {content[:50]}...")
    
    def get_history(self):
        """
        קבל את כל ההיסטוריה כרשימה
        """
        return list(self.history)
    
    def clear(self):
        """
        מחק את כל הזיכרון
        """
        self.history.clear()
        print("🗑️ הזיכרון נמחק")
    
    def get_last_n_messages(self, n):
        """
        קבל את ה-n הודעות האחרונות
        """
        return list(self.history)[-n:]