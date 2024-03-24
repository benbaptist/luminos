from .basetool import BaseTool
import os

class FileIO(BaseTool):
    name = "fileio"

    def list(self, path):
        """
        openai.function: List the contents of a directory

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
    
    def read(self, path, line_numbers=True):
        """
        openai.function: Read the contents of a file. If you are unsure of what names exist, use fileio_list.

        path,line_numbers

        :param str path: The path of the file to read.
        :param bool line_numbers: Whether or not to read with line numbers activated. This is useful IF you are going to use the fileio_edit function to modify/patch a part of the file. If you use fileio_write, NEVER bake the line numbers into the file itself, unless instructed explicitly to do so.
        """
        
        with open(path, "r") as f:
            if line_numbers:
                return '\n'.join([f'{i+1} | {line}' for i, line in enumerate(f.read().split('\n'))])
            else:
                return f.read()
        
    def create(self, path):
        """
        openai.function: Create a new file at the specified path. If you are wanting to write data to the file, you can just use fileio_write directly, and skip this step.

        path

        :param str path: The path of the file to create.
        """

        self.safe(f"Create blank file {path}")

        with open(path, "w") as f:
            pass

        return "Successfully created {path}"

    def write(self, path, content):
        """
        openai.function: Write content to a file at the specified path. IMPORTANT: You must output the whole file as it should be written, without truncating it.

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
        """openai.function: Delete a file at the specified path.

        path

        :param str path: The path of the file to delete.
        """
        import os
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
                print(f'File {path} has been deleted')
            elif os.path.isdir(path):
                os.rmdir(path)
                print(f'Directory {path} has been deleted')
            else:
                print(f'Error: {path} is not a file or directory')
        except Exception as e:
            print(f'Error deleting {path}: {e}')

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

    def cd(self, path):
        """openai.function: Change the current working directory of the program.

        path

        :param str path: The path to change the working directory to.
        """
        os.chdir(path)
        return f"Changed working directory to {path}"

    def walk(self, directory):
        """
        openai.function: Walk the directory tree and return a formatted filesystem tree.

        directory

        :param str directory: The directory to walk.
        """
        import os

        def tree_structure(start_path, level=0):
            tree_str = ''
            for root, dirs, files in os.walk(start_path):
                indent = '    ' * level
                tree_str += f'{indent}+ {root}]\n'
                for dir in sorted(dirs):
                    tree_str += f'{indent}    - {dir}\n'
                for file in sorted(files):
                    tree_str += f'{indent}    * {file}\n'
                level += 1
            return tree_str

        return tree_structure(directory)

    def edit(self, path, changes):
        """openai.function: Modify/patch a file by specifying a list of each line that needs changing and the replacement string for that line.

        path,changes

        :param str path: The path of the file to edit.
        :param list changes: Array of arrays containing line numbers and replacement strings. e.g. [[5, 'i am line five'], [10, 'i am line ten']]
        """
        self.safe(f"Edit {path} with {len(changes)} lines changed")

        try:
            with open(path, 'r') as file:
                lines = file.read().splitlines()

            for line_num, replacement in changes:
                try:
                    lines[line_num - 1] = replacement
                except IndexError:
                    lines.insert(line_num - 1, replacement)

            with open(path, 'w') as file:
                file.write("\n".join(lines))

            return f'Successfully edited {path} with {len(changes)} line changes'
        except Exception as e:
            raise Exception(f'Error editing {path}: {e}')