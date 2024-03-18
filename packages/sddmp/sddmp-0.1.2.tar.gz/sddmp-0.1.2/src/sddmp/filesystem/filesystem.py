"""
This file represents the file system. It contains the FileSystem class, which is used to read a
directory and create a tree of Directory and File objects.
"""

from pathlib import Path
from .directory import Directory
from .file import File


class FileSystem:
    """
    A class for representing the file system.

    Methods:
        read_directory: Reads a directory and creates a tree of Directory and File objects.
    """

    def read_directory(self, path: Path, parent: Directory = None) -> Directory:
        """
        Reads a directory and creates a tree of Directory and File objects.

        Applies recursively to all subdirectories, resulting in a tree of Directory and File
        objects.

        Args:
            path (Path): The path to the directory to read.
            parent (Directory): The parent directory of the directory to read.

        Returns:
            Directory: The directory object representing the directory and its contents.
        """
        # In case the path is provided as a string, convert it to a Path object.
        if isinstance(path, str):
            path = Path(path)

        directory = Directory(path=path, parent=parent)
        for child in path.iterdir():
            if child.is_file():
                directory.files.append(File(path=child, parent=directory))
            elif child.is_dir():
                directory.children.append(self.read_directory(child, directory))
        return directory

    def get_directory(self, path: Path) -> Directory:
        """
        Returns a Directory object representing the directory and its contents.

        Args:
            path (Path): The path to the directory.

        Returns:
            Directory: The directory object representing the directory and its contents.
        """
        return self.read_directory(path)

    def get_file(self, path: Path) -> File:
        """
        Returns a File object representing the file.

        Args:
            path (Path): The path to the file.

        Returns:
            File: The file object representing the file.
        """
        return File(path=path, parent=Directory(path.parent))

    def get_directory_structure(self, directory: Directory) -> dict:
        """
        Get a nested list of all directories in the file system.

        Args:
            directory (Directory): The root directory to start from.

        Returns:
            dict: A dictionary representing the directory structure.
        """
        sorted_children = sorted(directory.children, key=lambda child: child.path.name)

        structure = {
            "name": directory.path.name,
            "children": [
                self.get_directory_structure(child) for child in sorted_children
            ],
        }
        return structure
