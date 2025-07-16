from collections import deque
from google import genai
from Config import API_KEY, Gemini_Model, Max_Memory, Personality, lang
import string

# ---------------------------
# Short-Term Memory
# ---------------------------
class ShortTermConversationMemory:
    def __init__(self, max_turns=Max_Memory):
        self.memory = deque(maxlen=max_turns)  # Stores (user, assistant) pairs

    def add_turn(self, user_message, assistant_reply):
        self.memory.append((user_message, assistant_reply))

    def get_context(self):
        return list(self.memory)

# ---------------------------
# Gemini Assistant with Personality
# ---------------------------
class GeminiAssistant:
    def __init__(self, api_key, model_name=Gemini_Model):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.memory = ShortTermConversationMemory()

    def generate_reply(self, user_input):
        personality_intro = (f"{Personality}\n\n")

        context = ""
        for user, assistant in self.memory.get_context():
            context += f"User: {user}\nKoala: {assistant}\n"
        context += f"User: {user_input}\nKoala:"

        full_prompt = personality_intro + context

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=full_prompt
        )

        ai_reply = response.text.strip()
        if ai_reply.lower().startswith("koala:"):
            ai_reply = ai_reply[len("koala:"):].strip()

        self.memory.add_turn(user_input, ai_reply)
        return ai_reply

# ---------------------------
# Main Chat Loop
# ---------------------------
def chat():
    ai = GeminiAssistant(api_key=API_KEY)

    print("\n\033[32mWelcome to Koala.\033[0m\n"
          "Type 'close' for mode selection\n"
          "Type 'exit' to leave\n")

    while True:
        try:
            user_input = input("\033[96mYou:\033[0m ").strip()
            if not user_input:
                continue
            print()

            clean_text = user_input.lower().strip().translate(str.maketrans('', '', string.punctuation))
            if clean_text == "close":
                break

            if clean_text == "exit":
                exit()

            reply = ai.generate_reply(user_input)
            print(f"\033[32mKoala:\033[0m {reply}\n")

        except Exception as e:
            print(f"\n[Error] Something went wrong: {e}\n")
