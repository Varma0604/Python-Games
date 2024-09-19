import time
import random

# List of sample sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language.",
    "Practice makes perfect when learning to type.",
    "Coding is both an art and a science.",
    "The early bird catches the worm.",
    "A journey of a thousand miles begins with a single step.",
    "All that glitters is not gold.",
    "To be or not to be, that is the question.",
    "Where there's a will, there's a way.",
    "Knowledge is power, but enthusiasm pulls the switch."
]

def calculate_wpm(start_time, end_time, typed_words):
    time_elapsed = end_time - start_time
    minutes = time_elapsed / 60
    wpm = typed_words / minutes
    return round(wpm)

def calculate_accuracy(original, typed):
    original_words = original.split()
    typed_words = typed.split()
    correct_words = sum(1 for o, t in zip(original_words, typed_words) if o == t)
    return round((correct_words / len(original_words)) * 100, 2)

def run_typing_test():
    print("Welcome to the Typing Speed Test!")
    print("You'll be given a random sentence to type. Press Enter when you're ready to start.")
    input()

    sentence = random.choice(sentences)
    print("\nType the following sentence:")
    print(sentence)
    print("\nPress Enter when you're ready to start typing.")
    input()

    start_time = time.time()
    user_input = input("Start typing: ")
    end_time = time.time()

    wpm = calculate_wpm(start_time, end_time, len(user_input.split()))
    accuracy = calculate_accuracy(sentence, user_input)

    print(f"\nTime elapsed: {round(end_time - start_time, 2)} seconds")
    print(f"Your typing speed: {wpm} WPM")
    print(f"Accuracy: {accuracy}%")

    print("\nOriginal sentence:")
    print(sentence)
    print("\nYour typed sentence:")
    print(user_input)

if __name__ == "__main__":
    while True:
        run_typing_test()
        play_again = input("\nWould you like to try again? (y/n): ").lower()
        if play_again != 'y':
            print("Thank you for using the Typing Speed Test. Goodbye!")
            break