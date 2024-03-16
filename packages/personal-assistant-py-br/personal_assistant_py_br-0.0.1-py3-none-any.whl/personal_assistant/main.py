import personal_assistant.src.messages as messages
from personal_assistant.commands import (
    greeting, exit_assistant,
)
from personal_assistant.menus import contacts_menu, notes_menu
from personal_assistant.src.utils import parser


def main():
    print(messages.welcome_message)

    while True:
        user_input = input("Enter command: main menu: ")
        command, *args, message = parser(user_input)
        if message:
            print(message)

        if command in ["exit", "close"]:
            exit_assistant()

        elif command in ["hello", "hi", "greetings"]:
            print(greeting(), end=" ")

        elif command == "help":
            print(messages.contacts_help_center + messages.notes_help_center)

        elif command == 'contacts':
            contacts_menu()

        elif command == 'notes':
            notes_menu()

        elif not command:
            pass

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
