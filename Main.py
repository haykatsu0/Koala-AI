from Chat import chat
from Audio import voice_chat

print("\nWelcome to Koala, choose a mode.\n")

while True:
    print("for \033[32mtext chat\033[0m type \033[31m1\033[0m\n"
        "for \033[35mvoice chat\033[0m type \033[31m2\033[0m\n")

    user_input = input("\033[96mYou:\033[0m ").strip()
    if user_input == "1":
            chat()
    elif user_input == "2":
            voice_chat()
    else:
        print("\nTry again...\n")
        continue