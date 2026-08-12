import os
import sys
from server import write_and_save_story

def main():
    print("=" * 60)
    print("      LM STUDIO CREATIVE STORY GENERATOR CHATBOT")
    print("==================================================")
    print("Type your story prompt below (or type 'exit' to quit).\n")

    counter = 1
    while True:
        try:
            prompt = input("Enter Story Topic/Prompt: ").strip()
            if not prompt:
                continue
            if prompt.lower() in ["exit", "quit", "q"]:
                print("Exiting story generator. Goodbye!")
                break

            genre = input("Enter Genre [default: fantasy]: ").strip() or "fantasy"
            filename = input(f"Enter Filename [default: story_{counter}.txt]: ").strip() or f"story_{counter}.txt"

            print("\nGenerating creative story via LM Studio... Please wait...\n")
            result = write_and_save_story(topic=prompt, filename=filename, genre=genre)
            print("-" * 50)
            print(result)
            print("-" * 50 + "\n")
            counter += 1

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
