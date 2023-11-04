import os

while True:
    text = input("Enter a line to read aloud (or type 'exit' to quit): ")

    if text.lower() == 'exit':
        break

    # Use the 'say' command to read the text aloud on macOS
    os.system(f"say '{text}'")

print("Goodbye!")
