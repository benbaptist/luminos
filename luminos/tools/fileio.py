from .basetool import BaseTool

import os

class FileIO(BaseTool):
    name = "fileio"

    def list(self, path):
        """openai.function: List the contents of a directory

        path

        :param str path: The path to list.
        """
        dir = []

        for name in os.listdir(path):
            full_path = os.path.join(path, name)

            if os.path.isdir(full_path):
                type = "dir"
            else:
                type = "file"

            dir.append({
                "type": type,
                "name": name
            })

        return dir
    
    def read(self, path):
        """openai.function: Read the contents of a file. If you are unsure of what names exist, use fileio_list.

        path

        :param str path: The path of the file to read.
        """
        
        with open(path, "r") as f:
            return f.read()
        
    def create(self, path):
        """
        openai.function: Create a new file at the specified path.

        path

        :param str path: The path of the file to create.
        """

        self.safe(f"Create blank file {path}")

        with open(path, "w") as f:
            pass

        return "Successfully created {path}"

    def write(self, path, content):
        """
        openai.function: Write content to a file at the specified path.

        path
        content

        :param str path: The path of the file to write to.
        :param str content: The content to write to the file.
        """

        self.safe(f"Write {len(content)} bytes to file {path}")

        with open(path, "w") as f:
            f.write(content)

        return "Successfully wrote {path}"

    def append(self, path, content):
        """
        openai.function: Append content to a file at the specified path.

        path
        content

        :param str path: The path of the file to append to.
        :param str content: The content to append to the file.
        """

        self.safe(f"Append {len(content)} bytes to file {path}")

        with open(path, "a") as f:
            f.write(content)

        return "Successfully appended to {path}"