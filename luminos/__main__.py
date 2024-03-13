from luminos.core import Core

import os
import sys
import time

def main():
    core_instance = Core()  # Initialize an instance of the Core class
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        os.chdir(target_dir)
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

if __name__ == "__main__":
    main()