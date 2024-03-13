"""
This module contains the Directory class, which is used to represent a directory in the file
system. The Directory class is used to create a tree structure of directories and files, and to
create a dataframe of all files in the directory tree.
"""

from dataclasses import dataclass, field
import logging
from pathlib import Path

import pandas as pd
import yaml

from .file import File
from .filetree import FileTree
from ..metadata import Metadata

logger = logging.getLogger(__name__)


@dataclass
class Directory:
    """
    Represents a directory in the file system.

    Attributes:
        path (Path): The path to the directory.
        parent (Directory): The parent directory of this directory.
        children (list[Directory]): The child directories of this directory.
        files (list[File]): The files in this directory.
        metadata_filename (str): The name of the metadata file in this directory.

    Properties:
        name (str): The name of the directory.
        metadata (Metadata): The metadata of the directory.
        all_descendants (list[Directory]): All descendant directories of this directory.

    Methods:
        get_metadata: Load the metadata file in this directory, or create a new metadata object.
        as_dataframe: Create a dataframe of all files in the directory tree.
    """

    path: Path
    parent: "Directory" = None
    children: list["Directory"] = field(default_factory=list, repr=False)
    files: list[File] = field(default_factory=list, repr=False)
    metadata_filename = "README.yaml"

    _filetree: FileTree = field(default=None, repr=False)

    @property
    def name(self):
        """
        The name of the directory.
        """
        return self.path.name

    @property
    def metadata(self):
        """
        The metadata of the directory.
        """
        if self._metadata is None:
            self._metadata = self.get_metadata()
        return self._metadata

    @property
    def all_descendants(self):
        """
        All descendant directories of this directory.
        """
        descendants = [self]
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.all_descendants)
        return descendants

    @property
    def filetree(self) -> str:
        """
        Get the filetree of the directory as a string.
        """
        return self._filetree.as_string()

    def __post_init__(self):
        # If the directory has no parent, it is the root directory.
        if self.parent is None:
            self.parent = self

        # If the directory has no children, it is a leaf directory.
        if self.children is None:
            self.children = []

        # If the directory has no files, it is an empty directory.
        if self.files is None:
            self.files = []

        self._metadata = None

        self._filetree = FileTree(self.path)

        logger.debug("Created directory object %s", self.path)

    def get_metadata(self) -> Metadata:
        """
        Get the metadata of the directory.

        If the metadata file exists, load it. Otherwise, create a new metadata object. If this
        directory is not the root directory, supplement the metadata with the metadata of the
        parent directory.

        Returns:
            Metadata: The metadata of the directory.
        """
        # Create a path to the metadata file in this directory.
        metadata_path = self.path / self.metadata_filename

        # Load the metadata file if it exists, otherwise create a new metadata object.
        my_metadata = (
            Metadata.load(metadata_path) if metadata_path.exists() else Metadata()
        )

        # If this directory is not the root directory, supplement the metadata with the
        if self.parent != self:
            my_metadata.supplement(self.parent.metadata)

        return my_metadata

    def as_dataframe(self) -> pd.DataFrame:
        """
        Create a dataframe of all files in the directory tree.

        Returns:
            pd.DataFrame: A dataframe of all files in the directory tree.
        """
        logger.debug("Creating dataframe for directory %s", self.path)
        # Create a dataframe by collecting all files in this directory as records.
        df = pd.DataFrame([file.as_record() for file in self.files])

        # Extend the dataframe by collecting all files in the child directories as records.
        df = pd.concat([df] + [child.as_dataframe() for child in self.children])

        return df

    def metadata_as_plaintext(self) -> dict[str, str]:
        """
        Create a dictionary of the directory tree in plaintext.

        Keys are the root items in the metadata

        Returns:
            dict[str, str]: A dictionary of the directory tree in plaintext.
        """
        logger.debug("Creating plaintext for directory %s", self.path)

        return_dict = {}
        for key, value in self.get_metadata().items():
            return_dict[key] = yaml.dump(value, default_flow_style=False)

        return return_dict

    def file_records_dataframe(self) -> pd.DataFrame:
        """
        Create a dataframe of all files in the directory tree.

        Returns:
            pd.DataFrame: A dataframe of all files in the directory tree.
        """
        df = pd.DataFrame([file.get_file_metadata() for file in self.files])

        full_df = pd.concat(
            [df] + [child.file_records_dataframe() for child in self.children]
        )

        return full_df
