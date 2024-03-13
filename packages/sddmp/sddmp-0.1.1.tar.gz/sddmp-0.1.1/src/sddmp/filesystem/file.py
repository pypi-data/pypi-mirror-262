"""
This file contains the File class, which is used to represent a file in the file system.
"""

from dataclasses import dataclass, field
import datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .directory import Directory

logger = logging.getLogger(__name__)


@dataclass
class File:
    """
    A File object represents a file in the file system.

    Attributes:
        path (Path): The path to the file.
        parent (Directory): The parent directory of the file.

    Properties:
        file_metadata (dict): The metadata of the file.
        name (str): The name of the file.
        extension (str): The extension of the file.
        size (int): The size of the file in bytes.
        created (datetime): The date and time the file was created.
        modified (datetime): The date and time the file was last modified.

    Methods:
        get_file_metadata: Returns the metadata of the file.
        as_record: Returns the file metadata as a record.
    """

    path: Path
    parent: "Directory" = field(default=None, repr=False)

    def __post_init__(self):
        self._metadata = None
        logger.debug("Created file object '%s'", self.path)

    @property
    def file_metadata(self) -> dict:
        """
        The metadata of the file as a dictionary.

        Returns:
            dict: The metadata of the file.
        """
        if self._metadata is None:
            self._metadata = self.get_file_metadata()
        return self._metadata

    @property
    def name(self) -> str:
        """
        The name of the file.

        Returns:
            str: The name of the file.
        """
        return self.path.name

    @property
    def extension(self) -> str:
        """
        The extension of the file.

        Returns:
            str: The extension of the file.
        """
        return self.path.suffix

    @property
    def size(self) -> int:
        """
        The size of the file in bytes.

        Returns:
            int: The size of the file in bytes.
        """
        return self.path.stat().st_size

    @property
    def created(self) -> datetime.datetime:
        """
        The date and time the file was created.

        Returns:
            datetime.datetime: The date and time the file was created.
        """
        return datetime.datetime.fromtimestamp(self.path.stat().st_ctime)

    @property
    def modified(self) -> datetime.datetime:
        """
        The date and time the file was last modified.

        Returns:
            datetime.datetime: The date and time the file was last modified.
        """
        return datetime.datetime.fromtimestamp(self.path.stat().st_mtime)

    def get_file_metadata(self) -> dict:
        """
        Returns the metadata of the file.

        Returns:
            dict: The metadata of the file.
        """
        return {
            "file_name": self.name,
            "path": str(self.path),
            "directory_name": self.parent.name,
            "file_extension": self.extension,
            "file_size": self.size,
            "date_created": self.created,
            "date_modified": self.modified,
        }

    def as_record(self) -> dict:
        """
        Returns the file metadata as a dictionary record intended for creating a pandas
        DataFrame record. The record contains the metadata of the file and the metadata of its
        parent directory, flattened into a single dictionary.

        Returns:
            dict: The file metadata as a record.
        """
        logger.debug("Creating record for file '%s", self.path)
        return {**self.parent.metadata.flat, **self.file_metadata}
