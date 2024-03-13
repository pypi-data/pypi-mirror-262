"""
This file contains the HTMLPage class, which is used to generate an HTML page for a directory in
the file system.
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
import pandas as pd

from ..filesystem import Directory
from .plots import PiePlot


class HTMLPage:
    """
    Represents an HTML page for a directory in the file system.

    Attributes:
        directory (Directory): The directory for which the HTML page is to be generated.
        output_directory (Path): The directory in which the HTML page is to be saved.

    Methods:
        generate: Generates the HTML page for the directory.
        generate_pie_plot: Generates a pie plot for a column in the dataframe.
    """

    # Class Variable for storing the directory structure
    directory_structure = None

    def __init__(self, directory: Directory, output_directory: Path):
        self.directory = directory
        self.output_directory = output_directory
        self.jinja_env = Environment(
            loader=FileSystemLoader("src/sddmp/outputs/templates"), autoescape=True
        )

    @property
    def relative_path_to_root(self) -> str:
        """
        Returns the relative path from the output directory to the root directory.
        """
        num_path_parts = len(self.directory.path.parts)
        if num_path_parts == 1:
            return ".."

        return "../" * (num_path_parts)

    def generate(self) -> None:
        """
        Generates the HTML page for the directory and saves it in the output directory.
        """

        # Create a dataframe of the files in the directory.
        df = self.directory.as_dataframe()

        # Get the template for the html page.
        template = self.jinja_env.get_template("directory.html.j2")

        # Create a dictionary of the plots to be rendered on the page.
        # The keys are the names of the plots, and the values are the plots in json format.
        pie_plot_columns = ["file_extension", "personal-data"]
        plots = {
            column: self.generate_pie_plot(df, column).as_json()
            for column in pie_plot_columns
            if column in df.columns
        }

        file_records_df = self.directory.file_records_dataframe()

        # Render the template with the dataframe.
        html = template.render(
            project_title=self.directory.metadata["ResearchProject"]["name"],
            relative_path_to_root=self.relative_path_to_root,
            directory_structure=self.directory_structure,
            my_path=self.directory.path.as_posix(),
            num_files=len(file_records_df),
            num_directories=len(self.directory.all_descendants) + 1,
            people=self.directory.metadata.get_people(),
            filetree=self.directory.filetree,
            plots=plots,
            metadata=self.directory.metadata_as_plaintext(),
            file_records_df=file_records_df,
            depth=len(self.directory.path.parts),
        )

        # Create a path to the html file.
        path = self.output_directory / self.directory.path / "index.html"

        # Create the directory for the html file if it does not exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write the html file.
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    def generate_pie_plot(self, df: pd.DataFrame, column: str) -> PiePlot:
        """
        Generates a pie plot for a column in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe.
            column (str): The name of the column in the dataframe.

        Returns:
            PiePlot: The pie plot.
        """

        # Create a dataframe that counts the number of files with each extension.
        df = df[column].value_counts().reset_index()

        # Rename the columns.
        df.columns = [column, "count"]

        # Create a pie plot.
        plot = PiePlot(
            title=f"Number of files by {column}".replace("-", " ").title(),
            labels=df[column],
            values=df["count"],
        )

        return plot
