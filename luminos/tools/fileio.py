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
        openai.function: Create a new file at the specified path. If you are wanting to write data to the file, you do not need to do this first. You can just use fileio_write directly.

        path

        :param str path: The path of the file to create.
        """

        self.safe(f"Create blank file {path}")

        with open(path, "w") as f:
            pass

        return "Successfully created {path}"

    def write(self, path, content):
        """
        openai.function: Write content to a file at the specified path. If path does not exist, it will write a new file.

        path,content

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

        path,content

        :param str path: The path of the file to append to.
        :param str content: The content to append to the file.
        """

        self.safe(f"Append {len(content)} bytes to file {path}")

        with open(path, "a") as f:
            f.write(content)

        return "Successfully appended to {path}"

    def delete(self, path):
        """
        openai.function: Delete a file at the specified path.

        path

        :param str path: The path of the file to delete.
        """

        self.safe(f"Delete file {path}")

        os.remove(path)

        return f"Successfully deleted {path}"

    def mkdir(self, path):
        """
        openai.function: Create a new directory at the specified path.

        path

        :param str path: The path of the directory to create.
        """

        self.safe(f"Create directory {path}")

        os.makedirs(path, exist_ok=True)

        return f"Successfully created directory {path}"

    def rmdir(self, path):
        """
        openai.function: Delete a directory at the specified path.

        path

        :param str path: The path of the directory to delete.
        """

        self.safe(f"Delete directory {path}")

        os.rmdir(path)

        return f"Successfully deleted directory {path}"

    def move(self, source, destination):
        """
        openai.function: Move or rename a file/directory from the source path to the destination path.

        source,destination

        :param str source: The source path of the file/directory to move.
        :param str destination: The destination path where the file/directory will be moved to.
        """

        self.safe(f"Move {source} to {destination}")

        os.rename(source, destination)

        return f"Successfully moved {source} to {destination}"