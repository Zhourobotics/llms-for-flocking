# your_script.py
while True:
    user_input = input("Enter your command: ")
    if user_input.lower() == "exit":
        break
    # Handle the command
    print(f"You entered: {user_input}")