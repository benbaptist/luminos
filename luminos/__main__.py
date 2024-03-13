from core import Core

import time

if __name__ == "__main__":
    core_instance = Core()  # Initialize an instance of the Core class
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

        core_instance.run_llm(prompt)  # Utilize the run_llm method of Core instance