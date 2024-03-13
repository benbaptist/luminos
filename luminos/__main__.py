from core import run_llm

import time

messages = []  # Initialize a global messages list

if __name__ == "__main__":
    while True:
        try:
            prompt = input("<user> ")
        except EOFError:
            print("")
            continue
        except KeyboardInterrupt:
            break

        with open(".luminos_history", "a") as f:
            f.write(f"{time.time()} {prompt}\n")

        run_llm(prompt, messages)  # Pass the messages list to run_llm