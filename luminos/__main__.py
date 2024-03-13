from luminos.core import Core
import os
import sys
import time

class Main:
    def __init__(self):
        self.core = Core()

    def start(self):
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

            self.core.run_llm(prompt)  # Utilize the run_llm method of core instance

def main():
    app = Main()
    app.start()

if __name__ == "__main__":
    main()