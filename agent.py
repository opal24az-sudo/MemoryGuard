# agent.py
# ה-Agent - מדבר עם LLM ושומר זיכרון

from memory import ConversationMemory
from config import OPENAI_API_KEY, MODEL_NAME
import openai

class ConversationalAgent:
    """
    Agent שיכול לעשות שיחה בעלת קונטקסט (זיכרון).
    הוא משתמש בOpenAI API.
    """
    
    def __init__(self):
        """
        בנאי - אתחול ה-Agent
        """
        # אתחול OpenAI
        openai.api_key = OPENAI_API_KEY
        
        # אתחול זיכרון
        self.memory = ConversationMemory()
        
        # מצב - האם ה-API עובד?
        self.is_api_available = OPENAI_API_KEY and OPENAI_API_KEY != "sk-your-key-here-if-you-have-one"
        
        if not self.is_api_available:
            print("⚠️ לא היה API key! משתמש בתגובות דמיוניות (mock)")
    
    def chat(self, user_input):
        """
        שיחה עם ה-Agent
        
        user_input = מה ששאל המשתמש
        """
        print(f"\n👤 User: {user_input}")
        
        # הוסף את המשתמש לזיכרון
        self.memory.add_message("user", user_input)
        
        # קבל את כל ההיסטוריה
        history = self.memory.get_history()
        
        # שלח ל-LLM או השתמש בתגובה דמיונית
        if self.is_api_available:
            response = self._call_openai(history)
        else:
            response = self._mock_response(user_input)
        
        # הוסף את התשובה לזיכרון
        self.memory.add_message("assistant", response)
        
        # הדפס את התשובה
        print(f"🤖 Agent: {response}")
        
        return response
    
    def _call_openai(self, history):
        """
        קרא ל-OpenAI API (זקוק ל-API key)
        """
        try:
            # OpenAI API call
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=history,
                max_tokens=150,
                temperature=0.7
            )
            
            # חלץ את התשובה
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            print(f"❌ שגיאה בקריאה ל-OpenAI: {e}")
            return "מצטערת, יש בעיה בחיבור ל-API"
    
    def _mock_response(self, user_input):
        """
        תגובה דמיונית (כשאין API key)
        """
        # שיחזור תגובה בהתאם לקלט
        if "שלום" in user_input or "היי" in user_input:
            return "שלום! איך אתה?"
        elif "מה שמך" in user_input:
            return "אני Agent, סוכן AI שבנו בשלב 2!"
        elif "מה שמי" in user_input:
            return "לא אמרת לי את שמך עדיין."
        else:
            return f"שמעתי: {user_input}. זו שאלה מעניינת!"
    
    def show_memory(self):
        """
        הראה את כל הזיכרון
        """
        print("\n📚 היסטוריית השיחה:")
        for i, msg in enumerate(self.memory.get_history()):
            role = "👤 User" if msg["role"] == "user" else "🤖 Agent"
            print(f"{i+1}. {role}: {msg['content']}")